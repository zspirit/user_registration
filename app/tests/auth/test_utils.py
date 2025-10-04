import pytest
from datetime import timedelta, datetime, timezone
from app.auth.utils import (
    generate_one_time_password,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    send_email_one_time_password
)
from app.config import SECRET_KEY, ALGORITHM

def test_generate_activation_code_length():
    code = generate_one_time_password(4)
    assert 1000 <= code <= 9999  # 4-digit code

def test_generate_activation_code_custom_length():
    code = generate_one_time_password(6)
    assert 100000 <= code <= 999999  # 6-digit code

def test_hash_and_verify_password():
    password = "mypassword123"
    hashed = hash_password(password)
    assert hashed != password  # Should be hashed
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False

def test_create_access_token_and_verify():
    data = {"user_id": 1}
    token = create_access_token(data)
    payload = verify_token(token)
    assert payload["user_id"] == 1
    assert payload["type"] == "access"
    assert "exp" in payload

def test_create_refresh_token_and_verify():
    data = {"user_id": 1}
    token = create_refresh_token(data)
    payload = verify_token(token)
    assert payload["user_id"] == 1
    assert payload["type"] == "refresh"
    assert "exp" in payload

def test_expired_token_returns_none():
    expired_token = create_access_token({"user_id": 1}, expires_delta=timedelta(seconds=-1))
    assert verify_token(expired_token) is None

def test_invalid_token_returns_none():
    assert verify_token("invalid.token.string") is None

def test_send_email_otp(capsys):
    send_email_one_time_password("test@example.com", 1234)
    captured = capsys.readouterr()
    assert "Sending OTP 1234 to test@example.com" in captured.out
