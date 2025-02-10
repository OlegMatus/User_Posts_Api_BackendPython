import os

import logging

logger = logging.getLogger(__name__)
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.template.loader import get_template

from core.services.jwt_service import JWTService
from core.services.jwt_service import ActivateToken

UserModel = get_user_model()


class EmailService:
    @staticmethod
    def _send_email(to: str, template_name: str, context: dict, subject: str) -> None:
        try:
            template = get_template(template_name)
            html_content = template.render(context)
            msg = EmailMultiAlternatives(
                to=[to],
                from_email=os.environ.get('EMAIL_HOST_USER'),
                subject=subject
            )
            msg.attach_alternative(html_content, "text/html")
            send_status = msg.send()
            if send_status == 0:
                logger.error(f"Email failed to send to {to}")
            else:
                logger.info(f"Email sent to {to}")
        except Exception as e:
            logger.error(f"Failed to send email to {to}: {str(e)}")
        # try:
        #     template = get_template(template_name)
        #     html_content = template.render(context)
        #     msg = EmailMultiAlternatives(
        #         to=[to],
        #         from_email=os.environ.get('EMAIL_HOST_USER'),
        #         subject=subject
        #     )
        #     msg.attach_alternative(html_content, "text/html")
        #     msg.send()
        #     logger.info(f"Email sent to {to}")
        # except Exception as e:
        #     logger.error(f"Failed to send email to {to}: {str(e)}")

    @classmethod
    def register(cls, user):
        try:
            token = JWTService.create_token(user, ActivateToken)
            url = f'http://localhost/activate/{token}'
            cls._send_email(
                to=user.email,
                template_name='register.html',
                context={'name': user.profile.first_name, 'url': url},
                subject='Register'
            )
        except Exception as e:
            logger.error(f"Error in email registration: {str(e)}")
