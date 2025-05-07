import enum
from datetime import datetime, UTC
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship, func

from app.models.user import User


class CourseStatus(enum.Enum):
    ACTIVE = "active"
    UPCOMING = "upcoming"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CourseLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class MemberRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    STAFF = "staff"
    ADMIN = "admin"


class Course(SQLModel, table=True):
    __tablename__ = "courses"
    course_id: Optional[int] = Field(default=None, primary_key=True)
    course_code: str = Field(..., max_length=20, index=True)
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    level: CourseLevel = Field(default=CourseLevel.BEGINNER)
    teacher_id: int = Field(foreign_key="users.user_id")
    credits: int = Field(default=0)
    max_students: int = Field(default=30)
    price: Optional[float] = Field(default=None, ge=0)
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
    image_url: Optional[str] = Field(default=None, max_length=255)
    syllabus: Optional[str] = None
    prerequisites: Optional[str] = None
    location: Optional[str] = Field(default=None, max_length=100)
    status: CourseStatus = Field(default=CourseStatus.UPCOMING)
    is_published: bool = Field(default=False)
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

    teacher: "User" = Relationship(back_populates="courses",
                                   sa_relationship_kwargs={"foreign_keys": "[Course.teacher_id]"})
    created_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Course.created_by]"})
    updated_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Course.updated_by]"})

    def __repr__(self) -> str:
        return f"Course(course_id={self.course_id}, title={self.title}, teacher_id={self.teacher_id})"

class CourseMember(SQLModel, table=True):
    __tablename__ = "course_members"
    course_member_id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.course_id")
    user_id: int = Field(foreign_key="users.user_id")
    role: MemberRole
    is_active: bool = Field(default=True)
    joined_date: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    access_level: int = Field(default=1)
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

    course: "Course" = Relationship(back_populates="members",
                                    sa_relationship_kwargs={"foreign_keys": "[CourseMember.course_id]"})
    user: "User" = Relationship(back_populates="course_members",
                                sa_relationship_kwargs={"foreign_keys": "[CourseMember.user_id]"})

    def __repr__(self) -> str:
        return f"CourseMember(course_member_id={self.course_member_id}, course_id={self.course_id}, user_id={self.user_id}, role={self.role})"