from datetime import datetime, timedelta, timezone
from typing import Optional
from app.auth.exceptions import InvalidCredentialsException, InvalidOTPException, InvalidTokenException, OTPExpiredException, UserAlreadyExistsException, UserNotFoundException
from app.auth.model import OTP, OTPResponse, LoginForm, RegisterForm, TokenResponse
from app.auth.repository import OTPRepository
from app.auth.utils import create_access_token, create_refresh_token, generate_one_time_password, hash_password, send_email_one_time_password, verify_password, verify_token
from app.users.model import User
from app.users.repository import UserRepository

class AuthService:
    def __init__(self):
        self.users_repo = UserRepository()
        self.activation_code_repo = OTPRepository()
        
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.users_repo.get_by_id(user_id)

    def register(self, register_data: RegisterForm) -> RegisterForm:
        """Register a new user and send OTP for verification."""
        existing_user = self.users_repo.get_by_email(register_data.email)
        if existing_user:
            raise UserAlreadyExistsException()
        
        hashed_password = hash_password(register_data.password)
        
        new_user = User(
            email=register_data.email,
            firstname=register_data.firstname,
            lastname=register_data.lastname,
            password_hash=hashed_password,
            is_active=False,
        )
        
        created_user = self.users_repo.add(new_user) # returns user ID or None
        if not created_user:
            raise UserAlreadyExistsException()
        
        activation_code = generate_one_time_password()
        otp = OTP(
            user_id=str(created_user),  # Placeholder for actual user ID after creation
            code=str(activation_code),
            email=register_data.email,
            purpose="registration",
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),  # Set token expiry to 10 minutes
        )
        
        self.activation_code_repo.add(otp)

        send_email_one_time_password(register_data.email, otp)
        
        return OTPResponse(activation_code=activation_code)
    
    def verify_registration(self, email: str, otp: int) -> TokenResponse:
        """Verify registration OTP and complete user registration."""
        otp_record = self.activation_code_repo.get_by_email_and_purpose(email, "registration")

        if not otp_record:
            raise InvalidOTPException()
        
        expires_at = otp_record['expires_at'].replace(tzinfo=timezone.utc)

        # Check expiration
        if expires_at < datetime.now(timezone.utc):
            raise OTPExpiredException()  # Only for expired OTPs

        # Check code mismatch
        if str(otp_record['code']) != str(otp):
            raise InvalidOTPException()  # Only for wrong OTP

        user = self.users_repo.get_by_id(otp_record['user_id'])
        if not user:
            raise UserNotFoundException()

        self.activation_code_repo.delete_by_email_and_purpose(user['email'], "registration")
        self.users_repo.update_user(user_id=user['id'], update_data={"is_active": True,})

        access_token = create_access_token(data={"sub": user['id'], "email": user['email']})
        refresh_token = create_refresh_token(data={"sub": user['id'], "email": user['email']})

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    def login(self, login_data: LoginForm) -> TokenResponse:
        """Authenticate user and return tokens."""
        user = self.users_repo.get_by_email(login_data.email)

        if not user or not verify_password(login_data.password, user['password_hash']):
            raise InvalidCredentialsException()

        access_token = create_access_token(data={"sub": str(user['id']), "email": user['email']})
        refresh_token = create_refresh_token(data={"sub": str(user['id']), "email": user['email']})

        return TokenResponse(access_token=access_token, refresh_token=refresh_token)
    
    def refresh_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""

        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise InvalidTokenException()

        user_id_str = payload.get("sub")
        email = payload.get("email")

        if not user_id_str or not email:
            raise InvalidTokenException()

        user = self.get_user_by_id(user_id_str)
        if not user:
            raise InvalidTokenException()

        access_token = create_access_token(data={"sub": str(user['id']), "email": user['email']})
        new_refresh_token = create_refresh_token(data={"sub": str(user['id']), "email": user['email']})

        return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)