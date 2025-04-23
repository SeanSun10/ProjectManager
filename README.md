# 大数据项目敏捷管理与成本估算系统

## 项目简介
这是一个用于管理大数据项目的敏捷开发流程和成本估算的系统。系统采用FastAPI框架开发，使用SQLite作为数据库，提供了项目、任务、团队和成本管理等功能。

## 技术栈
- 后端框架：FastAPI
- 数据库：SQLite
- 认证：JWT
- 密码加密：bcrypt

## 项目结构
```
app/
├── api/
│   └── v1/
│       ├── auth.py      # 认证相关API
│       ├── projects.py  # 项目管理API
│       ├── sprints.py   # 迭代管理API
│       ├── tasks.py     # 任务管理API
│       ├── team_members.py  # 团队成员管理API
│       └── costs.py     # 成本管理API
├── core/
│   ├── config.py    # 配置管理
│   ├── deps.py      # 依赖注入
│   └── security.py  # 安全相关功能
├── db/
│   └── session.py   # 数据库会话管理
├── models/
│   └── models.py    # 数据模型
└── schemas/
    └── schemas.py   # Pydantic模型
```

## 认证系统
系统采用简化的JWT认证机制，主要特点：
- 使用JWT令牌进行身份验证
- 密码使用bcrypt加密存储
- 支持用户注册和登录
- 支持密码修改
- 移除了复杂的权限控制，适合单人使用

## 开发基准
1. 认证系统
   - 使用JWT进行身份验证
   - 密码使用bcrypt加密
   - 不实现复杂的权限控制
   - 不实现角色管理
   - 不实现权限范围检查

2. 数据模型
   - 使用SQLAlchemy ORM
   - 使用Pydantic进行数据验证
   - 保持模型简单清晰

3. API设计
   - RESTful风格
   - 清晰的错误处理
   - 适当的HTTP状态码
   - 详细的API文档

4. 安全考虑
   - 环境变量管理敏感信息
   - 密码加密存储
   - 基本的XSS和CSRF防护
   - 适当的请求速率限制

## 环境配置
1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
复制`.env.example`为`.env`并修改配置：
```bash
cp .env.example .env
```

4. 运行应用
```bash
uvicorn app.main:app --reload
```

## API文档
启动应用后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 开发规范
1. 代码风格
   - 遵循PEP 8规范
   - 使用类型注解
   - 编写清晰的文档字符串

2. 提交规范
   - 提交信息清晰明确
   - 相关改动一起提交
   - 避免提交敏感信息

3. 测试规范
   - 编写单元测试
   - 测试覆盖率要求
   - 测试数据隔离

## 注意事项
1. 本项目为单人使用，不包含复杂的权限控制
2. 生产环境部署时注意修改密钥
3. 定期备份数据库
4. 注意保护敏感信息

## 后续开发
1. 保持代码简洁清晰
2. 遵循已建立的开发基准
3. 优先实现核心功能
4. 保持向后兼容性

## 核心功能模块

### 1. 项目管理模块
- Sprint管理
  - Sprint周期设置（2-4周）
  - Sprint目标设定
  - 任务看板（To Do/In Progress/Done）
  - 每日站会记录
- 项目基础信息
  - 项目名称、描述
  - 项目时间线
  - 项目团队组成
  - 项目状态跟踪

### 2. 成本管理模块
- 固定成本管理
  - 基础设施成本（服务器、云服务等）
  - 软件许可成本
  - 其他固定支出
- 人力成本计算
  - 团队成员基本信息
  - 月薪设置
  - 工时统计
  - 成本自动计算
- 成本预警
  - 预算超支提醒
  - 成本趋势分析

### 3. 敏捷度量模块
- 团队效能指标
  - Sprint速度（Velocity）
  - 故事点完成率
  - 任务完成时间
- 项目健康度
  - 燃尽图
  - 累积流量图
  - 技术债务追踪

## 数据库设计

### 主要数据表
```sql
-- 项目表
projects
  - id
  - name
  - description
  - start_date
  - end_date
  - status
  - fixed_cost_monthly
  - created_at
  - updated_at

-- Sprint表
sprints
  - id
  - project_id
  - name
  - start_date
  - end_date
  - status
  - velocity
  - created_at

-- 团队成员表
team_members
  - id
  - name
  - role
  - monthly_salary
  - join_date
  - leave_date
  - created_at

-- 项目成员关联表
project_members
  - id
  - project_id
  - member_id
  - allocation_percentage
  - start_date
  - end_date

-- 任务表
tasks
  - id
  - sprint_id
  - title
  - description
  - story_points
  - status
  - assignee_id
  - created_at
  - updated_at

-- 成本记录表
cost_records
  - id
  - project_id
  - record_date
  - cost_type (fixed/human)
  - amount
  - description
  - created_at
```

## 特色功能

### 1. 成本估算功能
- 基于固定成本和人力成本的自动计算
- 支持不同时间维度的成本预测（月度/季度/年度）
- 成本偏差分析
- 可视化成本报表

### 2. 敏捷管理功能
- Sprint规划和追踪
- 任务看板
- 团队效能分析
- 项目健康度仪表盘

### 3. 报表功能
- 成本分析报表
  - 月度成本汇总
  - 成本构成分析
  - 成本趋势图
- 敏捷项目报表
  - Sprint报告
  - 团队效能报告
  - 项目进度报告

## 数据导入导出
- 支持Excel模板导入项目成员信息
- 支持成本数据导出
- 支持项目报表导出

## 部署要求
- Python 3.8+
- Node.js 14+
- Docker

## 安装说明
（待补充）

## 使用说明
（待补充）

## 贡献指南
（待补充）

## 许可证
（待补充） 