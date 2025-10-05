from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import ClassVar, Optional


class User(BaseModel):
    table_name: ClassVar[str] = "users"

    id: Optional[int] = None
    email: EmailStr
    firstname: str = Field(min_length=2, max_length=128)
    lastname: str = Field(min_length=2, max_length=128)
    password_hash: str
    is_active: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserResponse(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    is_active: bool