from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from . import apis
from . import services
from . import tasks
from .models import AfricasTalkingSMS


class SMSDeliveryReportTestCase(APITestCase):
    def setUp(self):
        self.endpoint = reverse("sms_delivery_report_callback")

    def test_sms_delivery_report_callback(self):
        africas_talking_sms = AfricasTalkingSMS.objects.create(
            message_id="1234567890",
            message="Hello, world!",
            phone_number="+254712345678",
            status="delivered",
            network_code="254",
        )

        # Verify that the sms instance is created
        self.assertEqual(str(africas_talking_sms), "SMS to +254712345678")

        delivery_report = {
            "id": africas_talking_sms.message_id,
            "status": "delivered",
            "phoneNumber": africas_talking_sms.phone_number,
            "networkCode": africas_talking_sms.network_code,
            "failureReason": "none",
            "retryCount": 0,
        }
        response = self.client.post(self.endpoint, data=delivery_report)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sms_delivery_report_callback_without_sms_instance(self):
        delivery_report = {
            "id": "1234567890",
            "status": "delivered",
            "phoneNumber": "+254712345678",
            "networkCode": "254",
            "failureReason": "none",
            "retryCount": 0,
        }
        response = self.client.post(self.endpoint, data=delivery_report)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@patch("africas_talking.services.send_sms")
class SendSMSTaskTestCase(APITestCase):
    def test_send_sms(self, mock_send_sms):
        mock_send_sms.return_value = True
        tasks.send_sms(
            message="Hello, world!",
            phone_numbers=["+254712345678"],
        )


@patch("africas_talking.apis.send_sms")
class SendSMSServiceTestCase(APITestCase):
    def test_send_sms(self, mock_send_sms):
        mock_send_sms.return_value = {
            "SMSMessageData": {
                "Recipients": [
                    {
                        "status": "success",
                        "messageId": "1234567890",
                        "cost": 10,
                        "number": "+254712345678",
                    }
                ]
            }
        }

        services.send_sms(
            message="Hello, world!",
            phone_numbers=["+254712345678"],
        )

        # Verify that an sms instance was created
        self.assertEqual(AfricasTalkingSMS.objects.count(), 1)
        africas_talking_sms = AfricasTalkingSMS.objects.first()
        self.assertEqual(africas_talking_sms.message, "Hello, world!")
        self.assertEqual(africas_talking_sms.phone_number, "+254712345678")
        self.assertEqual(africas_talking_sms.message_id, "1234567890")
        self.assertEqual(africas_talking_sms.cost, "10")


@patch("africas_talking.apis.sms")
class SendSMSAPITestCase(APITestCase):
    def test_send_sms(self, mock_sms):
        mock_sms.send.return_value = {
            "SMSMessageData": {
                "Recipients": [
                    {
                        "status": "success",
                        "messageId": "1234567890",
                        "cost": 10,
                    }
                ]
            }
        }
        apis.send_sms(message="Hello, world!", phone_numbers=["+254712345678"])
