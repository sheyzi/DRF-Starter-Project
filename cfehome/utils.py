import threading
import jwt
from datetime import datetime, timedelta
from typing import TypedDict
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from accounts.models import BlacklistedToken


class TemplatePaths(TypedDict):
    html: str
    text: str


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(
        email: str, subject: str, template_urls: TemplatePaths, context: dict
    ):

        html_message = render_to_string(template_urls["html"], context)
        plain_text_message = render_to_string(template_urls["text"], context)

        msg = EmailMultiAlternatives(
            subject, plain_text_message, settings.EMAIL_FROM, [email]
        )
        msg.attach_alternative(html_message, "text/html")
        EmailThread(msg).start()

    @staticmethod
    def generate_verification_token(user):
        return jwt.encode(
            {
                "user_id": user.id,
                "email": user.email,
                "scope": "email_verification",
                "exp": datetime.now(tz=timezone.utc)
                + settings.EMAIL_VERIFICATION_EXPIRY,
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    @staticmethod
    def validate_verification_token(key: str):
        blacklisted = BlacklistedToken.objects.filter(token=key).first()

        if blacklisted:
            return None

        try:
            payload = jwt.decode(key, settings.SECRET_KEY, algorithms=["HS256"])
            if payload["scope"] != "email_verification":
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
