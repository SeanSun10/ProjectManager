# 统计模块 API 文档

## 概述
统计模块负责提供项目数据的统计和分析。

## API 接口

### 1. 获取统计数据
- **接口**: `/api/v1/statistics`
- **方法**: GET
- **描述**: 获取项目统计数据
- **请求头**: 
  - Authorization: Bearer {token}
- **响应**:
  ```json
  {
    "total_tasks": 0,
    "completed_tasks": 0,
    "in_progress_tasks": 0,
    "total_estimated_hours": 0,
    "total_actual_hours": 0,
    "project_start_date": "string",
    "project_end_date": "string",
    "status_distribution": [
      {
        "status": "string",
        "count": 0,
        "percentage": 0
      }
    ]
  }
  ```

## 参数说明

### 统计数据说明
- `total_tasks`: 总任务数
- `completed_tasks`: 已完成任务数
- `in_progress_tasks`: 进行中任务数
- `total_estimated_hours`: 预估总工时
- `total_actual_hours`: 实际总工时
- `project_start_date`: 项目开始日期
- `project_end_date`: 项目结束日期
- `status_distribution`: 任务状态分布
  - `status`: 任务状态
  - `count`: 该状态的任务数量
  - `percentage`: 该状态的任务占比

## 错误码
- 401: 未认证
- 403: 未授权
- 500: 服务器错误

## 注意事项
1. 该接口需要用户登录并携带有效的 JWT Token
2. 统计数据基于当前数据库中的所有任务和项目信息
3. 如果数据库中没有项目信息，`project_start_date` 和 `project_end_date` 将返回 `null`
4. 如果数据库中没有任务信息，所有统计数值将返回 0 