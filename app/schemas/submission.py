from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class SubmissionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    GRADING = "grading"
    GRADED = "graded"
    LATE = "late"
    RETURNED = "returned"
    RESUBMITTED = "resubmitted"


class SubmissionType(str, Enum):
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    EXAM = "exam"
    PROJECT = "project"
    LAB = "lab"


# SubmissionAttachment schemas
class SubmissionAttachmentBase(BaseModel):
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class SubmissionAttachmentCreate(SubmissionAttachmentBase):
    submission_id: int


class SubmissionAttachmentOut(SubmissionAttachmentBase):
    attachment_id: int
    submission_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Submission schemas
class SubmissionBase(BaseModel):
    title: str
    content: Optional[str] = None
    submission_type: SubmissionType


class SubmissionCreate(SubmissionBase):
    user_id: int
    course_id: int
    assignment_id: int
    lesson_id: Optional[int] = None
    status: SubmissionStatus = SubmissionStatus.SUBMITTED


class SubmissionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[SubmissionStatus] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    feedback: Optional[str] = None


class SubmissionGrade(BaseModel):
    score: float
    max_score: float
    feedback: Optional[str] = None
    status: SubmissionStatus = SubmissionStatus.GRADED


class SubmissionOut(SubmissionBase):
    submission_id: int
    user_id: int
    course_id: int
    lesson_id: Optional[int] = None
    assignment_id: int
    status: SubmissionStatus
    score: Optional[float] = None
    max_score: Optional[float] = None
    graded_by: Optional[int] = None
    feedback: Optional[str] = None
    submitted_at: datetime
    graded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    attachments: List[SubmissionAttachmentOut] = []

    class Config:
        orm_mode = True
