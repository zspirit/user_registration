from typing import Optional
from app.users.model import User
from app.users.repository import UserRepository


class UsersService:
    def __init__(self):
        self.users_repo = UserRepository()

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users_repo.get_by_id(user_id)

