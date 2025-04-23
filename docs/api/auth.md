# 认证API文档

## 1. 用户登录

### 请求
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded
```

### 参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

### 响应
```json
{
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
}
```

### 错误码
- 401: 用户名或密码错误
- 403: 用户未激活

## 2. 获取当前用户信息

### 请求
```http
GET /auth/me
Authorization: Bearer <token>
```

### 响应
```json
{
    "data": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "is_active": true,
        "is_superuser": true
    }
}
```

### 错误码
- 401: 未认证
- 403: 未授权

## 3. 刷新Token

### 请求
```http
POST /auth/refresh
Authorization: Bearer <token>
```

### 响应
```json
{
    "data": {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer"
    }
}
```

### 错误码
- 401: Token无效或已过期

## 4. 用户登出

### 请求
```http
POST /auth/logout
Authorization: Bearer <token>
```

### 响应
```json
{
    "data": {
        "message": "Successfully logged out"
    }
}
```

### 错误码
- 401: 未认证 