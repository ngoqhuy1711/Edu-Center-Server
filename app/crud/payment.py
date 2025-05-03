from datetime import datetime
from typing import Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.payment import Payment, PaymentStatus, PaymentMethod, PaymentType
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentList, PaymentInDB


def create_payment(db: Session, payment: PaymentCreate) -> Payment:
    """Create a new payment record in the database"""
    db_payment = Payment(
        user_id=payment.user_id,
        amount=payment.amount,
        currency=payment.currency,
        payment_method=payment.payment_method,
        status=payment.status,
        payment_type=payment.payment_type,
        reference_id=payment.reference_id,
        transaction_reference=payment.transaction_reference,
        description=payment.description,
        tax_amount=payment.tax_amount,
        discount_amount=payment.discount_amount,
        is_tax_exempt=payment.is_tax_exempt,
        billing_address=payment.billing_address,
        billing_city=payment.billing_city,
        billing_state=payment.billing_state,
        billing_country=payment.billing_country,
        billing_postal_code=payment.billing_postal_code,
        payment_date=payment.payment_date,
        invoice_number=payment.invoice_number
    )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
    """Get a payment by its ID"""
    return db.query(Payment).filter(Payment.payment_id == payment_id).first()


def get_payments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = None,
        status: Optional[PaymentStatus] = None,
        payment_type: Optional[PaymentType] = None,
        payment_method: Optional[PaymentMethod] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        sort_by: str = "created_at",
        sort_desc: bool = True
) -> PaymentList:
    """Get multiple payments with optional filtering and pagination"""
    query = db.query(Payment)

    # Apply filters if provided
    if user_id is not None:
        query = query.filter(Payment.user_id == user_id)

    if status is not None:
        query = query.filter(Payment.status == status)

    if payment_type is not None:
        query = query.filter(Payment.payment_type == payment_type)

    if payment_method is not None:
        query = query.filter(Payment.payment_method == payment_method)

    if min_amount is not None:
        query = query.filter(Payment.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Payment.amount <= max_amount)

    if start_date is not None:
        query = query.filter(Payment.created_at >= start_date)

    if end_date is not None:
        query = query.filter(Payment.created_at <= end_date)

    # Get total count before pagination
    total = query.count()

    # Apply sorting
    if sort_by:
        sort_column = getattr(Payment, sort_by, Payment.created_at)
        if sort_desc:
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)

    # Apply pagination
    payment_models = query.offset(skip).limit(limit).all()
    payments = [PaymentInDB.model_validate(payment) for payment in payment_models]

    return PaymentList(
        items=payments,
        total=total,
        page=(skip // limit) + 1 if limit else 1,
        size=limit
    )


def update_payment(db: Session, payment_id: int, payment_update: PaymentUpdate) -> Optional[Payment]:
    """Update a payment record"""
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return None

    # Convert payment_update to dict, filtering out None values
    update_data = payment_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return db_payment


def delete_payment(db: Session, payment_id: int) -> bool:
    """Delete a payment record"""
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return False

    db.delete(db_payment)
    db.commit()
    return True


def get_payment_by_transaction_reference(db: Session, transaction_reference: str) -> Optional[Payment]:
    """Get a payment by its transaction reference"""
    return db.query(Payment).filter(Payment.transaction_reference == transaction_reference).first()


def get_user_payments(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> PaymentList:
    """Get all payments for a specific user with pagination"""
    return get_payments(db, skip=skip, limit=limit, user_id=user_id)


def update_payment_status(db: Session, payment_id: int, status: PaymentStatus) -> Optional[Payment]:
    """Update only the status of a payment"""
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return None

    db_payment.status = status
    if status == PaymentStatus.COMPLETED and not db_payment.payment_date:
        db_payment.payment_date = datetime.now()

    db.commit()
    db.refresh(db_payment)
    return db_payment
