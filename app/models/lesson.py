from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, func
from datetime import datetime, UTC

from app.models.course import Course
from app.models.user import User

if TYPE_CHECKING:
    from app.models.assignment import Assignment
    from app.models.submission import Submission
    from app.models.teaching_material import TeachingMaterial
    from app.models.staff_assignment import StaffAssignment


class LessonStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    ARCHIVED = "archived"

class LessonType(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"


class Lesson(SQLModel, table=True):
    __tablename__ = "lessons"
    lesson_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(..., max_length=255)
    content: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    course_id: int = Field(foreign_key="courses.course_id", nullable=False)
    lesson_type: LessonType = Field(default=LessonType.TEXT, sa_column_kwargs={"nullable": False})
    status: LessonStatus = Field(default=LessonStatus.DRAFT, sa_column_kwargs={"nullable": False})
    duration: Optional[int] = Field(default=None, sa_column_kwargs={"nullable": True})
    sequence_order: int = Field(default=0)
    is_required: bool = Field(default=False)
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
    meeting_link: Optional[str] = Field(default=None, max_length=255)
    start_time: datetime = Field(
        ...,
        sa_column_kwargs={
            "nullable": False
        }
    )
    end_time: datetime = Field(
        ...,
        sa_column_kwargs={
            "nullable": False
        }
    )

    course: "Course" = Relationship(back_populates="lessons",
                                     sa_relationship_kwargs={"foreign_keys": "[Lesson.course_id]"})
    created_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Lesson.created_by]"})
    updated_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Lesson.updated_by]"})
    
    # Add relationships to other models
    assignments: List["Assignment"] = Relationship(back_populates="lesson",
                                                 sa_relationship_kwargs={"foreign_keys": "[Assignment.lesson_id]"})
    submissions: List["Submission"] = Relationship(back_populates="lesson",
                                                 sa_relationship_kwargs={"foreign_keys": "[Submission.lesson_id]"})
    resources: List["LessonResource"] = Relationship(back_populates="lesson",
                                                   sa_relationship_kwargs={"foreign_keys": "[LessonResource.lesson_id]"})
    user_progress: List["UserLessonProgress"] = Relationship(back_populates="lesson",
                                                           sa_relationship_kwargs={"foreign_keys": "[UserLessonProgress.lesson_id]"})
    teaching_materials: List["TeachingMaterial"] = Relationship(back_populates="lesson",
                                                              sa_relationship_kwargs={"foreign_keys": "[TeachingMaterial.lesson_id]"})
    staff_assignments: List["StaffAssignment"] = Relationship(back_populates="lesson",
                                                            sa_relationship_kwargs={"foreign_keys": "[StaffAssignment.lesson_id]"})

    def __repr__(self) -> str:
        return f"Lesson(lesson_id={self.lesson_id}, title={self.title}, course_id={self.course_id})"


class LessonResource(SQLModel, table=True):
    __tablename__ = "lesson_resources"
    resource_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    lesson_id: int = Field(foreign_key="lessons.lesson_id", nullable=False)
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(default=None)
    resource_type: str = Field(..., max_length=50)
    url: str = Field(..., max_length=512)
    file_path: str = Field(..., max_length=512)
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

    lesson: "Lesson" = Relationship(back_populates="resources",
                                        sa_relationship_kwargs={"foreign_keys": "[LessonResource.lesson_id]"})
    created_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[LessonResource.created_by]"})
    updated_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[LessonResource.updated_by]"})

    def __repr__(self) -> str:
        return f"LessonResource(resource_id={self.resource_id}, title={self.title}, lesson_id={self.lesson_id})"

class UserLessonProgress(SQLModel, table=True):
    __tablename__ = "user_lesson_progress"
    progress_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    lesson_id: int = Field(foreign_key="lessons.lesson_id", nullable=False)
    is_completed: bool = Field(default=False)
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    last_position: Optional[str] = Field(default=None)
    time_spent: int = Field(default=0)
    completed_at: datetime = Field(
        ...,
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
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

    user: "User" = Relationship(back_populates="lesson_progress",
                            sa_relationship_kwargs={"foreign_keys": "[UserLessonProgress.user_id]"})
    lesson: "Lesson" = Relationship(back_populates="user_progress",
                                     sa_relationship_kwargs={"foreign_keys": "[UserLessonProgress.lesson_id]"})

    def __repr__(self) -> str:
        return f"UserLessonProgress(progress_id={self.progress_id}, user_id={self.user_id}, lesson_id={self.lesson_id})"
