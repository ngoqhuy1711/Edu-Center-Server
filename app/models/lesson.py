from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import LessonType, LessonStatus

class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"
    lesson_id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    content: Optional[str] = None
    summary: Optional[str] = None
    course_id: int = Field(foreign_key="course.course_id")
    lesson_type: LessonType = Field(default=LessonType.text)
    status: LessonStatus = Field(default=LessonStatus.draft)
    duration: Optional[int] = None
    sequence_order: Optional[int] = Field(default=0)
    is_required: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False)
    meeting_link: Optional[str] = Field(default=None, max_length=255)
    start_time: datetime
    end_time: datetime 