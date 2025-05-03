import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class MessageStatus(enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"
    DELETED = "deleted"


class MessageType(enum.Enum):
    DIRECT = "direct"
    COURSE = "course"
    SYSTEM = "system"
    NOTIFICATION = "notification"


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    subject = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    message_type = Column(Enum(MessageType), default=MessageType.DIRECT, nullable=False)
    status = Column(Enum(MessageStatus), default=MessageStatus.UNREAD, nullable=False)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)

    # Optional - for course-related messages
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=True)

    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")
    course = relationship("Course", back_populates="messages")
    attachments = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Message {self.message_id}: From {self.sender_id} to {self.recipient_id}>"


class MessageAttachment(Base):
    __tablename__ = "message_attachments"

    attachment_id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.message_id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=True)  # Size in bytes
    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)

    # Relationships
    message = relationship("Message", back_populates="attachments")

    def __repr__(self):
        return f"<MessageAttachment {self.attachment_id}: {self.file_name}>"
