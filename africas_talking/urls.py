from django.urls import path

from . import views


urlpatterns = [
    path(
        "callback/sms-delivery-report/",
        views.SMSDeliveryReportCallback.as_view(),
        name="sms_delivery_report_callback",
    ),
]
