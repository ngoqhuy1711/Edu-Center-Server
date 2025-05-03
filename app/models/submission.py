import enum

from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SubmissionStatus(enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    GRADING = "grading"
    GRADED = "graded"
    LATE = "late"
    RETURNED = "returned"
    RESUBMITTED = "resubmitted"


class SubmissionType(enum.Enum):
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    EXAM = "exam"
    PROJECT = "project"
    LAB = "lab"


class Submission(Base):
    __tablename__ = "submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"), nullable=True)
    assignment_id = Column(Integer, ForeignKey("assignments.assignment_id"), nullable=False)

    submission_type = Column(Enum(SubmissionType), nullable=False)
    status = Column(Enum(SubmissionStatus), default=SubmissionStatus.SUBMITTED, nullable=False)

    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)

    # Grading information
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    graded_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    feedback = Column(Text, nullable=True)

    submitted_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    graded_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(),
                        onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="submissions")
    grader = relationship("User", foreign_keys=[graded_by], back_populates="graded_submissions")
    course = relationship("Course", back_populates="submissions")
    lesson = relationship("Lesson", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")
    attachments = relationship("SubmissionAttachment", back_populates="submission",
                               cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Submission {self.submission_id}: {self.title} by User {self.user_id}>"


class SubmissionAttachment(Base):
    __tablename__ = "submission_attachments"

    attachment_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.submission_id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)  # Size in bytes
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)

    # Relationships
    submission = relationship("Submission", back_populates="attachments")

    def __repr__(self):
        return f"<SubmissionAttachment {self.attachment_id}: {self.file_name}>"
