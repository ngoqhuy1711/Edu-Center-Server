from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.models.teaching_material import TeachingMaterialType


# Base schema for teaching material
class TeachingMaterialBase(BaseModel):
    course_id: int
    lesson_id: Optional[int] = None
    created_by: int
    title: str
    description: Optional[str] = None
    material_type: TeachingMaterialType
    external_url: Optional[str] = None
    display_order: int = 0
    is_public: bool = False
    is_downloadable: bool = True


# Schema for creating a teaching material
class TeachingMaterialCreate(TeachingMaterialBase):
    pass


# Schema for updating a teaching material
class TeachingMaterialUpdate(BaseModel):
    course_id: Optional[int] = None
    lesson_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    material_type: Optional[TeachingMaterialType] = None
    external_url: Optional[str] = None
    display_order: Optional[int] = None
    is_public: Optional[bool] = None
    is_downloadable: Optional[bool] = None


# Base schema for teaching material attachment
class TeachingMaterialAttachmentBase(BaseModel):
    material_id: int
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


# Schema for creating a teaching material attachment
class TeachingMaterialAttachmentCreate(TeachingMaterialAttachmentBase):
    pass


# Schema for updating a teaching material attachment
class TeachingMaterialAttachmentUpdate(BaseModel):
    file_name: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None


# Schema for reading a teaching material attachment
class TeachingMaterialAttachment(TeachingMaterialAttachmentBase):
    attachment_id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Schema for reading a teaching material
class TeachingMaterial(TeachingMaterialBase):
    material_id: int
    created_at: datetime
    updated_at: datetime
    attachments: List[TeachingMaterialAttachment] = []

    class Config:
        orm_mode = True
