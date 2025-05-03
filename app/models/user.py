import enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class UserRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"
    STAFF = "staff"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    profile_picture = Column(String(255), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    taught_courses = relationship("Course", back_populates="teacher", foreign_keys="Course.teacher_id")
    assignments_created = relationship("Assignment", back_populates="teacher", foreign_keys="Assignment.teacher_id")
    assignment_submissions = relationship("AssignmentSubmission", back_populates="student",
                                          foreign_keys="AssignmentSubmission.student_id")
    exams_created = relationship("Exam", back_populates="teacher", foreign_keys="Exam.teacher_id")
    exam_submissions = relationship("ExamSubmission", back_populates="student",
                                    foreign_keys="ExamSubmission.student_id")
    materials_uploaded = relationship("TeachingMaterial", back_populates="teacher",
                                      foreign_keys="TeachingMaterial.teacher_id")
    sent_messages = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    received_messages = relationship("Message", back_populates="receiver", foreign_keys="Message.receiver_id")
    forum_topics = relationship("ForumTopic", back_populates="creator", foreign_keys="ForumTopic.creator_id")
    forum_posts = relationship("ForumPost", back_populates="author", foreign_keys="ForumPost.author_id")
    staff_assignments = relationship("StaffAssignment", back_populates="staff", foreign_keys="StaffAssignment.staff_id")
    enrollment_requests = relationship("EnrollmentRequest", back_populates="user",
                                       foreign_keys="EnrollmentRequest.user_id")
    handled_requests = relationship("EnrollmentRequest", back_populates="assigned_staff",
                                    foreign_keys="EnrollmentRequest.assigned_staff_id")
    payments = relationship("Payment", back_populates="student", foreign_keys="Payment.student_id")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"
