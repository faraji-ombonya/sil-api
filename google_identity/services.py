from urllib.parse import urlencode

import cachecontrol
import requests
import google.auth.transport.requests
from django.conf import settings
from google.oauth2 import id_token

from .types import DiscoveryDocumentKeys, TokenResponse, IDTokenPayload


DISCOVERY_DOCUMENT_URL = "https://accounts.google.com/.well-known/openid-configuration"
REDIRECT_URI = f"{settings.HOST}/v1/google-identity/signin-callback/"


class DiscoveryDocument:
    def __init__(self):
        response = requests.get(DISCOVERY_DOCUMENT_URL)
        self.discovery_document = response.json()

    def get(self, key: DiscoveryDocumentKeys):
        """Get the value of a key from the discovery document.

        Args:
            key (DiscoveryDocumentKeys): The key to get from the discovery document.

        Returns:
            The value of the key.

        Raises:
            KeyError: If the key is not found in the discovery document.
        """
        return self.discovery_document[key]


def get_signin_url(state: str, nonce: str) -> str:
    """Get the signin URL for the Google OAuth2.0 server.

    Args:
        state (str): The state to use for the signin URL.

    Returns:
        The signin URL.
    """
    url_params = {
        "response_type": "code",
        "client_id": settings.GOOGLE_CLIENT_ID,
        "scope": "openid email profile",
        "redirect_uri": REDIRECT_URI,
        "state": state,
        "nonce": nonce,
    }
    authorization_endpoint = DiscoveryDocument().get("authorization_endpoint")
    url = f"{authorization_endpoint}?{urlencode(url_params)}"
    return url


def get_tokens(code: str) -> TokenResponse:
    """Get the tokens for the Google OAuth2.0 server.

    Args:
        code (str): The code to use for the tokens.

    Returns:
        The tokens.
    """
    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    token_endpoint = DiscoveryDocument().get("token_endpoint")
    response = requests.post(token_endpoint, data=data)
    return response.json()


def validate_id_token(token: str) -> IDTokenPayload:
    """
    Validates a Google ID token.

    Args:
        token (str): The Google ID token to validate.

    Returns:
        IDTokenPayload: The decoded token payload if valid, None otherwise.
    """
    session = requests.session()
    cached_session = cachecontrol.CacheControl(session)
    request = google.auth.transport.requests.Request(session=cached_session)
    return id_token.verify_oauth2_token(token, request, settings.GOOGLE_CLIENT_ID)
