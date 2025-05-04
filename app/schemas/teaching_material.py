from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TeachingMaterialBase(BaseModel):
    course_id: int
    lesson_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    material_type: str
    url: Optional[str] = None
    file_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TeachingMaterialCreate(TeachingMaterialBase):
    pass


class TeachingMaterialUpdate(BaseModel):
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    material_type: Optional[str] = None
    url: Optional[str] = None
    file_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TeachingMaterialOut(TeachingMaterialBase):
    material_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
