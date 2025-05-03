from typing import Optional, Type

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.sercurity import verify_password, get_password_hash
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()


def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
) -> list[Type[User]]:
    """
    Get multiple users with optional filtering.
    """
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                User.username.ilike(search_term),
                User.email.ilike(search_term),
                User.full_name.ilike(search_term)
            )
        )

    return query.offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    # Check if username or email already exists
    existing_user = get_user_by_email(db, email=str(user.email))
    if existing_user:
        raise ValueError("Email already registered")

    existing_user = get_user_by_username(db, username=user.username)
    if existing_user:
        raise ValueError("Username already taken")

    # Create new user
    db_user = User(
        username=user.username,
        email=str(user.email),
        password_hash=get_password_hash(user.password),
        full_name=user.full_name,
        role=user.role,
        profile_picture=user.profile_picture,
        date_of_birth=user.date_of_birth,
        phone_number=user.phone_number,
        address=user.address,
        bio=user.bio,
        is_active=user.is_active
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    """Update an existing user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user.model_dump(exclude_unset=True)

    # Handle username update
    if "username" in update_data and update_data["username"] != db_user.username:
        existing_user = get_user_by_username(db, username=update_data["username"])
        if existing_user:
            raise ValueError("Username already taken")

    # Handle email update
    if "email" in update_data and update_data["email"] != db_user.email:
        existing_user = get_user_by_email(db, email=update_data["email"])
        if existing_user:
            raise ValueError("Email already registered")

    # Handle password update
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

    # Update user attributes
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> Optional[User]:
    """Delete a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    db.delete(db_user)
    db.commit()
    return db_user


def authenticate_user(db: Session, username_or_email: str, password: str) -> Optional[User]:
    """Authenticate a user by username/email and password."""
    # Try to find user by email first
    user = get_user_by_email(db, email=username_or_email)

    # If not found, try by username
    if not user:
        user = get_user_by_username(db, username=username_or_email)

    if not user or not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user


def count_users(db: Session, role: Optional[UserRole] = None, is_active: Optional[bool] = None) -> int:
    """Count users with optional filtering."""
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    return query.count()
