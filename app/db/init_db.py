from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.session import SessionLocal, engine
from app.models import models

def init_db() -> None:
    # 创建所有表
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    # 创建超级用户
    user = db.query(models.User).filter(models.User.username == "admin").first()
    if not user:
        user = models.User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    db.close()

if __name__ == "__main__":
    init_db() 