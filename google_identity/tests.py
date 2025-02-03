import hashlib
import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from unittest.mock import patch

from .models import AuthState


class GoogleIdentityAuthenticationServerFlowTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.auth_state = AuthState.objects.create(
            state=hashlib.sha256(os.urandom(1024)).hexdigest(),
            nonce=hashlib.sha256(os.urandom(1024)).hexdigest(),
        )
        self.call_back_url = "/v1/google-identity/signin-callback/?state={}&code=4%2F0ASVgi3IF-f6iLHWcagSB6dIlEBsrg-lJyts6YPZdLMBprzfSJUx5l3QcSXq60B7CrS7PNg&scope=email+profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+openid&authuser=0&prompt=none"

    def test_server_flow_sign_in(self):
        url = reverse("signin_page")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_server_flow_callback_with_invalid_state(self):
        url = self.call_back_url.format("invalid_state")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_server_flow_callback_with_invalid_id_token(self):
        url = self.call_back_url.format(self.auth_state.state)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("google_identity.views.validate_id_token")
    def test_server_flow_callback_without_nonce(self, mock_validate_id_token):
        # Mock the validate_id_token function to return a token without a nonce
        mock_validate_id_token.return_value = {
            "sub": "1234567890",
            "email": "test@example.com",
            "email_verified": True,
        }

        url = self.call_back_url.format(self.auth_state.state)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("google_identity.views.validate_id_token")
    def test_server_flow_callback_with_a_wrong_nonce(self, mock_validate_id_token):
        # Mock the validate_id_token function to return a token without a nonce
        mock_validate_id_token.return_value = {
            "sub": "1234567890",
            "email": "test@example.com",
            "email_verified": True,
            "nonce": "wrong_nonce",
        }
        url = self.call_back_url.format(self.auth_state.state)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("google_identity.views.validate_id_token")
    def test_server_flow_callback_with_valid_id_token(self, mock_validate_id_token):
        # Mock the validate_id_token function to return a token with the correct nonce
        mock_validate_id_token.return_value = {
            "sub": "1234567890",
            "email": "test@example.com",
            "email_verified": True,
            "nonce": self.auth_state.nonce,
        }

        url = self.call_back_url.format(self.auth_state.state)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Confirm that we have refresh and access tokens in the response
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
