import uuid

from django.db import models


class AfricasTalkingSMS(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Response fields
    message_id = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255)
    cost = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    status_code = models.IntegerField(null=True, blank=True)
    response_message = models.TextField(null=True, blank=True)

    # Result fields(callback)
    network_code = models.CharField(max_length=50, null=True, blank=True)
    failure_reason = models.CharField(max_length=50, null=True, blank=True)
    retry_count = models.IntegerField(default=0)

    def __str__(self):
        return f"SMS to {self.phone_number}"
