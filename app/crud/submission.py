from typing import Sequence

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app.models.submission import Submission
from app.schemas.submission import SubmissionCreate, SubmissionUpdate


def get_submission(db: Session, submission_id: int) -> Submission | None:
    try:
        stmt = (
            select(Submission)
            .options(selectinload(Submission.attachments))
            .where(Submission.submission_id == submission_id, Submission.is_deleted == False)
        )
        return db.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError:
        db.rollback()
        raise


def get_submissions(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Submission]:
    try:
        stmt = (
            select(Submission)
            .options(selectinload(Submission.attachments))
            .where(Submission.is_deleted == False)
            .offset(skip)
            .limit(limit)
        )
        return db.execute(stmt).scalars().all()
    except SQLAlchemyError:
        db.rollback()
        raise


def create_submission(db: Session, submission_in: SubmissionCreate, created_by: int) -> Submission:
    obj = Submission(**submission_in.model_dump(), created_by=created_by, updated_by=created_by)
    try:
        with db.begin():
            db.add(obj)
        return obj
    except SQLAlchemyError:
        db.rollback()
        raise


def update_submission(db: Session, submission_id: int, submission_in: SubmissionUpdate,
                      updated_by: int) -> Submission | None:
    try:
        with db.begin():
            obj = db.get(Submission, submission_id)
            if not obj or obj.is_deleted:
                return None
            for field, value in submission_in.model_dump(exclude_unset=True).items():
                setattr(obj, field, value)
            obj.updated_by = updated_by
            db.add(obj)
        return obj
    except SQLAlchemyError:
        db.rollback()
        raise


def soft_delete_submission(db: Session, submission_id: int, updated_by: int) -> Submission | None:
    try:
        with db.begin():
            obj = db.get(Submission, submission_id)
            if not obj or obj.is_deleted:
                return None
            obj.is_deleted = True
            obj.updated_by = updated_by
            db.add(obj)
        return obj
    except SQLAlchemyError:
        db.rollback()
        raise
