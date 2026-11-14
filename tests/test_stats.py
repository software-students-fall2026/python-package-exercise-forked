import random
from funcasino.wallet import Wallet
from funcasino.slots import Slots
from funcasino.cointoss import CoinToss
from funcasino.craps import Craps
from funcasino.blackjack import Blackjack
from funcasino.stats import show_stats

def test_show_stats_empty(capsys):
    wallet = Wallet(100)
    games = {
        "Slots": Slots(wallet),
        "Coin Toss": CoinToss(wallet),
        "Craps": Craps(wallet),
        "Blackjack": Blackjack(wallet),
    }

    show_stats(games, wallet)
    out = capsys.readouterr().out

    assert "Total Wins:   0" in out
    assert "Total Losses: 0" in out
    assert "Total Ties:" not in out
    assert "Win Rate:     0.0%" in out
    assert "Net Profit:   $+0" in out
    assert "Balance:      $100" in out

def test_show_stats_totals(capsys):
    wallet = Wallet(140)
    slots = Slots(wallet)
    cointoss = CoinToss(wallet)
    craps = Craps(wallet)
    blackjack = Blackjack(wallet)

    slots.wins, slots.losses = 2, 1
    cointoss.wins = 1
    craps.losses = 2
    blackjack.wins, blackjack.losses = 1, 1

    games = {
        "Slots": slots,
        "Coin Toss": cointoss,
        "Craps": craps,
        "Blackjack": blackjack,
    }

    show_stats(games, wallet)
    out = capsys.readouterr().out

    assert "Slots        2W / 1L" in out
    assert "Coin Toss    1W / 0L" in out
    assert "Craps        0W / 2L" in out
    assert "Blackjack    1W / 1L" in out
    assert "Total Wins:   4" in out
    assert "Total Losses: 4" in out
    assert "Win Rate:     50.0%" in out
    assert "Net Profit:   $+40" in out
    assert "Balance:      $140" in out

def test_show_stats_ties_and_loss(capsys):
    wallet = Wallet(75)
    blackjack = Blackjack(wallet)
    blackjack.wins = 1
    blackjack.losses = 2
    blackjack.ties = 1

    show_stats({"Blackjack": blackjack}, wallet)
    out = capsys.readouterr().out

    assert "Blackjack    1W / 2L / 1T" in out
    assert "Total Wins:   1" in out
    assert "Total Losses: 2" in out
    assert "Total Ties:   1" in out
    assert "Win Rate:     25.0%" in out
    assert "Net Profit:   $-25" in out
    assert "Balance:      $75" in out

def test_show_stats_after_rounds(capsys):
    random.seed(1)
    wallet = Wallet(100)
    slots = Slots(wallet)
    craps = Craps(wallet)

    slots.play_round(10, animate=False)
    slots.play_round(10, animate=False)

    show_stats({"Slots": slots, "Craps": craps}, wallet)
    out = capsys.readouterr().out

    assert slots.wins + slots.losses == 2
    assert f"Balance:      ${wallet.balance}" in out
    assert f"Net Profit:   ${wallet.balance - 100:+d}" in out