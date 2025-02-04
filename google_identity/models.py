import uuid

from django.db import models


class AuthState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    state = models.CharField(max_length=255)
    nonce = models.CharField(max_length=255)
