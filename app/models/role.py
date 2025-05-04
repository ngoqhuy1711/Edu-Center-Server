from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

from app.core.database import Base


class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))
    is_deleted = Column(Boolean, default=False)

    permissions = relationship('RolePermission', back_populates='role')


class RolePermission(Base):
    __tablename__ = 'role_permissions'
    role_permission_id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.role_id'), nullable=False)
    permission = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_by = Column(Integer, ForeignKey('users.user_id'))
    updated_by = Column(Integer, ForeignKey('users.user_id'))
    is_deleted = Column(Boolean, default=False)

    role = relationship('Role', back_populates='permissions')
