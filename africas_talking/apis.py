"""This module contains the API integrations for the Africa's Talking service."""

import africastalking

from django.conf import settings

from .types import SendSMSResponse


username = settings.AFRICAS_TALKING_USERNAME
api_key = settings.AFRICAS_TALKING_API_KEY

africastalking.initialize(username, api_key)

sms = africastalking.SMS


def send_sms(message: str, phone_numbers: list[str]) -> SendSMSResponse:
    """Send an SMS to a phone number.

    Args:
        message (str): The message to send.
        phone_number (str): The phone number to send the message to.

    Returns:
        SendSMSResponse: The response from the Africa's Talking API.
    """
    response = sms.send(message, phone_numbers)
    return response
