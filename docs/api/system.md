# 系统设置模块 API 文档

## 概述
系统设置模块负责处理系统参数的配置和管理。

## API 接口

### 1. 获取系统参数
- **接口**: `/api/v1/system/params`
- **方法**: GET
- **描述**: 获取系统参数配置
- **请求头**: 
  - Authorization: Bearer {token}
- **响应**:
  ```json
  {
    "system_name": "string",
    "system_description": "string",
    "default_task_priority": "string",
    "default_task_status": "string",
    "allowed_file_types": ["string"],
    "max_file_size": "integer"
  }
  ```

### 2. 更新系统参数
- **接口**: `/api/v1/system/params`
- **方法**: PUT
- **描述**: 更新系统参数配置
- **请求头**: 
  - Authorization: Bearer {token}
- **请求参数**:
  ```json
  {
    "system_name": "string",
    "system_description": "string",
    "default_task_priority": "string",
    "default_task_status": "string",
    "allowed_file_types": ["string"],
    "max_file_size": "integer"
  }
  ```
- **响应**: 200 OK

## 参数说明

### 系统参数说明
- `system_name`: 系统名称
- `system_description`: 系统描述
- `default_task_priority`: 任务默认优先级
  - 可选值: "low", "medium", "high"
- `default_task_status`: 任务默认状态
  - 可选值: "pending", "in_progress", "completed"
- `allowed_file_types`: 允许上传的文件类型
  - 示例: ["image/*", ".doc,.docx,.pdf", ".xls,.xlsx", ".zip,.rar"]
- `max_file_size`: 最大文件大小（MB）
  - 范围: 1-100

## 错误码说明
- 401: 未授权
- 403: 禁止访问
- 422: 请求参数错误 