from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enrollment_request import EnrollmentRequest
from app.schemas.enrollment_request import EnrollmentRequestCreate, EnrollmentRequestUpdate


def get_enrollment_request(db: Session, request_id: int) -> Type[EnrollmentRequest]:
    enrollment = (
        db.query(EnrollmentRequest)
        .filter(EnrollmentRequest.request_id == request_id, EnrollmentRequest.is_deleted == False)
        .first()
    )
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="EnrollmentRequest not found")
    return enrollment


def get_enrollment_requests(db: Session, skip: int = 0, limit: int = 100) -> list[Type[EnrollmentRequest]]:
    return (
        db.query(EnrollmentRequest)
        .filter(EnrollmentRequest.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_enrollment_request(db: Session, req_in: EnrollmentRequestCreate, user_id: int) -> EnrollmentRequest:
    new_req = EnrollmentRequest(**req_in.model_dump(), created_by=user_id, updated_by=user_id)
    try:
        with db.begin():
            db.add(new_req)
            db.flush()
            db.refresh(new_req)
        return new_req
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create request")


def update_enrollment_request(db: Session, request_id: int, req_in: EnrollmentRequestUpdate,
                              user_id: int) -> Type[EnrollmentRequest]:
    enrollment = get_enrollment_request(db, request_id)
    for field, value in req_in.model_dump(exclude_unset=True).items():
        setattr(enrollment, field, value)
    enrollment.updated_by = user_id
    try:
        with db.begin():
            db.add(enrollment)
            db.flush()
            db.refresh(enrollment)
        return enrollment
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update request")


def delete_enrollment_request(db: Session, request_id: int, user_id: int) -> Type[EnrollmentRequest]:
    enrollment = get_enrollment_request(db, request_id)
    enrollment.is_deleted = True
    enrollment.updated_by = user_id
    try:
        with db.begin():
            db.add(enrollment)
            db.flush()
            db.refresh(enrollment)
        return enrollment
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete request")
