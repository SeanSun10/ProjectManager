from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.models import User
from app.core.deps import get_db
from app.db.session import engine

def reset_admin_password():
    # 获取数据库会话
    db = next(get_db())
    
    # 获取管理员用户
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        # 重置密码
        admin.hashed_password = get_password_hash("admin123")
        db.commit()
        print("Admin password has been reset to: admin123")
    else:
        print("Admin user not found")

if __name__ == "__main__":
    print("Resetting admin password...")
    reset_admin_password()
    print("Password reset completed") 