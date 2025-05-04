from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class SubmissionType(str, Enum):
    file = 'file'
    text = 'text'
    url = 'url'


class SubmissionStatus(str, Enum):
    submitted = 'submitted'
    graded = 'graded'
    late = 'late'
    resubmitted = 'resubmitted'


class SubmissionAttachment(BaseModel):
    attachment_id: int
    submission_id: int
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class SubmissionBase(BaseModel):
    user_id: int
    course_id: int
    lesson_id: Optional[int] = None
    assignment_id: int
    submission_type: SubmissionType
    status: SubmissionStatus = SubmissionStatus.submitted
    title: str
    content: Optional[str] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    graded_by: Optional[int] = None
    feedback: Optional[str] = None
    submitted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class SubmissionCreate(SubmissionBase):
    pass


class SubmissionUpdate(BaseModel):
    user_id: Optional[int] = None
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    assignment_id: Optional[int] = None
    submission_type: Optional[SubmissionType] = None
    status: Optional[SubmissionStatus] = None
    title: Optional[str] = None
    content: Optional[str] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    graded_by: Optional[int] = None
    feedback: Optional[str] = None
    submitted_at: Optional[datetime] = None
    is_deleted: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class SubmissionInDB(SubmissionBase):
    submission_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool
    attachments: List[SubmissionAttachment] = []

    model_config = ConfigDict(from_attributes=True)
