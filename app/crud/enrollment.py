from sqlmodel import Session, select
from app.models import EnrollmentRequest

def create_enrollment_request(session: Session, request: EnrollmentRequest):
    session.add(request)
    session.commit()
    session.refresh(request)
    return request

def get_enrollment_request(session: Session, request_id: int):
    return session.get(EnrollmentRequest, request_id)

def get_enrollment_requests(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(EnrollmentRequest).offset(skip).limit(limit)).all()

def update_enrollment_request(session: Session, request_id: int, request_data: dict):
    db_request = session.get(EnrollmentRequest, request_id)
    if not db_request:
        return None
    for key, value in request_data.items():
        setattr(db_request, key, value)
    session.add(db_request)
    session.commit()
    session.refresh(db_request)
    return db_request

def delete_enrollment_request(session: Session, request_id: int):
    db_request = session.get(EnrollmentRequest, request_id)
    if not db_request:
        return None
    session.delete(db_request)
    session.commit()
    return db_request 