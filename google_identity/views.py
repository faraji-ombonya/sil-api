import hashlib
import os

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import AuthState
from .services import get_signin_url, get_tokens, validate_id_token
from shop.models import Customer


class ServerFlowSignIn(APIView):
    def get(self, request, format=None):
        # Create a state token and a nonce to prevent request forgery
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        nonce = hashlib.sha256(os.urandom(1024)).hexdigest()
        AuthState.objects.create(state=state, nonce=nonce)

        url = get_signin_url(state, nonce)
        return render(request, "login.html", {"URL": url})


class ServerFlowCallback(APIView):
    def get(self, request, format=None):
        # Validate the state to prevent request forgery
        state = request.GET.get("state")

        try:
            auth_state = AuthState.objects.get(state=state)
        except AuthState.DoesNotExist:
            return Response(
                {"error": "Invalid state."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Exchange code for access token and ID token
            code = request.GET.get("code")
            tokens = get_tokens(code)
            id_token = tokens.get("id_token")
            id_token_payload = validate_id_token(id_token)

            # Validate the nonce
            nonce = id_token_payload.get("nonce")
            if not nonce:
                return Response(
                    {"error": "No nonce in the ID token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if auth_state.nonce != nonce:
                return Response(
                    {"error": "Invalid nonce."}, status=status.HTTP_400_BAD_REQUEST
                )

            auth_state.delete()

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Check if the user exists in the database
            User = get_user_model()
            print("id_token_payload::::::", id_token_payload)
            user = User.objects.get(sub=id_token_payload.get("sub"))
        except User.DoesNotExist:
            # Create a user if they don't exist
            user = User.objects.create_user(
                email=id_token_payload.get("email"),
                sub=id_token_payload.get("sub"),
                first_name=id_token_payload.get("given_name"),
                last_name=id_token_payload.get("family_name"),
                image=id_token_payload.get("picture"),
            )

            # Create a customer profile for the user
            Customer.objects.create(user=user)

        # Generate a token for the user
        refresh = RefreshToken.for_user(user)
        token_data = {"access": str(refresh.access_token), "refresh": str(refresh)}
        return Response(token_data, status=status.HTTP_200_OK)
