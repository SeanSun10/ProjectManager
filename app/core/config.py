from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import Optional, Dict, Any, List
import secrets
from functools import lru_cache
from pathlib import Path
import os

# 获取项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    """
    应用配置类，从环境变量或.env文件读取配置
    """
    # 项目基本信息
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    
    # 数据库配置
    SQLITE_URL: str

    @property
    def SQLITE_URL_WITH_ABS_PATH(self) -> str:
        """
        获取使用绝对路径的数据库URL
        """
        if self.SQLITE_URL.startswith("sqlite:///./"):
            db_path = os.path.join(BASE_DIR, self.SQLITE_URL.replace("sqlite:///./", ""))
            return f"sqlite:///{db_path}"
        return self.SQLITE_URL
    
    # JWT配置
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # CORS配置
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # 安全配置
    SECURE_COOKIES: bool = True
    SECURE_SSL_REDIRECT: bool = True
    
    class Config:
        case_sensitive = True
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"

    def generate_new_secret_key(self) -> None:
        """
        生成新的密钥（在需要时使用）
        """
        self.SECRET_KEY = secrets.token_urlsafe(32)

@lru_cache()
def get_settings() -> Settings:
    """
    获取应用配置的单例实例
    """
    return Settings()

settings = get_settings() 