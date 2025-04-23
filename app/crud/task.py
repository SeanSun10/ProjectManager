from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models import Task
from app.schemas import TaskCreate
from app.crud import activity

def create_task(db: Session, task: TaskCreate, user_id: int) -> Task:
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        project_id=task.project_id,
        assignee_id=task.assignee_id,
        estimated_hours=task.estimated_hours,
        actual_hours=task.actual_hours,
        due_date=task.due_date,
        sprint_id=task.sprint_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # 创建活动记录
    activity.create_activity(
        db=db,
        user_id=user_id,
        activity_type="task_created",
        content=f"创建了任务 \"{db_task.title}\""
    )
    
    return db_task

def get_task(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).options(
        joinedload(Task.project),
        joinedload(Task.assignee)
    ).filter(Task.id == task_id).first()

def get_tasks_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
    return db.query(Task).options(
        joinedload(Task.project),
        joinedload(Task.assignee)
    ).filter(Task.project_id == project_id).offset(skip).limit(limit).all()

def update_task(db: Session, task_id: int, task: TaskCreate, user_id: int) -> Optional[Task]:
    db_task = get_task(db, task_id)
    if db_task:
        old_status = db_task.status
        for key, value in task.model_dump().items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        
        # 如果任务状态发生变化，创建活动记录
        if old_status != db_task.status:
            activity.create_activity(
                db=db,
                user_id=user_id,
                activity_type="task_updated",
                content=f"将任务 \"{db_task.title}\" 状态更新为 \"{db_task.status}\""
            )
    
    return db_task

def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return True
    return False 