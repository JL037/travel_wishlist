"""AT Protocol OAuth orchestration: PAR, the authorization redirect, and
token exchange/refresh.

There is no mature, officially-maintained Python OAuth client for AT
Protocol at the time this was written (the ecosystem's guidance for Python
is to implement the flow directly against the spec - see
https://atproto.com/guides/oauth-client). This module does that: standard
OAuth 2.1 + PKCE + Pushed Authorization Requests (RFC 9126) + DPoP
(RFC 9449).

NOTE ON VERIFICATION: atproto.com/docs.bsky.app were not reachable from
this environment to double check exact PAR parameter names and scope
values against the live spec. The values below (scope="atproto
transition:generic", token_endpoint_auth_method="none" for a public
client, dpop_bound_access_tokens=true) reflect the spec as understood at
implementation time - re-verify against
https://atproto.com/specs/oauth and a working reference client before
relying on this in production.
"""

import base64
import hashlib
import secrets
import time

import httpx

from app.core.config import settings
from app.utils.atproto_dpop import generate_dpop_proof


class AtprotoOAuthError(Exception):
    pass


def generate_pkce_pair() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(48)).rstrip(b"=").decode("ascii")
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ascii")).digest()
    ).rstrip(b"=").decode("ascii")
    return verifier, challenge


def build_client_metadata() -> dict:
    """The client metadata document we host at settings.ATPROTO_CLIENT_ID.

    Public client (no client secret): identity is the client_id URL itself,
    and requests are authenticated only via PKCE + DPoP, which AT Protocol
    supports for exactly this kind of first-party web app.
    """
    return {
        "client_id": settings.ATPROTO_CLIENT_ID,
        "client_name": "Travel Wishlist",
        "client_uri": settings.ATPROTO_CLIENT_URI,
        "redirect_uris": [settings.ATPROTO_REDIRECT_URI],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "scope": "atproto transition:generic",
        "token_endpoint_auth_method": "none",
        "application_type": "web",
        "dpop_bound_access_tokens": True,
    }


async def _post_with_dpop_retry(
    client: httpx.AsyncClient,
    url: str,
    data: dict,
    dpop_private_key_pem: str,
    dpop_public_jwk: dict,
    nonce: str | None,
) -> tuple[httpx.Response, str | None]:
    """POST a form request with a DPoP proof, retrying once if the server
    demands a fresh nonce (the standard DPoP nonce handshake: the first
    request commonly gets rejected with use_dpop_nonce and a DPoP-Nonce
    response header, and the retry must include that nonce)."""
    proof = generate_dpop_proof(dpop_private_key_pem, dpop_public_jwk, "POST", url, nonce=nonce)
    resp = await client.post(url, data=data, headers={"DPoP": proof})

    new_nonce = resp.headers.get("DPoP-Nonce", nonce)
    if resp.status_code == 400 and new_nonce and new_nonce != nonce:
        try:
            if resp.json().get("error") == "use_dpop_nonce":
                proof = generate_dpop_proof(
                    dpop_private_key_pem, dpop_public_jwk, "POST", url, nonce=new_nonce
                )
                resp = await client.post(url, data=data, headers={"DPoP": proof})
                new_nonce = resp.headers.get("DPoP-Nonce", new_nonce)
        except ValueError:
            pass

    return resp, new_nonce


async def push_authorization_request(
    as_metadata: dict,
    dpop_private_key_pem: str,
    dpop_public_jwk: dict,
    login_hint: str,
    state: str,
    code_challenge: str,
) -> tuple[str, str | None]:
    """Submit a Pushed Authorization Request, returning (request_uri, nonce)."""
    par_endpoint = as_metadata.get("pushed_authorization_request_endpoint")
    if not par_endpoint:
        raise AtprotoOAuthError("Authorization server does not advertise a PAR endpoint")

    data = {
        "client_id": settings.ATPROTO_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": settings.ATPROTO_REDIRECT_URI,
        "scope": "atproto transition:generic",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "login_hint": login_hint,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp, nonce = await _post_with_dpop_retry(
            client, par_endpoint, data, dpop_private_key_pem, dpop_public_jwk, nonce=None
        )
        if resp.status_code not in (200, 201):
            raise AtprotoOAuthError(f"PAR request failed ({resp.status_code}): {resp.text}")
        request_uri = resp.json().get("request_uri")
        if not request_uri:
            raise AtprotoOAuthError("PAR response missing request_uri")
        return request_uri, nonce


def build_authorization_url(as_metadata: dict, request_uri: str) -> str:
    authorize_endpoint = as_metadata.get("authorization_endpoint")
    if not authorize_endpoint:
        raise AtprotoOAuthError("Authorization server does not advertise an authorization_endpoint")
    return (
        f"{authorize_endpoint}?client_id={settings.ATPROTO_CLIENT_ID}"
        f"&request_uri={request_uri}"
    )


async def exchange_code_for_tokens(
    as_metadata: dict,
    code: str,
    code_verifier: str,
    dpop_private_key_pem: str,
    dpop_public_jwk: dict,
    nonce: str | None,
) -> tuple[dict, str | None]:
    """Exchange an authorization code for a DPoP-bound token pair."""
    token_endpoint = as_metadata.get("token_endpoint")
    if not token_endpoint:
        raise AtprotoOAuthError("Authorization server does not advertise a token_endpoint")

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.ATPROTO_REDIRECT_URI,
        "client_id": settings.ATPROTO_CLIENT_ID,
        "code_verifier": code_verifier,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp, new_nonce = await _post_with_dpop_retry(
            client, token_endpoint, data, dpop_private_key_pem, dpop_public_jwk, nonce=nonce
        )
        if resp.status_code != 200:
            raise AtprotoOAuthError(f"Token exchange failed ({resp.status_code}): {resp.text}")
        return resp.json(), new_nonce


async def refresh_tokens(
    as_metadata: dict,
    refresh_token: str,
    dpop_private_key_pem: str,
    dpop_public_jwk: dict,
    nonce: str | None,
) -> tuple[dict, str | None]:
    token_endpoint = as_metadata.get("token_endpoint")
    if not token_endpoint:
        raise AtprotoOAuthError("Authorization server does not advertise a token_endpoint")

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": settings.ATPROTO_CLIENT_ID,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        resp, new_nonce = await _post_with_dpop_retry(
            client, token_endpoint, data, dpop_private_key_pem, dpop_public_jwk, nonce=nonce
        )
        if resp.status_code != 200:
            raise AtprotoOAuthError(f"Token refresh failed ({resp.status_code}): {resp.text}")
        return resp.json(), new_nonce


def token_expiry_from_response(token_response: dict) -> float:
    return time.time() + float(token_response.get("expires_in", 3600))
