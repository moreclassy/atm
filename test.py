import unittest
from bank_service import BankService
from atm_service import ATMService
from exception import BankServiceException, ATMServiceException
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
        BankService.get_balance_with_account_number(correct_account_number)

        # test with wrong account number
        wrong_account_number = '111111'
        with self.assertRaises(BankServiceException.NotFound):
            BankService.get_balance_with_account_number(wrong_account_number)

    def test_deposit(self):
        # test with correct account number and amount
        correct_account_number = '123456789'
        correct_pin = '1111'
        
        prev_balance = BankService.get_balance_with_account_number(correct_account_number)
        
        amount = 10000
        BankService.deposit(correct_account_number, amount)
        
        next_balance = BankService.get_balance_with_account_number(correct_account_number)
        self.assertEqual(next_balance, prev_balance + amount)

        # test with wrong account number
        wrong_account_number = '111111'
        with self.assertRaises(BankServiceException.NotFound):
            BankService.deposit(wrong_account_number, amount)

        # test with negative amount
        prev_balance = BankService.get_balance_with_account_number(correct_account_number)

        amount = -10000
        with self.assertRaises(BankServiceException.WrongInput):
            BankService.deposit(correct_account_number, amount)
        
        next_balance = BankService.get_balance_with_account_number(correct_account_number)
        self.assertEqual(next_balance, prev_balance)

    def test_withdraw(self):
        # test with correct account number and amount
        correct_account_number = '123456789'
        correct_pin = '1111'
        prev_balance = BankService.get_balance_with_account_number(correct_account_number)

        amount = 10000
        BankService.withdraw(correct_account_number, amount, correct_pin)

        next_balance = BankService.get_balance_with_account_number(correct_account_number)
        self.assertEqual(next_balance, prev_balance - amount)

        # test with wrong account number
        wrong_account_number = '111111'
        with self.assertRaises(BankServiceException.NotFound):
            BankService.withdraw(wrong_account_number, amount, correct_pin)

        # test with negative amount
        prev_balance = BankService.get_balance_with_account_number(correct_account_number)

        negative_amount = -10000
        with self.assertRaises(BankServiceException.WrongInput):
            BankService.withdraw(correct_account_number, negative_amount, correct_pin)

        next_balance = BankService.get_balance_with_account_number(correct_account_number)
        self.assertEqual(next_balance, prev_balance)

        # test with wrong pin
        prev_balance = BankService.get_balance_with_account_number(correct_account_number)

        wrong_pin = '9838'
        with self.assertRaises(BankServiceException.Unauthorized):
            BankService.withdraw(correct_account_number, amount, wrong_pin)

        next_balance = BankService.get_balance_with_account_number(correct_account_number)
        self.assertEqual(next_balance, prev_balance)

        # test with insufficient balance
        insufficient_account_number = '98769876'
        insufficient_account_pin = '4444'
        prev_balance = BankService.get_balance_with_account_number(insufficient_account_number)

        with self.assertRaises(BankServiceException.InsufficientBalance):
            BankService.withdraw(insufficient_account_number, amount, insufficient_account_pin)

        next_balance = BankService.get_balance_with_account_number(insufficient_account_number)
        self.assertEqual(next_balance, prev_balance)


class ATMServiceTest(unittest.TestCase):

    def test_read_card(self):
        # test with correct card number
        correct_card_number = '111111'
        correct_pin = '1111'
        ATMService(correct_card_number, correct_pin)

        # test with wrong card number
        wrong_card_number = '121212'
        with self.assertRaises(BankServiceException.NotFound):
            ATMService(wrong_card_number, correct_pin)

        # test with wrong pin
        wrong_pin = '8383'
        with self.assertRaises(BankServiceException.Unauthorized):
            ATMService(correct_card_number, wrong_pin)

    def test_deposit(self):
        correct_card_number = '111111'
        correct_pin = '1111'
        atm = ATMService(correct_card_number, correct_pin)

        # test with correct amount
        prev_balance = atm.get_account_balance()

        amount = 10000
        atm.deposit(amount)

        next_balance = atm.get_account_balance()
        self.assertEqual(next_balance, prev_balance + amount)

        # test with negative amount
        prev_balance = atm.get_account_balance()

        amount = -10000
        with self.assertRaises(ATMServiceException.WrongInput):
            atm.deposit(amount)

        next_balance = atm.get_account_balance()
        self.assertEqual(next_balance, prev_balance)

    def test_withdraw(self):
        correct_card_number = '111111'
        correct_pin = '1111'
        atm = ATMService(correct_card_number, correct_pin)

        # test with correct amount
        prev_balance = atm.get_account_balance()

        amount = 10000
        atm.withdraw(amount, correct_pin)

        next_balance = atm.get_account_balance()
        self.assertEqual(next_balance, prev_balance - amount)

        # test with wrong pin
        prev_balance = atm.get_account_balance()

        wrong_pin = '8372'
        with self.assertRaises(BankServiceException.Unauthorized):
            atm.withdraw(amount, wrong_pin)

        next_balance = atm.get_account_balance()
        self.assertEqual(next_balance, prev_balance)

        # test with negative amount
        prev_balance = atm.get_account_balance()

        negative_amount = -10000
        with self.assertRaises(ATMServiceException.WrongInput):
            atm.withdraw(negative_amount, correct_pin)

        next_balance = atm.get_account_balance()
        self.assertEqual(next_balance, prev_balance)

