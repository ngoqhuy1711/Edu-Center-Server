import enum

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class CourseMemberRole(enum.Enum):
    STUDENT = "student"
    TEACHING_ASSISTANT = "teaching_assistant"
    GUEST_LECTURER = "guest_lecturer"
    OBSERVER = "observer"


class CourseMember(Base):
    __tablename__ = "course_members"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.course_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    role = Column(Enum(CourseMemberRole), nullable=False)
    is_active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=func.current_timestamp())
    access_level = Column(Integer, default=1, nullable=False)  # 1=basic, 2=intermediate, 3=full
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    course = relationship("Course", back_populates="members")
    user = relationship("User", back_populates="course_memberships")

    def __repr__(self):
        return f"<CourseMember {self.user_id} in course {self.course_id} as {self.role}>"
