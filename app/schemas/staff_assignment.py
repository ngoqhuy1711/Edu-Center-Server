import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.staff_assignment import StaffAssignmentRole, StaffAssignmentStatus


class StaffAssignmentBase(BaseModel):
    staff_id: int
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    role: StaffAssignmentRole = Field(...)
    status: StaffAssignmentStatus = Field(default=StaffAssignmentStatus.pending)
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None
    description: Optional[str] = None
    is_primary: bool = False

    model_config = ConfigDict(from_attributes=True)


class StaffAssignmentCreate(StaffAssignmentBase):
    pass


class StaffAssignmentUpdate(BaseModel):
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    role: Optional[StaffAssignmentRole] = None
    status: Optional[StaffAssignmentStatus] = None
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None
    description: Optional[str] = None
    is_primary: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class StaffAssignmentRead(StaffAssignmentBase):
    assignment_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
