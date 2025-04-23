# 项目管理模块 API 文档

## 概述
项目管理模块负责处理项目的创建、查询、更新和删除等操作。

## API 接口

### 1. 获取项目列表
- **接口**: `/api/v1/projects`
- **方法**: GET
- **描述**: 获取所有项目列表
- **请求头**: 
  - Authorization: Bearer {token}
- **响应**:
  ```json
  {
    "items": [
      {
        "id": "integer",
        "name": "string",
        "description": "string",
        "status": "string",
        "start_date": "date",
        "end_date": "date",
        "monthly_cost": "float",
        "created_at": "datetime",
        "updated_at": "datetime"
      }
    ],
    "total": "integer"
  }
  ```

### 2. 创建项目
- **接口**: `/api/v1/projects`
- **方法**: POST
- **描述**: 创建新项目
- **请求头**: 
  - Authorization: Bearer {token}
- **请求参数**:
  ```json
  {
    "name": "string",
    "description": "string",
    "status": "string",
    "start_date": "date",
    "end_date": "date",
    "monthly_cost": "float"
  }
  ```
- **响应**: 201 Created

### 3. 获取项目详情
- **接口**: `/api/v1/projects/{project_id}`
- **方法**: GET
- **描述**: 获取指定项目的详细信息
- **请求头**: 
  - Authorization: Bearer {token}
- **响应**:
  ```json
  {
    "id": "integer",
    "name": "string",
    "description": "string",
    "status": "string",
    "start_date": "date",
    "end_date": "date",
    "monthly_cost": "float",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

### 4. 更新项目
- **接口**: `/api/v1/projects/{project_id}`
- **方法**: PUT
- **描述**: 更新项目信息
- **请求头**: 
  - Authorization: Bearer {token}
- **请求参数**: 同创建项目
- **响应**: 200 OK

### 5. 删除项目
- **接口**: `/api/v1/projects/{project_id}`
- **方法**: DELETE
- **描述**: 删除指定项目
- **请求头**: 
  - Authorization: Bearer {token}
- **响应**: 204 No Content

## 错误码说明
- 401: 未授权
- 403: 禁止访问
- 404: 项目不存在
- 422: 请求参数错误 