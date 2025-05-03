import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class TeachingMaterialType(enum.Enum):
    LECTURE_SLIDES = "lecture_slides"
    VIDEO = "video"
    DOCUMENT = "document"
    ARTICLE = "article"
    EXTERNAL_RESOURCE = "external_resource"
    REFERENCE = "reference"
    WORKSHEET = "worksheet"
    OTHER = "other"


class TeachingMaterial(Base):
    __tablename__ = "teaching_materials"

    material_id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    material_type = Column(Enum(TeachingMaterialType), nullable=False)

    # For external resources
    external_url = Column(String(512), nullable=True)

    # For ordering in the course/lesson
    display_order = Column(Integer, default=0, nullable=False)

    is_public = Column(Boolean, default=False, nullable=False)
    is_downloadable = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    course = relationship("Course", back_populates="teaching_materials")
    lesson = relationship("Lesson", back_populates="teaching_materials")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_materials")
    attachments = relationship("MaterialAttachment", back_populates="material", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TeachingMaterial {self.material_id}: {self.title}>"


class TeachingMaterialAttachment(Base):
    __tablename__ = "material_attachments"

    attachment_id = Column(Integer, primary_key=True, index=True)
    material_id = Column(Integer, ForeignKey("teaching_materials.material_id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)  # Size in bytes
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)

    # Relationships
    material = relationship("TeachingMaterial", back_populates="attachments")

    def __repr__(self):
        return f"<MaterialAttachment {self.attachment_id}: {self.file_name}>"