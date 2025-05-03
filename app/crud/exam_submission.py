from typing import Optional, Dict, Any, Type

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.exam_submission import ExamSubmission
from app.schemas.exam_submission import ExamSubmissionCreate, ExamSubmissionUpdate


def create_exam_submission(db: Session, submission: ExamSubmissionCreate) -> ExamSubmission:
    """Create a new exam submission."""
    db_submission = ExamSubmission(**submission.model_dump())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def get_exam_submission(db: Session, submission_id: int) -> Optional[ExamSubmission]:
    """Get a specific exam submission by ID."""
    return db.query(ExamSubmission).filter(ExamSubmission.submission_id == submission_id).first()


def get_exam_submissions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
) -> list[Type[ExamSubmission]]:
    """
    Get all exam submissions with optional filtering.

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        filters: Dictionary of filter conditions
    """
    query = db.query(ExamSubmission)

    if filters:
        for field, value in filters.items():
            if hasattr(ExamSubmission, field):
                query = query.filter(getattr(ExamSubmission, field).__eq__(value))

    return query.offset(skip).limit(limit).all()


def get_submissions_count(db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
    """Get count of exam submissions with optional filtering."""
    query = db.query(func.count(ExamSubmission.submission_id))

    if filters:
        for field, value in filters.items():
            if hasattr(ExamSubmission, field):
                query = query.filter(getattr(ExamSubmission, field).__eq__(value))

    return query.scalar()


def get_student_submissions(db: Session, student_id: int, skip: int = 0, limit: int = 100) -> list[
    Type[ExamSubmission]]:
    """Get all exam submissions for a specific student."""
    return db.query(ExamSubmission).filter(
        ExamSubmission.student_id == student_id
    ).offset(skip).limit(limit).all()


def get_exam_all_submissions(db: Session, exam_id: int, skip: int = 0, limit: int = 100) -> list[Type[ExamSubmission]]:
    """Get all student submissions for a specific exam."""
    return db.query(ExamSubmission).filter(
        ExamSubmission.exam_id == exam_id
    ).offset(skip).limit(limit).all()


def update_exam_submission(
        db: Session,
        submission_id: int,
        submission_update: ExamSubmissionUpdate
) -> Optional[ExamSubmission]:
    """Update an existing exam submission."""
    db_submission = get_exam_submission(db, submission_id)

    if db_submission:
        update_data = submission_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_submission, key, value)

        db.commit()
        db.refresh(db_submission)

    return db_submission


def delete_exam_submission(db: Session, submission_id: int) -> bool:
    """Delete an exam submission by ID."""
    db_submission = get_exam_submission(db, submission_id)

    if db_submission:
        db.delete(db_submission)
        db.commit()
        return True

    return False


def submit_exam(db: Session, submission_id: int, answers: str) -> Optional[ExamSubmission]:
    """Submit an exam with answers and change status to "SUBMITTED"."""
    from app.schemas.exam_submission import ExamSubmissionStatus

    db_submission = get_exam_submission(db, submission_id)

    if db_submission:
        db_submission.answers = answers
        db_submission.status = ExamSubmissionStatus.SUBMITTED
        db_submission.is_completed = True
        db_submission.submission_date = func.current_timestamp()

        db.commit()
        db.refresh(db_submission)

    return db_submission


def grade_submission(
        db: Session,
        submission_id: int,
        score: float,
        feedback: Optional[str] = None
) -> Optional[ExamSubmission]:
    """Grade an exam submission with score and optional feedback."""
    from app.schemas.exam_submission import ExamSubmissionStatus

    db_submission = get_exam_submission(db, submission_id)

    if db_submission:
        db_submission.score = score
        db_submission.feedback = feedback
        db_submission.status = ExamSubmissionStatus.GRADED

        db.commit()
        db.refresh(db_submission)

    return db_submission
