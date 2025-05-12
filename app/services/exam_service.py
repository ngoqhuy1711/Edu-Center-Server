from sqlmodel import Session
from app.crud import *

# Service cho Exam

def create_exam_service(session: Session, exam):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_exam(session, exam)

# Service cho ExamSubmission có thể làm tương tự. 