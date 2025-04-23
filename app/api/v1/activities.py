from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter()

@router.post("/", response_model=schemas.Activity)
def create_activity(
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_activity = models.Activity(**activity.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.get("/", response_model=List[schemas.Activity])
def read_activities(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    activities = db.query(models.Activity)\
        .order_by(desc(models.Activity.created_at))\
        .offset(skip)\
        .limit(limit)\
        .all()
    return activities 