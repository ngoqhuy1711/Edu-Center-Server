import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class LessonStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class LessonType(enum.Enum):
    TEXT = "text"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"


class Lesson(Base):
    __tablename__ = "lessons"

    lesson_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)

    lesson_type = Column(Enum(LessonType), default=LessonType.TEXT, nullable=False)
    status = Column(Enum(LessonStatus), default=LessonStatus.DRAFT, nullable=False)
    duration = Column(Integer, nullable=True)  # Duration in minutes
    sequence_order = Column(Integer, default=0)
    is_required = Column(Boolean, default=True)

    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="lessons")
    resources = relationship("LessonResource", back_populates="lesson", cascade="all, delete-orphan")
    user_progress = relationship("UserLessonProgress", back_populates="lesson", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Lesson {self.lesson_id}: {self.title}>"


class LessonResource(Base):
    __tablename__ = "lesson_resources"

    resource_id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    resource_type = Column(String(50), nullable=False)  # file, link, etc.
    url = Column(String(512), nullable=True)
    file_path = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)

    # Relationships
    lesson = relationship("Lesson", back_populates="resources")

    def __repr__(self):
        return f"<LessonResource {self.resource_id}: {self.title}>"


class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"

    progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    progress_percentage = Column(Float, default=0.0)
    last_position = Column(String(50), nullable=True)  # For video/audio position
    time_spent = Column(Integer, default=0)  # Time spent in seconds
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="lesson_progress")
    lesson = relationship("Lesson", back_populates="user_progress")

    def __repr__(self):
        return f"<UserLessonProgress {self.progress_id}: User {self.user_id}, Lesson {self.lesson_id}>"
