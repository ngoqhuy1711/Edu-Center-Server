from typing import Type

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.models.role import Role, RolePermission
from app.schemas.role import RoleCreate, RolePermissionCreate


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Role]]:
    return (
        db.query(Role)
        .filter(Role.is_deleted == False, Role.is_active == True)
        .order_by(Role.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_role(db: Session, role_id: int) -> Type[Role]:
    role = (
        db.query(Role)
        .options(joinedload(Role.permissions))
        .filter(Role.role_id == role_id, Role.is_deleted == False)
        .first()
    )
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


def create_role(db: Session, payload: RoleCreate, user_id: int) -> Role:
    new_role = Role(
        name=payload.name,
        description=payload.description,
        is_active=payload.is_active,
        created_by=user_id,
        updated_by=user_id,
    )
    try:
        with db.begin():
            db.add(new_role)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return new_role


def update_role(db: Session, role_id: int, payload: RoleCreate, user_id: int) -> Type[Role]:
    role = get_role(db, role_id)
    for attr, value in payload.model_dump(exclude_unset=True).items():
        setattr(role, attr, value)
    role.updated_by = user_id
    try:
        with db.begin():
            db.add(role)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return role


def delete_role(db: Session, role_id: int, user_id: int) -> None:
    role = get_role(db, role_id)
    role.is_deleted = True
    role.updated_by = user_id
    try:
        with db.begin():
            db.add(role)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def add_role_permission(db: Session, role_id: int, payload: RolePermissionCreate, user_id: int) -> RolePermission:
    _ = get_role(db, role_id)  # ensure role exists
    perm = RolePermission(
        role_id=role_id,
        permission=payload.permission,
        is_active=payload.is_active,
        created_by=user_id,
        updated_by=user_id,
    )
    try:
        with db.begin():
            db.add(perm)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return perm


def remove_role_permission(db: Session, role_permission_id: int, user_id: int) -> None:
    perm = (
        db.query(RolePermission)
        .filter(RolePermission.role_permission_id == role_permission_id, RolePermission.is_deleted == False)
        .first()
    )
    if not perm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    perm.is_deleted = True
    perm.updated_by = user_id
    try:
        with db.begin():
            db.add(perm)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
