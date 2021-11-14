from bank_api import BankApi
from error_handler import ErrorHandler
from constants import Code
from cash_bin import CashBin


class Account:
    __account = {}

    def read_card(self, card_number, pin):
        try:
            result = BankApi.get_account_with_card_number_and_pin(card_number, pin)
            result_code = result.get('code', None)
            if result_code == Code.NotFound.code:
                ErrorHandler.inform_to_user('등록되지 않은 카드입니다.')
                return
            if result_code == Code.Unauthorized.code:
                ErrorHandler.inform_to_user('잘못된 비밀번호입니다.')
                return
            if result_code != Code.Success.code:
                raise Exception(f'bank api error: {result}')

            self.__account = result.get('data', {})
        except Exception as e:
            ErrorHandler.inform_to_user('카드 정보를 읽는 중 오류가 발생했습니다. 관리자에게 문의해주세요.')
            ErrorHandler.raise_error(e)

    def deposit(self, amount):
        try:
            account_number = self.get_account_number()
            if amount <= 0:
                ErrorHandler.inform_to_user('$0 이상을 입금해주세요.')
                return

            result = BankApi.deposit(account_number, amount)
            result_code = result.get('code', None)
            if result_code == Code.NotFound.code:
                ErrorHandler.inform_to_user('유효하지 않은 계좌입니다.')
                return
            if result_code != Code.Success.code:
                raise Exception(f'bank api error: {result}')

            CashBin.insert(amount)
        except Exception as e:
            transaction_id = result.get('transaction_id', None)
            if transaction_id:
                BankApi.revert_transaction(transaction_id)
            CashBin.give_back_bill()

            ErrorHandler.inform_to_user('입금 과정에서 오류가 발생했습니다. 관리자에게 문의해주세요.')
            ErrorHandler.raise_error(e)

    def withdraw(self, amount, pin):
        try:
            account_number = self.get_account_number()
            if amount <= 0:
                ErrorHandler.inform_to_user('$0 이상을 출금해주세요.')
                return

            account_balance = self.__get_account_balance()
            if account_balance < amount:
                ErrorHandler.inform_to_user('잔액이 부족합니다.')
                return

            result = BankApi.withdraw(account_number, amount, pin)
            result_code = result.get('code', None)
            if result_code == Code.NotFound.code:
                ErrorHandler.inform_to_user('유효하지 않은 계좌입니다.')
                return
            if result_code == Code.Unauthorized.code:
                ErrorHandler.inform_to_user('잘못된 비밀번호입니다.')
                return
            if result_code == Code.InsufficientBalance.code:
                ErrorHandler.inform_to_user('잔액이 부족합니다.')
                return
            if result_code != Code.Success.code:
                raise Exception(f'bank api error: {result}')

            CashBin.extract(amount)
        except Exception as e:
            transaction_id = result.get('transaction_id', None)
            if transaction_id:
                BankApi.revert_transaction(transaction_id)

            ErrorHandler.inform_to_user('출금 과정에서 오류가 발생했습니다. 관리자에게 문의해주세요.')
            ErrorHandler.raise_error(e)

    def get_account_number(self):
        account_number = self.__account.get('account_number', None)
        if account_number is None:
            ErrorHandler.raise_error(ValueError(f'no account information. account: {self.account}'))

        return account_number

    def __get_account_balance(self):
        account_balance = self.__account.get('account_number', None)
        if account_balance is None:
            ErrorHandler.raise_error(ValueError(f'no account information. account: {self.account}'))

        return account_balance
