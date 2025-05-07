from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.schemas.lesson import LessonBase


def get_lesson(db: Session, lesson_id: int) -> Type[Lesson]:
    lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id, Lesson.is_deleted.is_(False)).first()
    if not lesson:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson


def get_lessons(db: Session, skip: int = 0, limit: int = 100) -> tuple[list[Type[Lesson]], int]:
    query = db.query(Lesson).filter(Lesson.is_deleted.is_(False))
    total = query.count()
    lessons = query.offset(skip).limit(limit).all()
    return lessons, total


def create_lesson(db: Session, lesson_in: LessonBase, course_id: int) -> Lesson:
    new_lesson = Lesson(course_id=course_id, **lesson_in.model_dump(exclude_unset=True))
    try:
        with db.begin():
            db.add(new_lesson)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create lesson")
    return new_lesson


def update_lesson(db: Session, lesson_id: int, lesson_in: LessonBase) -> Type[Lesson]:
    lesson = get_lesson(db, lesson_id)
    update_data = lesson_in.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in update_data.items():
        setattr(lesson, field, value)
    try:
        with db.begin():
            db.add(lesson)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update lesson")
    return lesson


def delete_lesson(db: Session, lesson_id: int) -> None:
    lesson = get_lesson(db, lesson_id)
    try:
        with db.begin():
            lesson.is_deleted = True
            db.add(lesson)
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete lesson")
