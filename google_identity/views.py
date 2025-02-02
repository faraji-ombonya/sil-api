import hashlib
import os

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_signin_url, get_tokens, validate_id_token


class ServerFlowSignIn(APIView):
    def get(self, request, format=None):
        # Create a state token to prevent request forgery.
        # Store it in the session for later validation.
        state = hashlib.sha256(os.urandom(1024)).hexdigest()
        request.session["state"] = state

        url = get_signin_url(state)
        return render(request, "login.html", {"URL": url})


class ServerFlowCallback(APIView):
    def get(self, request, format=None):
        # TODO: Validate the state to prevent request forgery

        # Exchange code for access token and ID token
        code = request.GET.get("code")

        try:
            tokens = get_tokens(code)
            id_token = tokens.get("id_token")
            id_token_payload = validate_id_token(id_token)
        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the user exists in the database
        User = get_user_model()
        user = User.objects.filter(email=id_token_payload.get("email")).first()
        
        # If not, create the user
        if not user:
            user = User.objects.create_user(
                email=id_token_payload.get("email"),
                first_name=id_token_payload.get("given_name"),
                last_name=id_token_payload.get("family_name"),
                image=id_token_payload.get("picture"),
            )

        # Generate a token for the user
        refresh = RefreshToken.for_user(user)
        token_data = {"access": str(refresh.access_token), "refresh": str(refresh)}
        return Response(token_data, status=status.HTTP_200_OK)
