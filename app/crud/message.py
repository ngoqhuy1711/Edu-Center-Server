from datetime import datetime
from typing import Optional, Dict, Any, Type

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.models.message import Message, MessageAttachment, MessageStatus, MessageType
from app.schemas.message import MessageCreate, MessageUpdate, MessageAttachmentCreate


def create_message(db: Session, message: MessageCreate, sender_id: int) -> Message:
    """Create a new message with optional attachments"""
    db_message = Message(
        sender_id=sender_id,
        recipient_id=message.recipient_id,
        subject=message.subject,
        content=message.content,
        message_type=message.message_type,
        course_id=message.course_id,
        status=MessageStatus.UNREAD,
        is_read=False
    )
    db.add(db_message)
    db.flush()  # Flush to get the message_id

    # Create attachments if any
    if message.attachments:
        for attachment in message.attachments:
            db_attachment = MessageAttachment(
                message_id=db_message.message_id,
                file_name=attachment.file_name,
                file_path=attachment.file_path,
                file_type=attachment.file_type,
                file_size=attachment.file_size
            )
            db.add(db_attachment)

    db.commit()
    db.refresh(db_message)
    return db_message


def get_message(db: Session, message_id: int) -> Optional[Message]:
    """Get a single message by ID"""
    return db.query(Message).filter(Message.message_id == message_id).first()


def get_messages(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
) -> list[Type[Message]]:
    """Get messages with optional filters"""
    query = db.query(Message)

    if filters:
        if filters.get("sender_id"):
            query = query.filter(Message.sender_id == filters["sender_id"])
        if filters.get("recipient_id"):
            query = query.filter(Message.recipient_id == filters["recipient_id"])
        if filters.get("status"):
            query = query.filter(Message.status == filters["status"])
        if filters.get("message_type"):
            query = query.filter(Message.message_type == filters["message_type"])
        if filters.get("course_id"):
            query = query.filter(Message.course_id == filters["course_id"])
        if "is_read" in filters:
            query = query.filter(Message.is_read == filters["is_read"])

    return query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()


def update_message(db: Session, message_id: int, message_update: MessageUpdate) -> Optional[Message]:
    """Update message properties"""
    db_message = get_message(db, message_id)
    if db_message:
        update_data = message_update.model_dump(exclude_unset=True)

        # If marking as read, set read_at timestamp
        if update_data.get("is_read") and not db_message.is_read:
            update_data["read_at"] = datetime.now()

        for key, value in update_data.items():
            setattr(db_message, key, value)

        db.commit()
        db.refresh(db_message)
    return db_message


def delete_message(db: Session, message_id: int) -> bool:
    """Delete a message (mark as deleted)"""
    db_message = get_message(db, message_id)
    if db_message:
        db_message.status = MessageStatus.DELETED
        db.commit()
        return True
    return False


def permanently_delete_message(db: Session, message_id: int) -> bool:
    """Permanently delete a message from database"""
    db_message = get_message(db, message_id)
    if db_message:
        db.delete(db_message)
        db.commit()
        return True
    return False


def mark_as_read(db: Session, message_id: int) -> Optional[Message]:
    """Mark a message as read"""
    db_message = get_message(db, message_id)
    if db_message and not db_message.is_read:
        db_message.is_read = True
        db_message.status = MessageStatus.READ
        db_message.read_at = datetime.now()
        db.commit()
        db.refresh(db_message)
    return db_message


def get_user_inbox(db: Session, user_id: int, skip: int = 0, limit: int = 100,
                   include_deleted: bool = False) -> list[Type[Message]]:
    """Get messages received by a user"""
    query = db.query(Message).filter(Message.recipient_id == user_id)

    if not include_deleted:
        query = query.filter(Message.status != MessageStatus.DELETED)

    return query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()


def get_user_sent(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Type[Message]]:
    """Get messages sent by a user"""
    return db.query(Message) \
        .filter(Message.sender_id == user_id) \
        .order_by(Message.created_at.desc()) \
        .offset(skip).limit(limit).all()


def get_conversation(db: Session, user1_id: int, user2_id: int,
                     skip: int = 0, limit: int = 100) -> list[Type[Message]]:
    """Get the conversation between two users"""
    return db.query(Message) \
        .filter(
        or_(
            and_(Message.sender_id == user1_id, Message.recipient_id == user2_id),
            and_(Message.sender_id == user2_id, Message.recipient_id == user1_id)
        ),
        Message.status != MessageStatus.DELETED
    ) \
        .order_by(Message.created_at) \
        .offset(skip).limit(limit).all()


def get_course_messages(db: Session, course_id: int, skip: int = 0, limit: int = 100) -> list[Type[Message]]:
    """Get messages related to a specific course"""
    return db.query(Message) \
        .filter(
        Message.course_id == course_id,
        Message.message_type == MessageType.COURSE,
        Message.status != MessageStatus.DELETED
    ) \
        .order_by(Message.created_at.desc()) \
        .offset(skip).limit(limit).all()


def get_unread_count(db: Session, user_id: int) -> int:
    """Get count of unread messages for a user"""
    return db.query(Message) \
        .filter(
        Message.recipient_id == user_id,
        Message.is_read == False,
        Message.status != MessageStatus.DELETED
    ) \
        .count()


# Message Attachment operations
def create_attachment(
        db: Session,
        message_id: int,
        attachment: MessageAttachmentCreate
) -> MessageAttachment:
    """Create a new attachment for a message"""
    db_attachment = MessageAttachment(
        message_id=message_id,
        file_name=attachment.file_name,
        file_path=attachment.file_path,
        file_type=attachment.file_type,
        file_size=attachment.file_size
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def get_attachments(db: Session, message_id: int) -> list[Type[MessageAttachment]]:
    """Get all attachments for a message"""
    return db.query(MessageAttachment) \
        .filter(MessageAttachment.message_id == message_id) \
        .all()
