from django.test import TestCase

from accounts.models import Account


class AccountModelTest(TestCase):
    def create_account(
        self,
        email="johndoe@gmail.com",
        first_name="John",
        last_name="Doe",
        password="12345678",
    ):
        return Account.objects.create(
            email=email, first_name=first_name, last_name=last_name, password=password
        )

    def test_create_account(self):
        account = self.create_account()
        self.assertTrue(isinstance(account, Account))
        self.assertEqual(account.__str__(), account.email)

    def test_get_full_name(self):
        account = self.create_account()
        self.assertEqual(account.get_full_name(), "John Doe")

    def test_get_short_name(self):
        account = self.create_account()
        self.assertEqual(account.get_short_name(), "John")
