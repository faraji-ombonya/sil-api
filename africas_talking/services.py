"""This module contains the services for the Africa's Talking service."""

import logging

from . import apis
from .models import AfricasTalkingSMS
from .types import SMSDeliveryReport


logger = logging.getLogger(__name__)


def send_sms(message: str, phone_numbers: list[str]) -> bool:
    """Send an SMS to a list of phone numbers.

    Args:
        message (str): The message to send.
        phone_numbers (list[str]): The list of phone numbers to send
            the message to.

    Returns:
        bool: Whether the SMS was sent successfully.
    """

    try:
        response = apis.send_sms(message, phone_numbers)
    except Exception as e:
        logger.error("Failed to send SMS", exc_info=True)
        return False

    recipients = response.get("SMSMessageData", {}).get("Recipients", [])
    for recipient in recipients:
        AfricasTalkingSMS.objects.create(
            message=message,
            phone_number=recipient.get("number"),
            message_id=recipient.get("messageId"),
            cost=recipient.get("cost"),
            status=recipient.get("status"),
            status_code=recipient.get("statusCode"),
            response_message=response.get("SMSMessageData", {}).get("Message", ""),
        )
    return True


def handle_sms_delivery_report(data: SMSDeliveryReport) -> bool:
    """Handle the SMS delivery report."""
    try:
        at_sms = AfricasTalkingSMS.objects.get(message_id=data["id"])
        at_sms.status = data["status"]
        at_sms.failure_reason = data["failureReason"]
        at_sms.retry_count = data["retryCount"]
        at_sms.save()
    except AfricasTalkingSMS.DoesNotExist:
        logger.error("SMS instance not found")
        return False
    return True
