from fastapi import Request
from app.core.config import settings

# 定义不需要认证的路由
PUBLIC_ROUTES = [
    f"{settings.API_V1_STR}/auth/login",
    f"{settings.API_V1_STR}/auth/register",
    f"{settings.API_V1_STR}/openapi.json",
    "/"
]

async def public_routes_middleware(request: Request, call_next):
    """
    公开路由中间件
    
    Args:
        request: 请求对象
        call_next: 下一个处理函数
        
    Returns:
        Response: 响应对象
    """
    # 检查是否是公开路由
    if request.url.path in PUBLIC_ROUTES:
        # 如果是公开路由，直接跳过认证
        response = await call_next(request)
        return response
    
    # 对于非公开路由，让 OAuth2 处理认证
    return await call_next(request) 