import unittest

from bank import BankAccount, InsufficientFundsError


class TestBankAccount(unittest.TestCase):
    def test_init_with_default_balance(self):
        account = BankAccount("Alice")

        self.assertEqual(account.owner, "Alice")
        self.assertEqual(account.balance, 0)
        self.assertEqual(account.get_balance(), 0)

   

    def test_init_with_negative_balance_raises_value_error(self):
        with self.assertRaisesRegex(
            ValueError, "Initial balance cannot be negative"
        ):
            BankAccount("Alice", -1)

    def test_deposit_positive_amount(self):
        account = BankAccount("Alice", 100)

        result = account.deposit(50)

        self.assertEqual(result, 150)
        self.assertEqual(account.get_balance(), 150)

    def test_deposit_zero_raises_value_error(self):
        account = BankAccount("Alice", 100)

        with self.assertRaisesRegex(ValueError, "Deposit must be positive"):
            account.deposit(0)

        self.assertEqual(account.get_balance(), 100)

    def test_deposit_negative_amount_raises_value_error(self):
        account = BankAccount("Alice", 100)

        with self.assertRaisesRegex(ValueError, "Deposit must be positive"):
            account.deposit(-10)

        self.assertEqual(account.get_balance(), 100)

    def test_withdraw_positive_amount_less_than_balance(self):
        account = BankAccount("Alice", 100)

        result = account.withdraw(40)

        self.assertEqual(result, 60)
        self.assertEqual(account.get_balance(), 60)

    def test_withdraw_amount_equal_to_balance(self):
        account = BankAccount("Alice", 100)

        result = account.withdraw(100)

        self.assertEqual(result, 0)
        self.assertEqual(account.get_balance(), 0)

    def test_withdraw_zero_raises_value_error(self):
        account = BankAccount("Alice", 100)

        with self.assertRaisesRegex(ValueError, "Withdrawal must be positive"):
            account.withdraw(0)

        self.assertEqual(account.get_balance(), 100)


    def test_transfer_positive_amount(self):
        sender = BankAccount("Alice", 100)
        recipient = BankAccount("Bob", 50)

        result = sender.transfer(recipient, 40)

        self.assertIsNone(result)
        self.assertEqual(sender.get_balance(), 60)
        self.assertEqual(recipient.get_balance(), 90)

    def test_transfer_amount_equal_to_sender_balance(self):
        sender = BankAccount("Alice", 100)
        recipient = BankAccount("Bob", 50)

        sender.transfer(recipient, 100)

        self.assertEqual(sender.get_balance(), 0)
        self.assertEqual(recipient.get_balance(), 150)

    def test_transfer_zero_raises_value_error(self):
        sender = BankAccount("Alice", 100)
        recipient = BankAccount("Bob", 50)

        with self.assertRaisesRegex(ValueError, "Withdrawal must be positive"):
            sender.transfer(recipient, 0)

        self.assertEqual(sender.get_balance(), 100)
        self.assertEqual(recipient.get_balance(), 50)

    def test_transfer_negative_amount_raises_value_error(self):
        sender = BankAccount("Alice", 100)
        recipient = BankAccount("Bob", 50)

        with self.assertRaisesRegex(ValueError, "Withdrawal must be positive"):
            sender.transfer(recipient, -10)

        self.assertEqual(sender.get_balance(), 100)
        self.assertEqual(recipient.get_balance(), 50)

    def test_transfer_amount_greater_than_sender_balance_raises_error(self):
        sender = BankAccount("Alice", 100)
        recipient = BankAccount("Bob", 50)

        with self.assertRaisesRegex(
            InsufficientFundsError, "Not enough balance"
        ):
            sender.transfer(recipient, 101)

        self.assertEqual(sender.get_balance(), 100)
        self.assertEqual(recipient.get_balance(), 50)


if __name__ == "__main__":
    unittest.main()
