from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone
from typing import Optional, ClassVar

class OTP(BaseModel):
    table_name: ClassVar[str] = "activations"
    
    id: Optional[int] = None
    user_id: str
    email: EmailStr
    purpose: str
    code: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    @property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now(timezone.utc)

class OTPResponse(BaseModel):
    activation_code: int

class RegisterForm(BaseModel):
    email: EmailStr
    firstname: str = Field(min_length=2, max_length=128)
    lastname: str = Field(min_length=2, max_length=128)
    password: str = Field(min_length=8, max_length=128)   
    
class LoginForm(BaseModel):
    email: EmailStr
    password: str

class VerifyForm(BaseModel):
    email: str
    activation_code: int
    
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str