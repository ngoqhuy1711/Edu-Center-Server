import enum

from sqlalchemy import Column, Integer, Boolean, DateTime, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ExamSubmissionStatus(enum.Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    GRADED = "graded"
    LATE = "late"


class ExamSubmission(Base):
    __tablename__ = "exam_submissions"

    submission_id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.exam_id"), nullable=False)
    answers = Column(Text, nullable=True)
    submission_date = Column(DateTime, default=func.current_timestamp())
    status = Column(Enum(ExamSubmissionStatus), default=ExamSubmissionStatus.DRAFT)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    time_spent = Column(Integer, nullable=True)  # Time spent in seconds
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    student = relationship("User", back_populates="exam_submissions", foreign_keys=[student_id])
    exam = relationship("Exam", back_populates="submissions")

    def __repr__(self):
        return f"<ExamSubmission {self.submission_id} - Student: {self.student_id}, Exam: {self.exam_id}>"
