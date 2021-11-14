import unittest
from bank_api import BankApi
from constants import Code
from main import Account
from cash_bin import CashBin


class BankApiTest(unittest.TestCase):

    def test_get_account_with_card_number_and_pin(self):
        # test with correct card number
        correct_card_number = '111111'
        correct_pin = '1111'
        result = BankApi.get_account_with_card_number_and_pin(correct_card_number, correct_pin)
        self.assertEqual(result.get('code', None), Code.Success.code)

        # test with wrong card number
        wrong_card_number = '121212'
        result = BankApi.get_account_with_card_number_and_pin(wrong_card_number, correct_pin)
        self.assertEqual(result.get('code', None), Code.NotFound.code)

        # test with wrong pin
        wrong_pin = '8383'
        result = BankApi.get_account_with_card_number_and_pin(correct_card_number, wrong_pin)
        self.assertEqual(result.get('code', None), Code.Unauthorized.code)

    def test_get_balance_with_account_number(self):
        # test with correct account number
        correct_account_number = '123456789'
        correct_pin = '1111'
        result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        self.assertEqual(result.get('code', None), Code.Success.code)

        # test with wrong account number
        wrong_account_number = '111111'
        result = BankApi.get_balance_with_account_number(wrong_account_number, correct_pin)
        self.assertEqual(result.get('code', None), Code.NotFound.code)

        # test with wrong pin
        wrong_account_number = '111111'
        wrong_pin = '1897'
        result = BankApi.get_balance_with_account_number(correct_account_number, wrong_pin)
        self.assertEqual(result.get('code', None), Code.Unauthorized.code)

    def test_deposit(self):
        # test with correct account number and amount
        correct_account_number = '123456789'
        correct_pin = '1111'
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        prev_balance = balance_result.get('data', 0)
        amount = 10000
        result = BankApi.deposit(correct_account_number, amount)
        self.assertEqual(result.get('code', None), Code.Success.code)
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        next_balance = balance_result.get('data', 0)
        self.assertEqual(next_balance, prev_balance + amount)

        # test with wrong account number
        wrong_account_number = '111111'
        result = BankApi.deposit(wrong_account_number, amount)
        self.assertEqual(result.get('code', None), Code.NotFound.code)

        # test with negative amount
        amount = -10000
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        prev_balance = balance_result.get('data', 0)
        result = BankApi.deposit(correct_account_number, amount)
        self.assertEqual(result.get('code', None), Code.NegativeAmount.code)
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        next_balance = balance_result.get('data', 0)
        self.assertEqual(next_balance, prev_balance)

    def test_withdraw(self):
        # test with correct account number and amount
        correct_account_number = '123456789'
        correct_pin = '1111'
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        prev_balance = balance_result.get('data', 0)
        amount = 10000
        result = BankApi.withdraw(correct_account_number, amount, correct_pin)
        self.assertEqual(result.get('code', None), Code.Success.code)
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        next_balance = balance_result.get('data', 0)
        self.assertEqual(next_balance, prev_balance - amount)

        # test with wrong account number
        wrong_account_number = '111111'
        result = BankApi.withdraw(wrong_account_number, amount, correct_pin)
        self.assertEqual(result.get('code', None), Code.NotFound.code)

        # test with negative amount
        negative_amount = -10000
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        prev_balance = balance_result.get('data', 0)
        result = BankApi.withdraw(correct_account_number, negative_amount, correct_pin)
        self.assertEqual(result.get('code', None), Code.NegativeAmount.code)
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        next_balance = balance_result.get('data', 0)
        self.assertEqual(next_balance, prev_balance)

        # test with wrong pin
        wrong_pin = '9838'
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        prev_balance = balance_result.get('data', 0)
        result = BankApi.withdraw(correct_account_number, amount, wrong_pin)
        self.assertEqual(result.get('code', None), Code.Unauthorized.code)
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        next_balance = balance_result.get('data', 0)
        self.assertEqual(next_balance, prev_balance)

        # test with insufficient balance
        insufficient_account_number = '98769876'
        insufficient_account_pin = '4444'
        balance_result = BankApi.get_balance_with_account_number(insufficient_account_number, insufficient_account_pin)
        prev_balance = balance_result.get('data', 0)
        result = BankApi.withdraw(insufficient_account_number, amount, insufficient_account_pin)
        self.assertEqual(result.get('code', None), Code.InsufficientBalance.code)
        balance_result = BankApi.get_balance_with_account_number(insufficient_account_number, insufficient_account_pin)
        next_balance = balance_result.get('data', 0)
        self.assertEqual(next_balance, prev_balance)


class AtmTest(unittest.TestCase):

    def test_deposit(self):
        # test with correct card number
        correct_card_number = '111111'
        correct_pin = '1111'
        account = Account()
        account.read_card(correct_card_number, correct_pin)
        correct_account_number = account.get_account_number()
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        prev_balance = balance_result.get('data', 0)
        prev_reserve = CashBin.get_reserve()
        amount = 10000
        account.deposit(amount)
        balance_result = BankApi.get_balance_with_account_number(correct_account_number, correct_pin)
        next_balance = balance_result.get('data', 0)
        self.assertEqual(next_balance, prev_balance + amount)
        next_reserve = CashBin.get_reserve()
        self.assertEqual(next_reserve, prev_reserve + amount)


