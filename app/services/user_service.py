from sqlmodel import Session
from app.crud import *

# Service cho User

def create_user_service(session: Session, user):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_user(session, user)

# Service cho các model khác (Role, UserRole, UserProfile) có thể làm tương tự. 