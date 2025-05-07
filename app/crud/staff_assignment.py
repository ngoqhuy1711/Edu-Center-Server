from typing import Optional, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.models.staff_assignment import StaffAssignment
from app.schemas.staff_assignment import (
    StaffAssignmentCreate,
    StaffAssignmentUpdate,
)


def get_staff_assignment(
        db: Session, assignment_id: int
) -> Optional[StaffAssignment]:
    return (
        db.query(StaffAssignment)
        .options(
            joinedload(StaffAssignment.staff),
            joinedload(StaffAssignment.course),
            joinedload(StaffAssignment.lesson),
        )
        .filter(
            StaffAssignment.assignment_id == assignment_id,
            StaffAssignment.is_deleted.is_(False),
        )
        .first()
    )


def get_staff_assignments(
        db: Session, skip: int = 0, limit: int = 100
) -> list[Type[StaffAssignment]]:
    return (
        db.query(StaffAssignment)
        .filter(StaffAssignment.is_deleted.is_(False))
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_staff_assignment(
        db: Session, obj_in: StaffAssignmentCreate, created_by: int
) -> StaffAssignment:
    db_obj = StaffAssignment(**obj_in.model_dump(), created_by=created_by)
    try:
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError:
        db.rollback()
        raise


def update_staff_assignment(
        db: Session,
        db_obj: StaffAssignment,
        obj_in: StaffAssignmentUpdate,
        updated_by: int,
) -> StaffAssignment:
    for field, value in obj_in.model_dump(exclude_none=True).items():
        setattr(db_obj, field, value)
    db_obj.updated_by = updated_by
    try:
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_staff_assignment(
        db: Session, db_obj: StaffAssignment, deleted_by: int
) -> StaffAssignment:
    db_obj.is_deleted = True
    db_obj.updated_by = deleted_by
    try:
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except SQLAlchemyError:
        db.rollback()
        raise
