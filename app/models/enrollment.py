from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC

class EnrollmentRequest(SQLModel, table=True):
    __tablename__ = "enrollment_requests"
    request_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.user_id")
    course_id: int = Field(foreign_key="course.course_id")
    assigned_staff_id: Optional[int] = Field(default=None, foreign_key="user.user_id")
    status: str = Field(default="pending", max_length=20)
    request_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
    response_date: Optional[datetime] = None
    request_notes: Optional[str] = None
    rejection_notes: Optional[str] = None
    additional_requirements: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow) 