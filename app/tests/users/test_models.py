import pytest
from datetime import datetime, timezone
from pydantic import ValidationError

from app.users.model import User

def test_user_model_initialization():
    # vars
    email = "test@example.com"
    firstname = "test"
    lastname = "demo"
    password_hash = "hashed123"

    # object
    user = User(
        id=1,  # Added id to satisfy required field
        email=email,
        firstname=firstname,
        lastname=lastname,
        password_hash=password_hash,
        is_active=True
    )

    # Assert
    assert user.id == 1
    assert user.email == email
    assert user.firstname == firstname
    assert user.lastname == lastname
    assert user.password_hash == password_hash
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)
    assert user.created_at.tzinfo == timezone.utc
    # ClassVar check (not part of instance dict, but accessible)
    assert User.table_name == "users"


def test_user_model_valid_data():
    user = User(
        id=2,  # Added id
        email="test@example.com",
        firstname="test",
        lastname="demo",
        password_hash="password123"
    )

    assert user.id == 2
    assert user.email == "test@example.com"
    assert user.firstname == "test"
    assert user.lastname == "demo"
    assert user.password_hash == "password123"
    assert user.is_active is False  # default value
    assert isinstance(user.created_at, datetime)
    assert user.created_at.tzinfo == timezone.utc


def test_user_model_invalid_email():
    with pytest.raises(ValidationError):
        User(
            id=3,
            email="not-an-email",
            firstname="test",
            lastname="demo",
            password_hash="password123"
        )


def test_user_model_firstname_too_short():
    with pytest.raises(ValidationError):
        User(
            id=4,
            email="valid@example.com",
            firstname="t",
            lastname="demo",
            password_hash="password123"
        )


def test_user_model_lastname_too_long():
    with pytest.raises(ValidationError):
        User(
            id=5,
            email="valid@example.com",
            firstname="test",
            lastname="demo" * 200,  # too long
            password_hash="password123"
        )
