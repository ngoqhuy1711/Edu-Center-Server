from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import SubmissionType, SubmissionStatus

class Submission(SQLModel, table=True):
    __tablename__ = "submissions"
    submission_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    lesson_id: Optional[int] = Field(default=None, foreign_key="lesson.lesson_id")
    assignment_id: int = Field(foreign_key="assignment.assignment_id")
    submission_type: SubmissionType
    status: SubmissionStatus = Field(default=SubmissionStatus.submitted)
    title: str = Field(max_length=255)
    content: Optional[str] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    graded_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    feedback: Optional[str] = None
    submitted_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    graded_at: Optional[datetime] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False) 