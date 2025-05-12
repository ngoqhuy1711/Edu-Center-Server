from sqlmodel import Session, select
from app.models import Lesson

def create_lesson(session: Session, lesson: Lesson):
    session.add(lesson)
    session.commit()
    session.refresh(lesson)
    return lesson

def get_lesson(session: Session, lesson_id: int):
    return session.get(Lesson, lesson_id)

def get_lessons(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Lesson).offset(skip).limit(limit)).all()

def update_lesson(session: Session, lesson_id: int, lesson_data: dict):
    db_lesson = session.get(Lesson, lesson_id)
    if not db_lesson:
        return None
    for key, value in lesson_data.items():
        setattr(db_lesson, key, value)
    session.add(db_lesson)
    session.commit()
    session.refresh(db_lesson)
    return db_lesson

def delete_lesson(session: Session, lesson_id: int):
    db_lesson = session.get(Lesson, lesson_id)
    if not db_lesson:
        return None
    session.delete(db_lesson)
    session.commit()
    return db_lesson 