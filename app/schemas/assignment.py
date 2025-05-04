from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.assignment import AssignmentStatus


class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    attachment_url: Optional[str] = None
    status: AssignmentStatus = AssignmentStatus.DRAFT
    is_active: bool = True
    teacher_id: int
    course_id: int
    lesson_id: Optional[int] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    attachment_url: Optional[str] = None
    status: Optional[AssignmentStatus] = None
    is_active: Optional[bool] = None
    teacher_id: Optional[int] = None
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    is_deleted: Optional[bool] = None


class AssignmentInDB(AssignmentBase):
    assignment_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True)


class AssignmentResponse(AssignmentInDB):
    pass
