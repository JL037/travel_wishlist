import pytest
from datetime import timedelta
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    create_reset_token,
    verify_reset_token
    )

def test_hash_and_verify_password():
    raw = "secret123"
    hashed = hash_password(raw)

    assert hashed != raw
    assert verify_password("secret123", hashed)
    assert not verify_password("wrongpass", hashed)

def test_create_and_decode_access_token():
    token = create_access_token(user_id=123, expires_delta=timedelta(minutes=5))
    decoded = decode_access_token(token)
    
    assert decoded["sub"] == "123"
    assert "exp" in decoded

def test_expired_token_returns_none():
    token = create_access_token(user_id=1, expires_delta=timedelta(seconds=-1))
    result = decode_access_token(token)

    assert result is None

def test_create_and_verify_reset_token():
    email = "test@example.com"
    token = create_reset_token(email = email, expires_minutes=1)

    result = verify_reset_token(token)
    assert result == email

def test_verify_reset_token_with_invalid_token():
    result = verify_reset_token("this.is.not.valid")
    assert result is None
    