from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.models.lesson import LessonType, LessonStatus


class TeachingMaterialBase(BaseModel):
    title: str
    description: Optional[str]
    material_type: str
    url: Optional[str]
    file_path: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeachingMaterial(TeachingMaterialBase):
    material_id: int
    course_id: int
    lesson_id: Optional[int]
    created_by: int
    updated_by: Optional[int]
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class LessonBase(BaseModel):
    title: str
    description: Optional[str]
    content: Optional[str]
    lesson_order: Optional[int]
    lesson_type: LessonType
    status: LessonStatus
    estimated_time: Optional[int]
    is_published: bool
    published_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Lesson(LessonBase):
    lesson_id: int
    course_id: int
    module_id: Optional[int]
    created_by: int
    updated_by: Optional[int]
    is_deleted: bool
    teaching_materials: List[TeachingMaterial] = []

    model_config = ConfigDict(from_attributes=True)


class LessonList(BaseModel):
    lessons: List[Lesson]
    total: int

    model_config = ConfigDict(from_attributes=True)
