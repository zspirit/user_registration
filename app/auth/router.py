from fastapi import APIRouter, status
from app.auth.dependencies import AuthServiceDep
from app.auth.model import OTPResponse, LoginForm, RefreshTokenRequest, RegisterForm, TokenResponse, VerifyForm

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=OTPResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Register a new user account. An activation code will be sent to the provided email for verification.",
)
async def register(
    register_data: RegisterForm, auth_service: AuthServiceDep
) -> OTPResponse:
    """Register a new user account."""
    return auth_service.register(register_data)


@router.post(
    "/verify",
    response_model=TokenResponse,
    summary="Verify registration with OTP",
    description="Verify user registration using the OTP sent to email.",
)
async def verify(
    verify_data: VerifyForm, auth_service: AuthServiceDep
) -> TokenResponse:
    """Verify user registration with OTP."""
    return auth_service.verify_registration(verify_data.email, verify_data.activation_code)

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login",
    description="Authenticate user and return access and refresh tokens.",
)
async def login(login_data: LoginForm, auth_service: AuthServiceDep) -> TokenResponse:
    """Authenticate user and return tokens."""
    return auth_service.login(login_data)

@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Refresh access token using refresh token.",
)
async def refresh_token(
    request: RefreshTokenRequest, auth_service: AuthServiceDep
) -> TokenResponse:
    """Refresh access token."""
    return auth_service.refresh_token(request.refresh_token)
