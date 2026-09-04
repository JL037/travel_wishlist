"""DPoP (Demonstrating Proof-of-Possession, RFC 9449) helpers.

AT Protocol OAuth requires every token request and every authenticated PDS
call to carry a DPoP proof: a short-lived JWT, signed by a key the client
holds, that binds the request to that specific keypair so a stolen access
token alone isn't enough to use it. This part of the flow is a generic OAuth
extension (not AT-Proto-specific), so it's implemented directly against
RFC 9449 rather than against AT Proto docs.
"""

import base64
import time
import uuid

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from jose import jwt


def _b64url_uint(n: int, length: int) -> str:
    raw = n.to_bytes(length, "big")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def generate_dpop_keypair() -> tuple[str, dict]:
    """Generate a new P-256 keypair for DPoP.

    Returns (private_key_pem, public_jwk) - the PEM is what we persist and
    feed back into jose for signing; the JWK is what gets embedded in the
    proof's header so the server can verify it.
    """
    private_key = ec.generate_private_key(ec.SECP256R1())
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("ascii")

    public_numbers = private_key.public_key().public_numbers()
    jwk = {
        "kty": "EC",
        "crv": "P-256",
        "x": _b64url_uint(public_numbers.x, 32),
        "y": _b64url_uint(public_numbers.y, 32),
    }
    return private_pem, jwk


def public_jwk_from_private_pem(private_key_pem: str) -> dict:
    """Re-derive the public JWK from a persisted private key PEM, so we only
    ever have to store one secret per session/request instead of two."""
    private_key = serialization.load_pem_private_key(private_key_pem.encode("ascii"), password=None)
    public_numbers = private_key.public_key().public_numbers()
    return {
        "kty": "EC",
        "crv": "P-256",
        "x": _b64url_uint(public_numbers.x, 32),
        "y": _b64url_uint(public_numbers.y, 32),
    }


def generate_dpop_proof(
    private_key_pem: str,
    public_jwk: dict,
    http_method: str,
    http_url: str,
    nonce: str | None = None,
    access_token: str | None = None,
) -> str:
    """Build one DPoP proof JWT for a single HTTP request.

    A fresh proof (fresh jti/iat) is required per-request - proofs are not
    reusable across calls.
    """
    claims = {
        "jti": str(uuid.uuid4()),
        "htm": http_method.upper(),
        "htu": http_url,
        "iat": int(time.time()),
    }
    if nonce:
        claims["nonce"] = nonce
    if access_token:
        # `ath` binds the proof to a specific access token (required when the
        # proof accompanies a resource request rather than a token request).
        import hashlib

        digest = hashlib.sha256(access_token.encode("ascii")).digest()
        claims["ath"] = base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")

    headers = {"typ": "dpop+jwt", "jwk": public_jwk}
    return jwt.encode(claims, private_key_pem, algorithm="ES256", headers=headers)
