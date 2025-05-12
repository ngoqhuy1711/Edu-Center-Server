from sqlmodel import Session, select
from app.models import Payment

def create_payment(session: Session, payment: Payment):
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment

def get_payment(session: Session, payment_id: int):
    return session.get(Payment, payment_id)

def get_payments(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(Payment).offset(skip).limit(limit)).all()

def update_payment(session: Session, payment_id: int, payment_data: dict):
    db_payment = session.get(Payment, payment_id)
    if not db_payment:
        return None
    for key, value in payment_data.items():
        setattr(db_payment, key, value)
    session.add(db_payment)
    session.commit()
    session.refresh(db_payment)
    return db_payment

def delete_payment(session: Session, payment_id: int):
    db_payment = session.get(Payment, payment_id)
    if not db_payment:
        return None
    session.delete(db_payment)
    session.commit()
    return db_payment 