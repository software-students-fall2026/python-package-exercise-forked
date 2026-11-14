import io
import random
import sys
from funcasino.craps import Craps, dice_art
from funcasino.wallet import Wallet
import time

#so it doesn't roll dice animation each time to delay tests
def no_sleep(time):
    pass

time.sleep = no_sleep

def test_init_default_wallet():
    craps = Craps()
    assert craps.wallet.balance == 100
    assert craps.wins == 0
    assert craps.losses == 0

def test_init_shared_wallet():
    wallet = Wallet(500)
    craps = Craps(wallet)
    assert craps.wallet is wallet
    assert craps.wallet.balance == 500
    wallet.deposit(50)
    assert craps.wallet.balance == 550

def test_dice_art():
    assert set(dice_art.keys()) == {1, 2, 3, 4, 5, 6}
    assert all(len(art) == 5 for art in dice_art.values())

def test_print_dice(capsys):
    craps = Craps()
    craps.print_dice(1, 6)
    out = capsys.readouterr().out
    assert "┌─────────┐" in out
    assert "└─────────┘" in out
    assert "●" in out

def test_roll_dice():
    craps = Craps()
    d1, d2, total = craps.roll_dice()
    assert 1 <= d1 <= 6
    assert 1 <= d2 <= 6
    assert total == d1 + d2

def test_place_bet_valid():
    sys.stdin = io.StringIO("25\n")
    wallet = Wallet(100)
    craps = Craps(wallet)
    bet = craps.place_bet()
    assert bet == 25
    assert wallet.balance == 75

def test_place_bet_invalid_then_valid(capsys):
    sys.stdin = io.StringIO("abc\n0\n-10\n200\n20\n")
    wallet = Wallet(50)
    craps = Craps(wallet)
    bet = craps.place_bet()
    out = capsys.readouterr().out
    assert bet == 20
    assert wallet.balance == 30
    assert "Please enter a valid number." in out
    assert "Invalid bet amount." in out

def test_play_round_natural_win(capsys):
    random.seed(1)
    sys.stdin = io.StringIO("20\n\n")
    wallet = Wallet(100)
    craps = Craps(wallet)
    craps.play_round()
    out = capsys.readouterr().out
    assert craps.wins == 1
    assert craps.losses == 0
    assert wallet.balance == 120
    assert "Natural 7! You won $40!" in out

def test_play_round_craps_loss(capsys):
    random.seed(2)
    sys.stdin = io.StringIO("20\n\n")
    wallet = Wallet(100)
    craps = Craps(wallet)
    craps.play_round()
    out = capsys.readouterr().out
    assert craps.wins == 0
    assert craps.losses == 1
    assert wallet.balance == 80
    assert "Craps (2)! You lost $20!" in out

def test_play_round_point_win_no_extra(capsys):
    random.seed(5)
    sys.stdin = io.StringIO("20\n\nn\n" + "\n" * 10)
    wallet = Wallet(100)
    craps = Craps(wallet)
    craps.play_round()
    out = capsys.readouterr().out
    assert craps.wins == 1
    assert craps.losses == 0
    assert wallet.balance == 120
    assert "You hit your number! You won $40!" in out

def test_play_round_point_win_extra_2_2x():
    random.seed(5)
    sys.stdin = io.StringIO("20\n\ny\n10\n" + "\n" * 10)
    wallet = Wallet(100)
    craps = Craps(wallet)
    craps.play_round()
    assert craps.wins == 1
    assert wallet.balance == 132

def test_play_round_point_win_extra_2_5x():
    random.seed(8)
    sys.stdin = io.StringIO("20\n\ny\n10\n" + "\n" * 10)
    wallet = Wallet(100)
    craps = Craps(wallet)
    craps.play_round()
    assert craps.wins == 1
    assert wallet.balance == 135

def test_play_round_point_win_extra_3x():
    random.seed(36)
    sys.stdin = io.StringIO("20\n\ny\n10\n" + "\n" * 20)
    wallet = Wallet(100)
    craps = Craps(wallet)
    craps.play_round()
    assert craps.wins == 1
    assert wallet.balance == 140

def test_play_round_seven_out_with_extra(capsys):
    random.seed(0)
    sys.stdin = io.StringIO("20\n\nmaybe\ny\n10\n" + "\n" * 10)
    wallet = Wallet(100)
    craps = Craps(wallet)
    craps.play_round()
    out = capsys.readouterr().out
    assert craps.wins == 0
    assert craps.losses == 1
    assert wallet.balance == 70
    assert "You lost $30!" in out

def test_play_round_extra_bet_zero_balance(capsys):
    random.seed(5)
    sys.stdin = io.StringIO("100\n\ny\n" + "\n" * 10)
    wallet = Wallet(100)
    craps = Craps(wallet)
    craps.play_round()
    out = capsys.readouterr().out
    assert "You have no money to add!" in out
    assert craps.wins == 1
    assert wallet.balance == 200

def test_show_stats(capsys):
    sys.stdin = io.StringIO("\n")
    craps = Craps(Wallet(80))
    craps.wins = 1
    craps.losses = 3
    craps.show_stats()
    out = capsys.readouterr().out
    assert "Wins: 1" in out
    assert "Losses: 3" in out
    assert "Win rate: 25.0%" in out
    assert "Balance: $80" in out

def test_show_stats_no_games(capsys):
    sys.stdin = io.StringIO("\n")
    Craps().show_stats()
    out = capsys.readouterr().out
    assert "Wins: 0" in out
    assert "Losses: 0" in out
    assert "Win rate: 0.0%" in out
    assert "Balance: $100" in out

def test_play_menu_quit(capsys):
    sys.stdin = io.StringIO("9\n2\n\n3\n\n")
    Craps().play()
    out = capsys.readouterr().out
    assert "Invalid option." in out
    assert "--- CRAPS STATS ---" in out
    assert "Thanks for playing!" in out