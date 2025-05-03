import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ExamType(enum.Enum):
    QUIZ = "quiz"
    MIDTERM = "midterm"
    FINAL = "final"
    PLACEMENT = "placement"
    PRACTICE = "practice"


class ExamStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


class Exam(Base):
    __tablename__ = "exams"

    exam_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    exam_type = Column(Enum(ExamType), default=ExamType.QUIZ)
    status = Column(Enum(ExamStatus), default=ExamStatus.DRAFT)
    duration = Column(Integer, nullable=True)  # Duration in minutes
    max_score = Column(Float, default=100.0)
    passing_score = Column(Float, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    questions = Column(Text, nullable=True)  # Typically JSON data for questions
    shuffle_questions = Column(Boolean, default=False)
    allow_multiple_attempts = Column(Boolean, default=False)
    max_attempts = Column(Integer, default=1)
    show_answers = Column(Boolean, default=True)
    show_score = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    teacher = relationship("User", back_populates="exams_created", foreign_keys=[teacher_id])
    course = relationship("Course", back_populates="exams")
    submissions = relationship("ExamSubmission", back_populates="exam", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Exam {self.exam_id}: {self.title}>"
