from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING, List

from sqlmodel import SQLModel, func, Field, Relationship

# Import for type checking only to prevent circular imports
if TYPE_CHECKING:
    from app.models.user import UserRole


class Role(SQLModel, table=True):
    __tablename__ = "roles"
    role_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    role_name: str = Field(max_length=20, nullable=False)
    description: Optional[str] = Field(max_length=255, nullable=True)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "nullable": False
        }
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={
            "server_default": func.current_timestamp(),
            "onupdate": func.current_timestamp(),
            "nullable": False
        }
    )

    users: List["UserRole"] = Relationship(back_populates="role",
                                           sa_relationship_kwargs={"foreign_keys": "[UserRole.role_id]"})

    def __repr__(self) -> str:
        return f"Role(role_id={self.role_id}, role_name={self.role_name}, description={self.description})"
