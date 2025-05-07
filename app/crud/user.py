from typing import Optional, Sequence

from passlib.context import CryptContext
from sqlmodel import select, Session

from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int) -> Optional[User]:
    stmt = select(User).where(User.user_id == user_id)
    return db.scalars(stmt).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    return db.scalars(stmt).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Sequence[User]:
    stmt = select(User).where(User.is_deleted == False).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_user(db: Session, user: User, created_by: int) -> User:
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        created_by=created_by,
        updated_by=created_by,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user: User, updated_by: int) -> User:
    data = user.model_dump(exclude_defaults=True)
    for field, value in data.items():
        setattr(db_user, field, value)
    db_user.updated_by = updated_by
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User, deleted_by: int) -> User:
    db_user.is_deleted = True
    db_user.updated_by = deleted_by
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
