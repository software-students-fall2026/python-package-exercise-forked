import pytest
from funcasino.blackjack import Blackjack
from funcasino.deck import Deck, Card

def cards(*ranks):
    return [Card(rank, "Hearts") for rank in ranks]

def make_hand(*ranks, bet=10, status="Playing"):
    return {
        "cards": cards(*ranks),
        "bet": bet,
        "status": status,
    }

@pytest.fixture
def game():
    game = Blackjack()
    game.wallet.balance = 100
    return game

def test_initial_state(game):
    assert game.wins == 0
    assert game.losses == 0
    assert game.pushes == 0
    assert game.max_hands == 4

def test_custom_wallet(game):
    other = Blackjack(game.wallet)

    assert other.wallet is game.wallet

@pytest.mark.parametrize("ranks, expected", [
    ([], 0),
    (["2"], 2),
    (["J", "Q"], 20),
    (["K", "7"], 17),
    (["A", "A", "K", "K"], 22),
    (["K", "Q", "2"], 22),
])
def test_hand_value(game, ranks, expected):
    assert game.hand_value(cards(*ranks)) == expected

def test_hand_value_does_not_change_cards(game):
    hand = cards("A", "K", "5")

    assert game.hand_value(hand) == 16
    assert [card.rank for card in hand] == ["A", "K", "5"]
    assert hand[0].blackjack_value() == 11

@pytest.mark.parametrize(
    "ranks, status, balance, count, expected",
    [
        (["8", "8"], "Playing", 100, 1, True),
        (["8"], "Playing", 100, 1, False),
        (["8", "8", "2"], "Playing", 100, 1, False),
        (["8", "8"], "Standing", 100, 1, False),
        (["8", "8"], "Playing", 100, 3, True),
        (["8", "8"], "Playing", 100, 4, False),
    ],
)
def test_can_split(game, ranks, status, balance, count, expected):
    game.wallet.balance = balance
    hand = make_hand(*ranks, status=status)
    hands = [hand] + [make_hand("2", "3") for _ in range(count - 1)]

    assert game.can_split(hand, hands) is expected
    assert game.wallet.balance == balance

@pytest.mark.parametrize("rank, expected_status", [
    ("8", "Playing"),
    ("K", "Playing"),
    ("A", "Standing"),
])
def test_split_hand(game, rank, expected_status):
    original = make_hand(rank, rank, bet=25)
    first, second = original["cards"]
    hands = [original]
    deck = Deck()
    remaining = len(deck.cards)

    game.split_hand(hands, 0, deck)

    assert len(hands) == 2
    assert hands[0]["cards"][0] is first
    assert hands[1]["cards"][0] is second
    assert all(len(h["cards"]) == 2 for h in hands)
    assert all(h["bet"] == 25 for h in hands)
    assert all(h["status"] == expected_status for h in hands)
    assert hands[0]["cards"] is not hands[1]["cards"]
    assert len(deck.cards) == remaining - 2
    assert game.wallet.balance == 75

def test_split_preserves_other_hands(game):
    untouched = make_hand("5", "6", status="Standing")
    hands = [untouched, make_hand("8", "8")]

    game.split_hand(hands, 1, Deck())

    assert len(hands) == 3
    assert hands[0] is untouched
    assert [h["cards"][0].rank for h in hands] == ["5", "8", "8"]

def test_no_initial_blackjack(game):
    hands = [make_hand("K", "9")]

    assert game.check_for_blackjack(cards("Q", "8"), hands) is False
    assert game.wallet.balance == 100
    assert (game.wins, game.losses, game.pushes) == (0, 0, 0)

@pytest.mark.parametrize(
    "player, dealer, payout, status, stats",
    [
        (["K", "Q", "2"], ["K", "8"], 0, "Lost", (0, 1, 0)),
        (["K", "Q", "2"], ["K", "Q", "3"], 0, "Lost", (0, 1, 0)),
        (["K", "8"], ["K", "Q", "2"], 20, "Won", (1, 0, 0)),
        (["K", "8"], ["K", "Q"], 0, "Lost", (0, 1, 0)),
        (["K", "8"], ["Q", "8"], 10, "Push", (0, 0, 1)),
        (["7", "7", "7"], ["K", "8"], 20, "Won", (1, 0, 0)),
        (["A", "K"], ["K", "8"], 20, "Won", (1, 0, 0)),
    ],
)
def test_settle_hand(game, player, dealer, payout, status, stats):
    hands = [make_hand(*player)]

    game.settle_all_hands(cards(*dealer), hands)

    assert hands[0]["status"] == status
    assert game.wallet.balance == 100 + payout
    assert (game.wins, game.losses, game.pushes) == stats

def test_settle_multiple_hands(game):
    hands = [
        make_hand("K", "Q", bet=10),
        make_hand("K", "7", bet=20),
        make_hand("K", "8", bet=30),
        make_hand("K", "Q", "5", bet=40),
    ]

    game.settle_all_hands(cards("Q", "8"), hands)

    assert [h["status"] for h in hands] == [
        "Won", "Lost", "Push", "Lost"
    ]
    assert game.wallet.balance == 150
    assert (game.wins, game.losses, game.pushes) == (1, 2, 1)

def test_settlement_accumulates_stats(game):
    game.wins = 2
    game.losses = 3
    game.pushes = 1

    game.settle_all_hands(
        cards("K", "8"),
        [
            make_hand("K", "Q"),
            make_hand("K", "7"),
            make_hand("Q", "8"),
        ],
    )

    assert (game.wins, game.losses, game.pushes) == (3, 4, 2)
    assert game.wallet.balance == 130

@pytest.mark.parametrize("wins, losses, pushes, rate", [
    (0, 0, 0, "0.0%"),
    (2, 1, 1, "50.0%"),
    (3, 0, 0, "100.0%"),
    (0, 2, 1, "0.0%"),
])
def test_show_stats(game, capsys, wins, losses, pushes, rate):
    game.wins = wins
    game.losses = losses
    game.pushes = pushes

    game.show_stats()

    output = capsys.readouterr().out
    assert f"Wins: {wins}" in output
    assert f"Losses: {losses}" in output
    assert f"Pushes: {pushes}" in output
    assert f"Win rate: {rate}" in output
    assert "Balance: $100" in output