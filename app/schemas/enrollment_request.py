from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.models.enrollment_request import EnrollmentRequestStatus


class EnrollmentRequestBase(BaseModel):
    """Base schema for enrollment request with common fields"""
    user_id: int
    course_id: int
    request_notes: Optional[str] = None
    additional_requirements: Optional[str] = None


class EnrollmentRequestCreate(EnrollmentRequestBase):
    """Schema for creating a new enrollment request"""
    pass


class EnrollmentRequestUpdate(BaseModel):
    """Schema for updating an enrollment request"""
    assigned_staff_id: Optional[int] = None
    status: Optional[EnrollmentRequestStatus] = None
    response_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None


class EnrollmentRequestInDB(EnrollmentRequestBase):
    """Schema for enrollment request in database"""
    request_id: int
    assigned_staff_id: Optional[int] = None
    status: EnrollmentRequestStatus
    request_date: datetime
    response_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EnrollmentRequestResponse(EnrollmentRequestInDB):
    """Schema for enrollment request response with user and course details"""
    pass


class EnrollmentRequestList(BaseModel):
    """Schema for list of enrollment requests"""
    items: List[EnrollmentRequestResponse]
    total: int
