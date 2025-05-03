from datetime import datetime
from typing import Optional, Type

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.assignment import Assignment
from app.schemas.assignment import AssignmentCreate, AssignmentUpdate, AssignmentStatus


async def create_assignment(db: Session, assignment: AssignmentCreate, teacher_id: int) -> Assignment:
    """
    Create a new assignment
    """
    db_assignment = Assignment(
        **assignment.model_dump(),
        teacher_id=teacher_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True
    )

    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


async def get_assignment(db: Session, assignment_id: int) -> Optional[Assignment]:
    """
    Get an assignment by ID
    """
    return db.query(Assignment).filter(Assignment.assignment_id == assignment_id).first()


async def get_assignments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        course_id: Optional[int] = None,
        teacher_id: Optional[int] = None,
        status: Optional[AssignmentStatus] = None,
        active_only: bool = True
) -> list[Type[Assignment]]:
    """
    Get assignments with optional filters
    """
    query = db.query(Assignment)

    filters = []
    if course_id is not None:
        filters.append(Assignment.course_id == course_id)

    if teacher_id is not None:
        filters.append(Assignment.teacher_id == teacher_id)

    if status is not None:
        filters.append(Assignment.status == status)

    if active_only:
        filters.append(Assignment.is_active == True)

    if filters:
        query = query.filter(and_(*filters))

    return query.offset(skip).limit(limit).all()


async def get_course_assignments(db: Session, course_id: int) -> list[Type[Assignment]]:
    """
    Get all assignments for a specific course
    """
    return db.query(Assignment).filter(
        Assignment.course_id == course_id,
        Assignment.is_active == True
    ).all()


async def update_assignment(
        db: Session,
        assignment_id: int,
        assignment_data: AssignmentUpdate
) -> Optional[Assignment]:
    """
    Update an assignment
    """
    db_assignment = await get_assignment(db, assignment_id)
    if not db_assignment:
        return None

    update_data = assignment_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_assignment, field, value)

    db_assignment.updated_at = datetime.now()

    db.commit()
    db.refresh(db_assignment)
    return db_assignment


async def delete_assignment(db: Session, assignment_id: int) -> bool:
    """
    Delete an assignment (soft delete by setting is_active to False)
    """
    db_assignment = await get_assignment(db, assignment_id)
    if not db_assignment:
        return False

    db_assignment.is_active = False
    db_assignment.updated_at = datetime.now()

    db.commit()
    return True


async def hard_delete_assignment(db: Session, assignment_id: int) -> bool:
    """
    Hard delete an assignment from database
    """
    db_assignment = await get_assignment(db, assignment_id)
    if not db_assignment:
        return False

    db.delete(db_assignment)
    db.commit()
    return True
