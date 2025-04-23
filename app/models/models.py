from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """
    用户模型
    
    Attributes:
        id: 用户ID
        username: 用户名
        email: 邮箱
        hashed_password: 加密后的密码
        is_active: 是否激活
        is_superuser: 是否为超级用户
        created_at: 创建时间
        updated_at: 更新时间
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    activities = relationship("Activity", back_populates="user")

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    fixed_cost_monthly = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    sprints = relationship("Sprint", back_populates="project")
    members = relationship("ProjectMember", back_populates="project")
    costs = relationship("CostRecord", back_populates="project")
    tasks = relationship("Task", back_populates="project")

class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    velocity = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="sprints")
    tasks = relationship("Task", back_populates="sprint")

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    monthly_salary = Column(Float)
    join_date = Column(DateTime)
    leave_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("ProjectMember", back_populates="member")
    tasks = relationship("Task", back_populates="assignee")

class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    member_id = Column(Integer, ForeignKey("team_members.id"))
    allocation_percentage = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="members")
    member = relationship("TeamMember", back_populates="projects")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    sprint_id = Column(Integer, ForeignKey("sprints.id"))
    title = Column(String)
    description = Column(Text)
    status = Column(String)
    priority = Column(String)
    assignee_id = Column(Integer, ForeignKey("team_members.id"))
    estimated_hours = Column(Float, default=0.0)
    actual_hours = Column(Float, default=0.0)
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="tasks")
    sprint = relationship("Sprint", back_populates="tasks")
    assignee = relationship("TeamMember", back_populates="tasks")

class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    record_date = Column(DateTime)
    cost_type = Column(String)  # fixed/human
    amount = Column(Float)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="costs")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # 活动类型：task_created, task_updated, project_created 等
    content = Column(String)  # 活动内容
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="activities") 