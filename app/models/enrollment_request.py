import enum

from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class EnrollmentRequestStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class EnrollmentRequest(Base):
    __tablename__ = "enrollment_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(EnrollmentRequestStatus), default=EnrollmentRequestStatus.PENDING, nullable=False)
    message = Column(Text)
    response_message = Column(Text)
    responded_at = Column(DateTime(timezone=True))
    responded_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    created_at = Column(DateTime(timezone=True), default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=func.current_timestamp(), onupdate=func.current_timestamp(),
                        nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    is_deleted = Column(Boolean, default=False)

    # Relationships
    user = relationship("User", foreign_keys="[user_id]")
    course = relationship("Course")
    responder = relationship("User", foreign_keys=[responded_by])  # type: ignore
    created_by_user = relationship("User", foreign_keys=[created_by])  # type: ignore
    updated_by_user = relationship("User", foreign_keys=[updated_by])  # type: ignore

    def __repr__(self):
        return f"<EnrollmentRequest by User {self.user_id} for Course {self.course_id} (Status: {self.status.value})>"
