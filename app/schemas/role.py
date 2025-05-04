from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class RolePermissionBase(BaseModel):
    permission: str
    is_active: bool = True


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionRead(RolePermissionBase):
    role_permission_id: int
    role_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True)


class RoleBase(BaseModel):
    name: str
    description: Optional[str]
    is_active: bool = True


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    role_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    is_deleted: bool = False
    permissions: List[RolePermissionRead] = []

    model_config = ConfigDict(from_attributes=True)
