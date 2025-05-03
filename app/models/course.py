import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class CourseStatus(enum.Enum):
    ACTIVE = "active"
    UPCOMING = "upcoming"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class CourseLevel(enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    level = Column(Enum(CourseLevel), default=CourseLevel.BEGINNER, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    credits = Column(Integer, default=0)
    max_students = Column(Integer, default=30)
    price = Column(Float, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    image_url = Column(String(255), nullable=True)
    syllabus = Column(Text, nullable=True)
    prerequisites = Column(Text, nullable=True)
    location = Column(String(100), nullable=True)
    status = Column(Enum(CourseStatus), default=CourseStatus.UPCOMING, nullable=False)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    teacher = relationship("User", back_populates="taught_courses", foreign_keys=[teacher_id])
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="course", cascade="all, delete-orphan")
    exams = relationship("Exam", back_populates="course", cascade="all, delete-orphan")
    materials = relationship("TeachingMaterial", back_populates="course", cascade="all, delete-orphan")
    forum_topics = relationship("ForumTopic", back_populates="course", cascade="all, delete-orphan")
    payment_items = relationship("PaymentItem", back_populates="course", cascade="all, delete-orphan")
    enrollment_requests = relationship("EnrollmentRequest", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course {self.course_code}: {self.title}>"
