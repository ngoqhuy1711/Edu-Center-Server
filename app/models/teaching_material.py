from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class TeachingMaterial(SQLModel, table=True):
    __tablename__ = "teaching_materials"
    material_id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="course.course_id")
    lesson_id: Optional[int] = Field(default=None, foreign_key="lesson.lesson_id")
    title: str = Field(max_length=255)
    description: Optional[str] = None
    material_type: str = Field(max_length=50)
    url: Optional[str] = Field(default=None, max_length=512)
    file_path: Optional[str] = Field(default=None, max_length=512)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False) 