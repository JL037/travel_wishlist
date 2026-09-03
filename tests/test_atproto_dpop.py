import hashlib
import base64

from jose import jwt

from app.utils.atproto_dpop import (
    generate_dpop_keypair,
    public_jwk_from_private_pem,
    generate_dpop_proof,
)
from app.utils.atproto_oauth import generate_pkce_pair


def test_generate_dpop_keypair_returns_p256_jwk():
    private_pem, public_jwk = generate_dpop_keypair()

    assert "BEGIN PRIVATE KEY" in private_pem
    assert public_jwk["kty"] == "EC"
    assert public_jwk["crv"] == "P-256"
    assert "x" in public_jwk and "y" in public_jwk


def test_public_jwk_from_private_pem_matches_generated_jwk():
    private_pem, public_jwk = generate_dpop_keypair()

    rederived = public_jwk_from_private_pem(private_pem)

    assert rederived == public_jwk


def test_generate_dpop_proof_is_a_verifiable_signed_jwt():
    private_pem, public_jwk = generate_dpop_keypair()

    proof = generate_dpop_proof(
        private_pem, public_jwk, "POST", "https://pds.example/oauth/token", nonce="abc123"
    )

    header = jwt.get_unverified_header(proof)
    assert header["typ"] == "dpop+jwt"
    assert header["alg"] == "ES256"
    assert header["jwk"] == public_jwk

    claims = jwt.decode(
        proof, public_jwk, algorithms=["ES256"],
        options={"verify_aud": False, "verify_exp": False},
    )
    assert claims["htm"] == "POST"
    assert claims["htu"] == "https://pds.example/oauth/token"
    assert claims["nonce"] == "abc123"
    assert "jti" in claims and "iat" in claims


def test_generate_dpop_proof_binds_access_token_hash_when_provided():
    private_pem, public_jwk = generate_dpop_keypair()
    access_token = "some-opaque-access-token"

    proof = generate_dpop_proof(private_pem, public_jwk, "GET", "https://pds.example/xrpc/foo", access_token=access_token)

    claims = jwt.decode(
        proof, public_jwk, algorithms=["ES256"],
        options={"verify_aud": False, "verify_exp": False},
    )
    expected_ath = base64.urlsafe_b64encode(
        hashlib.sha256(access_token.encode("ascii")).digest()
    ).rstrip(b"=").decode("ascii")
    assert claims["ath"] == expected_ath


def test_generate_dpop_proof_jti_is_unique_per_call():
    private_pem, public_jwk = generate_dpop_keypair()

    proof1 = generate_dpop_proof(private_pem, public_jwk, "POST", "https://pds.example/x")
    proof2 = generate_dpop_proof(private_pem, public_jwk, "POST", "https://pds.example/x")

    jti1 = jwt.decode(proof1, public_jwk, algorithms=["ES256"], options={"verify_aud": False, "verify_exp": False})["jti"]
    jti2 = jwt.decode(proof2, public_jwk, algorithms=["ES256"], options={"verify_aud": False, "verify_exp": False})["jti"]
    assert jti1 != jti2


def test_generate_pkce_pair_challenge_is_s256_of_verifier():
    verifier, challenge = generate_pkce_pair()

    expected_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ascii")).digest()
    ).rstrip(b"=").decode("ascii")

    assert challenge == expected_challenge
    assert verifier != challenge
    # RFC 7636 requires a 43-128 char verifier from the unreserved character set.
    assert 43 <= len(verifier) <= 128
