# 迭代管理API文档

## 1. 获取迭代列表

### 请求
```http
GET /sprints
Authorization: Bearer <token>
```

### 查询参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| skip | integer | 否 | 跳过的记录数 |
| limit | integer | 否 | 返回的最大记录数 |
| project_id | integer | 否 | 项目ID过滤 |
| status | string | 否 | 迭代状态过滤 |
| search | string | 否 | 迭代名称搜索 |

### 响应
```json
{
    "data": {
        "items": [
            {
                "id": 1,
                "project_id": 1,
                "name": "迭代1",
                "start_date": "2024-01-01",
                "end_date": "2024-01-14",
                "status": "进行中",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        ],
        "total": 1,
        "skip": 0,
        "limit": 10
    }
}
```

## 2. 创建迭代

### 请求
```http
POST /sprints
Authorization: Bearer <token>
Content-Type: application/json
```

### 请求体
```json
{
    "project_id": 1,
    "name": "迭代1",
    "start_date": "2024-01-01",
    "end_date": "2024-01-14",
    "status": "待开始"
}
```

### 响应
```json
{
    "data": {
        "id": 1,
        "project_id": 1,
        "name": "迭代1",
        "start_date": "2024-01-01",
        "end_date": "2024-01-14",
        "status": "待开始",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
}
```

## 3. 获取迭代详情

### 请求
```http
GET /sprints/{sprint_id}
Authorization: Bearer <token>
```

### 响应
```json
{
    "data": {
        "id": 1,
        "project_id": 1,
        "name": "迭代1",
        "start_date": "2024-01-01",
        "end_date": "2024-01-14",
        "status": "进行中",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
        "tasks": [
            {
                "id": 1,
                "title": "任务1",
                "status": "进行中",
                "priority": "高",
                "assignee_id": 1
            }
        ]
    }
}
```

## 4. 更新迭代

### 请求
```http
PUT /sprints/{sprint_id}
Authorization: Bearer <token>
Content-Type: application/json
```

### 请求体
```json
{
    "name": "新迭代名称",
    "start_date": "2024-01-15",
    "end_date": "2024-01-28",
    "status": "已完成"
}
```

### 响应
```json
{
    "data": {
        "id": 1,
        "project_id": 1,
        "name": "新迭代名称",
        "start_date": "2024-01-15",
        "end_date": "2024-01-28",
        "status": "已完成",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-02T00:00:00"
    }
}
```

## 5. 删除迭代

### 请求
```http
DELETE /sprints/{sprint_id}
Authorization: Bearer <token>
```

### 响应
```json
{
    "data": {
        "message": "迭代已删除"
    }
}
```

## 错误码
- 400: 请求参数错误
- 401: 未认证
- 403: 未授权
- 404: 迭代不存在
- 422: 数据验证错误 