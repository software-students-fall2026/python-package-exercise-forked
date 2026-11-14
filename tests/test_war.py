import io
import sys
import random
import pytest
from funcasino.deck import Card, Deck
from funcasino.war import War
from funcasino.wallet import Wallet
from collections import deque

def make_hand(*ranks):
    return deque(Card(rank, "Hearts") for rank in ranks)

def test_init_default_wallet():
    war = War()
    assert war.wallet.balance == 100
    assert war.hand_size == 10
    assert war.max_battles == 20
    assert len(war.player_hand) == 0
    assert len(war.dealer_hand) == 0

def test_init_shared_wallet():
    wallet = Wallet(500)
    war = War(wallet)
    assert war.wallet is wallet
    assert war.wallet.balance == 500
    wallet.deposit(50)
    assert war.wallet.balance == 550

def test_card_value():
    war = War()
    twoOfh = Card("2", "Hearts")
    tenOfc = Card("10", "Clubs")
    aceOfs = Card("A", "Spades")
    assert war.card_value(twoOfh) == 0
    assert war.card_value(tenOfc) == 8
    assert war.card_value(aceOfs) == 12
    assert war.card_value(Card("K", "Hearts")) > war.card_value(Card("Q", "Hearts"))

def test_deal_hands():
    war = War()
    war.deal_hands()
    assert len(war.player_hand) == 10
    assert len(war.dealer_hand) == 10
    cards = {(c.rank, c.suit) for c in war.player_hand + war.dealer_hand}
    assert len(cards) == 20

def test_deal_hands_resets():
    war = War()
    war.deal_hands()
    war.deal_hands()
    assert len(war.player_hand) == 10
    assert len(war.dealer_hand) == 10

def test_deal_hands_custom_size():
    war = War(hand_size=5)
    war.deal_hands()
    assert len(war.player_hand) == 5
    assert len(war.dealer_hand) == 5

def test_battle_player_wins():
    war = War()
    war.player_hand = make_hand("K")
    war.dealer_hand = make_hand("5")
    assert war.battle() == "player"
    assert len(war.player_hand) == 2
    assert len(war.dealer_hand) == 0

def test_battle_dealer_wins():
    war = War()
    war.player_hand = make_hand("3", "4")
    war.dealer_hand = make_hand("J", "6")
    assert war.battle() == "dealer"
    assert len(war.player_hand) == 1
    assert len(war.dealer_hand) == 3

def test_battle_war():
    war = War()
    war.player_hand = make_hand("7", "3", "4", "5", "K")
    war.dealer_hand = make_hand("7", "2", "2", "2", "2")
    assert war.battle() == "player"
    assert len(war.player_hand) == 10
    assert len(war.dealer_hand) == 0

def test_battle_war_short_hand():
    war = War()
    war.player_hand = make_hand("7", "9")
    war.dealer_hand = make_hand("7", "2", "2", "2", "3")
    assert war.battle() == "player"
    assert len(war.player_hand) == 7
    assert len(war.dealer_hand) == 0

def test_battle_runs_out_during_war():
    war = War()
    war.player_hand = make_hand("7")
    war.dealer_hand = make_hand("7", "5")
    assert war.battle() is None
    assert len(war.player_hand) == 0
    assert len(war.dealer_hand) == 3

def test_battle_cards_conserved():
    random.seed(0)
    war = War()
    war.deal_hands()
    for _ in range(10):
        if war.player_hand and war.dealer_hand:
            war.battle()
        assert len(war.player_hand) + len(war.dealer_hand) == 20

def test_simulate_result():
    for seed in range(10):
        random.seed(seed)
        war = War()
        result = war.simulate()
        assert result in ["player", "dealer", "tie"]
        assert len(war.player_hand) + len(war.dealer_hand) == 20

def test_simulate_winner_has_more_cards():
    random.seed(3)
    war = War()
    result = war.simulate()
    p, d = len(war.player_hand), len(war.dealer_hand)
    if result == "player":
        assert p > d
    elif result == "dealer":
        assert d > p
    else:
        assert p == d

def test_simulate_no_battles_is_tie():
    war = War(max_battles=0)
    assert war.simulate() == "tie"

def test_show(capsys):
    war = War()
    war.delay = 0
    war.show(Card("K", "Hearts"), Card("5", "Spades"), "Player takes 2 cards")
    out = capsys.readouterr().out
    assert "Player takes 2 cards" in out
    assert war.drawn is True
    war.show(Card("2", "Clubs"), Card("3", "Clubs"), "Dealer takes 2 cards")
    out = capsys.readouterr().out
    assert "\033[9A" in out

def test_payout():
    war = War()
    assert war.payout("player", "player", 10) == 20
    assert war.payout("dealer", "dealer", 10) == 20
    assert war.payout("tie", "tie", 10) == 90
    assert war.payout("player", "dealer", 10) == 0
    assert war.payout("tie", "player", 10) == 0

def test_place_bet_valid():
    sys.stdin = io.StringIO("25\n")
    wallet = Wallet(100)
    war = War(wallet)
    assert war.place_bet() == 25
    assert wallet.balance == 75

def test_place_bet_invalid_then_valid(capsys):
    sys.stdin = io.StringIO("abc\n0\n-10\n500\n20\n")
    wallet = Wallet(100)
    war = War(wallet)
    bet = war.place_bet()
    out = capsys.readouterr().out
    assert bet == 20
    assert wallet.balance == 80
    assert "Please enter a valid number." in out
    assert "Invalid bet amount." in out

def test_choose_side():
    sys.stdin = io.StringIO("PLAYER\n")
    assert War().choose_side() == "player"

def test_choose_side_invalid_then_valid():
    sys.stdin = io.StringIO("me\n\nTie\n")
    assert War().choose_side() == "tie"

def test_play_round_win(capsys):
    sys.stdin = io.StringIO("20\nplayer\n")
    war = War()
    war.simulate = lambda verbose: "player"
    war.play_round()
    out = capsys.readouterr().out
    assert war.wallet.balance == 120
    assert "Result: PLAYER" in out
    assert "You won $20!" in out

def test_play_round_loss(capsys):
    sys.stdin = io.StringIO("20\nplayer\n")
    war = War()
    war.simulate = lambda verbose: "dealer"
    war.play_round()
    out = capsys.readouterr().out
    assert war.wallet.balance == 80
    assert "You lost $20." in out

def test_play_round_tie_bet(capsys):
    sys.stdin = io.StringIO("10\ntie\n")
    war = War()
    war.simulate = lambda verbose: "tie"
    war.play_round()
    out = capsys.readouterr().out
    assert war.wallet.balance == 180
    assert "You won $80!" in out
