from sqlmodel import Session
from app.crud import *

# Service cho Message

def create_message_service(session: Session, message):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_message(session, message)

# Service cho MessageAttachment có thể làm tương tự. 