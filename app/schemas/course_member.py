from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.course_member import CourseMemberRole


# Base CourseMember schema with common fields
class CourseMemberBase(BaseModel):
    course_id: int
    user_id: int
    role: CourseMemberRole
    is_active: bool = True
    access_level: int = Field(1, ge=1, le=3)


# Schema for creating a new course member
class CourseMemberCreate(CourseMemberBase):
    pass


# Schema for updating an existing course member
class CourseMemberUpdate(BaseModel):
    role: Optional[CourseMemberRole] = None
    is_active: Optional[bool] = None
    access_level: Optional[int] = Field(None, ge=1, le=3)


# Schema for database course member (includes all fields)
class CourseMemberInDB(CourseMemberBase):
    id: int
    joined_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schema for course member response
class CourseMemberResponse(CourseMemberInDB):
    pass
