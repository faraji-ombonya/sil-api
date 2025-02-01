from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def mail_admins(subject: str, message: str) -> bool:
    """Send an email to all admins.

    Args:
        subject (str): The subject of the email.
        message (str): The message of the email.

    Returns:
        bool: Whether the email was sent successfully.
    """
    admins = get_user_model().objects.filter(is_admin=True)
    emails = [admin.email for admin in admins]
    send_mail(subject, message, settings.EMAIL_HOST_USER, emails)
    return True
