from sqlmodel import Session, select
from app.models import Assignment

def create_assignment(session: Session, assignment: Assignment):
    session.add(assignment)
    session.commit()
    session.refresh(assignment)
    return assignment

def get_assignment(session: Session, assignment_id: int):
    return session.get(Assignment, assignment_id)

def get_assignments(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Assignment).offset(skip).limit(limit)).all()

def update_assignment(session: Session, assignment_id: int, assignment_data: dict):
    db_assignment = session.get(Assignment, assignment_id)
    if not db_assignment:
        return None
    for key, value in assignment_data.items():
        setattr(db_assignment, key, value)
    session.add(db_assignment)
    session.commit()
    session.refresh(db_assignment)
    return db_assignment

def delete_assignment(session: Session, assignment_id: int):
    db_assignment = session.get(Assignment, assignment_id)
    if not db_assignment:
        return None
    session.delete(db_assignment)
    session.commit()
    return db_assignment 