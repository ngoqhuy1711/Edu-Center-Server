from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.models.forum import TopicType, TopicStatus, PostType, PostStatus


class ForumTopicBase(BaseModel):
    course_id: int
    title: str
    description: Optional[str] = None
    type: TopicType = TopicType.DISCUSSION
    status: TopicStatus = TopicStatus.OPEN
    is_pinned: bool = False
    is_locked: bool = False


class ForumTopicCreate(ForumTopicBase):
    pass


class ForumTopicRead(ForumTopicBase):
    topic_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class ForumPostBase(BaseModel):
    topic_id: int
    user_id: int
    parent_post_id: Optional[int] = None
    content: str
    type: PostType = PostType.COMMENT
    status: PostStatus = PostStatus.APPROVED
    is_solution: bool = False


class ForumPostCreate(ForumPostBase):
    pass


class ForumPostRead(ForumPostBase):
    post_id: int
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool
    replies: List["ForumPostRead"] = []

    model_config = ConfigDict(from_attributes=True)


class PostLikeBase(BaseModel):
    post_id: int
    user_id: int


class PostLikeCreate(PostLikeBase):
    pass


class PostLikeRead(PostLikeBase):
    like_id: int
    created_at: datetime
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)
