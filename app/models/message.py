from datetime import datetime, UTC
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, func

from app.models.course import Course
from app.models.user import User


class MessageType(str, Enum):
    DIRECT = "direct"
    GROUP = "group"
    ANNOUNCEMENT = "announcement"


class MessageStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    REPLIED = "replied"
    FORWARDED = "forwarded"


class Message(SQLModel, table=True):
    __tablename__ = "messages"
    message_id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="users.user_id", nullable=False)
    recipient_id: Optional[int] = Field(foreign_key="users.user_id", nullable=True)
    subject: str = Field(..., max_length=255)
    content: str = Field(...)
    message_type: MessageType = Field(default=MessageType.DIRECT)
    status: MessageStatus = Field(default=MessageStatus.UNREAD)
    is_read: bool = Field(default=False)
    read_at: Optional[datetime] = Field(
        default=None,
        sa_column_kwargs={
            "nullable": True
        }
    )
    course_id: Optional[int] = Field(foreign_key="courses.course_id", nullable=True)
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

    sender: User = Relationship(back_populates="sent_messages",
                                sa_relationship_kwargs={"foreign_keys": "[Message.sender_id]"})
    recipient: Optional[User] = Relationship(back_populates="received_messages",
                                             sa_relationship_kwargs={"foreign_keys": "[Message.recipient_id]"})
    course: Optional[Course] = Relationship(back_populates="messages",
                                            sa_relationship_kwargs={"foreign_keys": "[Message.course_id]"})
    created_by_user: Optional[User] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Message.created_by]"})
    updated_by_user: Optional[User] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Message.updated_by]"})
    attachments: List["MessageAttachment"] = Relationship(back_populates="message",
                                                        sa_relationship_kwargs={"foreign_keys": "[MessageAttachment.message_id]"})

    def __repr__(self) -> str:
        return f"Message(message_id={self.message_id}, sender_id={self.sender_id}, recipient_id={self.recipient_id}, subject={self.subject})"


class MessageAttachment(SQLModel, table=True):
    __tablename__ = "message_attachments"
    attachment_id: Optional[int] = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="messages.message_id", nullable=False)
    file_name: str = Field(..., max_length=255)
    file_path: str = Field(..., max_length=512)
    file_type: Optional[str] = Field(default=None, max_length=100)
    file_size: Optional[int] = Field(default=None)
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

    message: "Message" = Relationship(back_populates="attachments",
                                      sa_relationship_kwargs={"foreign_keys": "[MessageAttachment.message_id]"})
    created_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[MessageAttachment.created_by]"})
    updated_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[MessageAttachment.updated_by]"})

    def __repr__(self) -> str:
        return f"MessageAttachment(attachment_id={self.attachment_id}, message_id={self.message_id}, file_name={self.file_name})"
