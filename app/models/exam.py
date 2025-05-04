import enum
from datetime import datetime, UTC

from sqlalchemy import (
    Column, Integer, String, Float, Text, Boolean,
    DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class ExamType(enum.Enum):
    QUIZ = "quiz"
    MIDTERM = "midterm"
    FINAL = "final"
    PRACTICE = "practice"


class ExamStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"
    CLOSED = "closed"


class ExamSubmissionStatus(enum.Enum):
    STARTED = "started"
    SUBMITTED = "submitted"
    GRADED = "graded"
    FAILED = "failed"
    PASSED = "passed"


class Exam(Base):
    __tablename__ = 'exams'

    # Primary keys and foreign keys
    exam_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))

    # Basic exam info
    title = Column(String(255), nullable=False)
    description = Column(Text)
    instructions = Column(Text)
    exam_type = Column(Enum(ExamType), default=ExamType.QUIZ)
    status = Column(Enum(ExamStatus), default=ExamStatus.DRAFT)

    # Timing and attempts
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)
    max_attempts = Column(Integer, default=1)

    # Exam settings
    passing_score = Column(Float)
    is_timed = Column(Boolean, default=True)
    randomize_questions = Column(Boolean, default=False)
    show_result_after = Column(Boolean, default=True)

    # Audit fields
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    course = relationship("Course", back_populates="exams")
    lesson = relationship("Lesson", back_populates="exams")
    submissions = relationship("ExamSubmission", back_populates="exam")


class ExamSubmission(Base):
    __tablename__ = 'exam_submissions'

    # Primary keys and foreign keys
    submission_id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey('exams.exam_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    # Submission status and timing
    status = Column(Enum(ExamSubmissionStatus), default=ExamSubmissionStatus.STARTED)
    start_time = Column(DateTime(timezone=True), default=datetime.now(UTC))
    submit_time = Column(DateTime(timezone=True))
    time_spent_minutes = Column(Integer)
    attempt_number = Column(Integer, default=1)

    # Grading info
    score = Column(Float)
    max_score = Column(Float)
    feedback = Column(Text)
    graded_by = Column(Integer, ForeignKey('users.user_id'))
    graded_at = Column(DateTime(timezone=True))

    # Audit fields
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    exam = relationship("Exam", back_populates="submissions")
    user = relationship("User", foreign_keys=[user_id])  # type: ignore
    grader = relationship("User", foreign_keys=[graded_by])  # type: ignore
