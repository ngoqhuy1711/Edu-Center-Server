from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELED = "canceled"


class PaymentMethod(str, Enum):
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    OTHER = "other"


class PaymentType(str, Enum):
    COURSE_PURCHASE = "course_purchase"
    SUBSCRIPTION = "subscription"
    MATERIAL = "material"
    SERVICE = "service"
    OTHER = "other"


# Base Payment Schema
class PaymentBase(BaseModel):
    amount: float
    currency: str = "USD"
    payment_method: PaymentMethod
    payment_type: PaymentType = PaymentType.OTHER
    reference_id: Optional[int] = None
    transaction_reference: Optional[str] = None
    description: Optional[str] = None
    tax_amount: float = 0.0
    discount_amount: float = 0.0
    is_tax_exempt: bool = False
    billing_address: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_country: Optional[str] = None
    billing_postal_code: Optional[str] = None
    invoice_number: Optional[str] = None


# Schema for creating a new payment
class PaymentCreate(PaymentBase):
    user_id: int
    status: PaymentStatus = PaymentStatus.PENDING
    payment_date: Optional[datetime] = None


# Schema for updating an existing payment
class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    status: Optional[PaymentStatus] = None
    payment_type: Optional[PaymentType] = None
    reference_id: Optional[int] = None
    transaction_reference: Optional[str] = None
    description: Optional[str] = None
    tax_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    is_tax_exempt: Optional[bool] = None
    billing_address: Optional[str] = None
    billing_city: Optional[str] = None
    billing_state: Optional[str] = None
    billing_country: Optional[str] = None
    billing_postal_code: Optional[str] = None
    payment_date: Optional[datetime] = None
    invoice_number: Optional[str] = None


# Schema for payment response
class PaymentInDB(PaymentBase):
    payment_id: int
    user_id: int
    status: PaymentStatus
    payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Schema for paginated payment responses
class PaymentList(BaseModel):
    items: List[PaymentInDB]
    total: int
    page: int
    size: int
