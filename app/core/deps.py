from typing import Generator, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.models import models
from app.schemas import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator:
    """
    获取数据库会话
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    获取当前用户

    Args:
        db: 数据库会话
        token: JWT令牌

    Returns:
        models.User: 当前用户

    Raises:
        HTTPException: 认证失败
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    获取当前活跃用户

    Args:
        current_user: 当前用户

    Returns:
        models.User: 当前活跃用户

    Raises:
        HTTPException: 用户未激活
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """
    获取当前超级用户

    Args:
        current_user: 当前用户

    Returns:
        models.User: 当前超级用户

    Raises:
        HTTPException: 用户不是超级用户
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user

def get_current_user_with_scopes(
    required_scopes: List[str],
    current_user: models.User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
) -> models.User:
    """
    获取具有特定权限范围的当前用户

    Args:
        required_scopes: 所需的权限范围列表
        current_user: 当前用户
        token: JWT令牌

    Returns:
        models.User: 具有所需权限的用户

    Raises:
        HTTPException: 用户没有所需权限
    """
    try:
        payload = get_token_payload(token)
        token_scopes = payload.get("scopes", [])
        for scope in required_scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions. Required scope: {scope}"
                )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return current_user 

def get_token_payload(token: str) -> dict:
    """
    解析JWT令牌的payload

    Args:
        token: JWT令牌

    Returns:
        dict: 解析后的payload

    Raises:
        JWTError: 令牌无效
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]) 