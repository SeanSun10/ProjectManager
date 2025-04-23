# API文档

## 目录

- [认证API](auth.md)
- [项目管理API](projects.md)
- [任务管理API](tasks.md)
- [迭代管理API](sprints.md)
- [成本记录API](costs.md)
- [统计API](statistics.md)
- [系统设置API](system.md)

## 通用说明

### 基础URL
```
http://localhost:8000/api/v1
```

### 认证方式
所有API（除登录接口外）都需要在请求头中携带JWT Token：
```
Authorization: Bearer <token>
```

### 响应格式
```json
{
    "data": {},  // 成功时返回的数据
    "detail": "", // 错误时返回的错误信息
    "code": 0    // 错误代码
}
```

### 状态码
- 200: 成功
- 201: 创建成功
- 400: 请求错误
- 401: 未认证
- 403: 未授权
- 404: 资源不存在
- 422: 数据验证错误
- 500: 服务器错误 

## 4. 任务管理 API

### 4.1 获取任务列表
- 请求方法：GET
- 请求路径：`/api/v1/tasks`
- 请求参数：
  - project_id: 项目ID（必填）
  - sprint_id: 迭代ID（选填）
  - status: 任务状态（选填）
  - assignee_id: 负责人ID（选填）
- 响应格式：
  ```json
  {
    "code": 200,
    "data": [
      {
        "id": 1,
        "title": "任务标题",
        "description": "任务描述",
        "status": "TODO",
        "priority": "HIGH",
        "project_id": 1,
        "sprint_id": 1,
        "assignee_id": 1,
        "estimated_hours": 8,
        "actual_hours": 10,
        "due_date": "2024-03-31",
        "created_at": "2024-03-20T10:00:00",
        "updated_at": "2024-03-20T10:00:00"
      }
    ]
  }
  ```

### 4.2 创建任务
- 请求方法：POST
- 请求路径：`/api/v1/tasks`
- 请求参数：
  ```json
  {
    "title": "任务标题",
    "description": "任务描述",
    "status": "TODO",
    "priority": "HIGH",
    "project_id": 1,
    "sprint_id": 1,
    "assignee_id": 1,
    "estimated_hours": 8,
    "due_date": "2024-03-31"
  }
  ```
- 响应格式：
  ```json
  {
    "code": 200,
    "data": {
      "id": 1,
      "title": "任务标题",
      "description": "任务描述",
      "status": "TODO",
      "priority": "HIGH",
      "project_id": 1,
      "sprint_id": 1,
      "assignee_id": 1,
      "estimated_hours": 8,
      "actual_hours": 0,
      "due_date": "2024-03-31",
      "created_at": "2024-03-20T10:00:00",
      "updated_at": "2024-03-20T10:00:00"
    }
  }
  ```

### 4.3 更新任务
- 请求方法：PUT
- 请求路径：`/api/v1/tasks/{task_id}`
- 请求参数：
  ```json
  {
    "title": "更新后的任务标题",
    "description": "更新后的任务描述",
    "status": "IN_PROGRESS",
    "priority": "MEDIUM",
    "sprint_id": 1,
    "assignee_id": 1,
    "estimated_hours": 10,
    "actual_hours": 5,
    "due_date": "2024-04-01"
  }
  ```
- 响应格式：
  ```json
  {
    "code": 200,
    "data": {
      "id": 1,
      "title": "更新后的任务标题",
      "description": "更新后的任务描述",
      "status": "IN_PROGRESS",
      "priority": "MEDIUM",
      "project_id": 1,
      "sprint_id": 1,
      "assignee_id": 1,
      "estimated_hours": 10,
      "actual_hours": 5,
      "due_date": "2024-04-01",
      "created_at": "2024-03-20T10:00:00",
      "updated_at": "2024-03-20T11:00:00"
    }
  }
  ```

### 4.4 删除任务
- 请求方法：DELETE
- 请求路径：`/api/v1/tasks/{task_id}`
- 响应格式：
  ```json
  {
    "code": 200,
    "message": "任务删除成功"
  }
  ```

## 5. 迭代管理 API

### 5.1 获取迭代列表
- 请求方法：GET
- 请求路径：`/api/v1/sprints`
- 请求参数：
  - project_id: 项目ID（必填）
  - status: 迭代状态（选填）
- 响应格式：
  ```json
  {
    "code": 200,
    "data": [
      {
        "id": 1,
        "name": "迭代名称",
        "description": "迭代描述",
        "start_date": "2024-03-20",
        "end_date": "2024-04-03",
        "status": "IN_PROGRESS",
        "project_id": 1,
        "created_at": "2024-03-20T10:00:00",
        "updated_at": "2024-03-20T10:00:00"
      }
    ]
  }
  ```

### 5.2 创建迭代
- 请求方法：POST
- 请求路径：`/api/v1/sprints`
- 请求参数：
  ```json
  {
    "name": "迭代名称",
    "description": "迭代描述",
    "start_date": "2024-03-20",
    "end_date": "2024-04-03",
    "status": "PLANNING",
    "project_id": 1
  }
  ```
- 响应格式：
  ```json
  {
    "code": 200,
    "data": {
      "id": 1,
      "name": "迭代名称",
      "description": "迭代描述",
      "start_date": "2024-03-20",
      "end_date": "2024-04-03",
      "status": "PLANNING",
      "project_id": 1,
      "created_at": "2024-03-20T10:00:00",
      "updated_at": "2024-03-20T10:00:00"
    }
  }
  ```

### 5.3 更新迭代
- 请求方法：PUT
- 请求路径：`/api/v1/sprints/{sprint_id}`
- 请求参数：
  ```json
  {
    "name": "更新后的迭代名称",
    "description": "更新后的迭代描述",
    "start_date": "2024-03-21",
    "end_date": "2024-04-04",
    "status": "IN_PROGRESS"
  }
  ```
- 响应格式：
  ```json
  {
    "code": 200,
    "data": {
      "id": 1,
      "name": "更新后的迭代名称",
      "description": "更新后的迭代描述",
      "start_date": "2024-03-21",
      "end_date": "2024-04-04",
      "status": "IN_PROGRESS",
      "project_id": 1,
      "created_at": "2024-03-20T10:00:00",
      "updated_at": "2024-03-20T11:00:00"
    }
  }
  ```

### 5.4 删除迭代
- 请求方法：DELETE
- 请求路径：`/api/v1/sprints/{sprint_id}`
- 响应格式：
  ```json
  {
    "code": 200,
    "message": "迭代删除成功"
  }
  ```

### 5.5 获取迭代统计
- 请求方法：GET
- 请求路径：`/api/v1/sprints/{sprint_id}/stats`
- 响应格式：
  ```json
  {
    "code": 200,
    "data": {
      "total_tasks": 10,
      "completed_tasks": 5,
      "in_progress_tasks": 3,
      "todo_tasks": 2,
      "total_estimated_hours": 80,
      "total_actual_hours": 60,
      "burndown_data": [
        {
          "date": "2024-03-20",
          "ideal": 10,
          "actual": 10
        },
        {
          "date": "2024-03-21",
          "ideal": 8,
          "actual": 9
        }
      ]
    }
  }
  ``` 