# 任务管理 API 文档

## 1. 获取任务列表

### 请求
```http
GET /tasks
Authorization: Bearer <token>
```

### 查询参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| project_id | integer | 是 | 项目ID |
| skip | integer | 否 | 跳过的记录数 |
| limit | integer | 否 | 返回的最大记录数 |

### 响应
```json
[
    {
        "id": 1,
        "title": "实现用户登录功能",
        "description": "实现基于 JWT 的用户登录功能",
        "status": "IN_PROGRESS",
        "priority": "HIGH",
        "project_id": 1,
        "sprint_id": 1,
        "assignee_id": 1,
        "estimated_hours": 8.0,
        "actual_hours": 6.5,
        "due_date": "2024-03-31T00:00:00",
        "created_at": "2024-03-20T10:00:00",
        "updated_at": "2024-03-21T15:30:00"
    }
]
```

## 2. 获取迭代任务列表

### 请求
```http
GET /tasks/sprint/{sprint_id}
Authorization: Bearer <token>
```

### 响应
```json
[
    {
        "id": 1,
        "title": "实现用户登录功能",
        "description": "实现基于 JWT 的用户登录功能",
        "status": "IN_PROGRESS",
        "priority": "HIGH",
        "project_id": 1,
        "sprint_id": 1,
        "assignee_id": 1,
        "estimated_hours": 8.0,
        "actual_hours": 6.5,
        "due_date": "2024-03-31T00:00:00",
        "created_at": "2024-03-20T10:00:00",
        "updated_at": "2024-03-21T15:30:00"
    }
]
```

## 3. 创建任务

### 请求
```http
POST /tasks
Authorization: Bearer <token>
Content-Type: application/json
```

### 请求体
```json
{
    "title": "实现用户登录功能",
    "description": "实现基于 JWT 的用户登录功能",
    "status": "TODO",
    "priority": "HIGH",
    "project_id": 1,
    "sprint_id": 1,
    "assignee_id": 1,
    "estimated_hours": 8.0,
    "due_date": "2024-03-31T00:00:00"
}
```

### 响应
```json
{
    "id": 1,
    "title": "实现用户登录功能",
    "description": "实现基于 JWT 的用户登录功能",
    "status": "TODO",
    "priority": "HIGH",
    "project_id": 1,
    "sprint_id": 1,
    "assignee_id": 1,
    "estimated_hours": 8.0,
    "actual_hours": 0.0,
    "due_date": "2024-03-31T00:00:00",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-20T10:00:00"
}
```

## 4. 获取任务详情

### 请求
```http
GET /tasks/{task_id}
Authorization: Bearer <token>
```

### 响应
```json
{
    "id": 1,
    "title": "实现用户登录功能",
    "description": "实现基于 JWT 的用户登录功能",
    "status": "IN_PROGRESS",
    "priority": "HIGH",
    "project_id": 1,
    "sprint_id": 1,
    "assignee_id": 1,
    "estimated_hours": 8.0,
    "actual_hours": 6.5,
    "due_date": "2024-03-31T00:00:00",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-21T15:30:00"
}
```

## 5. 更新任务

### 请求
```http
PUT /tasks/{task_id}
Authorization: Bearer <token>
Content-Type: application/json
```

### 请求体
```json
{
    "title": "实现用户登录功能",
    "description": "实现基于 JWT 的用户登录功能，包括刷新令牌",
    "status": "IN_PROGRESS",
    "priority": "HIGH",
    "sprint_id": 1,
    "assignee_id": 1,
    "estimated_hours": 10.0,
    "actual_hours": 6.5,
    "due_date": "2024-04-05T00:00:00"
}
```

### 响应
```json
{
    "id": 1,
    "title": "实现用户登录功能",
    "description": "实现基于 JWT 的用户登录功能，包括刷新令牌",
    "status": "IN_PROGRESS",
    "priority": "HIGH",
    "project_id": 1,
    "sprint_id": 1,
    "assignee_id": 1,
    "estimated_hours": 10.0,
    "actual_hours": 6.5,
    "due_date": "2024-04-05T00:00:00",
    "created_at": "2024-03-20T10:00:00",
    "updated_at": "2024-03-21T15:30:00"
}
```

## 6. 删除任务

### 请求
```http
DELETE /tasks/{task_id}
Authorization: Bearer <token>
```

### 响应
```json
{
    "message": "Task deleted successfully"
}
```

## 状态说明
- TODO: 待处理
- IN_PROGRESS: 进行中
- REVIEW: 评审中
- DONE: 已完成

## 优先级说明
- URGENT: 紧急
- HIGH: 高
- MEDIUM: 中
- LOW: 低

## 错误码
- 400: 请求参数错误
- 401: 未认证
- 403: 未授权
- 404: 任务不存在
- 422: 数据验证错误 