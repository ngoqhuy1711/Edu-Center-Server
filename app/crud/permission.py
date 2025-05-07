from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionRead


def get_permission(db: Session, permission_id: int) -> PermissionRead:
    permission = (
        db.query(Permission)
        .filter(Permission.permission_id == permission_id, Permission.is_deleted == False)
        .first()
    )
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return PermissionRead.model_validate(permission)


def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> list[PermissionRead]:
    permissions = (
        db.query(Permission)
        .filter(Permission.is_deleted == False)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [PermissionRead.model_validate(p) for p in permissions]


def create_permission(db: Session, permission_in: PermissionCreate, user_id: int) -> PermissionRead:
    new_perm = Permission(**permission_in.model_dump(), created_by=user_id, updated_by=user_id)
    try:
        db.add(new_perm)
        db.commit()
        db.refresh(new_perm)
        return PermissionRead.model_validate(new_perm)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to create permission")


def update_permission(db: Session, permission_id: int, permission_in: PermissionCreate, user_id: int) -> PermissionRead:
    permission = (
        db.query(Permission)
        .filter(Permission.permission_id == permission_id, Permission.is_deleted == False)
        .first()
    )
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    for field, value in permission_in.model_dump(exclude_unset=True).items():
        setattr(permission, field, value)
    permission.updated_by = user_id
    try:
        db.commit()
        db.refresh(permission)
        return PermissionRead.model_validate(permission)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to update permission")


def delete_permission(db: Session, permission_id: int, user_id: int) -> None:
    permission = (
        db.query(Permission)
        .filter(Permission.permission_id == permission_id, Permission.is_deleted == False)
        .first()
    )
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    permission.is_deleted = True
    permission.updated_by = user_id
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to delete permission")
