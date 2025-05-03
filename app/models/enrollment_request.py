import enum

from sqlalchemy import Column, Integer, Enum, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class EnrollmentRequestStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class EnrollmentRequest(Base):
    __tablename__ = "enrollment_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    assigned_staff_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)

    status = Column(Enum(EnrollmentRequestStatus), default=EnrollmentRequestStatus.PENDING, nullable=False)
    request_date = Column(DateTime, default=func.current_timestamp(), nullable=False)
    response_date = Column(DateTime, nullable=True)
    request_notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    additional_requirements = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship("User", foreign_keys=[user_id], back_populates="enrollment_requests")
    assigned_staff = relationship("User", foreign_keys=[assigned_staff_id], back_populates="handled_requests")
    course = relationship("Course", back_populates="enrollment_requests")

    def __repr__(self):
        return f"<EnrollmentRequest {self.request_id}: {self.status.value}>"
