from typing import Optional, Dict, Any, Type

from sqlalchemy import or_, and_
from sqlalchemy.orm import Session

from app.models.course import Course, CourseStatus
from app.schemas.course import CourseCreate, CourseUpdate


def create_course(db: Session, course: CourseCreate, teacher_id: int) -> Course:
    """
    Create a new course in the database.
    """
    db_course = Course(
        **course.model_dump(),
        teacher_id=teacher_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_course(db: Session, course_id: int) -> Optional[Course]:
    """
    Get a course by ID.
    """
    return db.query(Course).filter(Course.course_id == course_id).first()


def get_courses(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
) -> list[Type[Course]]:
    """
    Get multiple courses with optional filtering.
    """
    query = db.query(Course)

    if filters:
        if "teacher_id" in filters:
            query = query.filter(Course.teacher_id == filters["teacher_id"])
        if "status" in filters:
            query = query.filter(Course.status == filters["status"])
        if "level" in filters:
            query = query.filter(Course.level == filters["level"])
        if "is_published" in filters:
            query = query.filter(Course.is_published.is_(filters["is_published"]))
        if "search" in filters and filters["search"]:
            search_term = f"%{filters['search']}%"
            query = query.filter(
                or_(
                    Course.title.ilike(search_term),
                    Course.description.ilike(search_term)
                )
            )

    return query.offset(skip).limit(limit).all()


def update_course(db: Session, course_id: int, course_update: CourseUpdate) -> Optional[Course]:
    """
    Update a course by ID.
    """
    db_course = get_course(db, course_id)
    if not db_course:
        return None

    update_data = course_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_course, key, value)

    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int) -> bool:
    """
    Delete a course by ID.
    """
    db_course = get_course(db, course_id)
    if not db_course:
        return False

    db.delete(db_course)
    db.commit()
    return True


def get_courses_by_teacher(db: Session, teacher_id: int, skip: int = 0, limit: int = 100) -> list[Type[Course]]:
    """
    Get all courses taught by a specific teacher.
    """
    return db.query(Course).filter(Course.teacher_id == teacher_id).offset(skip).limit(limit).all()


def get_active_courses(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Course]]:
    """
    Get all active courses.
    """
    return db.query(Course).filter(
        and_(
            Course.is_published == True,
            Course.status == CourseStatus.ACTIVE,
        )
    ).offset(skip).limit(limit).all()
