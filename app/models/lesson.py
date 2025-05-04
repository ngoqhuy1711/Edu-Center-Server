from datetime import datetime, UTC
from enum import Enum

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class LessonType(str, Enum):
    LECTURE = "lecture"
    LAB = "lab"
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    EXAM = "exam"
    OTHER = "other"


class LessonStatus(str, Enum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Lesson(Base):
    __tablename__ = 'lessons'

    lesson_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.module_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content = Column(Text)
    lesson_order = Column(Integer)
    lesson_type = Column(SQLAlchemyEnum(LessonType), nullable=False)
    status = Column(SQLAlchemyEnum(LessonStatus), default=LessonStatus.DRAFT, nullable=False)
    estimated_time = Column(Integer)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))
    is_deleted = Column(Boolean, default=False)

    course = relationship("Course")
    module = relationship("Module")
    assignments = relationship("Assignment", back_populates="lesson")
    teaching_materials = relationship("TeachingMaterial", back_populates="lesson")
    submissions = relationship("Submission", back_populates="lesson")
    staff_assignments = relationship("StaffAssignment", back_populates="lesson")


class TeachingMaterial(Base):
    __tablename__ = 'teaching_materials'

    material_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    material_type = Column(String(50), nullable=False)
    url = Column(String(512))
    file_path = Column(String(512))
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))
    is_deleted = Column(Boolean, default=False)

    course = relationship("Course")
    lesson = relationship("Lesson", back_populates="teaching_materials")
