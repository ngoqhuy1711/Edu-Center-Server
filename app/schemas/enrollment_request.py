from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.enrollment_request import EnrollmentRequestStatus


class EnrollmentRequestBase(BaseModel):
    user_id: int
    course_id: int
    status: EnrollmentRequestStatus = EnrollmentRequestStatus.PENDING
    message: Optional[str] = None
    response_message: Optional[str] = None
    responded_at: Optional[datetime] = None
    responded_by: Optional[int] = None


class EnrollmentRequestCreate(EnrollmentRequestBase):
    pass


class EnrollmentRequestUpdate(BaseModel):
    user_id: Optional[int] = None
    course_id: Optional[int] = None
    status: Optional[EnrollmentRequestStatus] = None
    message: Optional[str] = None
    response_message: Optional[str] = None
    responded_at: Optional[datetime] = None
    responded_by: Optional[int] = None
    is_deleted: Optional[bool] = None


class EnrollmentRequestInDB(EnrollmentRequestBase):
    request_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool = False

    model_config = {"from_attributes": True}


class EnrollmentRequestResponse(EnrollmentRequestInDB):
    pass
