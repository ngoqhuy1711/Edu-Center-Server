from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class ExamSubmissionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"


# Base ExamSubmission Schema (shared properties)
class ExamSubmissionBase(BaseModel):
    student_id: int
    exam_id: int
    answers: Optional[str] = None
    status: ExamSubmissionStatus = ExamSubmissionStatus.DRAFT
    score: Optional[float] = None
    feedback: Optional[str] = None
    is_completed: bool = False
    time_spent: Optional[int] = None  # Time spent in seconds


# Schema for creating a new exam submission
class ExamSubmissionCreate(ExamSubmissionBase):
    pass


# Schema for updating an exam submission (all fields optional)
class ExamSubmissionUpdate(BaseModel):
    answers: Optional[str] = None
    submission_date: Optional[datetime] = None
    status: Optional[ExamSubmissionStatus] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    is_completed: Optional[bool] = None
    time_spent: Optional[int] = None


# Schema for database representation (includes DB fields)
class ExamSubmissionInDB(ExamSubmissionBase):
    submission_id: int
    submission_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # For Pydantic v1
        from_attributes = True  # For Pydantic v2


# Schema for API responses
class ExamSubmissionResponse(ExamSubmissionInDB):
    pass


# Schema for listing exam submissions
class ExamSubmissionList(BaseModel):
    items: List[ExamSubmissionResponse]
    total: int
