from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models import models
from app.schemas import team_member as team_member_schema

router = APIRouter()

@router.post("/", response_model=team_member_schema.TeamMember, status_code=status.HTTP_201_CREATED)
def create_team_member(
    team_member: team_member_schema.TeamMemberCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    创建团队成员
    """
    db_team_member = models.TeamMember(
        name=team_member.name,
        role=team_member.role,
        monthly_salary=team_member.monthly_salary,
        join_date=team_member.join_date or datetime.utcnow()
    )
    db.add(db_team_member)
    db.commit()
    db.refresh(db_team_member)
    return db_team_member

@router.get("/", response_model=List[team_member_schema.TeamMember])
def read_team_members(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    获取团队成员列表
    """
    team_members = db.query(models.TeamMember).offset(skip).limit(limit).all()
    return team_members

@router.get("/{team_member_id}", response_model=team_member_schema.TeamMember)
def read_team_member(
    team_member_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    获取团队成员详情
    """
    db_team_member = db.query(models.TeamMember).filter(models.TeamMember.id == team_member_id).first()
    if db_team_member is None:
        raise HTTPException(status_code=404, detail="Team member not found")
    return db_team_member

@router.put("/{team_member_id}", response_model=team_member_schema.TeamMember)
def update_team_member(
    team_member_id: int,
    team_member: team_member_schema.TeamMemberUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    更新团队成员信息
    """
    db_team_member = db.query(models.TeamMember).filter(models.TeamMember.id == team_member_id).first()
    if db_team_member is None:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    for field, value in team_member.dict(exclude_unset=True).items():
        setattr(db_team_member, field, value)
    
    db.commit()
    db.refresh(db_team_member)
    return db_team_member

@router.delete("/{team_member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_team_member(
    team_member_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    删除团队成员
    """
    db_team_member = db.query(models.TeamMember).filter(models.TeamMember.id == team_member_id).first()
    if db_team_member is None:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    db.delete(db_team_member)
    db.commit()
    return None

@router.post("/project-members/", response_model=team_member_schema.ProjectMember)
def create_project_member(
    project_member: team_member_schema.ProjectMemberCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_project_member = models.ProjectMember(**project_member.dict())
    db.add(db_project_member)
    db.commit()
    db.refresh(db_project_member)
    return db_project_member

@router.get("/project-members/{project_id}", response_model=List[team_member_schema.ProjectMember])
def read_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    project_members = db.query(models.ProjectMember).filter(
        models.ProjectMember.project_id == project_id
    ).all()
    return project_members 