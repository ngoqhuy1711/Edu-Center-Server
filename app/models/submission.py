import enum

from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SubmissionType(enum.Enum):
    file = 'file'
    text = 'text'
    url = 'url'


class SubmissionStatus(enum.Enum):
    submitted = 'submitted'
    graded = 'graded'
    late = 'late'
    resubmitted = 'resubmitted'


class Submission(Base):
    __tablename__ = 'submissions'

    submission_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id', ondelete='SET NULL'), nullable=True)
    assignment_id = Column(Integer, ForeignKey('assignments.assignment_id', ondelete='CASCADE'), nullable=False)
    submission_type = Column(ENUM(SubmissionType, name='submission_type'), nullable=False)
    status = Column(ENUM(SubmissionStatus, name='submission_status'), nullable=False,
                    default=SubmissionStatus.submitted)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)
    graded_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    graded_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    is_deleted = Column(Boolean, default=False)

    user = relationship('User', foreign_keys=[user_id], back_populates='submissions')  # type: ignore
    course = relationship('Course', back_populates='submissions')
    lesson = relationship('Lesson', back_populates='submissions')
    assignment = relationship('Assignment', back_populates='submissions')
    grader = relationship('User', foreign_keys=[graded_by], back_populates='graded_submissions')  # type: ignore
    attachments = relationship('SubmissionAttachment', back_populates='submission', cascade='all, delete-orphan')
    creator = relationship('User', foreign_keys=[created_by])  # type: ignore
    updater = relationship('User', foreign_keys=[updated_by])  # type: ignore

    __table_args__ = (
        Index('idx_submissions_user_id', 'user_id'),
        Index('idx_submissions_course_id', 'course_id'),
        Index('idx_submissions_lesson_id', 'lesson_id'),
        Index('idx_submissions_assignment_id', 'assignment_id'),
        Index('idx_submissions_graded_by', 'graded_by'),
        Index('idx_submissions_submitted_at', 'submitted_at'),
        Index('idx_submissions_is_deleted', 'is_deleted'),
    )


class SubmissionAttachment(Base):
    __tablename__ = 'submission_attachments'

    attachment_id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submissions.submission_id', ondelete='CASCADE'), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    is_deleted = Column(Boolean, default=False)

    submission = relationship('Submission', back_populates='attachments')
    creator = relationship('User', foreign_keys=[created_by])  # type: ignore
    updater = relationship('User', foreign_keys=[updated_by])  # type: ignore

    __table_args__ = (
        Index('idx_submission_attachments_submission_id', 'submission_id'),
        Index('idx_submission_attachments_is_deleted', 'is_deleted'),
    )
