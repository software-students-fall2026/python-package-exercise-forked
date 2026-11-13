import random
import pytest
from funcasino.slots import Slots
from funcasino.wallet import Wallet, InsufficientFunds


def test_init_default_wallet():
    slots = Slots()
    assert slots.wallet.balance == 100
    assert slots.wins == 0
    assert slots.losses == 0
    assert slots.money_lost == 0
    assert slots.rescue_used is False

def test_init_shared_wallet():
    wallet = Wallet(500)
    slots = Slots(wallet)
    assert slots.wallet is wallet
    assert slots.wallet.balance == 500
    wallet.deposit(50)
    assert slots.wallet.balance == 550

def test_spin():
    slots = Slots()
    result = slots.spin()
    assert isinstance(result, list)
    assert len(result) == 3
    assert all(symbol in Slots.SYMBOLS for symbol in result)

def test_spin_custom_weights():
    slots = Slots()
    assert slots.spin([0, 0, 0, 0, 1]) == ["💎", "💎", "💎"]
    assert slots.spin([1, 0, 0, 0, 0]) == ["🍒", "🍒", "🍒"]
    assert slots.spin([0, 0, 1, 0, 0]) == ["🔔", "🔔", "🔔"]

def test_weights():
    assert len(Slots.WEIGHTS) == len(Slots.SYMBOLS)
    assert len(Slots.NEAR_WEIGHTS) == len(Slots.SYMBOLS)
    assert Slots.WEIGHTS == sorted(Slots.WEIGHTS, reverse=True)
    assert Slots.NEAR_WEIGHTS[-1] > Slots.WEIGHTS[-1]

def test_spin_grid():
    slots = Slots()
    grid = slots.spin_grid()
    assert len(grid) == 3
    assert all(len(row) == 3 for row in grid)
    assert all(symbol in Slots.SYMBOLS for row in grid for symbol in row)

def test_payout_wins():
    slots = Slots()
    assert slots.payout(["💎", "💎", "💎"], 10) == 640
    assert slots.payout(["⭐", "⭐", "⭐"], 10) == 250
    assert slots.payout(["🔔", "🔔", "🔔"], 10) == 150
    assert slots.payout(["🍋", "🍋", "🍋"], 10) == 100
    assert slots.payout(["🍒", "🍒", "🍒"], 10) == 50

def test_payout_cherry_pair():
    slots = Slots()
    assert slots.payout(["🍒", "🍒", "🍋"], 10) == 5
    assert slots.payout(["🍒", "🍒", "💎"], 1) == 0
    assert slots.payout(["🍒", "🍋", "🍒"], 10) == 0
    assert slots.payout(["🍋", "🍒", "🍒"], 10) == 0

def test_payout_no_match():
    slots = Slots()
    assert slots.payout(["🍒", "🍋", "🔔"], 10) == 0
    assert slots.payout(["💎", "💎", "⭐"], 10) == 0
    assert slots.payout(["⭐", "🔔", "💎"], 100) == 0

def test_payout_invalid_bet():
    slots = Slots()
    with pytest.raises(ValueError):
        slots.payout(["🍒", "🍒", "🍒"], 0)
    with pytest.raises(ValueError):
        slots.payout(["🍒", "🍒", "🍒"], -5)
    with pytest.raises(ValueError):
        slots.payout(["💎", "💎", "💎"], -1)

def test_near_miss():
    slots = Slots()
    assert slots.is_near_miss([["💎", "🍒", "🍋"], ["🍒", "💎", "🍋"], ["🍒", "🍋", "🔔"]])
    assert slots.is_near_miss([["💎", "🍒", "🍋"], ["🍒", "🍋", "🔔"], ["🍒", "🍋", "💎"]])
    assert not slots.is_near_miss([["💎", "🍒", "🍋"], ["🍒", "🍋", "🔔"], ["🍒", "🍋", "🔔"]])
    assert not slots.is_near_miss([["🍒", "🍒", "🍋"], ["🍒", "🍋", "🔔"], ["⭐", "🍋", "🔔"]])

def test_estimate_rtp():
    random.seed(0)
    slots = Slots()
    rtp = slots.estimate_rtp(20000)
    assert isinstance(rtp, float)
    assert 0.8 < rtp < 1.0
    assert rtp < 1

def test_play_round_balance():
    wallet = Wallet(1000)
    slots = Slots(wallet)
    result, winnings = slots.play_round(10, animate=False)
    assert len(result) == 3
    assert winnings >= 0
    assert wallet.balance == 1000 - 10 + winnings

def test_play_round_stats():
    wallet = Wallet(1000)
    slots = Slots(wallet)
    total = 0
    for _ in range(10):
        _, winnings = slots.play_round(10, animate=False)
        total += winnings
    assert slots.wins + slots.losses == 10
    assert 0 <= slots.money_lost <= 10 * slots.losses
    assert wallet.balance == 1000 - 100 + total
    assert slots.rescue_used is False

def test_play_round_rescue():
    wallet = Wallet(10)
    slots = Slots(wallet)
    result, winnings = slots.play_round(10, animate=False)
    assert result == ["🍋", "🍋", "🍋"]
    assert winnings == 100
    assert wallet.balance == 100
    assert slots.rescue_used is True
    assert slots.wins == 1

def test_play_round_rescue_only_once():
    wallet = Wallet(10)
    slots = Slots(wallet)
    slots.play_round(10, animate=False)
    slots.play_round(100, animate=False)
    assert slots.rescue_used is True
    assert slots.wins + slots.losses == 2
    assert wallet.balance >= 0

def test_play_round_invalid_bet():
    slots = Slots(Wallet(50))
    with pytest.raises(InsufficientFunds):
        slots.play_round(100, animate=False)
    with pytest.raises(ValueError):
        slots.play_round(0, animate=False)
    with pytest.raises(ValueError):
        slots.play_round(-10, animate=False)
    assert slots.wallet.balance == 50
    assert slots.wins + slots.losses == 0

def test_draw_grid(capsys):
    slots = Slots()
    slots.draw_grid([["🍒", "🍋", "🔔"], ["⭐", "⭐", "⭐"], ["💎", "🍒", "🍋"]])
    out = capsys.readouterr().out
    assert "⭐   ⭐   ⭐" in out
    assert "┌" in out and "┘" in out
    assert len(out.splitlines()) == 5

def test_show_menu(capsys):
    slots = Slots(Wallet(250))
    slots.show_menu()
    out = capsys.readouterr().out
    assert "S L O T S" in out
    assert "Balance: $250" in out
    assert "1 ▸ Spin" in out

def test_show_stats(capsys):
    slots = Slots(Wallet(80))
    slots.wins = 1
    slots.losses = 3
    slots.money_lost = 20
    slots.show_stats()
    out = capsys.readouterr().out
    assert "Wins: 1" in out
    assert "Losses: 3" in out
    assert "Money lost: $20" in out
    assert "Win rate: 25.0%" in out
    assert "Balance: $80" in out

def test_show_stats_no_games(capsys):
    Slots().show_stats()
    out = capsys.readouterr().out
    assert "Win rate: 0.0%" in out
    assert "Wins: 0" in out
    assert "Balance: $100" in out