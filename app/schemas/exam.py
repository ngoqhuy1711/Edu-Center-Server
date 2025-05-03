from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class ExamType(str, Enum):
    QUIZ = "quiz"
    MIDTERM = "midterm"
    FINAL = "final"
    PLACEMENT = "placement"
    PRACTICE = "practice"


class ExamStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


# Base Exam Schema (shared properties)
class ExamBase(BaseModel):
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    course_id: int
    teacher_id: int
    exam_type: ExamType = ExamType.QUIZ
    status: ExamStatus = ExamStatus.DRAFT
    duration: Optional[int] = None  # Duration in minutes
    max_score: float = 100.0
    passing_score: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    questions: Optional[str] = None  # JSON string containing questions
    shuffle_questions: bool = False
    allow_multiple_attempts: bool = False
    max_attempts: int = 1
    show_answers: bool = True
    show_score: bool = True


# Schema for creating a new exam
class ExamCreate(ExamBase):
    pass


# Schema for updating an exam (all fields optional)
class ExamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    course_id: Optional[int] = None
    teacher_id: Optional[int] = None
    exam_type: Optional[ExamType] = None
    status: Optional[ExamStatus] = None
    duration: Optional[int] = None
    max_score: Optional[float] = None
    passing_score: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    questions: Optional[str] = None
    shuffle_questions: Optional[bool] = None
    allow_multiple_attempts: Optional[bool] = None
    max_attempts: Optional[int] = None
    show_answers: Optional[bool] = None
    show_score: Optional[bool] = None


# Schema for database representation (includes DB fields)
class ExamInDB(ExamBase):
    exam_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # For Pydantic v1
        from_attributes = True  # For Pydantic v2


# Schema for API responses
class ExamResponse(ExamInDB):
    pass


# Schema for listing exams
class ExamList(BaseModel):
    items: List[ExamResponse]
    total: int
