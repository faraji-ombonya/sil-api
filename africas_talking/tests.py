from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import AfricasTalkingSMS
from .services import send_sms


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
