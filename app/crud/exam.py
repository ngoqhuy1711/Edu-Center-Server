from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.exam import Exam, ExamSubmission
from app.schemas.exam import (
    ExamCreate,
    ExamUpdate,
    ExamSubmissionCreate,
    ExamSubmissionUpdate,
)


def get_exams(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Exam]]:
    return (
        db.query(Exam)
        .filter(Exam.is_deleted.is_(False))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_exam(db: Session, exam_id: int) -> Type[Exam]:
    exam = (
        db.query(Exam)
        .filter(Exam.exam_id == exam_id, Exam.is_deleted.is_(False))
        .first()
    )
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return exam


def create_exam(db: Session, data: ExamCreate, user_id: int) -> Exam:
    exam = Exam(**data.model_dump(), created_by=user_id, updated_by=user_id)
    try:
        db.add(exam)
        db.commit()
        db.refresh(exam)
        return exam
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def update_exam(db: Session, exam_id: int, data: ExamUpdate, user_id: int) -> Type[Exam]:
    exam = get_exam(db, exam_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(exam, field, value)
    exam.updated_by = user_id
    try:
        db.commit()
        db.refresh(exam)
        return exam
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_exam(db: Session, exam_id: int, user_id: int) -> None:
    exam = get_exam(db, exam_id)
    exam.is_deleted = True
    exam.updated_by = user_id
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_submissions(db: Session, skip: int = 0, limit: int = 100) -> list[Type[ExamSubmission]]:
    return (
        db.query(ExamSubmission)
        .filter(ExamSubmission.is_deleted.is_(False))
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_submission(db: Session, submission_id: int) -> Type[ExamSubmission]:
    sub = (
        db.query(ExamSubmission)
        .filter(ExamSubmission.submission_id == submission_id, ExamSubmission.is_deleted.is_(False))
        .first()
    )
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found")
    return sub


def create_submission(db: Session, data: ExamSubmissionCreate, user_id: int) -> ExamSubmission:
    sub = ExamSubmission(**data.model_dump(), created_by=user_id, updated_by=user_id)
    try:
        db.add(sub)
        db.commit()
        db.refresh(sub)
        return sub
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def update_submission(db: Session, submission_id: int, data: ExamSubmissionUpdate, user_id: int) -> Type[
    ExamSubmission]:
    sub = get_submission(db, submission_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(sub, field, value)
    sub.updated_by = user_id
    try:
        db.commit()
        db.refresh(sub)
        return sub
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_submission(db: Session, submission_id: int, user_id: int) -> None:
    sub = get_submission(db, submission_id)
    sub.is_deleted = True
    sub.updated_by = user_id
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
