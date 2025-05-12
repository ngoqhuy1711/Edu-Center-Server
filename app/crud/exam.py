from sqlmodel import Session, select
from app.models import Exam, ExamSubmission

def create_exam(session: Session, exam: Exam):
    session.add(exam)
    session.commit()
    session.refresh(exam)
    return exam

def get_exam(session: Session, exam_id: int):
    return session.get(Exam, exam_id)

def get_exams(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Exam).offset(skip).limit(limit)).all()

def update_exam(session: Session, exam_id: int, exam_data: dict):
    db_exam = session.get(Exam, exam_id)
    if not db_exam:
        return None
    for key, value in exam_data.items():
        setattr(db_exam, key, value)
    session.add(db_exam)
    session.commit()
    session.refresh(db_exam)
    return db_exam

def delete_exam(session: Session, exam_id: int):
    db_exam = session.get(Exam, exam_id)
    if not db_exam:
        return None
    session.delete(db_exam)
    session.commit()
    return db_exam

# CRUD cho ExamSubmission có thể làm tương tự. 