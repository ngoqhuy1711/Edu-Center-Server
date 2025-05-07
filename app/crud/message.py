from typing import Type

from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.models.message import Message, MessageAttachment
from app.schemas.message import MessageCreate, MessageUpdate, MessageAttachmentCreate


def get_message(db: Session, message_id: int, user_id: int) -> Type[Message]:
    query = (
        db.query(Message)
        .options(selectinload(Message.attachments))
        .filter(
            Message.message_id == message_id,
            Message.is_deleted == False,
            or_(Message.sender_id == user_id, Message.recipient_id == user_id),
        )
    )
    message = query.first()
    if not message:
        raise ValueError(f"Message {message_id} not found or access denied")
    return message


def get_messages(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Type[Message]]:
    return (
        db.query(Message)
        .options(selectinload(Message.attachments))
        .filter(
            Message.is_deleted == False,
            or_(Message.sender_id == user_id, Message.recipient_id == user_id),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_message(db: Session, message_in: MessageCreate, user_id: int) -> Message:
    try:
        with db.begin():
            message = Message(
                **message_in.model_dump(exclude_unset=True),
                created_by=user_id,
                updated_by=user_id,
            )
            db.add(message)
        return message
    except SQLAlchemyError:
        db.rollback()
        raise


def update_message(db: Session, message_id: int, message_in: MessageUpdate, user_id: int) -> Type[Message]:
    message = get_message(db, message_id, user_id)
    try:
        with db.begin():
            for field, value in message_in.model_dump(exclude_unset=True).items():
                setattr(message, field, value)
            message.updated_by = user_id
            db.add(message)
        return message
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_message(db: Session, message_id: int, user_id: int) -> None:
    message = get_message(db, message_id, user_id)
    try:
        with db.begin():
            message.is_deleted = True
            message.updated_by = user_id
            db.add(message)
    except SQLAlchemyError:
        db.rollback()
        raise


def create_attachment(db: Session, attachment_in: MessageAttachmentCreate, user_id: int) -> MessageAttachment:
    get_message(db, attachment_in.message_id, user_id)
    try:
        with db.begin():
            attachment = MessageAttachment(
                **attachment_in.model_dump(),
                created_by=user_id,
                updated_by=user_id,
            )
            db.add(attachment)
        return attachment
    except SQLAlchemyError:
        db.rollback()
        raise
