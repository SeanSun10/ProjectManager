from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.crud import activity

router = APIRouter()

@router.post("/", response_model=schemas.Sprint)
def create_sprint(
    sprint: schemas.SprintCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_sprint = models.Sprint(**sprint.dict())
    db.add(db_sprint)
    db.commit()
    db.refresh(db_sprint)
    
    # 创建活动记录
    activity.create_activity(
        db=db,
        user_id=current_user.id,
        activity_type="sprint_created",
        content=f"创建了迭代 \"{db_sprint.name}\""
    )
    
    return db_sprint

@router.get("/", response_model=List[schemas.Sprint])
def read_sprints(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    sprints = db.query(models.Sprint).offset(skip).limit(limit).all()
    return sprints

@router.get("/{sprint_id}", response_model=schemas.Sprint)
def read_sprint(
    sprint_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if db_sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return db_sprint

@router.get("/project/{project_id}", response_model=List[schemas.Sprint])
def read_project_sprints(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    sprints = db.query(models.Sprint).filter(models.Sprint.project_id == project_id).all()
    return sprints

@router.put("/{sprint_id}", response_model=schemas.Sprint)
def update_sprint(
    sprint_id: int,
    sprint: schemas.SprintCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if db_sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    old_name = db_sprint.name
    for key, value in sprint.dict().items():
        setattr(db_sprint, key, value)
    
    db.commit()
    db.refresh(db_sprint)
    
    # 如果迭代名称发生变化，创建活动记录
    if old_name != db_sprint.name:
        activity.create_activity(
            db=db,
            user_id=current_user.id,
            activity_type="sprint_updated",
            content=f"将迭代名称从 \"{old_name}\" 更新为 \"{db_sprint.name}\""
        )
    
    return db_sprint

@router.delete("/{sprint_id}")
def delete_sprint(
    sprint_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_sprint = db.query(models.Sprint).filter(models.Sprint.id == sprint_id).first()
    if db_sprint is None:
        raise HTTPException(status_code=404, detail="Sprint not found")
    
    db.delete(db_sprint)
    db.commit()
    return {"message": "Sprint deleted successfully"} 