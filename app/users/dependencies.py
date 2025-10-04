from typing import Annotated
from fastapi import Depends

from app.users.service import UsersService


def get_users_service() -> UsersService:
    """Get users service instance with dependencies."""
    return UsersService()


# Type aliases for dependency injection
UsersServiceDep = Annotated[UsersService, Depends(get_users_service)]
