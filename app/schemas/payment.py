from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.payment import PaymentMethodEnum, PaymentStatusEnum, PaymentTypeEnum


class PaymentBase(BaseModel):
    user_id: int
    amount: float
    currency: str = "USD"
    payment_method: PaymentMethodEnum
    status: PaymentStatusEnum = PaymentStatusEnum.PENDING
    payment_type: PaymentTypeEnum = PaymentTypeEnum.OTHER
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
    payment_date: Optional[datetime] = None
    invoice_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    payment_method: Optional[PaymentMethodEnum] = None
    status: Optional[PaymentStatusEnum] = None
    payment_type: Optional[PaymentTypeEnum] = None
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

    model_config = ConfigDict(from_attributes=True)


class PaymentInDB(PaymentBase):
    payment_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)


class PaymentResponse(PaymentInDB):
    pass
