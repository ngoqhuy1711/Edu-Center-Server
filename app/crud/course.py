from sqlmodel import Session, select
from app.models import Course, CourseMember

def create_course(session: Session, course: Course):
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

def get_course(session: Session, course_id: int):
    return session.get(Course, course_id)

def get_courses(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Course).offset(skip).limit(limit)).all()

def update_course(session: Session, course_id: int, course_data: dict):
    db_course = session.get(Course, course_id)
    if not db_course:
        return None
    for key, value in course_data.items():
        setattr(db_course, key, value)
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course

def delete_course(session: Session, course_id: int):
    db_course = session.get(Course, course_id)
    if not db_course:
        return None
    session.delete(db_course)
    session.commit()
    return db_course

# CRUD cho CourseMember có thể làm tương tự. 