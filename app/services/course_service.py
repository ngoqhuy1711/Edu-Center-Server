from sqlmodel import Session
from app.crud import *

# Service cho Course

def create_course_service(session: Session, course):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_course(session, course)

# Service cho CourseMember có thể làm tương tự. 