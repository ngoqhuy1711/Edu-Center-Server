from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class TeachingMaterial(Base):
    __tablename__ = 'teaching_materials'

    material_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id', ondelete='SET NULL'), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    material_type = Column(String(50), nullable=False)
    url = Column(String(512), nullable=True)
    file_path = Column(String(512), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    is_deleted = Column(Boolean, default=False)

    course = relationship('Course', back_populates='teaching_materials')
    lesson = relationship('Lesson', back_populates='teaching_materials')
    creator = relationship('User', foreign_keys=[created_by]) # type: ignore
    updater = relationship('User', foreign_keys=[updated_by]) # type: ignore

    __table_args__ = (
        Index('idx_teaching_materials_course_id', 'course_id'),
        Index('idx_teaching_materials_lesson_id', 'lesson_id'),
        Index('idx_teaching_materials_is_deleted', 'is_deleted'),
    )
