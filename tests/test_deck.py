import pytest
from collections import Counter
from funcasino.deck import Card, Deck

def test_default_deck():
    deck = Deck()

    assert deck.num_decks == 1
    assert deck.size() == 52
    assert all(isinstance(card,Card) for card in deck.cards)

@pytest.mark.parametrize("num_decks", [1, 2, 8])
def test_multiple_decks(num_decks):
    deck = Deck(num_decks)

    assert deck.num_decks == num_decks
    assert deck.size() == 52 * num_decks
    assert all(isinstance(card,Card) for card in deck.cards)

@pytest.mark.parametrize("num_decks", [1, 2, 8])
def test_deck_correct_cards(num_decks):
    deck = Deck(num_decks)

    suits = ("Hearts", "Diamonds", "Clubs", "Spades")
    ranks = ("2", "3", "4", "5", "6", "7", "8", "9",
             "10", "J", "Q", "K", "A")

    expected = Counter({
        (rank, suit): num_decks
        for suit in suits
        for rank in ranks
    })
    actual = Counter((card.rank, card.suit) for card in deck.cards)

    assert actual == expected

@pytest.mark.parametrize("num_decks", [0, -1, -10])
def test_invalid_deck_count(num_decks):
    with pytest.raises(ValueError, match="at least 1"):
        Deck(num_decks)

@pytest.mark.parametrize("num_decks", [1.5, "2", None, [], {}, ";"])
def test_invalid_deck_type(num_decks):
    with pytest.raises(TypeError, match="must be an integer"):
        Deck(num_decks)

def test_deal_card():
    deck = Deck()

    top_card = deck.cards[-1]
    dealt_card = deck.deal()

    assert dealt_card is top_card
    assert deck.size() == 51
    assert dealt_card not in deck.cards

def test_deal_cards():
    deck = Deck()

    for _ in range(30):
        deck.deal()

    assert deck.size() == 22

def test_deal_deck():
    deck = Deck()

    dealt_cards = []
    for i in range(52):
        dealt_cards.append(deck.deal())

    assert deck.size() == 0
    assert len(dealt_cards) == 52

def test_deal_empty_deck():
    deck = Deck()

    for _ in range(52):
        deck.deal()

    with pytest.raises(ValueError, match="The deck is empty"):
        deck.deal()

@pytest.mark.parametrize("num_decks", [1, 2, 5, 100, 305])
def test_shuffle(num_decks):
    deck = Deck(num_decks)

    orig_cards = Counter(deck.cards)
    deck.shuffle()

    assert deck.size() == 52 * num_decks
    assert Counter(deck.cards) == orig_cards