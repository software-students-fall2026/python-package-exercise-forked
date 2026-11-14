import pytest
from funcasino.card_art import SUIT_SYMBOLS, CARD_BACK, card_lines, render_cards, render_battle
from funcasino.deck import Card, Deck, SUITS

def test_suit_symbols():
    assert SUIT_SYMBOLS["Hearts"] == "♥"
    assert SUIT_SYMBOLS["Diamonds"] == "♦"
    assert SUIT_SYMBOLS["Clubs"] == "♣"
    assert SUIT_SYMBOLS["Spades"] == "♠"
    assert set(SUIT_SYMBOLS) == set(SUITS)

def test_card_back():
    assert len(CARD_BACK) == 7
    assert all(len(row) == 11 for row in CARD_BACK)
    assert CARD_BACK[0] == "┌─────────┐"
    assert CARD_BACK[-1] == "└─────────┘"
    assert all("░" in row for row in CARD_BACK[1:-1])

def test_card_lines():
    lines = card_lines(Card("K", "Hearts"))
    assert len(lines) == 7
    assert lines[1] == "│ K       │"
    assert lines[3] == "│    ♥    │"
    assert lines[5] == "│       K │"

def test_card_lines_ten():
    lines = card_lines(Card("10", "Spades"))
    assert lines[1] == "│ 10      │"
    assert lines[5] == "│      10 │"
    assert "♠" in lines[3]

def test_card_lines_same_width():
    for card in Deck().cards:
        lines = card_lines(card)
        assert len(lines) == len(CARD_BACK)
        assert all(len(row) == 11 for row in lines)
    assert len(Deck().cards) == 52

def test_card_lines_invalid():
    with pytest.raises(AttributeError):
        card_lines(None)
    with pytest.raises(AttributeError):
        card_lines("K of Hearts")
    with pytest.raises(AttributeError):
        card_lines(42)

def test_render_cards_single():
    art = render_cards(Card("A", "Diamonds"))
    rows = art.split("\n")
    assert len(rows) == 7
    assert rows[1] == "│ A       │"
    assert "♦" in rows[3]

def test_render_cards_multiple():
    art = render_cards(Card("2", "Clubs"), Card("Q", "Hearts"))
    rows = art.split("\n")
    assert len(rows) == 7
    assert rows[0] == "┌─────────┐  ┌─────────┐"
    assert rows[1] == "│ 2       │  │ Q       │"
    assert "♣" in rows[3] and "♥" in rows[3]

def test_render_cards_face_down():
    art = render_cards(Card("7", "Spades"), None)
    rows = art.split("\n")
    assert rows[1].endswith(CARD_BACK[1])
    assert rows[1].startswith("│ 7")
    assert render_cards(None) == "\n".join(CARD_BACK)

def test_render_cards_custom_gap():
    art = render_cards(Card("3", "Hearts"), Card("4", "Hearts"), gap=" | ")
    rows = art.split("\n")
    assert all(" | " in row for row in rows)
    assert len(rows[0]) == 11 + 3 + 11
    assert render_cards(None, None, gap="").split("\n")[0] == "┌─────────┐┌─────────┐"