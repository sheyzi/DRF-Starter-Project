from rest_framework.test import APITestCase
from django.urls import reverse

from accounts.models import Account

user_data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@gmail.com",
    "password": "NewPassword@2022",
}


class AuthenticationViewsTest(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(**user_data)

        self.login_details = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

    def get_tokens(self):
        url = reverse("accounts:login")
        response = self.client.post(url, self.login_details)
        return response.data["access"], response.data["refresh"]

    def authenticate(self):
        access_token, _ = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_register(self):
        Account.objects.all().delete()
        url = reverse("accounts:register")
        data = user_data.copy()
        data["password2"] = data["password"]
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("id" in response.data)
        self.assertTrue("first_name" in response.data)
        self.assertTrue("last_name" in response.data)
        self.assertTrue("email" in response.data)
        self.assertTrue("email_verified" in response.data)
        self.assertTrue("is_staff" in response.data)
        self.assertTrue("is_active" in response.data)
        self.assertTrue("is_superuser" in response.data)
        self.assertFalse("password" in response.data)
        self.assertFalse("password2" in response.data)

        self.assertFalse(response.data["email_verified"])
        self.assertTrue(response.data["is_active"])
        self.assertFalse(response.data["is_staff"])
        self.assertFalse(response.data["is_superuser"])

    def test_register_with_different_passwords(self):
        Account.objects.all().delete()
        url = reverse("accounts:register")
        data = user_data.copy()
        data["password2"] = "invalidpassword"
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertTrue("password" in response.data)
        self.assertEqual(
            response.data["password"][0],
            "The two password fields didn’t match.",
        )

    def test_login(self):
        url = reverse("accounts:login")
        response = self.client.post(url, self.login_details)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_refresh(self):
        _, refresh_token = self.get_tokens()
        refresh_url = reverse("accounts:refresh")
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(refresh_url, refresh_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_verify_token(self):
        access_token, _ = self.get_tokens()
        verify_url = reverse("accounts:verify_token")
        verify_data = {"token": access_token}
        response = self.client.post(verify_url, verify_data)
        self.assertEqual(response.status_code, 200)

    def test_user_exists(self):
        url = reverse("accounts:admin_exists")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("exists" in response.data)
        self.assertTrue(response.data["exists"])

    def test_user_does_not_exist(self):
        Account.objects.all().delete()
        url = reverse("accounts:admin_exists")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("exists" in response.data)
        self.assertFalse(response.data["exists"])

    def test_admin_setup(self):
        Account.objects.all().delete()
        url = reverse("accounts:setup_admin")
        data = user_data.copy()
        data["password2"] = data["password"]
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("id" in response.data)
        self.assertTrue("first_name" in response.data)
        self.assertTrue("last_name" in response.data)
        self.assertTrue("email" in response.data)
        self.assertTrue("email_verified" in response.data)
        self.assertTrue("is_staff" in response.data)

        self.assertTrue(response.data["email_verified"])
        self.assertTrue(response.data["is_active"])
        self.assertTrue(response.data["is_staff"])
        self.assertTrue(response.data["is_superuser"])

    def test_admin_setup_when_admin_exists(self):
        user = Account.objects.first()
        user.is_staff = True
        user.is_superuser = True
        user.save()
        url = reverse("accounts:setup_admin")
        data = user_data.copy()
        data["email"] = "maryjane@gmail.com"
        data["password2"] = data["password"]
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("message" in response.data)
        self.assertEqual(response.data["message"], "Admin already exists")

    def test_admin_setup_with_different_passwords(self):
        Account.objects.all().delete()
        url = reverse("accounts:setup_admin")
        data = user_data.copy()
        data["password2"] = "invalidpassword"
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertTrue("password" in response.data)
        self.assertEqual(
            response.data["password"][0],
            "The two password fields didn’t match.",
        )

    def test_me_not_authenticated(self):
        url = reverse("accounts:me")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.assertTrue("detail" in response.data)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )

    def test_me_authenticated(self):
        self.authenticate()
        url = reverse("accounts:me")
        response = self.client.get(url)

        # Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Make sure that the response data does not contain the password fields
        self.assertFalse("password" in response.data)
        self.assertFalse("password2" in response.data)

        # Check if the response data matches the user data
        self.assertEqual(response.data["id"], self.user.id)
        self.assertEqual(response.data["first_name"], self.user.first_name)
        self.assertEqual(response.data["last_name"], self.user.last_name)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["email_verified"], self.user.email_verified)
        self.assertEqual(response.data["is_staff"], self.user.is_staff)
        self.assertEqual(response.data["is_active"], self.user.is_active)
        self.assertEqual(response.data["is_superuser"], self.user.is_superuser)

    def test_partial_update_me(self):
        self.authenticate()
        url = reverse("accounts:me")
        data = {"first_name": "Jane"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], data["first_name"])

    def test_full_update_me(self):
        self.authenticate()
        url = reverse("accounts:me")
        data = {
            "first_name": "Jane",
            "last_name": "Doe",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["first_name"], data["first_name"])
        self.assertEqual(response.data["last_name"], data["last_name"])

    def test_change_password(self):
        self.authenticate()
        url = reverse("accounts:change_password")
        data = {
            "old_password": user_data["password"],
            "new_password": "NewPassword@2023",
            "new_password2": "NewPassword@2023",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("message" in response.data)
        self.assertEqual(response.data["message"], "Password changed successfully")

    def test_change_password_with_different_passwords(self):
        self.authenticate()
        url = reverse("accounts:change_password")
        data = {
            "old_password": user_data["password"],
            "new_password": "NewPassword@2023",
            "new_password2": "NewPassword@2024",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("new_password" in response.data)
        self.assertEqual(
            response.data["new_password"][0],
            "The two password fields didn’t match.",
        )

    def test_change_password_with_invalid_old_password(self):
        self.authenticate()
        url = reverse("accounts:change_password")
        data = {
            "old_password": "invalidpassword",
            "new_password": "NewPassword@2023",
            "new_password2": "NewPassword@2023",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("old_password" in response.data)
        self.assertEqual(
            response.data["old_password"][0],
            "Incorrect old password",
        )

    def test_change_password_with_same_passwords(self):
        self.authenticate()
        url = reverse("accounts:change_password")
        data = {
            "old_password": user_data["password"],
            "new_password": user_data["password"],
            "new_password2": user_data["password"],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertTrue("new_password" in response.data)
        self.assertEqual(
            response.data["new_password"][0],
            "New password must be different from old password",
        )
