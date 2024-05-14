def add(num1, num2):
    return num1 + num2


class InsufficientBalanceException(Exception):
    pass


class BankAccount():
    def __init__(self, start_balance=0) -> None:
        self.balance = start_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientBalanceException("Insufficient Balance")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
