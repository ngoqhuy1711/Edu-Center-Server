from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.course import CourseStatus, MemberRole, MemberStatus


class CourseBase(BaseModel):
    title: str
    code: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    credit_hours: Optional[int] = None
    status: Optional[CourseStatus] = CourseStatus.DRAFT
    enrollment_limit: Optional[int] = None
    teacher_id: Optional[int] = None
    department_id: Optional[int] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    credit_hours: Optional[int] = None
    status: Optional[CourseStatus] = None
    enrollment_limit: Optional[int] = None
    teacher_id: Optional[int] = None
    department_id: Optional[int] = None
    is_deleted: Optional[bool] = None


class CourseInDB(CourseBase):
    course_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool = False

    model_config = {"from_attributes": True}


class CourseResponse(CourseInDB):
    pass


class CourseMemberBase(BaseModel):
    course_id: int
    user_id: int
    role: MemberRole
    status: MemberStatus
    joined_at: Optional[datetime] = None


class CourseMemberCreate(CourseMemberBase):
    pass


class CourseMemberUpdate(BaseModel):
    course_id: Optional[int] = None
    user_id: Optional[int] = None
    role: Optional[MemberRole] = None
    status: Optional[MemberStatus] = None
    is_deleted: Optional[bool] = None


class CourseMemberInDB(CourseMemberBase):
    member_id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    is_deleted: bool = False

    model_config = {"from_attributes": True}


class CourseMemberResponse(CourseMemberInDB):
    pass
