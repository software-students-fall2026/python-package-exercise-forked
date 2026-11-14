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
    assert slots.payout(["💎", "💎", "💎"], 10) == 1000
    assert slots.payout(["⭐", "⭐", "⭐"], 10) == 500
    assert slots.payout(["🔔", "🔔", "🔔"], 10) == 200
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
    assert 0.7 < rtp < 0.95
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
    wallet = Wallet(1000)
    slots = Slots(wallet)
    for _ in range(3):
        slots.play_round(10, animate=False)
    bet = wallet.balance
    result, winnings = slots.play_round(bet, animate=False)
    assert result == ["🍋", "🍋", "🍋"]
    assert winnings == bet * 10
    assert wallet.balance == bet * 10
    assert slots.rescue_used is True

def test_play_round_no_rescue_too_early():
    for _ in range(20):
        slots = Slots(Wallet(10))
        slots.play_round(10, animate=False)
        assert slots.rescue_used is False
    assert slots.wins + slots.losses == 1
    assert slots.wallet.balance >= 0

def test_play_round_rescue_only_once():
    wallet = Wallet(1000)
    slots = Slots(wallet)
    for _ in range(3):
        slots.play_round(10, animate=False)
    slots.play_round(wallet.balance, animate=False)
    slots.play_round(wallet.balance, animate=False)
    assert slots.rescue_used is True
    assert slots.wins + slots.losses == 5
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

def test_loss_hint():
    slots = Slots()
    assert slots.loss_hint(0) is None
    assert slots.loss_hint(Slots.HINT_AFTER - 1) is None
    assert slots.loss_hint(Slots.HINT_AFTER) in Slots.HOT_HINTS
    assert slots.loss_hint(Slots.HINT_AFTER + 7) in Slots.HOT_HINTS

def test_loss_hint_invalid():
    slots = Slots()
    with pytest.raises(ValueError):
        slots.loss_hint(-1)
    with pytest.raises(ValueError):
        slots.loss_hint(-10)
    assert slots.loss_hint(Slots.HINT_AFTER) is not None

def test_loss_streak():
    slots = Slots(Wallet(1000))
    assert slots.loss_streak == 0
    for _ in range(30):
        _, winnings = slots.play_round(10, animate=False)
        if winnings >= 10:
            assert slots.loss_streak == 0
        else:
            assert slots.loss_streak >= 1
    assert slots.loss_streak <= slots.losses

def test_add_to_jackpot():
    slots = Slots()
    assert slots.jackpot == Slots.JACKPOT_START
    assert slots.add_to_jackpot(100) == 10
    assert slots.add_to_jackpot(5) == 1
    assert slots.jackpot == Slots.JACKPOT_START + 11

def test_add_to_jackpot_invalid():
    slots = Slots()
    with pytest.raises(ValueError):
        slots.add_to_jackpot(0)
    with pytest.raises(ValueError):
        slots.add_to_jackpot(-20)
    assert slots.jackpot == Slots.JACKPOT_START

def test_jackpot_win():
    wallet = Wallet(100)
    slots = Slots(wallet)
    slots.WEIGHTS = [0, 0, 0, 0, 1]
    slots.jackpot = 1000
    result, winnings = slots.play_round(10, animate=False)
    assert result == ["💎", "💎", "💎"]
    assert winnings == 10 * 100 + 1001
    assert wallet.balance == 100 - 10 + 2001
    assert slots.jackpot == Slots.JACKPOT_START

def test_free_spin_no_jackpot_cut():
    slots = Slots(Wallet(100))
    slots.WEIGHTS = [1, 0, 0, 0, 0]
    slots.play_round(10, animate=False, free=True)
    assert slots.jackpot == Slots.JACKPOT_START
    slots.play_round(10, animate=False)
    assert slots.jackpot == Slots.JACKPOT_START + 1