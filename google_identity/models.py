import uuid

from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class GoogleCredential(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # API Fields.
    token = models.TextField()
    refresh_token = models.TextField(null=True, blank=True)
    token_uri = models.URLField(max_length=100)
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    granted_scopes = models.JSONField()
    expiry = models.DateTimeField()

    # Meta fields.
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="google_credential"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_expired(self):
        return now() > self.expiry
