from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class LessonStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class LessonType(str, Enum):
    TEXT = "text"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"


# Base schemas
class LessonBase(BaseModel):
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    lesson_type: LessonType = LessonType.TEXT
    duration: Optional[int] = None
    sequence_order: int = 0
    is_required: bool = True


class LessonResourceBase(BaseModel):
    title: str
    description: Optional[str] = None
    resource_type: str
    url: Optional[str] = None
    file_path: Optional[str] = None


class UserLessonProgressBase(BaseModel):
    is_completed: bool = False
    progress_percentage: float = 0.0
    last_position: Optional[str] = None
    time_spent: int = 0


# Create schemas
class LessonCreate(LessonBase):
    course_id: int
    status: LessonStatus = LessonStatus.DRAFT


class LessonResourceCreate(LessonResourceBase):
    lesson_id: int


class UserLessonProgressCreate(UserLessonProgressBase):
    user_id: int
    lesson_id: int


# Update schemas
class LessonUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    lesson_type: Optional[LessonType] = None
    status: Optional[LessonStatus] = None
    duration: Optional[int] = None
    sequence_order: Optional[int] = None
    is_required: Optional[bool] = None


class LessonResourceUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    resource_type: Optional[str] = None
    url: Optional[str] = None
    file_path: Optional[str] = None


class UserLessonProgressUpdate(BaseModel):
    is_completed: Optional[bool] = None
    progress_percentage: Optional[float] = None
    last_position: Optional[str] = None
    time_spent: Optional[int] = None
    completed_at: Optional[datetime] = None


# Database schemas
class LessonResourceInDB(LessonResourceBase):
    resource_id: int
    lesson_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLessonProgressInDB(UserLessonProgressBase):
    progress_id: int
    user_id: int
    lesson_id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class LessonInDB(LessonBase):
    lesson_id: int
    course_id: int
    status: LessonStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Response schemas
class LessonResourceResponse(LessonResourceInDB):
    pass


class UserLessonProgressResponse(UserLessonProgressInDB):
    pass


class LessonResponse(LessonInDB):
    resources: Optional[List[LessonResourceResponse]] = []
