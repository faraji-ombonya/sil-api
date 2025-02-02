from typing import Literal, TypedDict


DiscoveryDocumentKeys = Literal[
    "issuer",
    "authorization_endpoint",
    "device_authorization_endpoint",
    "token_endpoint",
    "userinfo_endpoint",
    "revocation_endpoint",
    "jwks_uri",
    "response_types_supported",
    "subject_types_supported",
    "id_token_signing_alg_values_supported",
    "scopes_supported",
    "token_endpoint_auth_methods_supported",
    "claims_supported",
    "code_challenge_methods_supported",
    "grant_types_supported  ",
]


class TokenResponse(TypedDict):
    access_token: str
    expires_in: int
    id_token: str
    scope: str
    token_type: str
    refresh_token: str

class IDTokenPayload(TypedDict):
    iss: str
    azp: str
    aud: str
    sub: str
    email: str
    email_verified: bool
    at_hash: str
    nonce: str
    name: str
    picture: str
    given_name: str
    family_name: str
    iat: int
    exp: int
