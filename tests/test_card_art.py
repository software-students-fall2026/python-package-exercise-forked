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

def test_render_cards_empty():
    assert render_cards() == "\n" * 6
    assert len(render_cards().split("\n")) == 7
    assert render_cards().strip() == ""

def test_render_cards_invalid():
    with pytest.raises(AttributeError):
        render_cards("K of Hearts")
    with pytest.raises(AttributeError):
        render_cards(Card("K", "Hearts"), 5)
    with pytest.raises(AttributeError):
        render_cards(Card("K", "Hearts"), None, gap=3)

def test_render_battle():
    art = render_battle(Card("K", "Hearts"), Card("7", "Spades"))
    rows = art.split("\n")
    assert len(rows) == 8
    assert "Player" in rows[0] and "Dealer" in rows[0]
    assert rows[0].index("Player") < rows[0].index("Dealer")
    assert rows[2] == "│ K       │        │ 7       │"

def test_render_battle_vs_in_middle():
    rows = render_battle(Card("2", "Clubs"), Card("A", "Diamonds")).split("\n")
    assert "vs" in rows[4]
    assert sum("vs" in row for row in rows) == 1
    assert all(len(row) == 11 + 8 + 11 for row in rows[1:])

def test_render_battle_invalid():
    with pytest.raises(AttributeError):
        render_battle(None, Card("K", "Hearts"))
    with pytest.raises(AttributeError):
        render_battle(Card("K", "Hearts"), None)
    with pytest.raises(TypeError):
        render_battle(Card("K", "Hearts"))