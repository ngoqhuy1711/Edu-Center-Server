from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import LessonStatus

class Course(SQLModel, table=True):
    __tablename__ = "courses"
    course_id: Optional[int] = Field(default=None, primary_key=True)
    course_code: str = Field(max_length=20, unique=True, index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    level: Optional[str] = Field(default="beginner", max_length=20)
    teacher_id: int = Field(foreign_key="user.user_id")
    credits: Optional[int] = Field(default=0)
    max_students: Optional[int] = Field(default=30)
    price: Optional[float] = None
    start_date: datetime
    end_date: datetime
    image_url: Optional[str] = Field(default=None, max_length=255)
    syllabus: Optional[str] = None
    prerequisites: Optional[str] = None
    location: Optional[str] = Field(default=None, max_length=100)
    status: Optional[str] = Field(default="upcoming", max_length=20)
    is_published: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")

class CourseMember(SQLModel, table=True):
    course_member_id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.course_id")
    user_id: int = Field(foreign_key="user.user_id")
    role: str = Field(max_length=20)
    is_active: bool = Field(default=True)
    joined_date: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    access_level: Optional[int] = Field(default=1)
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC)) 