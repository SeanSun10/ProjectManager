from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from pydantic import validator

# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: str
    start_date: datetime
    end_date: datetime
    status: str
    fixed_cost_monthly: float

    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['PLANNING', 'IN_PROGRESS', 'COMPLETED', 'ON_HOLD']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of {allowed_statuses}')
        return v

    @validator('fixed_cost_monthly')
    def validate_fixed_cost(cls, v):
        if v < 0:
            raise ValueError('Fixed cost cannot be negative')
        return v

    @validator('end_date')
    def validate_end_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Sprint schemas
class SprintBase(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    status: str
    velocity: Optional[float] = None

class SprintCreate(SprintBase):
    project_id: int

class Sprint(SprintBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# TeamMember schemas
class TeamMemberBase(BaseModel):
    name: str
    role: str
    monthly_salary: float
    join_date: datetime
    leave_date: Optional[datetime] = None

class TeamMemberCreate(TeamMemberBase):
    pass

class TeamMember(TeamMemberBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ProjectMember schemas
class ProjectMemberBase(BaseModel):
    allocation_percentage: float
    start_date: datetime
    end_date: Optional[datetime] = None

class ProjectMemberCreate(ProjectMemberBase):
    project_id: int
    member_id: int

class ProjectMember(ProjectMemberBase):
    id: int
    project_id: int
    member_id: int

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    project_id: int
    assignee_id: int
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    sprint_id: Optional[int] = None

class ProjectInTask(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class TeamMemberInTask(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class Task(TaskBase):
    id: int
    sprint_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    project: ProjectInTask
    assignee: TeamMemberInTask

    class Config:
        from_attributes = True

# CostRecord schemas
class CostRecordBase(BaseModel):
    record_date: datetime
    cost_type: str
    amount: float
    description: Optional[str] = None

class CostRecordCreate(CostRecordBase):
    project_id: int

class CostRecord(CostRecordBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    """
    用户基础模型
    """
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    """
    用户创建模型
    """
    password: str

class UserUpdate(UserBase):
    """
    用户更新模型
    """
    password: Optional[str] = None

class User(UserBase):
    """
    用户响应模型
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    """
    Token模型
    """
    access_token: str
    token_type: str
    scopes: List[str] = []

class TokenData(BaseModel):
    """
    Token数据模型
    """
    username: Optional[str] = None
    scopes: List[str] = []

class TokenPayload(BaseModel):
    """
    Token载荷模型
    """
    sub: Optional[str] = None
    exp: Optional[int] = None
    scopes: List[str] = []

class Msg(BaseModel):
    """
    消息模型
    """
    msg: str

class UserLogin(BaseModel):
    """
    用户登录模型
    """
    username: str
    password: str

class UserRegister(UserBase):
    """
    用户注册模型
    """
    password: str
    password_confirm: str

    @validator('password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

class UserUpdatePassword(BaseModel):
    """
    用户更新密码模型
    """
    current_password: str
    new_password: str
    new_password_confirm: str

    @validator('new_password_confirm')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('passwords do not match')
        return v

class ActivityBase(BaseModel):
    type: str
    content: str

class ActivityCreate(ActivityBase):
    user_id: int

class Activity(ActivityBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True 