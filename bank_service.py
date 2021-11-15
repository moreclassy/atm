import data
from data import Values
from exception import BankServiceException
from model import Account


class BankService:

    @classmethod
    def get_account_with_card_number_and_pin(cls, card_number, pin):
        account = [val for val in Values.accounts if val['card_number'] == card_number]

        if not account:
            raise BankServiceException.NotFound('wrong card number')
        account = account[0]

        account_number = account.get('account_number', None)
        balance = account.get('balance', None)
        account_pin = account.get('pin', None)

        if account_number is None or balance is None or account_pin is None:
            raise BankServiceException.InternalError('invalid account')

        if account_pin != pin:
            raise BankServiceException.Unauthorized('wrong pin')

        return Account(account_number=account_number, balance=balance)

    @classmethod
    def get_balance_with_account_number(cls, account_number):
        account = [val for val in Values.accounts if val['account_number'] == account_number]

        if len(account) < 1:
            raise BankServiceException.NotFound('wrong account number')
        account = account[0]

        balance = account.get('balance', None)
        if balance is None:
            raise BankServiceException.InternalError('invalid account')

        return balance

    @classmethod
    def get_account_with_account_number(cls, account_number):
        account = cls.__get_account_with_account_number(account_number)

        account_number = account.get('account_number', None)
        balance = account.get('balance', None)

        if account_number is None or balance is None:
            raise BankServiceException.InternalError('invalid account')

        return Account(account_number=account_number, balance=balance)

    @classmethod
    def deposit(cls, account_number, amount):
        if amount <= 0:
            raise BankServiceException.WrongInput('deposit amount has to be bigger than zero')

        account = cls.__get_account_with_account_number(account_number)

        balance = account.get('balance', None)
        if balance is None:
            raise BankServiceException.InternalError('invalid account')

        new_balance = balance + amount
        account['balance'] = new_balance

        transaction_id = cls.__log_transaction('deposit', account_number, amount)

        return transaction_id

    @classmethod
    def withdraw(cls, account_number, amount, pin):
        if amount <= 0:
            raise BankServiceException.WrongInput('withdraw amount has to be bigger than zero')

        account = cls.__get_account_with_account_number(account_number)

        account_pin = account.get('pin', None)
        balance = account.get('balance', None)
        if account_pin is None or balance is None:
            raise BankServiceException.InternalError('invalid account')

        if account_pin != pin:
            raise BankServiceException.Unauthorized('wrong pin')

        new_balance = balance - amount
        if new_balance < 0:
            raise BankServiceException.InsufficientBalance('insufficient balance')

        account['balance'] = new_balance

        transaction_id = cls.__log_transaction('withdraw', account_number, -amount)

        return transaction_id

    @classmethod
    def revert_transaction(cls, transaction_id):
        transaction = [val for val in Values.transactions if val['key'] == transaction_id]
        if len(transaction) <= 0:
            raise BankServiceException.NotFound('insufficient balance')

        transaction = transaction[0]

        # Todo: revert transaction
        cls.__log_transaction('revert', transaction.get('account_number', None), -transaction.get('amount', 0))

        return True

    @classmethod
    def __get_account_with_account_number(cls, account_number):
        account = [val for val in Values.accounts if val['account_number'] == account_number]

        if len(account) < 1:
            raise BankServiceException.NotFound('wrong account number')

        return account[0]

    @classmethod
    def __log_transaction(cls, transaction_type, account_number, amount):
        new_key = len(data.Values.transactions) + 1

        data.Values.transactions.append({
            'key': new_key,
            'type': transaction_type,
            'account_number': account_number,
            'amount': amount,
        })

        return new_key
