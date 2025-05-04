from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from app.models.message import MessageType


class MessageBase(BaseModel):
    sender_id: Optional[int]
    recipient_id: Optional[int]
    message_type: MessageType
    subject: str
    content: Optional[str] = None
    is_read: bool = False
    read_at: Optional[datetime] = None
    course_id: Optional[int]

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    subject: Optional[str] = None
    content: Optional[str] = None
    is_read: Optional[bool] = None
    read_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class MessageAttachmentBase(BaseModel):
    message_id: int
    file_name: str
    file_path: str
    file_type: Optional[str] = None
    file_size: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class MessageAttachmentCreate(MessageAttachmentBase):
    pass


class MessageAttachmentInDB(MessageAttachmentBase):
    attachment_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class MessageAttachmentResponse(MessageAttachmentInDB):
    pass


class MessageInDB(MessageBase):
    message_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(MessageInDB):
    attachments: List[MessageAttachmentResponse] = []

    model_config = ConfigDict(from_attributes=True)
