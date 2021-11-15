from dataclasses import dataclass


@dataclass
class Account:
    account_number: str
    balance: int

    def __init__(self, account_number: str, balance: int):
        self.account_number = account_number
        self.balance = balance
