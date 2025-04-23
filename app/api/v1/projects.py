from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, case

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.crud import activity

router = APIRouter()

@router.post("/", response_model=schemas.Project)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # 创建活动记录
    activity.create_activity(
        db=db,
        user_id=current_user.id,
        activity_type="project_created",
        content=f"创建了项目 \"{db_project.name}\""
    )
    
    return db_project

@router.get("/", response_model=List[schemas.Project])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=schemas.Project)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=schemas.Project)
def update_project(
    project_id: int,
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    old_name = db_project.name
    for key, value in project.dict().items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    
    # 如果项目名称发生变化，创建活动记录
    if old_name != db_project.name:
        activity.create_activity(
            db=db,
            user_id=current_user.id,
            activity_type="project_updated",
            content=f"将项目名称从 \"{old_name}\" 更新为 \"{db_project.name}\""
        )
    
    return db_project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}

@router.get("/{project_id}/stats")
def get_project_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # 检查项目是否存在
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 获取任务统计
    task_stats = db.query(
        func.count(models.Task.id).label('total'),
        func.sum(case((models.Task.status == 'in_progress', 1), else_=0)).label('in_progress'),
        func.sum(case((models.Task.status == 'completed', 1), else_=0)).label('completed')
    ).filter(models.Task.project_id == project_id).first()
    
    # 获取工时统计
    time_stats = db.query(
        func.sum(models.Task.estimated_hours).label('estimated'),
        func.sum(models.Task.actual_hours).label('actual')
    ).filter(models.Task.project_id == project_id).first()
    
    # 获取成本统计
    cost_stats = db.query(
        func.sum(case((models.CostRecord.cost_type == 'fixed', models.CostRecord.amount), else_=0)).label('fixed'),
        func.sum(case((models.CostRecord.cost_type == 'human', models.CostRecord.amount), else_=0)).label('human')
    ).filter(models.CostRecord.project_id == project_id).first()
    
    return {
        "taskStats": {
            "total": task_stats.total or 0,
            "inProgress": task_stats.in_progress or 0,
            "completed": task_stats.completed or 0
        },
        "timeStats": {
            "estimated": time_stats.estimated or 0,
            "actual": time_stats.actual or 0
        },
        "costStats": {
            "fixed": cost_stats.fixed or 0,
            "human": cost_stats.human or 0
        }
    }

@router.get("/{project_id}/activities", response_model=List[schemas.Activity])
def get_project_activities(
    project_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # 检查项目是否存在
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 获取与项目相关的活动
    # 这里我们假设活动内容中包含项目ID或项目名称
    activities = db.query(models.Activity)\
        .filter(models.Activity.content.like(f"%{db_project.name}%"))\
        .order_by(desc(models.Activity.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return activities 