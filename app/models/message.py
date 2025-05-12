from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import MessageType, MessageStatus

class Message(SQLModel, table=True):
    __tablename__ = "messages"
    message_id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="user.user_id")
    recipient_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    subject: str = Field(max_length=255)
    content: str
    message_type: MessageType = Field(default=MessageType.direct)
    status: MessageStatus = Field(default=MessageStatus.unread)
    is_read: bool = Field(default=False)
    read_at: Optional[datetime] = None
    course_id: Optional[int] = Field(default=None, foreign_key="course.course_id")
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False) 