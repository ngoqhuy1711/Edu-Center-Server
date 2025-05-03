from datetime import datetime, UTC
from typing import Optional, Dict, Any

from sqlalchemy import desc, asc
from sqlalchemy.orm import Session

from app.models.exam import Exam, ExamStatus, ExamType
from app.schemas.exam import ExamCreate, ExamUpdate


def create_exam(db: Session, exam: ExamCreate) -> Exam:
    """
    Create a new exam in the database.
    """
    db_exam = Exam(
        title=exam.title,
        description=exam.description,
        instructions=exam.instructions,
        course_id=exam.course_id,
        teacher_id=exam.teacher_id,
        exam_type=exam.exam_type,
        status=exam.status,
        duration=exam.duration,
        max_score=exam.max_score,
        passing_score=exam.passing_score,
        start_date=exam.start_date,
        end_date=exam.end_date,
        questions=exam.questions,
        shuffle_questions=exam.shuffle_questions,
        allow_multiple_attempts=exam.allow_multiple_attempts,
        max_attempts=exam.max_attempts,
        show_answers=exam.show_answers,
        show_score=exam.show_score,
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam


def get_exam(db: Session, exam_id: int) -> Optional[Exam]:
    """
    Get a single exam by ID.
    """
    return db.query(Exam).filter(Exam.exam_id == exam_id).first()


def get_exams(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        course_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        status: Optional[ExamStatus] = None,
        exam_type: Optional[ExamType] = None,
        sort_by: str = "created_at",
        sort_order: str = "desc"
) -> Dict[str, Any]:
    """
    Get multiple exams with filtering and pagination.
    Returns dict with items (list of exams) and total (count of all matching exams).
    """
    query = db.query(Exam)

    # Apply filters
    if course_id is not None:
        query = query.filter(Exam.course_id == course_id)
    if teacher_id is not None:
        query = query.filter(Exam.teacher_id == teacher_id)
    if status is not None:
        query = query.filter(Exam.status == status)
    if exam_type is not None:
        query = query.filter(Exam.exam_type == exam_type)

    # Get total count before pagination
    total = query.count()

    # Apply sorting
    if hasattr(Exam, sort_by):
        order_column = getattr(Exam, sort_by)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(order_column))
        else:
            query = query.order_by(asc(order_column))

    # Apply pagination
    exams = query.offset(skip).limit(limit).all()

    return {
        "items": exams,
        "total": total
    }


def update_exam(db: Session, exam_id: int, exam_update: ExamUpdate) -> Optional[Exam]:
    """
    Update an existing exam.
    """
    db_exam = get_exam(db, exam_id)
    if not db_exam:
        return None

    update_data = exam_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_exam, key, value)

    db_exam.updated_at = datetime.now(tz=UTC)
    db.commit()
    db.refresh(db_exam)
    return db_exam


def delete_exam(db: Session, exam_id: int) -> bool:
    """
    Delete an exam by ID.
    Returns True if the exam was deleted, False if it wasn't found.
    """
    db_exam = get_exam(db, exam_id)
    if not db_exam:
        return False

    db.delete(db_exam)
    db.commit()
    return True


def get_exams_by_course(db: Session, course_id: int, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
    """
    Get all exams for a specific course.
    """
    return get_exams(db, skip=skip, limit=limit, course_id=course_id)


def get_exams_by_teacher(db: Session, teacher_id: int, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
    """
    Get all exams created by a specific teacher.
    """
    return get_exams(db, skip=skip, limit=limit, teacher_id=teacher_id)


def get_active_exams(db: Session, skip: int = 0, limit: int = 100) -> Dict[str, Any]:
    """
    Get all active exams.
    """
    return get_exams(db, skip=skip, limit=limit, status=ExamStatus.ACTIVE)
