from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str
    is_active: Optional[bool] = True

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_deleted: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    user_id: int
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    roles: List[str] = []
    profile: Optional[dict] = None
    lesson_progress: List[dict] = []

    model_config = ConfigDict(from_attributes=True)
