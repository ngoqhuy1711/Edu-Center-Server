from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.course import CourseStatus, CourseLevel


# Base Course schema with common fields
class CourseBase(BaseModel):
    course_code: str = Field(..., max_length=20)
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    level: CourseLevel = CourseLevel.BEGINNER
    credits: int = 0
    max_students: int = 30
    price: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None
    syllabus: Optional[str] = None
    prerequisites: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    status: CourseStatus = CourseStatus.UPCOMING
    is_published: bool = False


# Schema for creating a new course
class CourseCreate(CourseBase):
    teacher_id: int


# Schema for updating an existing course
class CourseUpdate(BaseModel):
    course_code: Optional[str] = Field(None, max_length=20)
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    level: Optional[CourseLevel] = None
    credits: Optional[int] = None
    max_students: Optional[int] = None
    price: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None
    syllabus: Optional[str] = None
    prerequisites: Optional[str] = None
    location: Optional[str] = Field(None, max_length=100)
    status: Optional[CourseStatus] = None
    is_published: Optional[bool] = None
    teacher_id: Optional[int] = None


# Schema for database course (includes all fields)
class CourseInDB(CourseBase):
    course_id: int
    teacher_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For Pydantic v2+, use orm_mode=True for v1


# Schema for course response
class CourseResponse(CourseInDB):
    pass
