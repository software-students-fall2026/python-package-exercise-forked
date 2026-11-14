import pytest
from funcasino.wallet import Wallet, InsufficientFunds

def test_default_balance():
    wallet = Wallet()
    assert wallet.balance == 100
    assert isinstance(wallet.balance, int)
    assert wallet.can_afford(100)

def test_custom_balance():
    assert Wallet(500).balance == 500
    assert Wallet(0).balance == 0
    assert Wallet(1).balance == 1

def test_balance_is_read_only():
    wallet = Wallet(50)
    with pytest.raises(AttributeError):
        wallet.balance = 1000
    assert wallet.balance == 50
    assert wallet._balance == 50

def test_can_afford_valid():
    wallet = Wallet(100)
    assert wallet.can_afford(1)
    assert wallet.can_afford(50)
    assert wallet.can_afford(100)

def test_can_afford_invalid():
    wallet = Wallet(100)
    assert not wallet.can_afford(101)
    assert not wallet.can_afford(0)
    assert not wallet.can_afford(-10)
    assert not Wallet(0).can_afford(1)

def test_withdraw():
    wallet = Wallet(100)
    wallet.withdraw(30)
    assert wallet.balance == 70
    wallet.withdraw(70)
    assert wallet.balance == 0
    assert not wallet.can_afford(1)

def test_withdraw_invalid_amount():
    wallet = Wallet(100)
    with pytest.raises(ValueError):
        wallet.withdraw(0)
    with pytest.raises(ValueError):
        wallet.withdraw(-5)
    assert wallet.balance == 100

def test_withdraw_insufficient_funds():
    wallet = Wallet(50)
    with pytest.raises(InsufficientFunds):
        wallet.withdraw(51)
    with pytest.raises(InsufficientFunds):
        Wallet(0).withdraw(1)
    assert wallet.balance == 50

def test_insufficient_funds_is_value_error():
    assert issubclass(InsufficientFunds, ValueError)
    with pytest.raises(ValueError):
        Wallet(10).withdraw(20)
    with pytest.raises(InsufficientFunds, match=r"balance is only \$10"):
        Wallet(10).withdraw(20)

def test_deposit():
    wallet = Wallet(100)
    wallet.deposit(50)
    assert wallet.balance == 150
    wallet.deposit(0)
    assert wallet.balance == 150
    wallet.deposit(1)
    assert wallet.balance == 151

def test_deposit_invalid():
    wallet = Wallet(100)
    with pytest.raises(ValueError):
        wallet.deposit(-1)
    with pytest.raises(ValueError):
        wallet.deposit(-100)
    assert wallet.balance == 100

def test_shared_wallet():
    wallet = Wallet(100)
    same = wallet
    wallet.withdraw(40)
    same.deposit(10)
    assert wallet.balance == 70
    assert same.balance == 70
    assert same is wallet