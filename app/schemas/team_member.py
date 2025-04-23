from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TeamMemberBase(BaseModel):
    name: str
    role: str
    monthly_salary: float
    join_date: Optional[datetime] = None
    leave_date: Optional[datetime] = None

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMemberUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    monthly_salary: Optional[float] = None
    join_date: Optional[datetime] = None
    leave_date: Optional[datetime] = None

class TeamMember(TeamMemberBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ProjectMemberBase(BaseModel):
    project_id: int
    member_id: int
    allocation_percentage: float
    start_date: datetime
    end_date: Optional[datetime] = None

class ProjectMemberCreate(ProjectMemberBase):
    pass

class ProjectMember(ProjectMemberBase):
    id: int

    class Config:
        orm_mode = True 