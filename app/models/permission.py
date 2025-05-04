from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from app.core.database import Base


class Permission(Base):
    __tablename__ = 'permissions'

    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'))
    updated_by = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'))
    is_deleted = Column(Boolean, default=False)
