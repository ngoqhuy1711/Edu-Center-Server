from typing import Optional, Type

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.teaching_material import TeachingMaterial
from app.schemas.teaching_material import TeachingMaterialCreate, TeachingMaterialUpdate


def get_material(db: Session, material_id: int) -> Type[TeachingMaterial]:
    material = db.query(TeachingMaterial).filter(
        TeachingMaterial.material_id == material_id,
        TeachingMaterial.is_deleted.is_(False)
    ).first()
    if not material:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Material not found")
    return material


def get_materials(
        db: Session,
        course_id: Optional[int] = None,
        lesson_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
) -> list[Type[TeachingMaterial]]:
    query = db.query(TeachingMaterial).filter(TeachingMaterial.is_deleted.is_(False))
    if course_id is not None:
        query = query.filter(TeachingMaterial.course_id == course_id)
    if lesson_id is not None:
        query = query.filter(TeachingMaterial.lesson_id == lesson_id)
    return query.offset(skip).limit(limit).all()


def create_material(db: Session, material_in: TeachingMaterialCreate, created_by: int) -> TeachingMaterial:
    new_material = TeachingMaterial(**material_in.model_dump(), created_by=created_by, updated_by=created_by)
    try:
        db.add(new_material)
        db.commit()
        db.refresh(new_material)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create material")
    return new_material


def update_material(db: Session, material_id: int, material_in: TeachingMaterialUpdate,
                    updated_by: int) -> Type[TeachingMaterial]:
    material = get_material(db, material_id)
    update_data = material_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(material, field, value)
    material.updated_by = updated_by
    try:
        db.commit()
        db.refresh(material)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update material")
    return material


def delete_material(db: Session, material_id: int, deleted_by: int) -> None:
    material = get_material(db, material_id)
    material.is_deleted = True
    material.updated_by = deleted_by
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete material")
