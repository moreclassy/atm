import unittest
from bank_service import BankService
from constants import Code
from main import Account
from cash_bin import CashBin
from exception import BankServiceException
from model import Account


class BankServiceTest(unittest.TestCase):

    def test_get_account_with_card_number_and_pin(self):
        # test with correct card number
        correct_card_number = '111111'
        correct_pin = '1111'
        result = BankService.get_account_with_card_number_and_pin(correct_card_number, correct_pin)
        self.assertIsInstance(result, Account)

        # test with wrong card number
        wrong_card_number = '121212'
        with self.assertRaises(BankServiceException.NotFound):
            BankService.get_account_with_card_number_and_pin(wrong_card_number, correct_pin)

        # test with wrong pin
        wrong_pin = '8383'
        with self.assertRaises(BankServiceException.Unauthorized):
            BankService.get_account_with_card_number_and_pin(correct_card_number, wrong_pin)

    def test_get_balance_with_account_number(self):
        # test with correct account number
        correct_account_number = '123456789'
        correct_pin = '1111'
        BankService.get_balance_with_account_number(correct_account_number, correct_pin)

        # test with wrong account number
        wrong_account_number = '111111'
        with self.assertRaises(BankServiceException.NotFound):
            BankService.get_balance_with_account_number(wrong_account_number, correct_pin)

        # test with wrong pin
        wrong_pin = '1897'
        with self.assertRaises(BankServiceException.Unauthorized):
            BankService.get_balance_with_account_number(correct_account_number, wrong_pin)

    def test_deposit(self):
        # test with correct account number and amount
        correct_account_number = '123456789'
        correct_pin = '1111'
        
        prev_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)
        
        amount = 10000
        BankService.deposit(correct_account_number, amount)
        
        next_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)
        self.assertEqual(next_balance, prev_balance + amount)

        # test with wrong account number
        wrong_account_number = '111111'
        with self.assertRaises(BankServiceException.NotFound):
            BankService.deposit(wrong_account_number, amount)

        # test with negative amount
        prev_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)

        amount = -10000
        with self.assertRaises(BankServiceException.WrongInput):
            BankService.deposit(correct_account_number, amount)
        
        next_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)
        self.assertEqual(next_balance, prev_balance)

    def test_withdraw(self):
        # test with correct account number and amount
        correct_account_number = '123456789'
        correct_pin = '1111'
        prev_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)

        amount = 10000
        BankService.withdraw(correct_account_number, amount, correct_pin)

        next_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)
        self.assertEqual(next_balance, prev_balance - amount)

        # test with wrong account number
        wrong_account_number = '111111'
        with self.assertRaises(BankServiceException.NotFound):
            BankService.withdraw(wrong_account_number, amount, correct_pin)

        # test with negative amount
        prev_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)

        negative_amount = -10000
        with self.assertRaises(BankServiceException.WrongInput):
            BankService.withdraw(correct_account_number, negative_amount, correct_pin)

        next_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)
        self.assertEqual(next_balance, prev_balance)

        # test with wrong pin
        prev_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)

        wrong_pin = '9838'
        with self.assertRaises(BankServiceException.Unauthorized):
            BankService.withdraw(correct_account_number, amount, wrong_pin)

        next_balance = BankService.get_balance_with_account_number(correct_account_number, correct_pin)
        self.assertEqual(next_balance, prev_balance)

        # test with insufficient balance
        insufficient_account_number = '98769876'
        insufficient_account_pin = '4444'
        prev_balance = BankService.get_balance_with_account_number(insufficient_account_number, insufficient_account_pin)

        with self.assertRaises(BankServiceException.InsufficientBalance):
            BankService.withdraw(insufficient_account_number, amount, insufficient_account_pin)

        next_balance = BankService.get_balance_with_account_number(insufficient_account_number, insufficient_account_pin)
        self.assertEqual(next_balance, prev_balance)

