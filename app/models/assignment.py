from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import AssignmentStatus

class Assignment(SQLModel, table=True):
    __tablename__ = "assignments"
    assignment_id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    instructions: str
    due_date: datetime
    max_score: float = Field(default=100.0)
    attachment_url: Optional[str] = Field(default=None, max_length=255)
    status: AssignmentStatus = Field(default=AssignmentStatus.draft)
    is_active: bool = Field(default=True)
    teacher_id: int = Field(foreign_key="user.user_id")
    lesson_id: Optional[int] = Field(default=None, foreign_key="lesson.lesson_id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False) 