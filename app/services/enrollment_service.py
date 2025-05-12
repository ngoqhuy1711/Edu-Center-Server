from sqlmodel import Session
from app.crud import *

# Service cho EnrollmentRequest

def create_enrollment_request_service(session: Session, request):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_enrollment_request(session, request) 