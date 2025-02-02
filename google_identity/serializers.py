from rest_framework import serializers

from .models import GoogleCredential


class GoogleCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleCredential
        fields = "__all__"


class GoogleOauthSignInRequestSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    next_url = serializers.URLField()
