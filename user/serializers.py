from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from user.models import User
from utils.serializers import CustomPaginationSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ["password"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["is_customer"] = hasattr(instance, "customer")

        if hasattr(instance, "customer"):
            ret["customer_id"] = instance.customer.id

        return ret


class LeanUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "image",
        ]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "first_name", "last_name", "image"]

        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["user_claims"] = {"id": str(user.id)}
        return token


class UserPaginationSerializer(CustomPaginationSerializer):
    results = serializers.ListSerializer(child=UserSerializer())
