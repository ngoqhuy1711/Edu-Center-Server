from typing import Optional, Type

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.staff_assignment import StaffAssignment, StaffAssignmentStatus, StaffAssignmentRole
from app.schemas.staff_assignment import StaffAssignmentCreate, StaffAssignmentUpdate


def create_staff_assignment(db: Session, staff_assignment: StaffAssignmentCreate) -> StaffAssignment:
    """Create a new staff assignment."""
    db_staff_assignment = StaffAssignment(
        staff_id=staff_assignment.staff_id,
        course_id=staff_assignment.course_id,
        lesson_id=staff_assignment.lesson_id,
        role=staff_assignment.role,
        status=staff_assignment.status,
        start_date=staff_assignment.start_date,
        end_date=staff_assignment.end_date,
        description=staff_assignment.description,
        is_primary=staff_assignment.is_primary
    )
    db.add(db_staff_assignment)
    db.commit()
    db.refresh(db_staff_assignment)
    return db_staff_assignment


def get_staff_assignment(db: Session, assignment_id: int) -> Optional[StaffAssignment]:
    """Get a staff assignment by ID."""
    return db.query(StaffAssignment).filter(StaffAssignment.assignment_id == assignment_id).first()


def get_staff_assignments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        staff_id: Optional[int] = None,
        course_id: Optional[int] = None,
        lesson_id: Optional[int] = None,
        role: Optional[StaffAssignmentRole] = None,
        status: Optional[StaffAssignmentStatus] = None,
        is_primary: Optional[bool] = None
) -> list[Type[StaffAssignment]]:
    """Get staff assignments with optional filters."""
    query = db.query(StaffAssignment)

    # Apply filters if provided
    if staff_id is not None:
        query = query.filter(StaffAssignment.staff_id == staff_id)
    if course_id is not None:
        query = query.filter(StaffAssignment.course_id == course_id)
    if lesson_id is not None:
        query = query.filter(StaffAssignment.lesson_id == lesson_id)
    if role is not None:
        query = query.filter(StaffAssignment.role == role)
    if status is not None:
        query = query.filter(StaffAssignment.status == status)
    if is_primary is not None:
        query = query.filter(StaffAssignment.is_primary == is_primary)

    return query.offset(skip).limit(limit).all()


def update_staff_assignment(
        db: Session,
        assignment_id: int,
        staff_assignment_update: StaffAssignmentUpdate
) -> Optional[StaffAssignment]:
    """Update a staff assignment."""
    db_staff_assignment = get_staff_assignment(db, assignment_id)
    if not db_staff_assignment:
        return None

    update_data = staff_assignment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_staff_assignment, key, value)

    db.commit()
    db.refresh(db_staff_assignment)
    return db_staff_assignment


def delete_staff_assignment(db: Session, assignment_id: int) -> bool:
    """Delete a staff assignment."""
    db_staff_assignment = get_staff_assignment(db, assignment_id)
    if not db_staff_assignment:
        return False

    db.delete(db_staff_assignment)
    db.commit()
    return True


def get_staff_course_assignments(db: Session, staff_id: int) -> list[Type[StaffAssignment]]:
    """Get all course assignments for a staff member."""
    return db.query(StaffAssignment).filter(
        and_(
            StaffAssignment.staff_id == staff_id,
            StaffAssignment.course_id.isnot(None)
        )
    ).all()


def get_course_staff(db: Session, course_id: int) -> list[Type[StaffAssignment]]:
    """Get all staff assignments for a specific course."""
    return db.query(StaffAssignment).filter(StaffAssignment.course_id == course_id).all()


def get_lesson_staff(db: Session, lesson_id: int) -> list[Type[StaffAssignment]]:
    """Get all staff assignments for a specific lesson."""
    return db.query(StaffAssignment).filter(StaffAssignment.lesson_id == lesson_id).all()
