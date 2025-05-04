import enum

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class UserRoleType(enum.Enum):
    admin = 'admin'
    instructor = 'instructor'
    student = 'student'


class LessonProgressStatus(enum.Enum):
    not_started = 'not_started'
    in_progress = 'in_progress'
    completed = 'completed'


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)

    roles = relationship('UserRole', back_populates='user', cascade='all, delete-orphan')
    profile = relationship('UserProfile', back_populates='user', uselist=False, cascade='all, delete-orphan')
    lesson_progress = relationship('UserLessonProgress', back_populates='user', cascade='all, delete-orphan')
    creator = relationship('User', remote_side=[user_id], foreign_keys=[created_by])  # type: ignore
    updater = relationship('User', remote_side=[user_id], foreign_keys=[updated_by])  # type: ignore

    __table_args__ = (
        Index('idx_users_email', 'email'),
        Index('idx_users_is_deleted', 'is_deleted'),
    )


class UserRole(Base):
    __tablename__ = 'user_roles'
    user_role_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    role = Column(ENUM(UserRoleType, name='user_role_type'), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)

    user = relationship('User', back_populates='roles')
    creator = relationship('User', foreign_keys=[created_by])  # type: ignore
    updater = relationship('User', foreign_keys=[updated_by])  # type: ignore

    __table_args__ = (
        Index('idx_user_roles_user_id', 'user_id'),
        Index('idx_user_roles_is_deleted', 'is_deleted'),
    )


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    user_profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(512), nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)

    user = relationship('User', back_populates='profile')
    creator = relationship('User', foreign_keys=[created_by])  # type: ignore
    updater = relationship('User', foreign_keys=[updated_by])  # type: ignore

    __table_args__ = (
        Index('idx_user_profiles_user_id', 'user_id'),
        Index('idx_user_profiles_is_deleted', 'is_deleted'),
    )


class UserLessonProgress(Base):
    __tablename__ = 'user_lesson_progress'
    user_lesson_progress_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.lesson_id', ondelete='CASCADE'), nullable=False)
    status = Column(ENUM(LessonProgressStatus, name='lesson_progress_status'), nullable=False,
                    default=LessonProgressStatus.not_started)
    last_accessed_at = Column(DateTime(timezone=True), nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)

    user = relationship('User', back_populates='lesson_progress')
    lesson = relationship('Lesson')
    creator = relationship('User', foreign_keys=[created_by])  # type: ignore
    updater = relationship('User', foreign_keys=[updated_by])  # type: ignore

    __table_args__ = (
        Index('idx_user_lesson_progress_user_id', 'user_id'),
        Index('idx_user_lesson_progress_lesson_id', 'lesson_id'),
        Index('idx_user_lesson_progress_is_deleted', 'is_deleted'),
    )
