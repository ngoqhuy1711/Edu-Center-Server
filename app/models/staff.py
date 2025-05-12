from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import StaffAssignmentRole, StaffAssignmentStatus

class StaffAssignment(SQLModel, table=True):
    __tablename__ = "staff_assignments"
    assignment_id: Optional[int] = Field(default=None, primary_key=True)
    staff_id: int = Field(foreign_key="user.user_id")
    course_id: Optional[int] = Field(default=None, foreign_key="course.course_id")
    lesson_id: Optional[int] = Field(default=None, foreign_key="lesson.lesson_id")
    role: StaffAssignmentRole
    status: StaffAssignmentStatus = Field(default=StaffAssignmentStatus.pending)
    start_date: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    end_date: Optional[datetime] = None
    description: Optional[str] = None
    is_primary: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False) 