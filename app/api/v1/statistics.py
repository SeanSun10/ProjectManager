from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from typing import Dict, Any
import logging

from app.core.deps import get_db
from app.models import models
from app.core.security import get_current_user

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("")
async def get_statistics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    获取统计数据
    
    Args:
        current_user: 当前登录用户
        db: 数据库会话
        
    Returns:
        Dict[str, Any]: 统计数据
    """
    try:
        logger.info("开始获取统计数据")
        
        # 获取项目统计
        try:
            # 临时：获取所有项目
            user_projects = db.query(models.Project).all()
            
            project_count = len(user_projects)
            active_project_count = sum(1 for p in user_projects if p.status == 'active')
            
            logger.info(f"项目统计获取成功: 总数={project_count}, 进行中={active_project_count}")
        except Exception as e:
            logger.error(f"获取项目统计时出错: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取项目统计失败: {str(e)}")
        
        # 获取任务统计
        try:
            # 只统计用户参与项目中的任务
            project_ids = [p.id for p in user_projects]
            total_tasks = db.query(func.count(models.Task.id)).filter(
                models.Task.project_id.in_(project_ids)
            ).scalar() or 0
            
            completed_tasks = db.query(func.count(models.Task.id)).filter(
                models.Task.project_id.in_(project_ids),
                models.Task.status == 'done'
            ).scalar() or 0
            
            in_progress_tasks = db.query(func.count(models.Task.id)).filter(
                models.Task.project_id.in_(project_ids),
                models.Task.status == 'in_progress'
            ).scalar() or 0
            
            logger.info(f"任务统计获取成功: 总数={total_tasks}, 已完成={completed_tasks}, 进行中={in_progress_tasks}")
        except Exception as e:
            logger.error(f"获取任务统计时出错: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取任务统计失败: {str(e)}")
        
        # 获取工时统计
        try:
            total_estimated_hours = db.query(func.sum(models.Task.estimated_hours)).filter(
                models.Task.project_id.in_(project_ids)
            ).scalar() or 0
            
            total_actual_hours = db.query(func.sum(models.Task.actual_hours)).filter(
                models.Task.project_id.in_(project_ids)
            ).scalar() or 0
            
            logger.info(f"工时统计获取成功: 预估={total_estimated_hours}, 实际={total_actual_hours}")
        except Exception as e:
            logger.error(f"获取工时统计时出错: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取工时统计失败: {str(e)}")
        
        # 获取任务状态分布
        try:
            status_distribution = []
            status_counts = db.query(
                models.Task.status,
                func.count(models.Task.id).label('count')
            ).filter(
                models.Task.project_id.in_(project_ids)
            ).group_by(models.Task.status).all()
            
            for status, count in status_counts:
                percentage = round((count / total_tasks) * 100, 2) if total_tasks > 0 else 0
                status_distribution.append({
                    'status': status,
                    'count': count,
                    'percentage': percentage
                })
            logger.info(f"任务状态分布获取成功: {status_distribution}")
        except Exception as e:
            logger.error(f"获取任务状态分布时出错: {str(e)}")
            raise HTTPException(status_code=500, detail=f"获取任务状态分布失败: {str(e)}")
        
        result = {
            'project_count': project_count,
            'active_project_count': active_project_count,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'in_progress_tasks': in_progress_tasks,
            'total_estimated_hours': total_estimated_hours,
            'total_actual_hours': total_actual_hours,
            'status_distribution': status_distribution
        }
        
        logger.info("统计数据获取成功")
        return result
        
    except Exception as e:
        logger.error(f"获取统计数据时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}") 