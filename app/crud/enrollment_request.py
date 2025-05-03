from datetime import datetime, UTC
from typing import Optional, Dict, Any, Type

from sqlalchemy.orm import Session

from app.models.enrollment_request import EnrollmentRequest, EnrollmentRequestStatus
from app.schemas.enrollment_request import EnrollmentRequestCreate, EnrollmentRequestUpdate


def create_enrollment_request(db: Session, request: EnrollmentRequestCreate) -> EnrollmentRequest:
    """
    Create a new enrollment request.
    """
    db_request = EnrollmentRequest(
        user_id=request.user_id,
        course_id=request.course_id,
        request_notes=request.request_notes,
        additional_requirements=request.additional_requirements,
        status=EnrollmentRequestStatus.PENDING
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_enrollment_request(db: Session, request_id: int) -> Optional[EnrollmentRequest]:
    """
    Get a single enrollment request by ID.
    """
    return db.query(EnrollmentRequest).filter(EnrollmentRequest.request_id == request_id).first()


def get_enrollment_requests(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
) -> list[Type[EnrollmentRequest]]:
    """
    Get multiple enrollment requests with filtering options.
    """
    query = db.query(EnrollmentRequest)

    if filters:
        if user_id := filters.get("user_id"):
            query = query.filter(EnrollmentRequest.user_id == user_id)

        if course_id := filters.get("course_id"):
            query = query.filter(EnrollmentRequest.course_id == course_id)

        if staff_id := filters.get("assigned_staff_id"):
            query = query.filter(EnrollmentRequest.assigned_staff_id == staff_id)

        if status := filters.get("status"):
            query = query.filter(EnrollmentRequest.status == status)

    return query.offset(skip).limit(limit).all()


def count_enrollment_requests(db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
    """
    Count enrollment requests with filtering options.
    """
    query = db.query(EnrollmentRequest)

    if filters:
        if user_id := filters.get("user_id"):
            query = query.filter(EnrollmentRequest.user_id == user_id)

        if course_id := filters.get("course_id"):
            query = query.filter(EnrollmentRequest.course_id == course_id)

        if staff_id := filters.get("assigned_staff_id"):
            query = query.filter(EnrollmentRequest.assigned_staff_id == staff_id)

        if status := filters.get("status"):
            query = query.filter(EnrollmentRequest.status == status)

    return query.count()


def update_enrollment_request(
        db: Session,
        request_id: int,
        request_update: EnrollmentRequestUpdate
) -> Optional[EnrollmentRequest]:
    """
    Update an enrollment request.
    """
    db_request = get_enrollment_request(db, request_id)
    if not db_request:
        return None

    update_data = request_update.model_dump(exclude_unset=True)

    # If status is changing to approved or rejected, set the response date
    if "status" in update_data and (
            update_data["status"] == EnrollmentRequestStatus.APPROVED or
            update_data["status"] == EnrollmentRequestStatus.REJECTED
    ):
        update_data["response_date"] = datetime.now(UTC)

    for key, value in update_data.items():
        setattr(db_request, key, value)

    db.commit()
    db.refresh(db_request)
    return db_request


def delete_enrollment_request(db: Session, request_id: int) -> bool:
    """
    Delete an enrollment request.
    """
    db_request = get_enrollment_request(db, request_id)
    if not db_request:
        return False

    db.delete(db_request)
    db.commit()
    return True
