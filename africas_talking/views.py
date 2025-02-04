from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .services import handle_sms_delivery_report


class SMSDeliveryReportCallback(APIView):
    def post(self, request: Request):
        handle_sms_delivery_report(request.data)
        return Response({"status": "success"}, status=200)
