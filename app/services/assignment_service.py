from sqlmodel import Session
from app.crud import *

# Service cho Assignment
 
def create_assignment_service(session: Session, assignment):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_assignment(session, assignment) 