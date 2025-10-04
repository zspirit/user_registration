from datetime import datetime, timedelta, timezone
import random
from typing import Optional
from passlib.hash import pbkdf2_sha256
from jose import ExpiredSignatureError, JWTError, jwt

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, REFRESH_TOKEN_EXPIRE_DAYS, SECRET_KEY

def generate_one_time_password(length: int = 4) -> int:
    """Generate a random OTP code."""
    return random.randrange(10 ** (length - 1), 10 ** length)

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pbkdf2_sha256.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT refresh token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=float(REFRESH_TOKEN_EXPIRE_DAYS))
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(str(token), SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return None
    except JWTError as e:
        return None
    
def send_email_one_time_password(email: str, otp: int):
    """Send OTP via email. This is a placeholder - implement with your email service."""
    # TODO: Implement actual email sending logic
    print(f"Sending OTP {otp} to {email}")
    # In production, use services like SendGrid, AWS SES, or SMTP
    pass