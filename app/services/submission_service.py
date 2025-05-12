from sqlmodel import Session
from app.crud import *

# Service cho Submission

def create_submission_service(session: Session, submission):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_submission(session, submission)

# Service cho SubmissionAttachment có thể làm tương tự. 