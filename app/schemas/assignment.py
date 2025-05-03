from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.assignment import AssignmentStatus


# Base Assignment schema with common fields
class AssignmentBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    instructions: str
    due_date: datetime
    max_score: float = Field(100.0, ge=0)
    attachment_url: Optional[str] = None
    status: AssignmentStatus = AssignmentStatus.DRAFT
    course_id: int


# Schema for creating a new assignment
class AssignmentCreate(AssignmentBase):
    pass


# Schema for updating an existing assignment
class AssignmentUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    instructions: Optional[str] = None
    due_date: Optional[datetime] = None
    max_score: Optional[float] = Field(None, ge=0)
    attachment_url: Optional[str] = None
    status: Optional[AssignmentStatus] = None
    is_active: Optional[bool] = None
    course_id: Optional[int] = None


# Schema for database assignment (includes all fields)
class AssignmentInDB(AssignmentBase):
    assignment_id: int
    teacher_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For Pydantic v2+, use orm_mode=True for v1


# Schema for assignment response
class AssignmentResponse(AssignmentInDB):
    pass
