from sqlmodel import Session
from app.crud import *

# Service cho Lesson

def create_lesson_service(session: Session, lesson):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_lesson(session, lesson) 