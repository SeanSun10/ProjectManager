# 数据库设计文档

## 1. 用户表 (users)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | Integer | 主键 | PK, AI |
| username | String(50) | 用户名 | UNIQUE, NOT NULL |
| email | String(100) | 邮箱 | UNIQUE, NOT NULL |
| hashed_password | String(255) | 密码哈希 | NOT NULL |
| is_active | Boolean | 是否激活 | DEFAULT True |
| is_superuser | Boolean | 是否超级用户 | DEFAULT False |
| created_at | DateTime | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DateTime | 更新时间 | DEFAULT CURRENT_TIMESTAMP |

## 2. 项目表 (projects)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | Integer | 主键 | PK, AI |
| name | String(100) | 项目名称 | NOT NULL |
| description | Text | 项目描述 | |
| status | String(20) | 项目状态 | NOT NULL |
| start_date | Date | 开始日期 | |
| end_date | Date | 结束日期 | |
| monthly_cost | Float | 月成本 | DEFAULT 0 |
| created_at | DateTime | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DateTime | 更新时间 | DEFAULT CURRENT_TIMESTAMP |

## 3. 项目成员表 (project_members)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | Integer | 主键 | PK, AI |
| project_id | Integer | 项目ID | FK(projects.id) |
| user_id | Integer | 用户ID | FK(users.id) |
| role | String(20) | 角色 | NOT NULL |
| created_at | DateTime | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DateTime | 更新时间 | DEFAULT CURRENT_TIMESTAMP |

## 4. 迭代表 (sprints)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | Integer | 主键 | PK, AI |
| project_id | Integer | 项目ID | FK(projects.id) |
| name | String(100) | 迭代名称 | NOT NULL |
| start_date | Date | 开始日期 | NOT NULL |
| end_date | Date | 结束日期 | NOT NULL |
| status | String(20) | 状态 | NOT NULL |
| created_at | DateTime | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DateTime | 更新时间 | DEFAULT CURRENT_TIMESTAMP |

## 5. 任务表 (tasks)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | Integer | 主键 | PK, AI |
| project_id | Integer | 项目ID | FK(projects.id) |
| sprint_id | Integer | 迭代ID | FK(sprints.id) |
| title | String(200) | 任务标题 | NOT NULL |
| description | Text | 任务描述 | |
| status | String(20) | 任务状态 | NOT NULL |
| priority | String(20) | 优先级 | NOT NULL |
| assignee_id | Integer | 负责人ID | FK(users.id) |
| estimated_hours | Float | 预估工时 | |
| actual_hours | Float | 实际工时 | |
| created_at | DateTime | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DateTime | 更新时间 | DEFAULT CURRENT_TIMESTAMP |

## 6. 成本记录表 (cost_records)

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| id | Integer | 主键 | PK, AI |
| project_id | Integer | 项目ID | FK(projects.id) |
| amount | Float | 金额 | NOT NULL |
| description | String(200) | 描述 | NOT NULL |
| date | Date | 日期 | NOT NULL |
| category | String(50) | 类别 | NOT NULL |
| created_at | DateTime | 创建时间 | DEFAULT CURRENT_TIMESTAMP |
| updated_at | DateTime | 更新时间 | DEFAULT CURRENT_TIMESTAMP |

## 7. 表关系

### 7.1 一对多关系
- 项目(projects) -> 迭代(sprints)
- 项目(projects) -> 任务(tasks)
- 项目(projects) -> 成本记录(cost_records)
- 迭代(sprints) -> 任务(tasks)
- 用户(users) -> 任务(tasks) [assignee]

### 7.2 多对多关系
- 项目(projects) <-> 用户(users) [通过project_members表]

## 8. 索引设计

### 8.1 主键索引
- 所有表的主键id字段

### 8.2 唯一索引
- users.username
- users.email
- project_members(project_id, user_id)

### 8.3 普通索引
- projects.status
- tasks.status
- tasks.priority
- tasks.assignee_id
- cost_records.date
- cost_records.category

## 9. 数据库配置

### 9.1 字符集
- 使用UTF-8字符集
- 排序规则：utf8mb4_unicode_ci

### 9.2 存储引擎
- 使用InnoDB引擎
- 支持事务和外键约束

### 9.3 连接池配置
- 最大连接数：100
- 最小空闲连接：10
- 连接超时：30秒 