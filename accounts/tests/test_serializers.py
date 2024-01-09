from django.test import TestCase
from rest_framework.serializers import ValidationError

from accounts.serializers import RegisterAccountSerializer, ChangePasswordSerializer


class RegisterAccountSerializerTest(TestCase):
    def setUp(self):
        self.serializer = RegisterAccountSerializer()
        self.data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@gmail.com",
            "password": "NewPassword@2022",
            "password2": "NewPassword@2022",
        }

    def test_validate_password(self):
        serializer = RegisterAccountSerializer(data=self.data)
        serializer.is_valid()
        self.assertTrue("password" in serializer.validated_data)
        self.assertTrue("password2" in serializer.validated_data)

    def test_validate_password2(self):
        data = self.data.copy()
        data["password2"] = "NewPassword@2021"
        serializer = RegisterAccountSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength(self):
        data = self.data.copy()
        data["password"] = "password"
        data["password2"] = "password"
        serializer = RegisterAccountSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength2(self):
        data = self.data.copy()
        data["password"] = "john1234"
        data["password2"] = "john1234"
        serializer = RegisterAccountSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength3(self):
        data = self.data.copy()
        data["password"] = "JOHN1234"
        data["password2"] = "JOHN1234"
        serializer = RegisterAccountSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength4(self):
        data = self.data.copy()
        data["password"] = "johnDoe"
        data["password2"] = "johnDoe"
        serializer = RegisterAccountSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_create(self):
        serializer = RegisterAccountSerializer(data=self.data)
        serializer.is_valid()
        account = serializer.save()
        self.assertTrue(account.email, self.data["email"])
        self.assertTrue(account.check_password(self.data["password"]))
        self.assertFalse(account.email_verified)
        self.assertTrue(account.is_active)
        self.assertFalse(account.is_staff)
        self.assertFalse(account.is_superuser)


class ChangePasswordSerializerTest(TestCase):
    def setUp(self):
        self.serializer = ChangePasswordSerializer()
        self.data = {
            "old_password": "OldPassword@2021",
            "new_password": "NewPassword@2022",
            "new_password2": "NewPassword@2022",
        }

    def test_validate(self):
        serializer = ChangePasswordSerializer(data=self.data)
        serializer.is_valid()
        self.assertTrue("old_password" in serializer.validated_data)
        self.assertTrue("new_password" in serializer.validated_data)
        self.assertTrue("new_password2" in serializer.validated_data)

    def test_same_password(self):
        data = self.data.copy()
        data["new_password"] = "OldPassword@2021"
        data["new_password2"] = "OldPassword@2021"
        serializer = ChangePasswordSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_passwords_dont_match(self):
        data = self.data.copy()
        data["new_password"] = "NewPassword@2023"
        data["new_password2"] = "NewPassword@2022"
        serializer = ChangePasswordSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength(self):
        data = self.data.copy()
        data["new_password"] = "password"
        data["new_password2"] = "password"
        serializer = ChangePasswordSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength2(self):
        data = self.data.copy()
        data["new_password"] = "john1234"
        data["new_password2"] = "john1234"
        serializer = ChangePasswordSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength3(self):
        data = self.data.copy()
        data["new_password"] = "JOHN1234"
        data["new_password2"] = "JOHN1234"
        serializer = ChangePasswordSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength4(self):
        data = self.data.copy()
        data["new_password"] = "johnDoe"
        data["new_password2"] = "johnDoe"
        serializer = ChangePasswordSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_validate_password_strength5(self):
        data = self.data.copy()
        data["new_password"] = "JohnDoe"
        data["new_password2"] = "JohnDoe"
        serializer = ChangePasswordSerializer(data=data)

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
