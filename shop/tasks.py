import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def mail_admin(subject: str, message: str) -> bool:
    """Send an email to the admin.

    Args:
        subject (str): The subject of the email.
        message (str): The message of the email.

    Returns:
        bool: Whether the email was sent successfully.
    """
    admin = get_user_model().objects.filter(is_admin=True).first()
    if not admin:
        logger.warning("No admin found")
        return False
    send_mail(subject, message, settings.EMAIL_HOST_USER, [admin.email])
    return True
