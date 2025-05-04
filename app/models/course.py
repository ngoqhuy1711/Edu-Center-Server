import enum

from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, func
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class CourseStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    COMPLETED = "completed"


class MemberRole(enum.Enum):
    STUDENT = "student"
    TEACHING_ASSISTANT = "teaching_assistant"
    OBSERVER = "observer"


class MemberStatus(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    credit_hours = Column(Integer)
    status = Column(Enum(CourseStatus), default=CourseStatus.DRAFT, nullable=False)
    enrollment_limit = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    department_id = Column(Integer, ForeignKey("departments.department_id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    is_deleted = Column(Boolean, default=False)

    members = relationship("CourseMember", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")
    teacher = relationship("User", foreign_keys="[teacher_id]")
    created_by_user = relationship("User", foreign_keys=[created_by])  # type: ignore
    updated_by_user = relationship("User", foreign_keys=[updated_by])  # type: ignore
    department = relationship("Department")
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    teaching_materials = relationship("TeachingMaterial", back_populates="course", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course {self.title} (Code: {self.code})>"


class CourseMember(Base):
    __tablename__ = "course_members"

    member_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(MemberRole), default=MemberRole.STUDENT, nullable=False)
    status = Column(Enum(MemberStatus), default=MemberStatus.PENDING, nullable=False)
    joined_at = Column(DateTime(timezone=True), default=func.current_timestamp(), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    is_deleted = Column(Boolean, default=False)

    course = relationship("Course", back_populates="members")
    user = relationship("User", foreign_keys="[user_id]")
    created_by_user = relationship("User", foreign_keys=[created_by])  # type: ignore
    updated_by_user = relationship("User", foreign_keys=[updated_by])  # type: ignore

    def __repr__(self):
        return f"<CourseMember {self.user_id} in Course {self.course_id}>"
