from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC
from app.models.enums import PaymentMethod, PaymentStatus, PaymentType

class Payment(SQLModel, table=True):
    __tablename__ = "payments"
    payment_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    amount: float
    currency: str = Field(default="VND", max_length=3)
    payment_method: PaymentMethod
    payment_status: PaymentStatus = Field(default=PaymentStatus.pending)
    payment_type: PaymentType = Field(default=PaymentType.other)
    reference_id: Optional[int] = None
    transaction_reference: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = Field(default=None, max_length=255)
    tax_amount: float = Field(default=0.0)
    discount_amount: float = Field(default=0.0)
    is_tax_exempt: bool = Field(default=False)
    billing_address: Optional[str] = Field(default=None, max_length=255)
    billing_city: Optional[str] = Field(default=None, max_length=100)
    billing_state: Optional[str] = Field(default=None, max_length=100)
    billing_country: Optional[str] = Field(default=None, max_length=100)
    billing_postal_code: Optional[str] = Field(default=None, max_length=20)
    payment_date: datetime
    invoice_number: Optional[str] = Field(default=None, max_length=50)
    created_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    updated_at: Optional[datetime] = Field(default_factory=datetime.now(UTC))
    created_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="user.user_id")
    is_deleted: bool = Field(default=False) 