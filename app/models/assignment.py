import enum

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, Enum, ForeignKey, Float, func
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class AssignmentStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class Assignment(Base):
    __tablename__ = "assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    instructions = Column(Text, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    max_score = Column(Float, default=100.0, nullable=False)
    attachment_url = Column(String(255))
    status = Column(Enum(AssignmentStatus), default=AssignmentStatus.DRAFT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    is_deleted = Column(Boolean, default=False)

    teacher = relationship("User", foreign_keys=[teacher_id])  # type: ignore
    course = relationship("Course", back_populates="assignments")
    lesson = relationship("Lesson")
    submissions = relationship("Submission", back_populates="assignment", cascade="all, delete-orphan")
    created_by_user = relationship("User", foreign_keys=[created_by])  # type: ignore
    updated_by_user = relationship("User", foreign_keys=[updated_by])  # type: ignore

    def __repr__(self):
        return f"<Assignment {self.title} (ID: {self.assignment_id})>"
