from sqlmodel import Session
from app.crud import *

# Service cho TeachingMaterial
 
def create_teaching_material_service(session: Session, material):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_teaching_material(session, material) 