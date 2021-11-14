import data
from constants import Code
from data import Values


class BankApi:

    @classmethod
    def get_account_with_card_number_and_pin(cls, card_number, pin):
        account = [val for val in Values.accounts if val['card_number'] == card_number]
        if not account:
            return {
                'code': Code.NotFound.code,
                'message': 'wrong card number',
            }
        account = account[0]

        account_pin = account.get('pin', None)
        if account_pin is None:
            return {
                'code': Code.InternalError.code,
                'message': 'invalid account',
            }

        if account_pin != pin:
            return {
                'code': Code.Unauthorized.code,
                'message': 'wrong pin'
            }

        return {
            'code': Code.Success.code,
            'message': Code.Success.message,
            'data': {key: account[key] for key in account if key == 'account_number' or key == 'balance'}
        }

    @classmethod
    def get_balance_with_account_number(cls, account_number, pin):
        account = [val for val in Values.accounts if val['account_number'] == account_number]
        if len(account) < 1:
            return {
                'code': Code.NotFound.code,
                'message': 'wrong account number',
            }
        account = account[0]

        account_pin = account.get('pin', None)
        if not account_pin:
            return {
                'code': Code.InternalError.code,
                'message': 'invalid account',
            }

        if account_pin != pin:
            return {
                'code': Code.Unauthorized.code,
                'message': 'wrong pin'
            }

        return {
            'code': Code.Success.code,
            'message': Code.Success.message,
            'data': account.get('balance', 0)
        }

    @classmethod
    def __get_account_with_account_number(cls, account_number):
        account = [val for val in Values.accounts if val['account_number'] == account_number]
        if len(account) < 1:
            raise ValueError('wrong account number')
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

    @classmethod
    def deposit(cls, account_number, amount):
        if amount <= 0:
            return {
                'code': Code.NegativeAmount.code,
                'message': 'deposit amount has to be bigger than zero',
            }

        try:
            account = cls.__get_account_with_account_number(account_number)
        except ValueError as e:
            return {
                'code': Code.NotFound.code,
                'message': str(e),
            }

        balance = account.get('balance', None)
        if not balance:
            balance = 0

        new_balance = balance + amount
        account['balance'] = new_balance

        transaction_id = cls.__log_transaction('deposit', account_number, amount)

        return {
            'code': Code.Success.code,
            'message': Code.Success.message,
            'data': {
                'account_number': account.get('account_number', None),
                'balance': account.get('balance', 0),
                'transaction_id': transaction_id,
            }
        }

    @classmethod
    def withdraw(cls, account_number, amount, pin):
        if amount <= 0:
            return {
                'code': Code.NegativeAmount.code,
                'message': 'withdraw amount has to be bigger than zero',
            }

        try:
            account = cls.__get_account_with_account_number(account_number)
        except ValueError as e:
            return {
                'code': Code.NotFound.code,
                'message': str(e),
            }

        account_pin = account.get('pin', None)
        if account_pin is None:
            return {
                'code': Code.InternalError.code,
                'message': 'invalid account',
            }

        if account_pin != pin:
            return {
                'code': Code.Unauthorized.code,
                'message': 'wrong pin'
            }

        balance = account.get('balance', None)
        if not balance:
            balance = 0

        new_balance = balance - amount
        if new_balance < 0:
            return {
                'code': Code.InsufficientBalance.code,
                'message': 'insufficient balance',
            }
        account['balance'] = new_balance

        transaction_id = cls.__log_transaction('withdraw', account_number, -amount)

        return {
            'code': Code.Success.code,
            'message': Code.Success.message,
            'data': {
                'account_number': account.get('account_number', None),
                'balance': account.get('balance', 0),
                'transaction_id': transaction_id,
            }
        }

    @classmethod
    def revert_transaction(cls, transaction_id):
        transaction = [val for val in Values.transactions if val['key'] == transaction_id]
        if len(transaction) <= 0:
            return {
                'code': Code.NotFound.code,
                'message': 'insufficient balance',
            }
        transaction = transaction[0]
        # Todo: revert transaction
        cls.__log_transaction('revert', transaction.get('account_number', None), -transaction.get('amount', 0))
        return True
