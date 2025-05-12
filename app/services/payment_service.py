from sqlmodel import Session
from app.crud import *

# Service cho Payment
 
def create_payment_service(session: Session, payment):
    # Thêm logic nghiệp vụ, validate, phân quyền ở đây nếu cần
    return create_payment(session, payment) 