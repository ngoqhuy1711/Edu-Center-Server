from datetime import datetime, UTC
from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship, func

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.lesson import Lesson
    from app.models.user import User


class TeachingMaterial(SQLModel, table=True):
    __tablename__ = "teaching_materials"
    material_id: Optional[int] = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.course_id", nullable=False)
    lesson_id: Optional[int] = Field(foreign_key="lessons.lesson_id", nullable=True)
    title: str = Field(max_length=255, nullable=False)
    description: Optional[str] = Field(default=None)
    material_type: str = Field(max_length=50, nullable=False)
    url: Optional[str] = Field(default=None, max_length=512)
    file_path: Optional[str] = Field(default=None, max_length=512)
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
    created_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    updated_by: Optional[int] = Field(default=None, foreign_key="users.user_id")
    is_deleted: bool = Field(default=False)

    course: "Course" = Relationship(back_populates="teaching_materials",
                                    sa_relationship_kwargs={"foreign_keys": "[TeachingMaterial.course_id]"})
    lesson: Optional["Lesson"] = Relationship(back_populates="teaching_materials",
                                              sa_relationship_kwargs={"foreign_keys": "[TeachingMaterial.lesson_id]"})
    created_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[TeachingMaterial.created_by]"})
    updated_by_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[TeachingMaterial.updated_by]"})

    def __repr__(self) -> str:
        return f"TeachingMaterial(material_id={self.material_id}, course_id={self.course_id}, lesson_id={self.lesson_id}, title={self.title}, material_type={self.material_type})"
