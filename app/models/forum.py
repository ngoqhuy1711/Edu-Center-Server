from datetime import datetime, UTC
from enum import Enum

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class TopicType(str, Enum):
    DISCUSSION = "discussion"
    QUESTION = "question"
    ANNOUNCEMENT = "announcement"


class TopicStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    RESOLVED = "resolved"


class PostType(str, Enum):
    QUESTION = "question"
    ANSWER = "answer"
    COMMENT = "comment"


class PostStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    FLAGGED = "flagged"


class ForumTopic(Base):
    __tablename__ = 'forum_topics'

    topic_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.course_id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(SQLAlchemyEnum(TopicType), default=TopicType.DISCUSSION, nullable=False)
    status = Column(SQLAlchemyEnum(TopicStatus), default=TopicStatus.OPEN, nullable=False)
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))
    is_deleted = Column(Boolean, default=False)

    course = relationship("Course")
    posts = relationship("ForumPost", back_populates="topic")
    creator = relationship("User", foreign_keys=[created_by])  # type: ignore


class ForumPost(Base):
    __tablename__ = 'forum_posts'

    post_id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('forum_topics.topic_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    parent_post_id = Column(Integer, ForeignKey('forum_posts.post_id'))
    content = Column(Text, nullable=False)
    type = Column(SQLAlchemyEnum(PostType), default=PostType.COMMENT, nullable=False)
    status = Column(SQLAlchemyEnum(PostStatus), default=PostStatus.APPROVED, nullable=False)
    is_solution = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC))
    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))
    is_deleted = Column(Boolean, default=False)

    topic = relationship("ForumTopic", back_populates="posts")
    user = relationship("User", foreign_keys=[user_id])  # type: ignore
    parent_post = relationship("ForumPost", remote_side="[post_id]", backref="replies")
    likes = relationship("PostLike", back_populates="post")


class PostLike(Base):
    __tablename__ = 'post_likes'

    like_id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('forum_posts.post_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC))
    is_deleted = Column(Boolean, default=False)

    post = relationship("ForumPost", back_populates="likes")
    user = relationship("User", foreign_keys=[user_id])  # type: ignore
