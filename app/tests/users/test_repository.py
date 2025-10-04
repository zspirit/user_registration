# app/tests/users/test_repository.py
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone, timedelta
from app.users.repository import UserRepository
from app.users.model import User
from app.repository import db

# ---------------------------
# Helper to create fake user
# ---------------------------
def fake_user_dict(
    user_id="1",
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
# Fixture to mock db.execute
# ---------------------------
@pytest.fixture
def mock_db(monkeypatch):
    """Patch Database.execute to return controlled results"""
    mock_execute = MagicMock()
    monkeypatch.setattr(db, "execute", mock_execute)
    return mock_execute

# ---------------------------
# Test get_all
# ---------------------------
def test_get_all_returns_results(mock_db):
    repo = UserRepository()
    fake_users = [fake_user_dict(), fake_user_dict(user_id="2", email="b@example.com")]
    mock_db.return_value = fake_users

    results = repo.get_all()
    assert results == fake_users
    mock_db.assert_called_once_with(f"""
        SELECT * FROM {repo.table_name}
        """, fetch=True)

def test_get_all_returns_none_if_empty(mock_db):
    repo = UserRepository()
    mock_db.return_value = []

    results = repo.get_all()
    assert results is None

# ---------------------------
# Test get_by_email
# ---------------------------
def test_get_by_email_returns_user(mock_db):
    repo = UserRepository()
    user_dict = fake_user_dict()
    mock_db.return_value = [user_dict]

    result = repo.get_by_email(user_dict["email"])
    assert result["email"] == user_dict["email"]
    mock_db.assert_called_once_with(f"""
        SELECT * FROM {repo.table_name}
        WHERE email=%s
        """, (user_dict["email"],), fetch=True)

def test_get_by_email_returns_none_if_not_found(mock_db):
    repo = UserRepository()
    mock_db.return_value = []

    result = repo.get_by_email("notfound@example.com")
    assert result is None

# ---------------------------
# Test update_user
# ---------------------------
def test_update_user_returns_updated_user(mock_db, monkeypatch):
    repo = UserRepository()
    user_dict = fake_user_dict()
    user_instance = User(**user_dict)

    # Patch get_by_id to return the user instance
    monkeypatch.setattr(repo, "get_by_id", lambda x: user_instance)

    # Prepare update return value
    updated_dict = user_dict.copy()
    updated_dict["firstname"] = "Jane"
    mock_db.return_value = [updated_dict]

    result = repo.update_user(user_instance.id, {"firstname": "Jane"})
    assert isinstance(result, User)
    assert result.firstname == "Jane"
    # Ensure execute called
    mock_db.assert_called_once()
    args, kwargs = mock_db.call_args
    assert "UPDATE" in args[0]

def test_update_user_returns_none_if_user_not_found(mock_db, monkeypatch):
    repo = UserRepository()
    # Patch get_by_id to return None
    monkeypatch.setattr(repo, "get_by_id", lambda x: None)

    result = repo.update_user("1", {"firstname": "Jane"})
    assert result is None

def test_update_user_returns_user_if_no_fields_to_update(mock_db, monkeypatch):
    repo = UserRepository()
    user_dict = fake_user_dict()
    user_instance = User(**user_dict)
    monkeypatch.setattr(repo, "get_by_id", lambda x: user_instance)

    result = repo.update_user(user_instance.id, {})
    assert isinstance(result, User)
    assert result == user_instance
    # No execute should happen
    mock_db.assert_not_called()
