import os

from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import get_template

from core.services.jwt_service import JWTService, ActionToken

UserModel = get_user_model()


class EmailService:
    @staticmethod
    def _send_email(to: str, template_name: str, context: dict, subject: str) -> None:
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(
            to=[to],
            from_email=os.environ.get('EMAIL_HOST_USER'),
            subject=subject
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @staticmethod
    def register(cls, user):
        token = JWTService.create_token(user, ActionToken)
        url = f'http://localhost/activate/{token}'
        cls._send_email.delay(
            to=user.email,
            template_name='register.html',
            context={'name': user.profile.first_name, 'url': url},
            subject='Register'
        )
