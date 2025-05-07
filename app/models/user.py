from datetime import datetime, UTC
from typing import Optional, Dict

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, func, PrimaryKeyConstraint, Relationship

from app.models.role import Role


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, nullable=False)
    email: str = Field(max_length=100, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )

    profiles: list["UserProfile"] = Relationship(back_populates="user",
                                                 sa_relationship_kwargs={"foreign_keys": "[UserProfile.user_id]"})
    roles: list["UserRole"] = Relationship(back_populates="user",
                                           sa_relationship_kwargs={"foreign_keys": "[UserRole.user_id]"})

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, username={self.username}, email={self.email})"


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"
    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    role_id: int = Field(foreign_key="roles.role_id", primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "role_id"),
    )

    user: "User" = Relationship(back_populates="roles",
                                sa_relationship_kwargs={"foreign_keys": "[UserRole.user_id]"})
    role: "Role" = Relationship(back_populates="users",
                                sa_relationship_kwargs={"foreign_keys": "[UserRole.role_id]"})

    def __repr__(self) -> str:
        return f"UserRole(user_id={self.user_id}, role_id={self.role_id})"


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    user_profile_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    full_name: str = Field(max_length=100, nullable=False)
    profile_picture: str = Field(max_length=255, nullable=True)
    date_of_birth: datetime = Field(nullable=True)
    phone_number: str = Field(max_length=20, nullable=True)
    address: str = Field(max_length=255, nullable=True)
    bio: str = Field(max_length=500, nullable=True)
    gender: str = Field(max_length=10, nullable=True)
    social_links: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )

    user: "User" = Relationship(back_populates="profiles",
                                sa_relationship_kwargs={"foreign_keys": "[UserProfile.user_id]"})

    def __repr__(self) -> str:
        return f"UserProfile(user_id={self.user_id}, full_name={self.full_name})"
