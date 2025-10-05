import pytest
from unittest.mock import MagicMock, ANY
from datetime import datetime, timezone
from app.users.repository import UserRepository
from app.users.model import User
from app.repository import db

# ---------------------------
# Helper to create fake user
# ---------------------------
def fake_user_dict(
    user_id=1,
    email="test@example.com",
    firstname="John",
    lastname="Doe",
    password_hash="hashed_pw",
    created_at=None,
    updated_at=None
):
    now = datetime.now(timezone.utc)
    return {
        "id": user_id,
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
        "password_hash": password_hash,
        "created_at": created_at or now,
        "updated_at": updated_at or now,
    }

# ---------------------------
# Fixture to mock db methods
# ---------------------------
@pytest.fixture
def mock_db_fetchAll(monkeypatch):
    """Patch Database.fetchAll to return controlled results"""
    mock_fetchAll = MagicMock()
    monkeypatch.setattr(db, "fetchAll", mock_fetchAll)
    return mock_fetchAll

@pytest.fixture
def mock_db_fetchOne(monkeypatch):
    """Patch Database.fetchOne to return controlled results"""
    mock_fetchOne = MagicMock()
    monkeypatch.setattr(db, "fetchOne", mock_fetchOne)
    return mock_fetchOne

@pytest.fixture
def mock_db_execute(monkeypatch):
    """Patch Database.execute for updates/deletes"""
    mock_execute = MagicMock()
    monkeypatch.setattr(db, "execute", mock_execute)
    return mock_execute

# ---------------------------
# Test get_all
# ---------------------------
def test_get_all_returns_results(mock_db_fetchAll):
    repo = UserRepository()
    fake_users = [fake_user_dict(), fake_user_dict(user_id="2", email="b@example.com")]
    mock_db_fetchAll.return_value = fake_users

    results = repo.get_all()
    assert results == fake_users
    mock_db_fetchAll.assert_called_once_with(ANY)

def test_get_all_returns_empty_if_no_results(mock_db_fetchAll):
    repo = UserRepository()
    mock_db_fetchAll.return_value = []

    results = repo.get_all()
    assert results == []
    mock_db_fetchAll.assert_called_once_with(ANY)

# ---------------------------
# Test get_by_email
# ---------------------------
def test_get_by_email_returns_user(mock_db_fetchOne):
    repo = UserRepository()
    user_dict = fake_user_dict()
    mock_db_fetchOne.return_value = user_dict

    result = repo.get_by_email(user_dict["email"])
    assert isinstance(result, User)
    assert result.email == user_dict["email"]
    mock_db_fetchOne.assert_called_once_with(ANY)

def test_get_by_email_returns_none_if_not_found(mock_db_fetchOne):
    repo = UserRepository()
    mock_db_fetchOne.return_value = None

    result = repo.get_by_email("notfound@example.com")
    assert result is None
    mock_db_fetchOne.assert_called_once_with(ANY)

# ---------------------------
# Test update_user
# ---------------------------
def test_update_user_returns_updated_user(mock_db_fetchOne, mock_db_execute, monkeypatch):
    repo = UserRepository()
    user_dict = fake_user_dict()
    user_instance = User(**user_dict)

    monkeypatch.setattr(repo, "get_by_id", lambda x: user_dict)

    updated_dict = user_dict.copy()
    updated_dict["firstname"] = "Jane"
    mock_db_fetchOne.return_value = updated_dict

    result = repo.update_user(user_instance.id, {"firstname": "Jane"})
    assert isinstance(result, User)
    assert result.firstname == "Jane"

def test_update_user_returns_none_if_user_not_found(monkeypatch, mock_db_execute):
    repo = UserRepository()
    monkeypatch.setattr(repo, "get_by_id", lambda x: None)

    result = repo.update_user("1", {"firstname": "Jane"})
    assert result is None
    mock_db_execute.assert_not_called()

def test_update_user_returns_user_if_no_fields_to_update(monkeypatch, mock_db_execute):
    repo = UserRepository()
    user_dict = fake_user_dict()
    user_instance = User(**user_dict)
    monkeypatch.setattr(repo, "get_by_id", lambda x: user_dict)

    result = repo.update_user(user_instance.id, {})
    assert isinstance(result, User)
    assert result.id == user_dict["id"]
    mock_db_execute.assert_not_called()
