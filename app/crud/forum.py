from sqlmodel import Session, select
from app.models import ForumPost, ForumTopic, PostLike

def create_forum_post(session: Session, post: ForumPost):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def get_forum_post(session: Session, post_id: int):
    return session.get(ForumPost, post_id)

def get_forum_posts(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(ForumPost).offset(skip).limit(limit)).all()

def update_forum_post(session: Session, post_id: int, post_data: dict):
    db_post = session.get(ForumPost, post_id)
    if not db_post:
        return None
    for key, value in post_data.items():
        setattr(db_post, key, value)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

def delete_forum_post(session: Session, post_id: int):
    db_post = session.get(ForumPost, post_id)
    if not db_post:
        return None
    session.delete(db_post)
    session.commit()
    return db_post

# CRUD cho ForumTopic, PostLike có thể làm tương tự. 