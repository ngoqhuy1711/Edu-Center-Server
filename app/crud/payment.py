from typing import Optional, Type

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
    return db.query(Payment).filter(Payment.payment_id == payment_id, Payment.is_deleted == False).first()


def list_payments(db: Session, skip: int = 0, limit: int = 100) -> list[Type[Payment]]:
    return db.query(Payment).filter(Payment.is_deleted == False).offset(skip).limit(limit).all()


def create_payment(db: Session, payment_in: PaymentCreate) -> Payment:
    new_payment = Payment(**payment_in.model_dump(exclude_unset=True))
    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        return new_payment
    except SQLAlchemyError:
        db.rollback()
        raise


def update_payment(db: Session, payment_id: int, payment_in: PaymentUpdate) -> Optional[Payment]:
    payment = get_payment(db, payment_id)
    if not payment:
        return None
    for field, value in payment_in.model_dump(exclude_unset=True).items():
        setattr(payment, field, value)
    try:
        db.commit()
        db.refresh(payment)
        return payment
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_payment(db: Session, payment_id: int) -> bool:
    payment = get_payment(db, payment_id)
    if not payment:
        return False
    try:
        payment.is_deleted = True
        db.commit()
        return True
    except SQLAlchemyError:
        db.rollback()
        raise
