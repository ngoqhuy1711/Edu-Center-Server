import enum
from datetime import datetime, UTC
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, func

from app.models.course import Course
from app.models.user import User


class ExamType(str, enum.Enum):
    QUIZ = "quiz"
    MIDTERM = "midterm"
    FINAL = "final"
    PLACEMENT = "placement"
    PRACTICE = "practice"


class ExamStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


class ExamSubmissionStatus(str, enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"


class Exam(SQLModel, table=True):
    __tablename__ = "exams"
    exam_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(default=None)
    instructions: Optional[str] = Field(default=None)
    course_id: int = Field(foreign_key="courses.course_id", nullable=False)
    teacher_id: int = Field(foreign_key="users.user_id", nullable=False)
    exam_type: ExamType = Field(default=ExamType.QUIZ, sa_column_kwargs={"nullable": False})
    status: ExamStatus = Field(default=ExamStatus.DRAFT, sa_column_kwargs={"nullable": False})
    duration: Optional[int] = Field(default=None, sa_column_kwargs={"nullable": True})
    max_score: float = Field(default=100.0, sa_column_kwargs={"nullable": False})
    passing_score: Optional[float] = Field(default=None, sa_column_kwargs={"nullable": True})
    start_date: datetime = Field(
        ...,
        sa_column_kwargs={
            "nullable": False
        }
    )
    end_date: datetime = Field(
        ...,
        sa_column_kwargs={
            "nullable": False
        }
    )
    questions: Optional[str] = Field(default=None)
    shuffle_questions: bool = Field(default=False)
    allow_multiple_attempts: bool = Field(default=False)
    max_attempts: int = Field(default=1)
    show_answers: bool = Field(default=True)
    show_score: bool = Field(default=True)
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

    course: "Course" = Relationship(back_populates="exams",
                                              sa_relationship_kwargs={"foreign_keys": "[Exam.course_id]"})
    teacher: "User" = Relationship(back_populates="exams",
                                             sa_relationship_kwargs={"foreign_keys": "[Exam.teacher_id]"})
    created_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Exam.created_by]"})
    updated_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Exam.updated_by]"})
    exam_submissions: List["ExamSubmission"] = Relationship(back_populates="exam",
                                                          sa_relationship_kwargs={"foreign_keys": "[ExamSubmission.exam_id]"})

    def __repr__(self) -> str:
        return f"Exam(exam_id={self.exam_id}, title={self.title}, course_id={self.course_id}, teacher_id={self.teacher_id})"


class ExamSubmission(SQLModel, table=True):
    __tablename__ = "exam_submissions"
    exam_submission_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    student_id: int = Field(foreign_key="users.user_id", nullable=False)
    exam_id: int = Field(foreign_key="exams.exam_id", nullable=False)
    answers: Optional[str] = Field(default=None)
    submission_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    status: ExamSubmissionStatus = Field(default=ExamSubmissionStatus.DRAFT, sa_column_kwargs={"nullable": False})
    score: Optional[float] = Field(default=None, sa_column_kwargs={"nullable": True})
    feedback: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    time_spent: Optional[int] = Field(default=None, sa_column_kwargs={"nullable": True})
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

    student: "User" = Relationship(back_populates="exam_submissions",
                                             sa_relationship_kwargs={"foreign_keys": "[ExamSubmission.student_id]"})
    exam: "Exam" = Relationship(back_populates="exam_submissions",
                                          sa_relationship_kwargs={"foreign_keys": "[ExamSubmission.exam_id]"})

    def __repr__(self) -> str:
        return f"ExamSubmission(exam_submission_id={self.exam_submission_id}, student_id={self.student_id}, exam_id={self.exam_id})"
