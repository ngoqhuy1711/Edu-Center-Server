from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ForumTopicStatus(str, Enum):
    ACTIVE = "active"
    LOCKED = "locked"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class ForumTopicType(str, Enum):
    GENERAL = "general"
    ANNOUNCEMENT = "announcement"
    QUESTION = "question"
    DISCUSSION = "discussion"
    ASSIGNMENT = "assignment"


class ForumTopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    topic_type: ForumTopicType = ForumTopicType.GENERAL
    is_pinned: bool = False


class ForumTopicCreate(ForumTopicBase):
    course_id: int


class ForumTopicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    topic_type: Optional[ForumTopicType] = None
    status: Optional[ForumTopicStatus] = None
    is_pinned: Optional[bool] = None


class ForumTopicInDB(ForumTopicBase):
    topic_id: int
    creator_id: int
    course_id: int
    status: ForumTopicStatus
    view_count: int
    last_activity: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ForumTopicResponse(ForumTopicInDB):
    pass
