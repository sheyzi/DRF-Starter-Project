from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class StrongPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("Password must be at least 8 characters long."),
                code="password_too_short",
            )

        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Password must contain at least 1 digit."),
                code="password_no_digit",
            )

        if not any(char.isalpha() for char in password):
            raise ValidationError(
                _("Password must contain at least 1 letter."),
                code="password_no_letter",
            )

        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Password must contain at least 1 uppercase letter."),
                code="password_no_upper",
            )

        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Password must contain at least 1 lowercase letter."),
                code="password_no_lower",
            )

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long and contain at least 1 digit and 1 letter."
        )
