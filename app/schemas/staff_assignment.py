from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class StaffAssignmentStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELED = "canceled"


class StaffAssignmentRole(str, Enum):
    INSTRUCTOR = "instructor"
    TEACHING_ASSISTANT = "teaching_assistant"
    TUTOR = "tutor"
    GUEST_LECTURER = "guest_lecturer"
    ADMIN = "admin"
    CONTENT_CREATOR = "content_creator"


# Base schema with common attributes
class StaffAssignmentBase(BaseModel):
    staff_id: int
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    role: StaffAssignmentRole
    status: StaffAssignmentStatus = StaffAssignmentStatus.PENDING
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    is_primary: bool = False


# Schema for creating a staff assignment
class StaffAssignmentCreate(StaffAssignmentBase):
    pass


# Schema for updating a staff assignment
class StaffAssignmentUpdate(BaseModel):
    staff_id: Optional[int] = None
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    role: Optional[StaffAssignmentRole] = None
    status: Optional[StaffAssignmentStatus] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    is_primary: Optional[bool] = None


# Schema for reading a staff assignment
class StaffAssignmentInDB(StaffAssignmentBase):
    assignment_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
