"""Types for the Africas Talking API."""

from typing import TypedDict, List


class SMSDeliveryReport(TypedDict):
    id: str
    status: str
    phoneNumber: str
    networkCode: str
    failureReason: str
    retryCount: int


class Recipient(TypedDict):
    cost: str
    messageId: str
    number: str
    status: str
    statusCode: int


class SMSMessageData(TypedDict):
    message: str
    recipients: List[Recipient]


class SendSMSResponse(TypedDict):
    SMSMessageData: SMSMessageData
