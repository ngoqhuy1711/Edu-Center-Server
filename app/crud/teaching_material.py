from sqlmodel import Session, select
from app.models import TeachingMaterial

def create_teaching_material(session: Session, material: TeachingMaterial):
    session.add(material)
    session.commit()
    session.refresh(material)
    return material

def get_teaching_material(session: Session, material_id: int):
    return session.get(TeachingMaterial, material_id)

def get_teaching_materials(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(TeachingMaterial).offset(skip).limit(limit)).all()

def update_teaching_material(session: Session, material_id: int, material_data: dict):
    db_material = session.get(TeachingMaterial, material_id)
    if not db_material:
        return None
    for key, value in material_data.items():
        setattr(db_material, key, value)
    session.add(db_material)
    session.commit()
    session.refresh(db_material)
    return db_material

def delete_teaching_material(session: Session, material_id: int):
    db_material = session.get(TeachingMaterial, material_id)
    if not db_material:
        return None
    session.delete(db_material)
    session.commit()
    return db_material 