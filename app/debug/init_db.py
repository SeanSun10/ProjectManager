import logging
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import models
from app.core.security import get_password_hash
from datetime import datetime, timedelta
from app.db.session import engine, SessionLocal
from app.models.models import Base

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_test_data(db: Session) -> None:
    """
    初始化测试数据
    
    这个脚本用于：
    1. 创建数据库表
    2. 创建测试用户
    3. 创建测试项目
    4. 创建测试任务
    5. 验证数据库连接
    6. 检查数据是否成功创建
    """
    try:
        # 创建测试用户
        test_user = models.User(
            username="admin",
            email="admin@example.com",
            is_active=True,
            is_superuser=True
        )
        test_user.set_password("admin123")
        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        # 创建测试项目
        test_project = models.Project(
            name="测试项目",
            description="这是一个测试项目",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=30),
            status="active",
            fixed_cost_monthly=10000.0
        )
        db.add(test_project)
        db.commit()
        db.refresh(test_project)

        # 创建测试活动
        activities = [
            models.Activity(
                user_id=test_user.id,
                type="project_created",
                content="创建了项目 \"{}\"".format(test_project.name),
                created_at=datetime.now() - timedelta(days=1)
            ),
            models.Activity(
                user_id=test_user.id,
                type="task_created",
                content="创建了任务 \"开发用户管理模块\"",
                created_at=datetime.now() - timedelta(hours=12)
            ),
            models.Activity(
                user_id=test_user.id,
                type="task_updated",
                content="将任务 \"开发用户管理模块\" 状态更新为 \"进行中\"",
                created_at=datetime.now() - timedelta(hours=6)
            ),
            models.Activity(
                user_id=test_user.id,
                type="sprint_created",
                content="创建了迭代 \"Sprint 1\"",
                created_at=datetime.now() - timedelta(hours=2)
            )
        ]
        
        for activity in activities:
            db.add(activity)
        
        db.commit()
        logger.info("Test activities created successfully")

        # 检查是否已存在测试项目
        project = db.query(models.Project).first()
        if not project:
            # 创建测试项目
            test_project = models.Project(
                name="测试项目",
                description="这是一个测试项目",
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=30),
                status="active",
                fixed_cost_monthly=10000.0
            )
            db.add(test_project)
            db.commit()
            logger.info("Test project created successfully")
            
            # 创建测试迭代
            sprint = models.Sprint(
                project_id=test_project.id,
                name="迭代1",
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=14),
                status="active",
                velocity=10.0
            )
            db.add(sprint)
            db.commit()
            logger.info("Test sprint created successfully")
            
            # 创建测试团队成员
            member = models.TeamMember(
                name="测试成员",
                role="开发",
                monthly_salary=10000.0,
                join_date=datetime.now()
            )
            db.add(member)
            db.commit()
            logger.info("Test team member created successfully")
            
            # 创建项目成员关系
            project_member = models.ProjectMember(
                project_id=test_project.id,
                member_id=member.id,
                allocation_percentage=100.0,
                start_date=datetime.now()
            )
            db.add(project_member)
            db.commit()
            logger.info("Test project member relationship created successfully")
            
            # 创建测试任务
            tasks = [
                models.Task(
                    project_id=test_project.id,
                    sprint_id=sprint.id,
                    title="任务1",
                    description="这是一个测试任务",
                    story_points=5.0,
                    status="done",
                    assignee_id=member.id,
                    estimated_hours=8.0,
                    actual_hours=10.0
                ),
                models.Task(
                    project_id=test_project.id,
                    sprint_id=sprint.id,
                    title="任务2",
                    description="这是另一个测试任务",
                    story_points=3.0,
                    status="in_progress",
                    assignee_id=member.id,
                    estimated_hours=4.0,
                    actual_hours=2.0
                ),
                models.Task(
                    project_id=test_project.id,
                    sprint_id=sprint.id,
                    title="任务3",
                    description="这是第三个测试任务",
                    story_points=8.0,
                    status="todo",
                    assignee_id=member.id,
                    estimated_hours=12.0,
                    actual_hours=0.0
                )
            ]
            for task in tasks:
                db.add(task)
            db.commit()
            logger.info("Test tasks created successfully")
            
            # 创建成本记录
            cost = models.CostRecord(
                project_id=test_project.id,
                record_date=datetime.now(),
                cost_type="fixed",
                amount=10000.0,
                description="月度固定成本"
            )
            db.add(cost)
            db.commit()
            logger.info("Test cost record created successfully")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        db.close()

def init_db() -> None:
    try:
        db = SessionLocal()
        # 创建数据库表
        Base.metadata.create_all(bind=engine)
        
        # 检查是否已经有管理员用户
        admin = db.query(models.User).filter(
            models.User.email == "admin@example.com"
        ).first()
        
        if not admin:
            init_test_data(db)
            print("Test data initialized successfully.")
        else:
            print("Admin user already exists. Skipping test data initialization.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 