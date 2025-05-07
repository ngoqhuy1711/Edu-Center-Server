from datetime import datetime, UTC
from typing import Optional

from sqlmodel import SQLModel, Field, func


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"
    permission_id: Optional[int] = Field(default=None, foreign_key="users.permission_id")
    permission_name: str = Field(max_length=100, nullable=False)
    permission_code: str = Field(max_length=50, nullable=False)
    module: Optional[str] = Field(max_length=50, nullable=True)
    description: Optional[str] = Field(max_length=255, nullable=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )

    def __repr__(self) -> str:
        return f"Permission(permission_id={self.permission_id}, permission_name={self.permission_name}, permission_code={self.permission_code})"
