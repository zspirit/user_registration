import pytest
from unittest.mock import MagicMock, ANY
from datetime import datetime, timezone, timedelta
from app.auth.repository import OTPRepository
from app.auth.model import OTP

def fake_otp_dict(user_id=1, email="test@example.com", purpose="activation", code="1234"):
    now = datetime.now(timezone.utc)
    return {
        "user_id": user_id,
        "email": email,
        "purpose": purpose,
        "code": code,
        "expires_at": now + timedelta(hours=1),
        "created_at": now,
    }

@pytest.fixture
def mock_db(monkeypatch):
    """Patch Database.execute to return controlled results"""
    from app.repository import db
    mock_execute = MagicMock()
    monkeypatch.setattr(db, "execute", mock_execute)
    return mock_execute

def test_get_by_user_and_code_returns_result(mock_db):
    repo = OTPRepository()
    user_id = 1
    code = "123456"
    fake_otp = fake_otp_dict(user_id=user_id, code=code)

    mock_db.return_value = [fake_otp]

    result = repo.get_by_user_and_code(user_id, code)
    assert result == fake_otp
    mock_db.assert_called_once()
    args, kwargs = mock_db.call_args
    assert args[1] == (user_id, code)
    assert kwargs.get("fetch") is True

def test_get_by_user_and_code_returns_none_if_no_result(mock_db):
    repo = OTPRepository()
    mock_db.return_value = []

    result = repo.get_by_user_and_code(1, "wrongcode")
    assert result is None
    mock_db.assert_called_once()
    args, kwargs = mock_db.call_args
    assert args[1] == (1, "wrongcode")
    assert kwargs.get("fetch") is True

def test_get_by_email_and_purpose_returns_result(mock_db):
    repo = OTPRepository()
    otp_dict = fake_otp_dict(email="test@example.com", purpose="registration")
    mock_db.return_value = [otp_dict]

    result = repo.get_by_email_and_purpose(otp_dict["email"], otp_dict["purpose"])
    assert result == otp_dict
    mock_db.assert_called_once()
    args, kwargs = mock_db.call_args
    assert args[1] == (otp_dict["email"], otp_dict["purpose"])
    assert kwargs.get("fetch") is True

def test_get_by_email_and_purpose_returns_none_if_no_result(mock_db):
    repo = OTPRepository()
    mock_db.return_value = []

    result = repo.get_by_email_and_purpose("noone@example.com", "registration")
    assert result is None
    mock_db.assert_called_once()
    args, kwargs = mock_db.call_args
    assert args[1] == ("noone@example.com", "registration")
    assert kwargs.get("fetch") is True

def test_delete_by_email_and_purpose_calls_execute(mock_db):
    repo = OTPRepository()
    mock_db.return_value = None

    result = repo.delete_by_email_and_purpose("test@example.com", "registration")
    assert result is None
    mock_db.assert_called_once()
    args, kwargs = mock_db.call_args
    assert args[1] == ("test@example.com", "registration")
