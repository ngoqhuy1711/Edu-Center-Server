from datetime import timedelta
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.sercurity import (
    create_access_token,
    create_refresh_token,
    validate_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.crud.user import authenticate_user, get_user
from app.models.user import User, UserRole


# Token models
class TokenPayload(BaseModel):
    refresh_token: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: Dict[str, Any]


router = APIRouter(tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user based on the provided token."""
    try:
        payload = validate_token(token)
        user_id: int = int(payload["sub"])
        user_role: str = payload.get("role")  # Lấy role từ payload
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user.role_from_token = user_role  # Gán role từ token vào user object
    return user


def check_role(allowed_roles: List[UserRole]):
    def _check_role(
            current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.role_from_token not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _check_role


@router.post("/login", response_model=Token)
async def login(
        email: str = Form(...),
        password: str = Form(...),
        remember_me: bool = Form(False),
        db: Session = Depends(get_db),
) -> Any:
    """
    Login endpoint for users with email/username and password.
    Supports "remember me" functionality to extend token validity.
    """
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Set token expiration based on remember_me flag
    access_token_expires = timedelta(
        days=7 if remember_me else 0,
        minutes=0 if remember_me else ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Create tokens
    access_token = create_access_token(
        subject=user.user_id,
        expires_delta=access_token_expires,
        extra_claims={"role": user.role.value if user.role else None}
    )

    return {
        "access_token": access_token,
        "refresh_token": create_refresh_token(subject=user.user_id),
        "token_type": "bearer",
        "user": {
            "id": user.user_id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active
        }
    }


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
        token: TokenPayload,
        db: Session = Depends(get_db)
) -> Any:
    """Use a refresh token to get a new access token."""
    try:
        payload = validate_token(token.refresh_token, token_type="refresh")
        user_id: int = int(payload["sub"])
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user(db, user_id=user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create new access token
    access_token = create_access_token(
        subject=user.user_id,
        extra_claims={"role": user.role.value if user.role else None}
    )

    return {
        "access_token": access_token,
        "refresh_token": token.refresh_token,  # Return the same refresh token
        "token_type": "bearer",
        "user": {
            "id": user.user_id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active
        }
    }


@router.get("/me", response_model=dict)
async def get_me(
        current_user: User = Depends(get_current_user)
) -> Any:
    """Get current authenticated user information."""
    return {
        "id": current_user.user_id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "profile_picture": current_user.profile_picture,
        "date_of_birth": current_user.date_of_birth,
        "phone_number": current_user.phone_number,
        "address": current_user.address,
        "bio": current_user.bio
    }
