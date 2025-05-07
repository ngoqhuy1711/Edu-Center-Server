from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship, func

from app.models.assignment import Assignment
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User


class SubmissionType(str, Enum):
    TEXT = "text"
    FILE = "file"
    LINK = "link"
    OTHER = "other"


class SubmissionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"
    RESUBMITTED = "resubmitted"


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"
    submission_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    course_id: int = Field(foreign_key="courses.course_id", nullable=False)
    lesson_id: Optional[int] = Field(foreign_key="lessons.lesson_id", nullable=True)
    assignment_id: int = Field(foreign_key="assignments.assignment_id", nullable=False)
    submission_type: SubmissionType = Field(sa_column_kwargs={"nullable": False})
    status: SubmissionStatus = Field(default=SubmissionStatus.SUBMITTED, sa_column_kwargs={"nullable": False})
    title: str = Field(..., max_length=255)
    content: Optional[str] = Field(default=None)
    score: Optional[float] = Field(default=None)
    max_score: Optional[float] = Field(default=None)
    graded_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    feedback: Optional[str] = Field(default=None)
    submitted_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    graded_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": True
        }
    )
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

    user: "User" = Relationship(back_populates="submissions",
                                sa_relationship_kwargs={"foreign_keys": "[Submission.user_id]"})
    course: "Course" = Relationship(back_populates="submissions",
                                    sa_relationship_kwargs={"foreign_keys": "[Submission.course_id]"})
    lesson: Optional["Lesson"] = Relationship(back_populates="submissions",
                                              sa_relationship_kwargs={"foreign_keys": "[Submission.lesson_id]"})
    assignment: "Assignment" = Relationship(back_populates="submissions",
                                            sa_relationship_kwargs={"foreign_keys": "[Submission.assignment_id]"})
    graded_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Submission.graded_by]"})
    created_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Submission.created_by]"})
    updated_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Submission.updated_by]"})

    def __repr__(self) -> str:
        return f"Submission(submission_id={self.submission_id}, user_id={self.user_id}, course_id={self.course_id}, lesson_id={self.lesson_id}, assignment_id={self.assignment_id}, submission_type={self.submission_type})"


class SubmissionAttachment(SQLModel, table=True):
    __tablename__ = "submission_attachments"
    attachment_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    submission_id: int = Field(foreign_key="submissions.submission_id", nullable=False)
    file_name: str = Field(..., max_length=255)
    file_path: str = Field(..., max_length=512)
    file_type: Optional[str] = Field(default=None, max_length=100)
    file_size: Optional[int] = Field(default=None)
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

    submission: "Submission" = Relationship(back_populates="attachments",
                                            sa_relationship_kwargs={
                                                "foreign_keys": "[SubmissionAttachment.submission_id]"})
    created_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[SubmissionAttachment.created_by]"})
    updated_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[SubmissionAttachment.updated_by]"})

    def __repr__(self) -> str:
        return f"SubmissionAttachment(attachment_id={self.attachment_id}, submission_id={self.submission_id}, file_name={self.file_name})"
