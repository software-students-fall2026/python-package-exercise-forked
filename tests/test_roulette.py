from funcasino import roulette
from funcasino.wallet import InsufficientFunds, Wallet


def test_build_bets_three_zero_splits():
    game = roulette.Roulette()
    bets = game.build_bets()

    assert bets["split 0 1"] == ({0, 1}, 17)
    assert bets["split 0 2"] == ({0, 2}, 17)
    assert bets["split 0 3"] == ({0, 3}, 17)


def test_bet_name_orders_split_numbers():
    game = roulette.Roulette()
    assert game.bet_name("split 20 17") == "split 17 20"


def test_bet_name_rejects_nonadjacent_split():
    game = roulette.Roulette()

    try:
        game.bet_name("split 17 19")
    except ValueError as error:
        assert "valid bet" in str(error)
    else:
        assert False, "Expected a split between nonadjacent pockets to be rejected"


def test_place_bet_reserve_money_until_spin():
    wallet = Wallet(100)
    game = roulette.Roulette(wallet=wallet)

    game.place_bet("red", 10)
    game.place_bet("even", 5)

    assert game.pending_stake() == 15
    assert game.available_chips() == 85
    assert wallet.balance == 100


def test_place_bet_reject_stake_above_available_money():
    wallet = Wallet(100)
    game = roulette.Roulette(wallet=wallet)
    game.place_bet("red", 90)

    try:
        game.place_bet("black", 11)
    except ValueError as error:
        assert "$10" in str(error)
    else:
        assert False, "Expected the $11 bet to be rejected when $10 was available"

    assert game.pending_stake() == 90
    assert wallet.balance == 100


def test_place_bet_reject_fractional_stake():
    game = roulette.Roulette()

    try:
        game.place_bet("red", 2.5)
    except ValueError as error:
        assert "whole-dollar" in str(error)
    else:
        assert False, "Expected a fractional stake to be rejected"

    assert game.pending_stake() == 0


def test_clear_bets_makes_reserved_money_available_again():
    wallet = Wallet(100)
    game = roulette.Roulette(wallet=wallet)
    game.place_bet("red", 25)

    game.clear_bets()

    assert game.pending_stake() == 0
    assert game.available_chips() == 100
    assert wallet.balance == 100


def test_spin_settles_multiple_bets_against_one_pocket():
    wallet = Wallet(100)
    game = roulette.Roulette(wallet=wallet)
    game.place_bet("straight 17", 10)
    game.place_bet("even", 5)

    pocket, results = game.spin()

    assert 0 <= pocket <= 36
    straight_change = -10
    if pocket == 17:
        straight_change = 350
    even_change = -5
    if pocket != 0 and pocket % 2 == 0:
        even_change = 5

    assert results == [("straight 17", straight_change), ("even", even_change)]
    assert wallet.balance == 100 + straight_change + even_change
    assert game.pending_stake() == 0


def test_zero_is_a_straight_bet_and_is_excluded_from_even():
    game = roulette.Roulette()
    bets = game.build_bets()

    assert bets["straight 0"] == ({0}, 35)
    assert 0 not in bets["even"][0]


def test_spin_rejects_an_empty_table():
    game = roulette.Roulette()

    try:
        game.spin()
    except ValueError as error:
        assert "before spinning" in str(error)
    else:
        assert False, "Expected a spin with no bets to be rejected"


def test_spin_rejects_a_round_when_the_shared_wallet_is_short():
    wallet = Wallet(100)
    game = roulette.Roulette(wallet=wallet)
    game.place_bet("red", 90)
    wallet.withdraw(20)

    try:
        game.spin()
    except InsufficientFunds:
        assert wallet.balance == 80
        assert game.pending_stake() == 90
    else:
        assert (
            False
        ), "Expected the spin to fail when the wallet could no longer cover the bet"
