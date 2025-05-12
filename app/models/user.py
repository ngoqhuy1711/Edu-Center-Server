from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, JSON
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=50, unique=True)
    email: str = Field(index=True, max_length=100, unique=True)
    password_hash: str = Field(max_length=255)
    role: str = Field(max_length=20)  # student, teacher, staff, admin
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    user_profile_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id", unique=True)
    full_name: str = Field(max_length=100)
    profile_picture: Optional[str] = Field(default=None, max_length=255)
    date_of_birth: Optional[datetime] = None
    phone_number: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=255)
    bio: Optional[str] = Field(default=None, max_length=500)
    gender: Optional[str] = Field(default=None, max_length=10)
    social_links: Optional[dict] = Field(default=None, sa_type=JSON)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now) 