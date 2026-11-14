import io
import sys
import pytest
from funcasino.cointoss import CoinToss
from funcasino.wallet import Wallet

def no_animation(result):
    pass

def test_init_default_wallet():
    cointoss = CoinToss()
    assert cointoss.wallet.balance == 100
    assert cointoss.wins == 0
    assert cointoss.losses == 0
    assert cointoss.history == []

def test_init_shared_wallet():
    wallet = Wallet(500)
    cointoss = CoinToss(wallet)
    assert cointoss.wallet is wallet
    assert cointoss.wallet.balance == 500
    wallet.deposit(50)
    assert cointoss.wallet.balance == 550

def test_flip_coin():
    cointoss = CoinToss()
    results = [cointoss.flip_coin() for _ in range(200)]
    assert all(result in ["heads", "tails"] for result in results)
    assert "heads" in results
    assert "tails" in results

def test_place_bet_valid():
    sys.stdin = io.StringIO("25\n")
    cointoss = CoinToss()
    assert cointoss.place_bet() == 25

def test_place_bet_full_balance():
    sys.stdin = io.StringIO("100\n")
    cointoss = CoinToss()
    assert cointoss.place_bet() == 100

def test_place_bet_invalid_then_valid(capsys):
    sys.stdin = io.StringIO("abc\n0\n-5\n101\n10\n")
    cointoss = CoinToss()
    bet = cointoss.place_bet()
    out = capsys.readouterr().out
    assert bet == 10
    assert "Please enter a valid number." in out
    assert "Invalid bet amount." in out

def test_play_round_win():
    sys.stdin = io.StringIO("20\nheads\n")
    cointoss = CoinToss()
    cointoss.flip_coin = lambda: "heads"
    cointoss.animate_flip = no_animation
    cointoss.play_round()
    assert cointoss.wallet.balance == 120
    assert cointoss.wins == 1
    assert cointoss.losses == 0
    assert cointoss.history[-1]["balance"] == 120

def test_play_round_loss():
    sys.stdin = io.StringIO("30\nheads\n")
    cointoss = CoinToss()
    cointoss.flip_coin = lambda: "tails"
    cointoss.animate_flip = no_animation
    cointoss.play_round()
    assert cointoss.wallet.balance == 70
    assert cointoss.wins == 0
    assert cointoss.losses == 1
    assert cointoss.history[-1]["result"] == "tails"

def test_play_round_uppercase_choice():
    sys.stdin = io.StringIO("10\nTAILS\n")
    cointoss = CoinToss()
    cointoss.flip_coin = lambda: "tails"
    cointoss.animate_flip = no_animation
    cointoss.play_round()
    assert cointoss.wins == 1
    assert cointoss.history[-1]["choice"] == "tails"

def test_play_round_invalid_choice():
    sys.stdin = io.StringIO("10\nedge\n\nheads\n")
    cointoss = CoinToss()
    cointoss.flip_coin = lambda: "heads"
    cointoss.animate_flip = no_animation
    cointoss.play_round()
    assert cointoss.wins == 1
    assert cointoss.history[-1]["choice"] == "heads"

def test_play_round_history():
    sys.stdin = io.StringIO("10\nheads\n10\nheads\n10\ntails\n")
    cointoss = CoinToss()
    results = iter(["heads", "tails", "heads"])
    cointoss.flip_coin = lambda: next(results)
    cointoss.animate_flip = no_animation
    for _ in range(3):
        cointoss.play_round()
    assert cointoss.wins == 1
    assert cointoss.losses == 2
    assert len(cointoss.history) == 3
    assert [h["balance"] for h in cointoss.history] == [110, 100, 90]

def test_show_stats(capsys):
    cointoss = CoinToss(Wallet(80))
    cointoss.wins = 1
    cointoss.losses = 2
    cointoss.show_stats()
    out = capsys.readouterr().out
    assert "Wins: 1" in out
    assert "Losses: 2" in out
    assert "Win rate: 33.3%" in out
    assert "Balance: $80" in out

def test_show_stats_no_games(capsys):
    CoinToss().show_stats()
    out = capsys.readouterr().out
    assert "Wins: 0" in out
    assert "Losses: 0" in out
    assert "Win rate: 0.0%" in out
    assert "Balance: $100" in out

def test_animate_flip(monkeypatch, capsys):
    monkeypatch.setattr("time.sleep", lambda seconds: None)
    cointoss = CoinToss()
    cointoss.animate_flip("heads")
    out = capsys.readouterr().out
    assert "Flipping coin..." in out
    assert out.strip().split("\r")[-1].strip() == "🪙 HEADS"

def test_play_menu_quit(capsys):
    sys.stdin = io.StringIO("9\n2\n3\n")
    cointoss = CoinToss()
    cointoss.play()
    out = capsys.readouterr().out
    assert "Invalid option." in out
    assert "Win rate:" in out
    assert "Thanks for playing!" in out

def test_play_ends_at_zero_balance(capsys):
    sys.stdin = io.StringIO("1\n100\nheads\n")
    cointoss = CoinToss()
    cointoss.flip_coin = lambda: "tails"
    cointoss.animate_flip = no_animation
    cointoss.play()
    out = capsys.readouterr().out
    assert cointoss.wallet.balance == 0
    assert "Thanks for playing!" in out
