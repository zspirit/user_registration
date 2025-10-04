import pytest
from datetime import datetime, timezone, timedelta
from pydantic import ValidationError, EmailStr

from app.auth.model import OTP


def test_otp_model_initialization():
    # vars
    user_id = "1"
    email = "otp@example.com"
    purpose = "account_activation"
    code = "1234"
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    # Act
    otp = OTP(
        id=1,
        user_id=user_id,
        email=email,
        purpose=purpose,
        code=code,
        expires_at=expires_at
    )

    # Assert fields
    assert otp.user_id == user_id
    assert otp.email == email
    assert otp.purpose == purpose
    assert otp.code == code
    assert otp.expires_at == expires_at

    # Assert types
    assert isinstance(otp.user_id, str)
    assert isinstance(otp.email, str)
    assert isinstance(otp.purpose, str)
    assert isinstance(otp.code, str)
    assert isinstance(otp.expires_at, datetime)
    assert isinstance(otp.created_at, datetime)

    # Assert datetime properties
    assert otp.expires_at.tzinfo == timezone.utc
    assert otp.created_at.tzinfo == timezone.utc
    assert otp.created_at <= datetime.now(timezone.utc)  # created_at is in the past

    # ClassVar check
    assert OTP.table_name == "activations"


def test_otp_model_invalid_email():
    # Invalid email should raise ValidationError
    with pytest.raises(ValidationError):
        OTP(
            id=1,
            user_id="123",
            email="invalid-email",
            purpose="test",
            code="123456",
            expires_at=datetime.now(timezone.utc)
        )


def test_otp_model_code_is_string():
    # Code must be a string
    with pytest.raises(ValidationError):
        OTP(
            id=1,
            user_id="123",
            email="valid@example.com",
            purpose="test",
            code=123456,  # invalid type
            expires_at=datetime.now(timezone.utc)
        )


def test_otp_model_expiration_in_future():
    # expires_at in the past
    past_time = datetime.now(timezone.utc) - timedelta(hours=1)
    otp = OTP(
        id=1,
        user_id="123",
        email="valid@example.com",
        purpose="test",
        code="123456",
        expires_at=past_time
    )

    # Assert that OTP is expired
    assert otp.is_expired is True


def test_otp_model_not_expired():
    # expires_at in the future
    future_time = datetime.now(timezone.utc) + timedelta(hours=1)
    otp = OTP(
        id=1,
        user_id="123",
        email="valid@example.com",
        purpose="test",
        code="123456",
        expires_at=future_time
    )

    # Assert that OTP is not expired
    assert otp.is_expired is False