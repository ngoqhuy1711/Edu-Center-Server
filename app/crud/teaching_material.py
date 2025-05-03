from typing import Optional, Type

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.teaching_material import TeachingMaterial, TeachingMaterialAttachment
from app.schemas.teaching_material import (
    TeachingMaterialCreate,
    TeachingMaterialUpdate,
    TeachingMaterialAttachmentCreate,
    TeachingMaterialAttachmentUpdate
)


# Teaching Material CRUD operations
def create_teaching_material(db: Session, material: TeachingMaterialCreate) -> TeachingMaterial:
    """Create a new teaching material"""
    db_material = TeachingMaterial(
        course_id=material.course_id,
        lesson_id=material.lesson_id,
        created_by=material.created_by,
        title=material.title,
        description=material.description,
        material_type=material.material_type,
        external_url=material.external_url,
        display_order=material.display_order,
        is_public=material.is_public,
        is_downloadable=material.is_downloadable
    )
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material


def get_teaching_material(db: Session, material_id: int) -> Optional[TeachingMaterial]:
    """Get a teaching material by ID"""
    return db.query(TeachingMaterial).filter(TeachingMaterial.material_id == material_id).first()


def get_teaching_materials(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        course_id: Optional[int] = None,
        lesson_id: Optional[int] = None,
        created_by: Optional[int] = None
) -> list[Type[TeachingMaterial]]:
    """Get teaching materials with optional filters"""
    query = db.query(TeachingMaterial)

    if course_id is not None:
        query = query.filter(TeachingMaterial.course_id == course_id)

    if lesson_id is not None:
        query = query.filter(TeachingMaterial.lesson_id == lesson_id)

    if created_by is not None:
        query = query.filter(TeachingMaterial.created_by == created_by)

    return query.order_by(desc(TeachingMaterial.created_at)).offset(skip).limit(limit).all()


def update_teaching_material(
        db: Session,
        material_id: int,
        material_update: TeachingMaterialUpdate
) -> Optional[TeachingMaterial]:
    """Update a teaching material"""
    db_material = get_teaching_material(db, material_id)
    if not db_material:
        return None

    update_data = material_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_material, key, value)

    db.commit()
    db.refresh(db_material)
    return db_material


def delete_teaching_material(db: Session, material_id: int) -> bool:
    """Delete a teaching material"""
    db_material = get_teaching_material(db, material_id)
    if not db_material:
        return False

    db.delete(db_material)
    db.commit()
    return True


# Teaching Material Attachment CRUD operations
def create_material_attachment(
        db: Session,
        attachment: TeachingMaterialAttachmentCreate
) -> TeachingMaterialAttachment:
    """Create a new teaching material attachment"""
    db_attachment = TeachingMaterialAttachment(
        material_id=attachment.material_id,
        file_name=attachment.file_name,
        file_path=attachment.file_path,
        file_type=attachment.file_type,
        file_size=attachment.file_size
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def get_material_attachment(db: Session, attachment_id: int) -> Optional[TeachingMaterialAttachment]:
    """Get a teaching material attachment by ID"""
    return db.query(TeachingMaterialAttachment).filter(
        TeachingMaterialAttachment.attachment_id == attachment_id
    ).first()


def get_material_attachments(db: Session, material_id: int) -> list[Type[TeachingMaterialAttachment]]:
    """Get all attachments for a specific teaching material"""
    return db.query(TeachingMaterialAttachment).filter(
        TeachingMaterialAttachment.material_id == material_id
    ).all()


def update_material_attachment(
        db: Session,
        attachment_id: int,
        attachment_update: TeachingMaterialAttachmentUpdate
) -> Optional[TeachingMaterialAttachment]:
    """Update a teaching material attachment"""
    db_attachment = get_material_attachment(db, attachment_id)
    if not db_attachment:
        return None

    update_data = attachment_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_attachment, key, value)

    db.commit()
    db.refresh(db_attachment)
    return db_attachment


def delete_material_attachment(db: Session, attachment_id: int) -> bool:
    """Delete a teaching material attachment"""
    db_attachment = get_material_attachment(db, attachment_id)
    if not db_attachment:
        return False

    db.delete(db_attachment)
    db.commit()
    return True
