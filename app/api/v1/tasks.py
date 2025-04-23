from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models import models
from app.schemas import schemas
from app.crud import task

router = APIRouter()

@router.post("/", response_model=schemas.Task)
def create_task(
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return task.create_task(db=db, task=task_in, user_id=current_user.id)

@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    project_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if project_id:
        return task.get_tasks_by_project(db=db, project_id=project_id, skip=skip, limit=limit)
    else:
        return db.query(models.Task).options(
            joinedload(models.Task.project),
            joinedload(models.Task.assignee)
        ).offset(skip).limit(limit).all()

@router.get("/{task_id}", response_model=schemas.Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_task = task.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/sprint/{sprint_id}", response_model=List[schemas.Task])
def read_sprint_tasks(
    sprint_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    tasks = db.query(models.Task).filter(models.Task.sprint_id == sprint_id).all()
    return tasks

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(
    task_id: int,
    task_in: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_task = task.update_task(db=db, task_id=task_id, task=task_in, user_id=current_user.id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if not task.delete_task(db=db, task_id=task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"} 