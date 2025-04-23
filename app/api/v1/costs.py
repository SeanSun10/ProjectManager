from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import datetime

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.post("/", response_model=schemas.CostRecord)
def create_cost_record(
    cost: schemas.CostRecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_cost = models.CostRecord(**cost.dict())
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost

@router.get("/", response_model=List[schemas.CostRecord])
def read_cost_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    costs = db.query(models.CostRecord).offset(skip).limit(limit).all()
    return costs

@router.get("/{cost_id}", response_model=schemas.CostRecord)
def read_cost_record(
    cost_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_cost = db.query(models.CostRecord).filter(models.CostRecord.id == cost_id).first()
    if db_cost is None:
        raise HTTPException(status_code=404, detail="Cost record not found")
    return db_cost

@router.get("/project/{project_id}", response_model=List[schemas.CostRecord])
def read_project_costs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    costs = db.query(models.CostRecord).filter(models.CostRecord.project_id == project_id).all()
    return costs

@router.get("/project/{project_id}/monthly", response_model=List[schemas.CostRecord])
def read_project_monthly_costs(
    project_id: int,
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    
    costs = db.query(models.CostRecord).filter(
        models.CostRecord.project_id == project_id,
        models.CostRecord.record_date >= start_date,
        models.CostRecord.record_date < end_date
    ).all()
    return costs

@router.put("/{cost_id}", response_model=schemas.CostRecord)
def update_cost_record(
    cost_id: int,
    cost: schemas.CostRecordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_cost = db.query(models.CostRecord).filter(models.CostRecord.id == cost_id).first()
    if db_cost is None:
        raise HTTPException(status_code=404, detail="Cost record not found")
    
    for key, value in cost.dict().items():
        setattr(db_cost, key, value)
    
    db.commit()
    db.refresh(db_cost)
    return db_cost

@router.delete("/{cost_id}")
def delete_cost_record(
    cost_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_cost = db.query(models.CostRecord).filter(models.CostRecord.id == cost_id).first()
    if db_cost is None:
        raise HTTPException(status_code=404, detail="Cost record not found")
    
    db.delete(db_cost)
    db.commit()
    return {"message": "Cost record deleted successfully"}

@router.get("/project/{project_id}/stats")
def read_project_cost_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # 检查项目是否存在
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # 获取成本统计
    cost_stats = db.query(
        func.sum(case((models.CostRecord.cost_type == 'fixed', models.CostRecord.amount), else_=0)).label('fixed'),
        func.sum(case((models.CostRecord.cost_type == 'human', models.CostRecord.amount), else_=0)).label('human'),
        func.sum(case((models.CostRecord.cost_type.notin_(['fixed', 'human']), models.CostRecord.amount), else_=0)).label('other')
    ).filter(models.CostRecord.project_id == project_id).first()
    
    return {
        "fixed": cost_stats.fixed or 0,
        "human": cost_stats.human or 0,
        "other": cost_stats.other or 0
    } 