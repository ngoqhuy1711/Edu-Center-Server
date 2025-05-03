import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELED = "canceled"


class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    OTHER = "other"


class PaymentType(enum.Enum):
    COURSE_PURCHASE = "course_purchase"
    SUBSCRIPTION = "subscription"
    MATERIAL = "material"
    SERVICE = "service"
    OTHER = "other"


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)

    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)

    payment_type = Column(Enum(PaymentType), default=PaymentType.OTHER, nullable=False)
    reference_id = Column(Integer, nullable=True)  # Generic reference to the entity being paid for

    transaction_reference = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    # Financial details
    tax_amount = Column(Float, default=0.0, nullable=False)
    discount_amount = Column(Float, default=0.0, nullable=False)
    is_tax_exempt = Column(Boolean, default=False, nullable=False)

    # Billing information
    billing_address = Column(Text, nullable=True)
    billing_city = Column(String(100), nullable=True)
    billing_state = Column(String(100), nullable=True)
    billing_country = Column(String(100), nullable=True)
    billing_postal_code = Column(String(20), nullable=True)

    payment_date = Column(DateTime, nullable=True)
    invoice_number = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="payments")

    def __repr__(self):
        return f"<Payment {self.payment_id}: {self.amount} {self.currency} by User {self.user_id}>"
