from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class MessageStatus(str, Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"
    DELETED = "deleted"


class MessageType(str, Enum):
    DIRECT = "direct"
    COURSE = "course"
    SYSTEM = "system"
    NOTIFICATION = "notification"


class MessageAttachmentBase(BaseModel):
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None


class MessageAttachmentCreate(MessageAttachmentBase):
    pass


class MessageAttachmentInDB(MessageAttachmentBase):
    attachment_id: int
    message_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    subject: Optional[str] = None
    content: str
    message_type: MessageType = MessageType.DIRECT


class MessageCreate(MessageBase):
    recipient_id: int
    course_id: Optional[int] = None
    attachments: Optional[List[MessageAttachmentCreate]] = None


class MessageUpdate(BaseModel):
    subject: Optional[str] = None
    content: Optional[str] = None
    status: Optional[MessageStatus] = None
    is_read: Optional[bool] = None


class MessageInDB(MessageBase):
    message_id: int
    sender_id: int
    recipient_id: int
    status: MessageStatus
    is_read: bool
    read_at: Optional[datetime] = None
    course_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class MessageResponse(MessageInDB):
    attachments: Optional[List[MessageAttachmentInDB]] = None
