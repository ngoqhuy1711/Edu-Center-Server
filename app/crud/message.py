from sqlmodel import Session, select
from app.models import Message, MessageAttachment

def create_message(session: Session, message: Message):
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

def get_message(session: Session, message_id: int):
    return session.get(Message, message_id)

def get_messages(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Message).offset(skip).limit(limit)).all()

def update_message(session: Session, message_id: int, message_data: dict):
    db_message = session.get(Message, message_id)
    if not db_message:
        return None
    for key, value in message_data.items():
        setattr(db_message, key, value)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message

def delete_message(session: Session, message_id: int):
    db_message = session.get(Message, message_id)
    if not db_message:
        return None
    session.delete(db_message)
    session.commit()
    return db_message

# CRUD cho MessageAttachment có thể làm tương tự. 