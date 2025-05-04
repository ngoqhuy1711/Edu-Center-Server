from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.models.exam import (
    ExamType,
    ExamStatus,
    ExamSubmissionStatus,
)


class ExamBase(BaseModel):
    course_id: int
    lesson_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    instructions: Optional[str] = None
    exam_type: ExamType = ExamType.QUIZ
    status: ExamStatus = ExamStatus.DRAFT
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    max_attempts: Optional[int] = 1
    passing_score: Optional[float] = None
    is_timed: bool = True
    randomize_questions: bool = False
    show_result_after: bool = True


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    exam_type: Optional[ExamType] = None
    status: Optional[ExamStatus] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    max_attempts: Optional[int] = None
    passing_score: Optional[float] = None
    is_timed: Optional[bool] = None
    randomize_questions: Optional[bool] = None
    show_result_after: Optional[bool] = None


class ExamInDB(ExamBase):
    exam_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class ExamResponse(ExamInDB):
    pass


class ExamList(BaseModel):
    items: List[ExamResponse]
    total: int


class ExamSubmissionBase(BaseModel):
    exam_id: int
    user_id: int
    status: ExamSubmissionStatus = ExamSubmissionStatus.STARTED
    start_time: Optional[datetime] = None
    submit_time: Optional[datetime] = None
    time_spent_minutes: Optional[int] = None
    attempt_number: Optional[int] = 1
    score: Optional[float] = None
    max_score: Optional[float] = None
    feedback: Optional[str] = None
    graded_by: Optional[int] = None
    graded_at: Optional[datetime] = None


class ExamSubmissionCreate(ExamSubmissionBase):
    pass


class ExamSubmissionUpdate(BaseModel):
    status: Optional[ExamSubmissionStatus] = None
    start_time: Optional[datetime] = None
    submit_time: Optional[datetime] = None
    time_spent_minutes: Optional[int] = None
    attempt_number: Optional[int] = None
    score: Optional[float] = None
    max_score: Optional[float] = None
    feedback: Optional[str] = None
    graded_by: Optional[int] = None
    graded_at: Optional[datetime] = None


class ExamSubmissionInDB(ExamSubmissionBase):
    submission_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class ExamSubmissionResponse(ExamSubmissionInDB):
    pass


class ExamSubmissionList(BaseModel):
    items: List[ExamSubmissionResponse]
    total: int
