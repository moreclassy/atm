from bank_service import BankService
from cash_bin import CashBin
from exception import ATMServiceException, CashBinException
from model import Account


class ATMService:
    __account: Account

    def __init__(self, card_number, pin):
        self.read_card(card_number, pin)

    def read_card(self, card_number, pin):
        result = BankService.get_account_with_card_number_and_pin(card_number, pin)

        self.__account = result

    def deposit(self, amount):
        try:
            if amount <= 0:
                raise ATMServiceException.WrongInput('deposit amount has to be bigger than zero')

            account_number = self.__get_account_number()

            transaction_id = BankService.deposit(account_number, amount)

            CashBin.insert(amount)
        except CashBinException.WrongInput as e:
            if transaction_id:
                BankService.revert_transaction(transaction_id)
            CashBin.give_back_bill()
            raise e

    def withdraw(self, amount, pin):
        try:
            if amount <= 0:
                raise ATMServiceException.WrongInput('withdraw amount has to be bigger than zero')

            self.__refresh_balance()

            account_number = self.__get_account_number()
            account_balance = self.__get_account_balance()
            if account_balance < amount:
                raise ATMServiceException.InsufficientBalance('account has insufficient balance')

            transaction_id = BankService.withdraw(account_number, amount, pin)

            CashBin.extract(amount)
        except (CashBinException.WrongInput, CashBinException.InsufficientReserve) as e:
            if transaction_id:
                BankService.revert_transaction(transaction_id)
            raise e

    def __get_account_number(self):
        return self.__account.account_number

    def __get_account_balance(self):
        return self.__account.balance

    def get_account_number(self):
        return self.get_account_number()

    def get_account_balance(self):
        self.__refresh_balance()
        return self.__get_account_balance()

    def __refresh_balance(self):
        account_number = self.__get_account_number()
        balance = BankService.get_balance_with_account_number(account_number)
        self.__account.balance = balance
