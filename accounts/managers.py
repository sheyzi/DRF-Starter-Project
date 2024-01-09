from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if not email:
            raise ValueError("Users must have an email address")

        if not first_name:
            raise ValueError("Users must have a first name")

        if not last_name:
            raise ValueError("Users must have a last name")

        user_exists = self.model.objects.filter(email=email).exists()

        if user_exists:
            raise ValueError("User with given email already exists")

        email = self.normalize_email(email)
        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self, first_name, last_name, email, password=None, **extra_fields
    ):
        user = self.create_user(
            first_name, last_name, email, password=password, **extra_fields
        )

        user.is_staff = True
        user.is_superuser = True
        user.email_verified = True

        user.save()

        return user
