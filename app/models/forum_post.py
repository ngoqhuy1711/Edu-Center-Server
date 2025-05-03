import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ForumPostStatus(enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class ForumPostType(enum.Enum):
    DISCUSSION = "discussion"
    QUESTION = "question"
    ANNOUNCEMENT = "announcement"
    RESOURCE = "resource"


class ForumPost(Base):
    __tablename__ = "forum_posts"

    post_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    parent_post_id = Column(Integer, ForeignKey("forum_posts.post_id"), nullable=True)

    post_type = Column(Enum(ForumPostType), default=ForumPostType.DISCUSSION, nullable=False)
    status = Column(Enum(ForumPostStatus), default=ForumPostStatus.PUBLISHED, nullable=False)
    is_pinned = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    author = relationship("User", foreign_keys=[author_id], back_populates="forum_posts")
    course = relationship("Course", back_populates="forum_posts")
    replies = relationship("ForumPost", backref="parent_post", remote_side=[post_id], cascade="all, delete-orphan")
    likes = relationship("PostLike", back_populates="post", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ForumPost {self.post_id}: {self.title}>"


class ForumPostLike(Base):
    __tablename__ = "post_likes"

    like_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("forum_posts.post_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)

    # Relationships
    post = relationship("ForumPost", back_populates="likes")
    user = relationship("User", back_populates="post_likes")

    def __repr__(self):
        return f"<PostLike {self.like_id}: Post {self.post_id} by User {self.user_id}>"
