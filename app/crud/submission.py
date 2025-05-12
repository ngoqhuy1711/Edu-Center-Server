from sqlmodel import Session, select
from app.models import Submission, SubmissionAttachment

def create_submission(session: Session, submission: Submission):
    session.add(submission)
    session.commit()
    session.refresh(submission)
    return submission

def get_submission(session: Session, submission_id: int):
    return session.get(Submission, submission_id)

def get_submissions(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Submission).offset(skip).limit(limit)).all()

def update_submission(session: Session, submission_id: int, submission_data: dict):
    db_submission = session.get(Submission, submission_id)
    if not db_submission:
        return None
    for key, value in submission_data.items():
        setattr(db_submission, key, value)
    session.add(db_submission)
    session.commit()
    session.refresh(db_submission)
    return db_submission

def delete_submission(session: Session, submission_id: int):
    db_submission = session.get(Submission, submission_id)
    if not db_submission:
        return None
    session.delete(db_submission)
    session.commit()
    return db_submission

# CRUD cho SubmissionAttachment có thể làm tương tự. 