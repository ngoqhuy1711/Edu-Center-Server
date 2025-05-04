from datetime import datetime, timedelta, UTC
from os import getenv
from typing import Any, Dict, Optional, Union

from dotenv import load_dotenv
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from pydantic import ValidationError

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
load_dotenv()
SECRET_KEY = getenv("JWT_SECRET_KEY", "ME_MAY_BEO_VCC")
if not SECRET_KEY:
    import secrets

    # Fallback for development only - not for production
    SECRET_KEY = secrets.token_hex(32)
    print("WARNING: Using a randomly generated JWT secret key")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate a password hash."""
    return pwd_context.hash(password)


def create_access_token(
        subject: Union[str, Any], expires_delta: Optional[timedelta] = None,
        extra_claims: Optional[Dict[str, Any]] = None
) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.now(tz=UTC) + expires_delta
    else:
        expire = datetime.now(tz=UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "iat": datetime.now(tz=UTC)}

    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any]) -> str:
    """Create a JWT refresh token with longer expiration."""
    datetime.now(tz=UTC) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return create_access_token(
        subject=subject,
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        extra_claims={"token_type": "refresh"}
    )


def decode_access_token(token: str, verify_exp: bool = True) -> Dict[str, Any]:
    """Decode a JWT access token."""
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": verify_exp}
        )
        return payload
    except (JWTError, ValidationError):
        raise ValueError("Invalid token")


def validate_token(token: str, token_type: str = "access") -> Dict[str, Any]:
    """Validate a token is authentic and of the correct type."""
    payload = decode_access_token(token)

    # Check token type if specified in payload
    if "token_type" in payload and payload["token_type"] != token_type:
        raise ValueError(f"Invalid token type. Expected {token_type}")

    return payload
