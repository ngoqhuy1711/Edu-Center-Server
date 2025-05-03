from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    STAFF = "staff"


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., max_length=100)
    role: UserRole
    profile_picture: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    bio: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    role: Optional[UserRole] = None
    profile_picture: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    password_hash: str

    class Config:
        orm_mode = True

