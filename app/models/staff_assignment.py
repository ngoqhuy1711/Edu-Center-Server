from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship, func


class StaffAssignmentRole(str, Enum):
    INSTRUCTOR = "instructor"
    TEACHER_ASSISTANT = "teacher_assistant"
    GRADER = "grader"
    MENTOR = "mentor"


class StaffAssignmentStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class StaffAssignment(SQLModel, table=True):
    __tablename__ = "staff_assignments"
    assignment_id: Optional[int] = Field(default=None, primary_key=True)
    staff_id: int = Field(foreign_key="users.user_id", nullable=False)
    course_id: int = Field(foreign_key="courses.course_id", nullable=False)
    lesson_id: Optional[int] = Field(foreign_key="lessons.lesson_id", nullable=True)
    role: StaffAssignmentRole = Field()
    status: StaffAssignmentStatus = Field(default=StaffAssignmentStatus.PENDING)
    start_date: datetime = Field(
        ...,
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    end_date: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "nullable": True
        }
    )
    description: Optional[str] = Field(default=None)
    is_primary: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )
    created_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    is_deleted: bool = Field(default=False)

    staff: "User" = Relationship(back_populates="staff_assignments",
                                 sa_relationship_kwargs={"foreign_keys": "[StaffAssignment.staff_id]"})
    course: "Course" = Relationship(back_populates="staff_assignments",
                                    sa_relationship_kwargs={"foreign_keys": "[StaffAssignment.course_id]"})
    lesson: Optional["Lesson"] = Relationship(back_populates="staff_assignments",
                                              sa_relationship_kwargs={"foreign_keys": "[StaffAssignment.lesson_id]"})
    created_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[StaffAssignment.created_by]"})
    updated_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[StaffAssignment.updated_by]"})

    def __repr__(self) -> str:
        return f"StaffAssignment(assignment_id={self.assignment_id}, staff_id={self.staff_id}, course_id={self.course_id}, lesson_id={self.lesson_id}, role={self.role})"
