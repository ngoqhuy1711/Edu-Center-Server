from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class ForumPostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class ForumPostType(str, Enum):
    DISCUSSION = "discussion"
    QUESTION = "question"
    ANNOUNCEMENT = "announcement"
    RESOURCE = "resource"


# Base schemas
class ForumPostBase(BaseModel):
    title: str
    content: str
    course_id: int
    parent_post_id: Optional[int] = None
    post_type: ForumPostType = ForumPostType.DISCUSSION
    is_pinned: bool = False


class ForumPostLikeBase(BaseModel):
    post_id: int
    user_id: int


# Create schemas
class ForumPostCreate(ForumPostBase):
    status: ForumPostStatus = ForumPostStatus.PUBLISHED


class ForumPostLikeCreate(ForumPostLikeBase):
    pass


# Update schemas
class ForumPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    post_type: Optional[ForumPostType] = None
    status: Optional[ForumPostStatus] = None
    is_pinned: Optional[bool] = None


# Response schemas
class ForumPostLike(ForumPostLikeBase):
    like_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ForumPostBrief(BaseModel):
    post_id: int
    title: str
    author_id: int
    created_at: datetime
    post_type: ForumPostType

    class Config:
        orm_mode = True


class ForumPost(ForumPostBase):
    post_id: int
    author_id: int
    status: ForumPostStatus
    view_count: int
    created_at: datetime
    updated_at: datetime
    likes: List[ForumPostLike] = []
    replies: List[ForumPostBrief] = []

    class Config:
        orm_mode = True


# List response schemas
class ForumPostList(BaseModel):
    posts: List[ForumPostBrief]
    total: int

    class Config:
        orm_mode = True
