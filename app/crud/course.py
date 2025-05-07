from typing import Optional, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


def get_course(db: Session, course_id: int) -> Optional[Course]:
    return (
        db.query(Course)
        .filter(Course.course_id == course_id, Course.is_deleted.is_(False))
        .first()
    )


def get_courses(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Course]]:
    return (
        db.query(Course)
        .filter(Course.is_deleted.is_(False))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_course(db: Session, course_in: CourseCreate, current_user_id: int) -> Course:
    new_course = Course(**course_in.model_dump(), created_by=current_user_id, updated_by=current_user_id)
    try:
        with db.begin():
            db.add(new_course)
        db.refresh(new_course)
        return new_course
    except SQLAlchemyError:
        db.rollback()
        raise


def update_course(db: Session, course_id: int, course_in: CourseUpdate, current_user_id: int) -> Optional[Course]:
    course = get_course(db, course_id)
    if not course:
        return None
    for field, value in course_in.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    course.updated_by = current_user_id
    try:
        with db.begin():
            db.add(course)
        db.refresh(course)
        return course
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_course(db: Session, course_id: int, current_user_id: int) -> bool:
    course = get_course(db, course_id)
    if not course:
        return False
    course.is_deleted = True
    course.updated_by = current_user_id
    try:
        with db.begin():
            db.add(course)
        return True
    except SQLAlchemyError:
        db.rollback()
        raise
