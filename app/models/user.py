from datetime import datetime, UTC
from typing import Optional, Dict, List, TYPE_CHECKING

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, func, PrimaryKeyConstraint, Relationship

from app.models.role import Role

if TYPE_CHECKING:
    from app.models.course import Course, CourseMember
    from app.models.message import Message
    from app.models.assignment import Assignment
    from app.models.submission import Submission
    from app.models.exam import Exam, ExamSubmission
    from app.models.forum import ForumPost, ForumTopic, PostLike
    from app.models.payment import Payment
    from app.models.enrollment_request import EnrollmentRequest
    from app.models.lesson import UserLessonProgress
    from app.models.staff_assignment import StaffAssignment


class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, nullable=False)
    email: str = Field(max_length=100, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
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

    profiles: List["UserProfile"] = Relationship(back_populates="user",
                                                 sa_relationship_kwargs={"foreign_keys": "[UserProfile.user_id]"})
    roles: List["UserRole"] = Relationship(back_populates="user",
                                           sa_relationship_kwargs={"foreign_keys": "[UserRole.user_id]"})
    
    # Course relationships
    courses: List["Course"] = Relationship(back_populates="teacher",
                                          sa_relationship_kwargs={"foreign_keys": "[Course.teacher_id]"})
    course_members: List["CourseMember"] = Relationship(back_populates="user",
                                                       sa_relationship_kwargs={"foreign_keys": "[CourseMember.user_id]"})
    
    # Message relationships
    sent_messages: List["Message"] = Relationship(back_populates="sender",
                                                sa_relationship_kwargs={"foreign_keys": "[Message.sender_id]"})
    received_messages: List["Message"] = Relationship(back_populates="recipient",
                                                    sa_relationship_kwargs={"foreign_keys": "[Message.recipient_id]"})
    
    # Assignment relationships
    assignments: List["Assignment"] = Relationship(back_populates="teacher",
                                                 sa_relationship_kwargs={"foreign_keys": "[Assignment.teacher_id]"})
    
    # Submission relationships
    submissions: List["Submission"] = Relationship(back_populates="user",
                                                 sa_relationship_kwargs={"foreign_keys": "[Submission.user_id]"})
    
    # Exam relationships
    exams: List["Exam"] = Relationship(back_populates="teacher",
                                      sa_relationship_kwargs={"foreign_keys": "[Exam.teacher_id]"})
    exam_submissions: List["ExamSubmission"] = Relationship(back_populates="student",
                                                          sa_relationship_kwargs={"foreign_keys": "[ExamSubmission.student_id]"})
    
    # Forum relationships
    forum_posts: List["ForumPost"] = Relationship(back_populates="author",
                                                sa_relationship_kwargs={"foreign_keys": "[ForumPost.author_id]"})
    forum_topics: List["ForumTopic"] = Relationship(back_populates="creator",
                                                  sa_relationship_kwargs={"foreign_keys": "[ForumTopic.creator_id]"})
    post_likes: List["PostLike"] = Relationship(back_populates="user",
                                              sa_relationship_kwargs={"foreign_keys": "[PostLike.user_id]"})
    
    # Payment relationships
    payments: List["Payment"] = Relationship(back_populates="user",
                                           sa_relationship_kwargs={"foreign_keys": "[Payment.user_id]"})
    
    # Enrollment request relationships
    enrollment_requests: List["EnrollmentRequest"] = Relationship(back_populates="user",
                                                                sa_relationship_kwargs={"foreign_keys": "[EnrollmentRequest.user_id]"})
    
    # Lesson progress relationships
    lesson_progress: List["UserLessonProgress"] = Relationship(back_populates="user",
                                                             sa_relationship_kwargs={"foreign_keys": "[UserLessonProgress.user_id]"})
    
    # Staff assignment relationships
    staff_assignments: List["StaffAssignment"] = Relationship(back_populates="staff",
                                                            sa_relationship_kwargs={"foreign_keys": "[StaffAssignment.staff_id]"})

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, username={self.username}, email={self.email})"


class UserRole(SQLModel, table=True):
    __tablename__ = "user_roles"
    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    role_id: int = Field(foreign_key="roles.role_id", primary_key=True)
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
        PrimaryKeyConstraint("user_id", "role_id"),
    )

    user: "User" = Relationship(back_populates="roles",
                                sa_relationship_kwargs={"foreign_keys": "[UserRole.user_id]"})
    role: "Role" = Relationship(back_populates="users",
                                sa_relationship_kwargs={"foreign_keys": "[UserRole.role_id]"})

    def __repr__(self) -> str:
        return f"UserRole(user_id={self.user_id}, role_id={self.role_id})"


class UserProfile(SQLModel, table=True):
    __tablename__ = "user_profiles"
    user_profile_id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.user_id", primary_key=True)
    full_name: str = Field(max_length=100, nullable=False)
    profile_picture: str = Field(max_length=255, nullable=True)
    date_of_birth: datetime = Field(nullable=True)
    phone_number: str = Field(max_length=20, nullable=True)
    address: str = Field(max_length=255, nullable=True)
    bio: str = Field(max_length=500, nullable=True)
    gender: str = Field(max_length=10, nullable=True)
    social_links: Optional[Dict] = Field(default=None, sa_column=Column(JSONB))
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

    user: "User" = Relationship(back_populates="profiles",
                                sa_relationship_kwargs={"foreign_keys": "[UserProfile.user_id]"})

    def __repr__(self) -> str:
        return f"UserProfile(user_id={self.user_id}, full_name={self.full_name})"
