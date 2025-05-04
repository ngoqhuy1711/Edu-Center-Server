import enum
from datetime import datetime, UTC

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class MessageType(enum.Enum):
    DIRECT = "direct"
    COURSE = "course"
    SYSTEM = "system"
    ANNOUNCEMENT = "announcement"
    FEEDBACK = "feedback"


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'))
    recipient_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'))
    message_type = Column(Enum(MessageType), nullable=False)
    subject = Column(String(255), nullable=False)
    content = Column(Text)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True))
    course_id = Column(Integer, ForeignKey('courses.course_id', ondelete='SET NULL'))
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False)
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'))
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'))
    is_deleted = Column(Boolean, default=False)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")  # type: ignore
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")  # type: ignore
    course = relationship("Course", back_populates="messages")
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")
    creator = relationship("User", foreign_keys=[created_by])  # type: ignore
    updater = relationship("User", foreign_keys=[updated_by])  # type: ignore


class MessageAttachment(Base):
    __tablename__ = 'message_attachments'

    attachment_id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('messages.message_id', ondelete='CASCADE'), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(100))
    file_size = Column(Integer)
    created_at = Column(DateTime(timezone=True), default=datetime.now(UTC), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now(UTC), onupdate=datetime.now(UTC), nullable=False)
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'))
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'))
    is_deleted = Column(Boolean, default=False)

    message = relationship("Message", back_populates="attachments")
    creator = relationship("User", foreign_keys=[created_by])  # type: ignore
    updater = relationship("User", foreign_keys=[updated_by])  # type: ignore
