import enum

from sqlalchemy import (
    Column, Integer, Float, String, Text, Boolean, DateTime, ForeignKey, Enum
)

from app.core.database import Base


class PaymentMethodEnum(enum.Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    OTHER = "other"


class PaymentStatusEnum(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentTypeEnum(enum.Enum):
    TUITION = "tuition"
    MATERIAL = "material"
    OTHER = "other"


class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    payment_method = Column(Enum(PaymentMethodEnum), nullable=False)
    status = Column(Enum(PaymentStatusEnum), nullable=False, default=PaymentStatusEnum.PENDING)
    payment_type = Column(Enum(PaymentTypeEnum), nullable=False, default=PaymentTypeEnum.OTHER)
    reference_id = Column(Integer)
    transaction_reference = Column(String(255))
    description = Column(Text)
    tax_amount = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, nullable=False, default=0.0)
    is_tax_exempt = Column(Boolean, default=False)
    billing_address = Column(Text)
    billing_city = Column(String(100))
    billing_state = Column(String(100))
    billing_country = Column(String(100))
    billing_postal_code = Column(String(20))
    payment_date = Column(DateTime(timezone=True))
    invoice_number = Column(String(50))
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    is_deleted = Column(Boolean, default=False)
