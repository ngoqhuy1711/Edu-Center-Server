from datetime import datetime, UTC
from enum import Enum as PyEnum
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, func, Relationship

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.user import User


class EnrollmentRequestStatus(PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class EnrollmentRequest(SQLModel, table=True):
    __tablename__ = "enrollment_requests"
    request_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    course_id: int = Field(foreign_key="courses.course_id", nullable=False)
    assigned_staff_id: Optional[int] = Field(foreign_key="users.user_id")
    status: EnrollmentRequestStatus = Field(default=EnrollmentRequestStatus.PENDING)
    request_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    response_date: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "nullable": True
        }
    )
    request_notes: Optional[str] = Field(default=None)
    rejection_notes: Optional[str] = Field(default=None)
    additional_requirements: Optional[str] = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )
    __table_args__ = (
        {
            "comment": "Enrollment requests for courses by users",
            "extend_existing": True,
        },
    )

    user: "User" = Relationship(back_populates="enrollment_requests",
                                sa_relationship_kwargs={"foreign_keys": "[EnrollmentRequest.user_id]"})
    course: "Course" = Relationship(back_populates="enrollment_requests",
                                    sa_relationship_kwargs={
                                        "foreign_keys": "[EnrollmentRequest.course_id]"})
    assigned_staff: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[EnrollmentRequest.assigned_staff_id]"}
    )

    def __repr__(self) -> str:
        return f"<EnrollmentRequest by User {self.user_id} for Course {self.course_id} (Status: {self.status.value})>"
