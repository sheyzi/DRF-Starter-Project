from django.conf import settings
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import Signal

from cfehome.utils import Util


send_verification_mail = Signal()


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    # Send an email to the user
    context = {
        "user": reset_password_token.user,
        "reset_password_url": f"{settings.FRONTEND_URL}/auth/reset-password/{reset_password_token.key}",
    }

    Util.send_email(
        reset_password_token.user.email,
        f"{settings.PROJECT_NAME} Password Reset",
        {
            "html": "email/password_reset/password_reset_email.html",
            "text": "email/password_reset/password_reset_email.txt",
        },
        context,
    )


@receiver(send_verification_mail)
def send_email_verification_signal(sender, instance, user, *args, **kwargs):
    """
    Handles email verification tokens
    When a token is created, an e-mail needs to be sent to the user

    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param email_verification_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """

    token = Util.generate_verification_token(user)

    # Send an email to the user
    context = {
        "current_user": user,
        "email_verification_url": f"{settings.FRONTEND_URL}/auth/verify-email/{token}",
    }

    Util.send_email(
        user.email,
        f"Verify Your {settings.PROJECT_NAME} Account",
        {
            "html": "email/email_verification/email_verification_email.html",
            "text": "email/email_verification/email_verification_email.txt",
        },
        context,
    )
