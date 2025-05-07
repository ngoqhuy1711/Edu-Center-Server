import enum
from datetime import datetime, UTC
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, func

from app.models.lesson import Lesson
from app.models.submission import Submission
from app.models.user import User


class AssignmentStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class Assignment(SQLModel, table=True):
    __tablename__ = "assignments"
    assignment_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(default=None)
    instructions: str = Field(...)
    due_date: datetime = Field(..., sa_column_kwargs={"nullable": False})
    max_score: float = Field(default=100.0, sa_column_kwargs={"nullable": False})
    attachment_url: Optional[str] = Field(default=None, max_length=255)
    status: AssignmentStatus = Field(default=AssignmentStatus.DRAFT, sa_column_kwargs={"nullable": False})
    is_active: bool = Field(default=True, sa_column_kwargs={"nullable": False})

    teacher_id: int = Field(foreign_key="users.user_id", nullable=False)
    lesson_id: int = Field(foreign_key="lessons.lesson_id", nullable=True)

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
    created_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    is_deleted: bool = Field(default=False)

    teacher: "User" = Relationship(back_populates="assignments",
                                   sa_relationship_kwargs={"foreign_keys": "[Assignment.teacher_id]"})
    lesson: "Lesson" = Relationship(back_populates="assignments",
                                    sa_relationship_kwargs={"foreign_keys": "[Assignment.lesson_id]"})
    submissions: List["Submission"] = Relationship(back_populates="assignment",
                                                   sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    created_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Assignment.created_by]"})
    updated_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Assignment.updated_by]"})

    def __repr__(self) -> str:
        return f"<Assignment {self.title} (ID: {self.assignment_id})>"
