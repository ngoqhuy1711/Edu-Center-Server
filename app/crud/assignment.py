from typing import Sequence

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.models.assignment import Assignment


def get_assignment(db: Session, assignment_id: int) -> Assignment:
    statement = select(Assignment).where(
        Assignment.assignment_id == assignment_id,
        Assignment.is_deleted == False
    )
    assignment = db.scalars(statement).first()
    if not assignment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return assignment


def get_assignments(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Assignment]:
    statement = (
        select(Assignment)
        .where(Assignment.is_deleted == False)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(statement).all()


def create_assignment(db: Session, assignment: Assignment, current_user) -> Assignment:
    if current_user.user_id != assignment.teacher_id and not getattr(current_user, "is_superuser", False):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    assignment.created_by = current_user.user_id
    assignment.updated_by = current_user.user_id
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def update_assignment(db: Session, assignment_id: int, assignment_data: Assignment, current_user) -> Assignment:
    assignment = get_assignment(db, assignment_id)
    if current_user.user_id != assignment.teacher_id and not getattr(current_user, "is_superuser", False):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    update_data = assignment_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(assignment, key, value)
    assignment.updated_by = current_user.user_id
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def delete_assignment(db: Session, assignment_id: int, current_user) -> Assignment:
    assignment = get_assignment(db, assignment_id)
    if current_user.user_id != assignment.teacher_id and not getattr(current_user, "is_superuser", False):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    assignment.is_deleted = True
    assignment.updated_by = current_user.user_id
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
