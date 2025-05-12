from sqlmodel import Session
from app.crud import *

# Service cho StaffAssignment
 
def create_staff_assignment_service(session: Session, assignment):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_staff_assignment(session, assignment) 