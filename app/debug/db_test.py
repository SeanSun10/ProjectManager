from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models import models
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_db_connection():
    """
    测试数据库连接和基本查询功能
    
    这个脚本用于：
    1. 验证数据库连接是否正常
    2. 测试基本的CRUD操作
    3. 检查数据一致性
    """
    try:
        db = next(get_db())
        logger.info("Database connection established")
        
        # 测试查询所有用户
        all_users = db.query(models.User).all()
        logger.info(f"Found {len(all_users)} users in database")
        for user in all_users:
            logger.info(f"User: {user.username}, Email: {user.email}, Active: {user.is_active}")
        
        # 测试特定用户查询
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        if admin:
            logger.info(f"Admin user found: {admin.username}")
            logger.info(f"Admin email: {admin.email}")
            logger.info(f"Admin is active: {admin.is_active}")
        else:
            logger.warning("Admin user not found")
            
    except Exception as e:
        logger.error(f"Database test failed: {e}")
        raise

if __name__ == "__main__":
    test_db_connection() 