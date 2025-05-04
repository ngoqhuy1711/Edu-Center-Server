import enum

from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, Boolean, Text, CheckConstraint, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class StaffAssignmentRole(enum.Enum):
    instructor = "instructor"
    assistant = "assistant"
    pending = "pending"


class StaffAssignmentStatus(enum.Enum):
    pending = "pending"
    active = "active"
    inactive = "inactive"


class StaffAssignment(Base):
    __tablename__ = "staff_assignments"
    __table_args__ = (
        CheckConstraint("start_date <= end_date", name="chk_staff_assignment_dates"),
    )

    assignment_id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="SET NULL"))
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id", ondelete="SET NULL"))
    role = Column(Enum(StaffAssignmentRole, name="staff_assignment_role"), nullable=False)
    status = Column(Enum(StaffAssignmentStatus, name="staff_assignment_status"), nullable=False,
                    default=StaffAssignmentStatus.pending)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    description = Column(Text)
    is_primary = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    updated_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))
    is_deleted = Column(Boolean, nullable=False, default=False)

    staff = relationship("User", foreign_keys=[staff_id])  # type: ignore
    creator = relationship("User", foreign_keys=[created_by])  # type: ignore
    updater = relationship("User", foreign_keys=[updated_by])  # type: ignore
    course = relationship("Course", foreign_keys=[course_id])  # type: ignore
    lesson = relationship("Lesson", foreign_keys=[lesson_id])  # type: ignore
