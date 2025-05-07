from datetime import datetime, UTC
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship, func

from app.models.course import Course
from app.models.user import User


class ForumPostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class ForumPostType(str, Enum):
    DISCUSSION = "discussion"
    QUESTION = "question"
    ANNOUNCEMENT = "announcement"
    RESOURCES = "resources"


class ForumTopicStatus(str, Enum):
    ACTIVE = "active"
    LOCKED = "locked"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class ForumTopicType(str, Enum):
    GENERAL = "general"
    ANNOUNCEMENTS = "announcements"
    QUESTIONS = "questions"
    DISCUSSIONS = "discussions"
    ASSIGNMENTS = "assignments"


class ForumPost(SQLModel, table=True):
    __tablename__ = "forum_posts"
    post_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(..., max_length=255)
    content: str = Field(...)
    author_id: int = Field(foreign_key="users.user_id", nullable=False)
    course_id: int = Field(foreign_key="courses.course_id", nullable=False)
    parent_post_id: Optional[int] = Field(default=None, foreign_key="forum_posts.post_id")
    post_type: ForumPostType = Field(default=ForumPostType.DISCUSSION)
    status: ForumPostStatus = Field(default=ForumPostStatus.DRAFT)
    is_pinned: bool = Field(default=False)
    view_count: int = Field(default=0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )
    created_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    is_deleted: bool = Field(default=False)

    author: "User" = Relationship(back_populates="forum_posts",
                                            sa_relationship_kwargs={"foreign_keys": "[ForumPost.author_id]"})
    course: "Course" = Relationship(back_populates="forum_posts",
                                              sa_relationship_kwargs={"foreign_keys": "[ForumPost.course_id]"})
    parent_post: Optional["ForumPost"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[ForumPost.parent_post_id]"},
        back_populates="child_posts"
    )
    created_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[ForumPost.created_by]"})
    updated_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[ForumPost.updated_by]"})

    def __repr__(self) -> str:
        return f"ForumPost(post_id={self.post_id}, title={self.title}, author_id={self.author_id}, course_id={self.course_id})"


class ForumTopic(SQLModel, table=True):
    __tablename__ = "forum_topics"
    topic_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(..., max_length=255)
    description: Optional[str] = Field(default=None)
    creator_id: int = Field(foreign_key="users.user_id", nullable=False)
    course_id: int = Field(foreign_key="courses.course_id", nullable=False)
    topic_type: ForumTopicType = Field(default=ForumTopicType.GENERAL)
    status: ForumTopicStatus = Field(default=ForumTopicStatus.ACTIVE)
    is_pinned: bool = Field(default=False)
    view_count: int = Field(default=0)
    last_activity: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )
    created_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    is_deleted: bool = Field(default=False)

    creator: "User" = Relationship(back_populates="forum_topics",
                                             sa_relationship_kwargs={"foreign_keys": "[ForumTopic.creator_id]"})
    course: "Course" = Relationship(back_populates="forum_topics",
                                              sa_relationship_kwargs={"foreign_keys": "[ForumTopic.course_id]"})
    created_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[ForumTopic.created_by]"})
    updated_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[ForumTopic.updated_by]"})

    def __repr__(self) -> str:
        return f"ForumTopic(topic_id={self.topic_id}, title={self.title}, creator_id={self.creator_id}, course_id={self.course_id})"


class PostLike(SQLModel, table=True):
    __tablename__ = "post_likes"
    like_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    post_id: int = Field(foreign_key="forum_posts.post_id", nullable=False)
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )

    post: "ForumPost" = Relationship(back_populates="likes",
                                               sa_relationship_kwargs={"foreign_keys": "[PostLike.post_id]"})
    user: "User" = Relationship(back_populates="post_likes",
                                          sa_relationship_kwargs={"foreign_keys": "[PostLike.user_id]"})

    def __repr__(self) -> str:
        return f"PostLike(like_id={self.like_id}, post_id={self.post_id}, user_id={self.user_id})"
