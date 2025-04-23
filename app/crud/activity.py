from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas

def create_activity(
    db: Session,
    user_id: int,
    activity_type: str,
    content: str
) -> models.Activity:
    """
    创建活动记录
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        activity_type: 活动类型
        content: 活动内容
    
    Returns:
        Activity: 创建的活动记录
    """
    activity = models.Activity(
        user_id=user_id,
        type=activity_type,
        content=content
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity 