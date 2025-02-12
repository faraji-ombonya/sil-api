"""Tasks for the Africa's Talking Service."""

from celery import shared_task

from . import services


@shared_task
def send_sms(message: str, phone_numbers: list[str]) -> bool:
    """Send an SMS to a list of phone numbers asynchronously.

    A wrapper around the `send_sms` function from the
    `africas_talking.services` module.

    Args:
        message (str): The message to send.
        phone_numbers (list[str]): The list of phone numbers to send
            the message to.

    Returns:
        bool: Whether the SMS was sent successfully.
    """
    return services.send_sms(message, phone_numbers)
