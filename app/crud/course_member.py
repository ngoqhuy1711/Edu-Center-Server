from typing import Optional, Type

from sqlalchemy.orm import Session

from app.models.course_member import CourseMember, CourseMemberRole
from app.schemas.course_member import CourseMemberCreate, CourseMemberUpdate


def create_course_member(db: Session, course_member: CourseMemberCreate) -> CourseMember:
    """Create a new course member in the database."""
    db_course_member = CourseMember(
        course_id=course_member.course_id,
        user_id=course_member.user_id,
        role=course_member.role,
        is_active=course_member.is_active,
        access_level=course_member.access_level
    )
    db.add(db_course_member)
    db.commit()
    db.refresh(db_course_member)
    return db_course_member


def get_course_member(db: Session, course_member_id: int) -> Optional[CourseMember]:
    """Get a course member by ID."""
    return db.query(CourseMember).filter(CourseMember.id == course_member_id).first()


def get_course_member_by_course_and_user(db: Session, course_id: int, user_id: int) -> Optional[CourseMember]:
    """Get a course member by course ID and user ID."""
    return db.query(CourseMember).filter(
        CourseMember.course_id == course_id,
        CourseMember.user_id == user_id
    ).first()


def get_course_members(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        course_id: Optional[int] = None,
        user_id: Optional[int] = None,
        role: Optional[CourseMemberRole] = None,
        is_active: Optional[bool] = None
) -> list[Type[CourseMember]]:
    """Get course members with optional filtering."""
    query = db.query(CourseMember)

    if course_id is not None:
        query = query.filter(CourseMember.course_id == course_id)

    if user_id is not None:
        query = query.filter(CourseMember.user_id == user_id)

    if role is not None:
        query = query.filter(CourseMember.role == role)

    if is_active is not None:
        query = query.filter(CourseMember.is_active == is_active)

    return query.offset(skip).limit(limit).all()


def update_course_member(
        db: Session,
        course_member_id: int,
        course_member_update: CourseMemberUpdate
) -> Optional[CourseMember]:
    """Update a course member's information."""
    db_course_member = get_course_member(db, course_member_id)
    if db_course_member is None:
        return None

    update_data = course_member_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course_member, key, value)

    db.commit()
    db.refresh(db_course_member)
    return db_course_member


def delete_course_member(db: Session, course_member_id: int) -> bool:
    """
    Delete a course member by ID.
    Returns True if deleted successfully, False if not found.
    """
    db_course_member = get_course_member(db, course_member_id)
    if db_course_member is None:
        return False

    db.delete(db_course_member)
    db.commit()
    return True


def get_members_by_course(db: Session, course_id: int, skip: int = 0, limit: int = 100) -> list[Type[CourseMember]]:
    """Get all members of a specific course."""
    return db.query(CourseMember).filter(CourseMember.course_id == course_id).offset(skip).limit(limit).all()


def get_courses_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Type[CourseMember]]:
    """Get all courses a user is a member of."""
    return db.query(CourseMember).filter(CourseMember.user_id == user_id).offset(skip).limit(limit).all()
