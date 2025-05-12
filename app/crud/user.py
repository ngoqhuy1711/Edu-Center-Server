from sqlmodel import Session, select
from app.models import User, UserProfile

def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session: Session, user_id: int):
    return session.get(User, user_id)

def get_users(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(User).offset(skip).limit(limit)).all()

def update_user(session: Session, user_id: int, user_data: dict):
    db_user = session.get(User, user_id)
    if not db_user:
        return None
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(session: Session, user_id: int):
    db_user = session.get(User, user_id)
    if not db_user:
        return None
    session.delete(db_user)
    session.commit()
    return db_user

# CRUD cho Role, UserRole, UserProfile có thể làm tương tự như trên. 