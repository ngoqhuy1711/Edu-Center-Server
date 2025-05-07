from datetime import datetime, timedelta, UTC

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session

from app.core.database import get_db
from app.crud.user import get_user_by_email

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Remove passlib context


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    # Handle hashed_password that might be stored as string in the DB
    hashed_bytes = hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    password_bytes = plain_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def get_password_hash(password: str) -> str:
    """Hashes a password using bcrypt."""
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    # Ensure user.password_hash is already a string.
    # If it's stored as bytes, you might need user.password_hash.decode('utf-8')
    # or ensure it's stored as a string in the database.
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    rememberMe: bool = False


@router.post("/login", response_model=dict)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # Get user by email
    user = get_user_by_email(db, str(request.email))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if password verification succeeds
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Authentication successful, create token
    expires_delta = timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES * (7 * 24 * 60) if request.rememberMe else ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token({"sub": user.username}, expires_delta=expires_delta)
    return {"access_token": access_token, "token_type": "bearer"}
