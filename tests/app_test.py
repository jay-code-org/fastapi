import pytest
from app.calculations import BankAccount, InsufficientBalanceException, add


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,expected", [(1, 3, 4), (5, 6, 11), (7, 8, 15), (20, 13, 33)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_bank_zero_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_deposit_amount(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_bank_withdraw_amount(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40


def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposit,withdraw,expected", [
    (100, 30, 70),
    (30, 10, 20),
    (50, 40, 10),
])
def test_bank_transactions(deposit, withdraw, expected, zero_bank_account):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected


def test_bank_insufficient_balance(zero_bank_account):
    zero_bank_account.deposit(100)
    with pytest.raises(InsufficientBalanceException):
        zero_bank_account.withdraw(200)
