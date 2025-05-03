import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ForumTopicStatus(enum.Enum):
    ACTIVE = "active"
    LOCKED = "locked"
    HIDDEN = "hidden"
    ARCHIVED = "archived"


class ForumTopicType(enum.Enum):
    GENERAL = "general"
    ANNOUNCEMENT = "announcement"
    QUESTION = "question"
    DISCUSSION = "discussion"
    ASSIGNMENT = "assignment"


class ForumTopic(Base):
    __tablename__ = "forum_topics"

    topic_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)

    topic_type = Column(Enum(ForumTopicType), default=ForumTopicType.GENERAL, nullable=False)
    status = Column(Enum(ForumTopicStatus), default=ForumTopicStatus.ACTIVE, nullable=False)
    is_pinned = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    last_activity = Column(DateTime, default=func.current_timestamp())

    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_topics")
    course = relationship("Course", back_populates="forum_topics")
    posts = relationship("ForumPost", back_populates="topic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ForumTopic {self.topic_id}: {self.title}>"
