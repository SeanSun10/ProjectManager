from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from app.core import security
from app.core.config import settings
from app.core.deps import get_db
from app.models import models
from app.schemas import schemas

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/login", response_model=schemas.Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    用户登录

    Args:
        db: 数据库会话
        form_data: 登录表单数据

    Returns:
        Any: 访问令牌

    Raises:
        HTTPException: 认证失败
    """
    logger.debug(f"Login attempt for username: {form_data.username}")
    
    # 打印所有用户
    all_users = db.query(models.User).all()
    logger.debug(f"All users in database: {[u.username for u in all_users]}")
    
    # 尝试直接使用SQL查询
    from sqlalchemy import text
    result = db.execute(text("SELECT username FROM users WHERE username = :username"), 
                       {"username": form_data.username})
    logger.debug(f"SQL query result: {result.fetchall()}")
    
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        logger.warning(f"User not found: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.debug(f"User found: {user.username}, is_active: {user.is_active}")
    
    if not security.verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Invalid password for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        logger.warning(f"Inactive user: {form_data.username}")
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    
    logger.debug(f"Login successful for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas.User)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    用户注册

    Args:
        db: 数据库会话
        user_in: 用户创建数据

    Returns:
        Any: 创建的用户

    Raises:
        HTTPException: 用户名或邮箱已存在
    """
    user = db.query(models.User).filter(models.User.username == user_in.username).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/me", response_model=schemas.User)
def read_users_me(
    current_user: models.User = Depends(security.get_current_user)
) -> Any:
    """
    获取当前用户信息

    Args:
        current_user: 当前登录用户

    Returns:
        Any: 用户信息
    """
    return current_user 