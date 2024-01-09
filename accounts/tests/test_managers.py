from django.test import TestCase

from accounts.models import Account


class AccountManagerTest(TestCase):
    def setUp(self):
        self.account_manager = Account.objects
        self.email = "johndoe@gmail.com"

    def test_create_user(self):
        account = self.account_manager.create_user(
            first_name="John",
            last_name="Doe",
            email=self.email,
            password="12345678",
        )

        self.assertEqual(account.email, self.email)
        self.assertEqual(account.first_name, "John")
        self.assertEqual(account.last_name, "Doe")
        self.assertFalse(account.email_verified)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)
        self.assertTrue(account.is_active)

    def test_create_superuser(self):
        account = self.account_manager.create_superuser(
            first_name="John",
            last_name="Doe",
            email=self.email,
            password="12345678",
        )

        self.assertEqual(account.email, self.email)
        self.assertEqual(account.first_name, "John")
        self.assertEqual(account.last_name, "Doe")
        self.assertTrue(account.email_verified)
        self.assertTrue(account.is_staff)
        self.assertTrue(account.is_superuser)
        self.assertTrue(account.is_active)

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            self.account_manager.create_user(
                first_name="John", last_name="Doe", email=None, password="12345678"
            )

    def test_create_superuser_without_email(self):
        with self.assertRaises(ValueError):
            self.account_manager.create_superuser(
                first_name="John", last_name="Doe", email=None, password="12345678"
            )

    def test_create_user_without_first_name(self):
        with self.assertRaises(ValueError):
            self.account_manager.create_user(
                first_name=None, last_name="Doe", email=self.email, password="12345678"
            )

    def test_create_superuser_without_first_name(self):
        with self.assertRaises(ValueError):
            self.account_manager.create_superuser(
                first_name=None, last_name="Doe", email=self.email, password="12345678"
            )

    def test_create_user_without_last_name(self):
        with self.assertRaises(ValueError):
            self.account_manager.create_user(
                first_name="John", last_name=None, email=self.email, password="12345678"
            )

    def test_create_superuser_without_last_name(self):
        with self.assertRaises(ValueError):
            self.account_manager.create_superuser(
                first_name="John", last_name=None, email=self.email, password="12345678"
            )

    def test_create_user_with_existing_email(self):
        self.account_manager.create_user(
            first_name="John", last_name="Doe", email=self.email, password="12345678"
        )

        with self.assertRaises(ValueError):
            self.account_manager.create_user(
                first_name="John",
                last_name="Doe",
                email=self.email,
                password="12345678",
            )

    def test_create_superuser_with_existing_email(self):
        self.account_manager.create_superuser(
            first_name="John", last_name="Doe", email=self.email, password="12345678"
        )

        with self.assertRaises(ValueError):
            self.account_manager.create_superuser(
                first_name="John",
                last_name="Doe",
                email=self.email,
                password="12345678",
            )
