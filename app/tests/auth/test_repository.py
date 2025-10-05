import pytest
from unittest.mock import MagicMock, ANY
from datetime import datetime, timezone, timedelta
from app.auth.repository import OTPRepository

# Helper to create fake OTP dict
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
def mock_db_fetchOne(monkeypatch):
    """Patch Database.fetchOne to return controlled results"""
    from app.repository import db
    mock_fetchOne = MagicMock()
    monkeypatch.setattr(db, "fetchOne", mock_fetchOne)
    return mock_fetchOne

@pytest.fixture
def mock_db_execute(monkeypatch):
    """Patch Database.execute for deletes"""
    from app.repository import db
    mock_execute = MagicMock()
    monkeypatch.setattr(db, "execute", mock_execute)
    return mock_execute

# ---------------------------
# Test get_by_user_and_code
# ---------------------------
def test_get_by_user_and_code_returns_result(mock_db_fetchOne):
    repo = OTPRepository()
    user_id = 1
    code = "123456"
    fake_otp = fake_otp_dict(user_id=user_id, code=code)
    mock_db_fetchOne.return_value = fake_otp

    result = repo.get_by_user_and_code(user_id, code)
    assert result == fake_otp
    mock_db_fetchOne.assert_called_once_with(ANY)

def test_get_by_user_and_code_returns_none_if_no_result(mock_db_fetchOne):
    repo = OTPRepository()
    mock_db_fetchOne.return_value = None

    result = repo.get_by_user_and_code(1, "wrongcode")
    assert result is None
    mock_db_fetchOne.assert_called_once_with(ANY)

# ---------------------------
# Test get_by_email_and_purpose
# ---------------------------
def test_get_by_email_and_purpose_returns_result(mock_db_fetchOne):
    repo = OTPRepository()
    otp_dict = fake_otp_dict(email="test@example.com", purpose="registration")
    mock_db_fetchOne.return_value = otp_dict

    result = repo.get_by_email_and_purpose(otp_dict["email"], otp_dict["purpose"])
    assert result == otp_dict
    mock_db_fetchOne.assert_called_once_with(ANY)

def test_get_by_email_and_purpose_returns_none_if_no_result(mock_db_fetchOne):
    repo = OTPRepository()
    mock_db_fetchOne.return_value = None

    result = repo.get_by_email_and_purpose("noone@example.com", "registration")
    assert result is None
    mock_db_fetchOne.assert_called_once_with(ANY)

# ---------------------------
# Test delete_by_email_and_purpose
# ---------------------------
def test_delete_by_email_and_purpose_calls_execute(mock_db_execute):
    repo = OTPRepository()
    mock_db_execute.return_value = None

    result = repo.delete_by_email_and_purpose("test@example.com", "registration")
    assert result is None
    mock_db_execute.assert_called_once_with(ANY)
