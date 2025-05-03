from typing import Optional, Type

from sqlalchemy.orm import Session

from app.models.lesson import Lesson, LessonResource, UserLessonProgress
from app.schemas.lesson import (
    LessonCreate, LessonUpdate,
    LessonResourceCreate, LessonResourceUpdate,
    UserLessonProgressCreate, UserLessonProgressUpdate
)


# Lesson CRUD operations
def create_lesson(db: Session, lesson: LessonCreate) -> Lesson:
    db_lesson = Lesson(
        title=lesson.title,
        content=lesson.content,
        summary=lesson.summary,
        course_id=lesson.course_id,
        lesson_type=lesson.lesson_type,
        status=lesson.status,
        duration=lesson.duration,
        sequence_order=lesson.sequence_order,
        is_required=lesson.is_required
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson


def get_lesson(db: Session, lesson_id: int) -> Optional[Lesson]:
    return db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()


def get_lessons(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        course_id: Optional[int] = None
) -> list[Type[Lesson]]:
    query = db.query(Lesson)
    if course_id is not None:
        query = query.filter(Lesson.course_id == course_id)
    return query.offset(skip).limit(limit).all()


def update_lesson(
        db: Session,
        lesson_id: int,
        lesson_update: LessonUpdate
) -> Optional[Lesson]:
    db_lesson = get_lesson(db, lesson_id)
    if db_lesson:
        update_data = lesson_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_lesson, key, value)
        db.commit()
        db.refresh(db_lesson)
    return db_lesson


def delete_lesson(db: Session, lesson_id: int) -> bool:
    db_lesson = get_lesson(db, lesson_id)
    if db_lesson:
        db.delete(db_lesson)
        db.commit()
        return True
    return False


# LessonResource CRUD operations
def create_lesson_resource(
        db: Session,
        resource: LessonResourceCreate
) -> LessonResource:
    db_resource = LessonResource(
        lesson_id=resource.lesson_id,
        title=resource.title,
        description=resource.description,
        resource_type=resource.resource_type,
        url=resource.url,
        file_path=resource.file_path
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def get_lesson_resource(
        db: Session,
        resource_id: int
) -> Optional[LessonResource]:
    return db.query(LessonResource).filter(
        LessonResource.resource_id == resource_id
    ).first()


def get_lesson_resources(
        db: Session,
        lesson_id: int,
        skip: int = 0,
        limit: int = 100
) -> list[Type[LessonResource]]:
    return db.query(LessonResource).filter(
        LessonResource.lesson_id == lesson_id
    ).offset(skip).limit(limit).all()


def update_lesson_resource(
        db: Session,
        resource_id: int,
        resource_update: LessonResourceUpdate
) -> Optional[LessonResource]:
    db_resource = get_lesson_resource(db, resource_id)
    if db_resource:
        update_data = resource_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_resource, key, value)
        db.commit()
        db.refresh(db_resource)
    return db_resource


def delete_lesson_resource(db: Session, resource_id: int) -> bool:
    db_resource = get_lesson_resource(db, resource_id)
    if db_resource:
        db.delete(db_resource)
        db.commit()
        return True
    return False


# UserLessonProgress CRUD operations
def create_user_lesson_progress(
        db: Session,
        progress: UserLessonProgressCreate
) -> UserLessonProgress:
    db_progress = UserLessonProgress(
        user_id=progress.user_id,
        lesson_id=progress.lesson_id,
        is_completed=progress.is_completed,
        progress_percentage=progress.progress_percentage,
        last_position=progress.last_position,
        time_spent=progress.time_spent
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress


def get_user_lesson_progress(
        db: Session,
        user_id: int,
        lesson_id: int
) -> Optional[UserLessonProgress]:
    return db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == user_id,
        UserLessonProgress.lesson_id == lesson_id
    ).first()


def get_user_progress_by_id(
        db: Session,
        progress_id: int
) -> Optional[UserLessonProgress]:
    return db.query(UserLessonProgress).filter(
        UserLessonProgress.progress_id == progress_id
    ).first()


def get_user_lessons_progress(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100
) -> list[Type[UserLessonProgress]]:
    return db.query(UserLessonProgress).filter(
        UserLessonProgress.user_id == user_id
    ).offset(skip).limit(limit).all()


def update_user_lesson_progress(
        db: Session,
        user_id: int,
        lesson_id: int,
        progress_update: UserLessonProgressUpdate
) -> Optional[UserLessonProgress]:
    db_progress = get_user_lesson_progress(db, user_id, lesson_id)
    if db_progress:
        update_data = progress_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_progress, key, value)
        db.commit()
        db.refresh(db_progress)
    return db_progress
