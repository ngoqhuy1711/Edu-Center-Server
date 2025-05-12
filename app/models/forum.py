from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import ForumPostType, ForumPostStatus, ForumTopicType, ForumTopicStatus

class ForumPost(SQLModel, table=True):
    __tablename__ = "forum_posts"
    post_id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    content: str
    author_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    parent_post_id: Optional[int] = Field(default=None, foreign_key="forum_post.post_id")
    post_type: ForumPostType = Field(default=ForumPostType.discussion)
    status: ForumPostStatus = Field(default=ForumPostStatus.draft)
    is_pinned: bool = Field(default=False)
    view_count: int = Field(default=0)
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False)

class ForumTopic(SQLModel, table=True):
    topic_id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    description: Optional[str] = None
    creator_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    topic_type: ForumTopicType = Field(default=ForumTopicType.general)
    status: ForumTopicStatus = Field(default=ForumTopicStatus.active)
    is_pinned: bool = Field(default=False)
    view_count: int = Field(default=0)
    last_activity: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False) 