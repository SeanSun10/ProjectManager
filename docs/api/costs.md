# 成本记录API文档

## 1. 获取成本记录列表

### 请求
```http
GET /costs
Authorization: Bearer <token>
```

### 查询参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| skip | integer | 否 | 跳过的记录数 |
| limit | integer | 否 | 返回的最大记录数 |
| project_id | integer | 否 | 项目ID过滤 |
| category | string | 否 | 类别过滤 |
| start_date | date | 否 | 开始日期过滤 |
| end_date | date | 否 | 结束日期过滤 |
| search | string | 否 | 描述搜索 |

### 响应
```json
{
    "data": {
        "items": [
            {
                "id": 1,
                "project_id": 1,
                "amount": 1000.0,
                "description": "服务器费用",
                "date": "2024-01-01",
                "category": "基础设施",
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

## 2. 获取项目成本记录列表

### 请求
```http
GET /costs/project/{project_id}
Authorization: Bearer <token>
```

### 响应
```json
[
    {
        "id": 1,
        "project_id": 1,
        "record_date": "2024-01-01T00:00:00",
        "cost_type": "fixed",
        "amount": 1000.0,
        "description": "服务器费用",
        "created_at": "2024-01-01T00:00:00"
    }
]
```

## 3. 获取项目成本统计

### 请求
```http
GET /costs/project/{project_id}/stats
Authorization: Bearer <token>
```

### 响应
```json
{
    "fixed": 1000.0,
    "human": 5000.0,
    "other": 2000.0
}
```

## 4. 创建成本记录

### 请求
```http
POST /costs
Authorization: Bearer <token>
Content-Type: application/json
```

### 请求体
```json
{
    "project_id": 1,
    "record_date": "2024-01-01T00:00:00",
    "cost_type": "fixed",
    "amount": 1000.0,
    "description": "服务器费用"
}
```

### 响应
```json
{
    "id": 1,
    "project_id": 1,
    "record_date": "2024-01-01T00:00:00",
    "cost_type": "fixed",
    "amount": 1000.0,
    "description": "服务器费用",
    "created_at": "2024-01-01T00:00:00"
}
```

## 5. 获取成本记录详情

### 请求
```http
GET /costs/{cost_id}
Authorization: Bearer <token>
```

### 响应
```json
{
    "data": {
        "id": 1,
        "project_id": 1,
        "amount": 1000.0,
        "description": "服务器费用",
        "date": "2024-01-01",
        "category": "基础设施",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00",
        "project": {
            "id": 1,
            "name": "项目名称"
        }
    }
}
```

## 6. 更新成本记录

### 请求
```http
PUT /costs/{cost_id}
Authorization: Bearer <token>
Content-Type: application/json
```

### 请求体
```json
{
    "record_date": "2024-01-15T00:00:00",
    "cost_type": "fixed",
    "amount": 1200.0,
    "description": "更新后的服务器费用"
}
```

### 响应
```json
{
    "id": 1,
    "project_id": 1,
    "record_date": "2024-01-15T00:00:00",
    "cost_type": "fixed",
    "amount": 1200.0,
    "description": "更新后的服务器费用",
    "created_at": "2024-01-01T00:00:00"
}
```

## 7. 删除成本记录

### 请求
```http
DELETE /costs/{cost_id}
Authorization: Bearer <token>
```

### 响应
```json
{
    "message": "Cost record deleted successfully"
}
```

## 错误码
- 400: 请求参数错误
- 401: 未认证
- 403: 未授权
- 404: 成本记录不存在
- 422: 数据验证错误 