from typing import Annotated

from fastapi import Depends, HTTPException, status, Request
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.exceptions import InvalidTokenException
from app.auth.service import AuthService
from app.auth.utils import verify_token
from app.users.model import User

security = HTTPBearer()

def get_auth_service() -> AuthService:
    """Get auth service instance with dependencies."""
    return AuthService()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service),
) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise InvalidTokenException()

    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidTokenException()

    user = auth_service.get_user_by_id(user_id)
    if user is None:
        raise InvalidTokenException()

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user (additional validation can be added here)."""
    return current_user

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
CurrentActiveUser = Annotated[User, Depends(get_current_active_user)]
