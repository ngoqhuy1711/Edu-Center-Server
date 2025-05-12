from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import ExamType, ExamStatus, ExamSubmissionStatus

class Exam(SQLModel, table=True):
    __tablename__ = "exams"
    exam_id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    instructions: Optional[str] = None
    course_id: int = Field(foreign_key="course.course_id")
    teacher_id: int = Field(foreign_key="user.user_id")
    exam_type: ExamType = Field(default=ExamType.quiz)
    status: ExamStatus = Field(default=ExamStatus.draft)
    duration: Optional[int] = None
    max_score: float = Field(default=100.0)
    passing_score: Optional[float] = None
    start_date: datetime
    end_date: datetime
    questions: Optional[str] = None
    shuffle_questions: bool = Field(default=False)
    allow_multiple_attempts: bool = Field(default=False)
    max_attempts: int = Field(default=1)
    show_answers: bool = Field(default=True)
    show_score: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False)

class ExamSubmission(SQLModel, table=True):
    exam_submission_id: Optional[int] = Field(default=None, primary_key=True)
    student_id: int = Field(foreign_key="user.user_id")
    exam_id: int = Field(foreign_key="exam.exam_id")
    answers: Optional[str] = None
    submission_date: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    status: ExamSubmissionStatus = Field(default=ExamSubmissionStatus.draft)
    score: Optional[float] = None
    feedback: Optional[str] = None
    is_completed: bool = Field(default=False)
    time_spent: Optional[int] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC)) 