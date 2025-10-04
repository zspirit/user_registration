from fastapi import APIRouter

from app.auth.dependencies import CurrentActiveUser
from app.users.dependencies import UsersServiceDep
from app.users.model import User, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Get current authenticated user profile information.",
)
async def get_current_user_profile(
    current_user: CurrentActiveUser, users_service: UsersServiceDep
) -> UserResponse:
    """Get current user profile information."""
    return UserResponse(**current_user)

