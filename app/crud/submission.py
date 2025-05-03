from datetime import UTC
from typing import Optional, Dict, Any, Type

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.submission import Submission, SubmissionAttachment, SubmissionStatus
from app.schemas.submission import SubmissionCreate, SubmissionUpdate, SubmissionGrade


def create_submission(db: Session, submission: SubmissionCreate) -> Submission:
    """Create a new submission."""
    db_submission = Submission(
        user_id=submission.user_id,
        course_id=submission.course_id,
        lesson_id=submission.lesson_id,
        assignment_id=submission.assignment_id,
        submission_type=submission.submission_type,
        status=submission.status,
        title=submission.title,
        content=submission.content
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission


def get_submission(db: Session, submission_id: int) -> Optional[Submission]:
    """Get a submission by ID."""
    return db.query(Submission).filter(Submission.submission_id == submission_id).first()


def get_submissions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
) -> list[Type[Submission]]:
    """Get multiple submissions with optional filtering."""
    query = db.query(Submission)

    if filters:
        if filters.get("user_id"):
            query = query.filter(Submission.user_id == filters["user_id"])
        if filters.get("course_id"):
            query = query.filter(Submission.course_id == filters["course_id"])
        if filters.get("lesson_id"):
            query = query.filter(Submission.lesson_id == filters["lesson_id"])
        if filters.get("assignment_id"):
            query = query.filter(Submission.assignment_id == filters["assignment_id"])
        if filters.get("status"):
            query = query.filter(Submission.status == filters["status"])
        if filters.get("submission_type"):
            query = query.filter(Submission.submission_type == filters["submission_type"])

    return query.order_by(desc(Submission.submitted_at)).offset(skip).limit(limit).all()


def update_submission(
        db: Session,
        submission_id: int,
        submission_update: SubmissionUpdate
) -> Optional[Submission]:
    """Update a submission."""
    db_submission = get_submission(db, submission_id)
    if db_submission:
        update_data = submission_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_submission, key, value)
        db.commit()
        db.refresh(db_submission)
    return db_submission


def delete_submission(db: Session, submission_id: int) -> bool:
    """Delete a submission."""
    db_submission = get_submission(db, submission_id)
    if db_submission:
        db.delete(db_submission)
        db.commit()
        return True
    return False


def grade_submission(
        db: Session,
        submission_id: int,
        grader_id: int,
        grade_data: SubmissionGrade
) -> Optional[Submission]:
    """Grade a submission."""
    from datetime import datetime

    db_submission = get_submission(db, submission_id)
    if db_submission:
        db_submission.score = grade_data.score
        db_submission.max_score = grade_data.max_score
        db_submission.feedback = grade_data.feedback
        db_submission.status = grade_data.status
        db_submission.graded_by = grader_id
        db_submission.graded_at = datetime.now(tz=UTC)
        db.commit()
        db.refresh(db_submission)
    return db_submission


def get_user_submissions(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[SubmissionStatus] = None
) -> list[Type[Submission]]:
    """Get submissions for a specific user."""
    query = db.query(Submission).filter(Submission.user_id == user_id)
    if status:
        query = query.filter(Submission.status == status)
    return query.order_by(desc(Submission.submitted_at)).offset(skip).limit(limit).all()


def get_course_submissions(
        db: Session,
        course_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[SubmissionStatus] = None
) -> list[Type[Submission]]:
    """Get submissions for a specific course."""
    query = db.query(Submission).filter(Submission.course_id == course_id)
    if status:
        query = query.filter(Submission.status == status)
    return query.order_by(desc(Submission.submitted_at)).offset(skip).limit(limit).all()


# Submission attachment functions

def create_submission_attachment(
        db: Session,
        submission_id: int,
        file_name: str,
        file_path: str,
        file_type: Optional[str] = None,
        file_size: Optional[int] = None
) -> SubmissionAttachment:
    """Create a submission attachment."""
    db_attachment = SubmissionAttachment(
        submission_id=submission_id,
        file_name=file_name,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def get_submission_attachments(
        db: Session,
        submission_id: int
) -> list[Type[SubmissionAttachment]]:
    """Get all attachments for a submission."""
    return db.query(SubmissionAttachment).filter(
        SubmissionAttachment.submission_id == submission_id
    ).all()


def delete_submission_attachment(
        db: Session,
        attachment_id: int
) -> bool:
    """Delete a submission attachment."""
    db_attachment = db.query(SubmissionAttachment).filter(
        SubmissionAttachment.attachment_id == attachment_id
    ).first()

    if db_attachment:
        db.delete(db_attachment)
        db.commit()
        return True
    return False
