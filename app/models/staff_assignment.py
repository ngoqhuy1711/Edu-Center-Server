import enum

from sqlalchemy import Column, Integer, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class StaffAssignmentStatus(enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELED = "canceled"


class StaffAssignmentRole(enum.Enum):
    INSTRUCTOR = "instructor"
    TEACHING_ASSISTANT = "teaching_assistant"
    TUTOR = "tutor"
    GUEST_LECTURER = "guest_lecturer"
    ADMIN = "admin"
    CONTENT_CREATOR = "content_creator"


class StaffAssignment(Base):
    __tablename__ = "staff_assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # The assignment can be to different entities
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.lesson_id"), nullable=True)

    role = Column(Enum(StaffAssignmentRole), nullable=False)
    status = Column(Enum(StaffAssignmentStatus), default=StaffAssignmentStatus.PENDING, nullable=False)

    # Assignment period
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    description = Column(Text, nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=func.current_timestamp(), nullable=False)
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=False)

    # Relationships
    staff = relationship("User", foreign_keys=[staff_id], back_populates="assignments")
    course = relationship("Course", back_populates="staff_assignments")
    lesson = relationship("Lesson", back_populates="staff_assignments")

    def __repr__(self):
        entity = f"Course {self.course_id}" if self.course_id else f"Lesson {self.lesson_id}"
        return f"<StaffAssignment {self.assignment_id}: {self.role.value} to {entity}>"
