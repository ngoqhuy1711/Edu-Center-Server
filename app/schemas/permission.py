from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool = False

    model_config = ConfigDict(from_attributes=True)


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    permission_id: int
    created_at: datetime
    updated_at: datetime
