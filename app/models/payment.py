from datetime import datetime, UTC
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship, func

from app.models.user import User


class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    OTHER = "other"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentType(str, Enum):
    COURSE_FEE = "course_fee"
    SUBSCRIPTION = "subscription"
    DONATION = "donation"
    OTHER = "other"


class Payment(SQLModel, table=True):
    __tablename__ = "payments"
    payment_id: Optional[int] = Field(default=None, foreign_key="users.payment_id")
    user_id: int = Field(foreign_key="users.user_id", nullable=False)
    amount: float = Field(..., ge=0)
    currency: str = Field(default='VND', max_length=3)
    payment_method: PaymentMethod = Field()
    payment_status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    payment_type: PaymentType = Field(default=PaymentType.OTHER)
    reference_id: Optional[int] = Field(default=None)
    transaction_reference: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)
    tax_amount: float = Field(default=0.0, ge=0)
    discount_amount: float = Field(default=0.0, ge=0)
    is_tax_exempt: bool = Field(default=False)
    billing_address: Optional[str] = Field(default=None, max_length=255)
    billing_city: Optional[str] = Field(default=None, max_length=100)
    billing_state: Optional[str] = Field(default=None, max_length=100)
    billing_country: Optional[str] = Field(default=None, max_length=100)
    billing_postal_code: Optional[str] = Field(default=None, max_length=20)
    payment_date: datetime = Field(
        ...,
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    invoice_number: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )
    created_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    is_deleted: bool = Field(default=False)

    user: "User" = Relationship(back_populates="payments",
                                sa_relationship_kwargs={"foreign_keys": "[Payment.user_id]"})
    created_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Payment.created_by]"})
    updated_by_user: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Payment.updated_by]"})

    def __repr__(self) -> str:
        return f"Payment(payment_id={self.payment_id}, user_id={self.user_id}, amount={self.amount}, payment_method={self.payment_method})"
