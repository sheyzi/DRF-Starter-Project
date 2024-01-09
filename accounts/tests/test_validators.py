from django.test import TestCase
from django.core.exceptions import ValidationError

from accounts.validators import StrongPasswordValidator


class StrongPasswordValidatorTest(TestCase):
    def setUp(self):
        self.validator = StrongPasswordValidator()

    def test_validate_password(self):
        self.validator.validate("NewPassword@2022")

    def test_validate_password_length(self):
        with self.assertRaises(ValidationError):
            self.validator.validate("NewPass")

    def test_validate_password_no_digit(self):
        with self.assertRaises(ValidationError):
            self.validator.validate("NewPassword")

    def test_validate_password_no_letter(self):
        with self.assertRaises(ValidationError):
            self.validator.validate("12345678")

    def test_validate_password_no_upper(self):
        with self.assertRaises(ValidationError):
            self.validator.validate("newpassword@2022")

    def test_validate_password_no_lower(self):
        with self.assertRaises(ValidationError):
            self.validator.validate("NEWPASSWORD@2022")

    def test_get_help_text(self):
        self.assertTrue(self.validator.get_help_text())
