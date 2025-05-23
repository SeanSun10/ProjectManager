# 开发规范文档

## 1. 代码规范

### 1.1 Python代码规范
- 遵循PEP 8规范
- 使用4个空格缩进
- 行长度限制在120字符以内
- 使用类型注解
- 所有函数必须有文档字符串
- 使用英文命名变量和函数
- 类名使用驼峰命名法
- 函数和变量使用下划线命名法

### 1.2 数据库模型规范
- 表名使用复数形式
- 主键统一使用id
- 创建时间和更新时间字段统一命名为created_at和updated_at
- 外键关系必须定义relationship
- 所有字符串字段必须指定长度限制
- 必须包含适当的索引

### 1.3 API规范
- 使用RESTful风格
- URL使用小写字母，单词间用连字符(-)分隔
- 使用适当的HTTP方法（GET, POST, PUT, DELETE）
- 返回统一的状态码
- 错误响应格式统一
- API版本控制
- 分页参数统一使用skip和limit

### 1.4 数据验证规范
- 使用Pydantic模型进行数据验证
- 每个数据库模型对应三个Pydantic模型：
  - Base: 基础字段
  - Create: 创建时使用
  - Response: 响应时使用
- 所有可选字段必须指定默认值
- 日期时间字段统一使用datetime类型

## 2. 命名规范

### 2.1 文件命名
- 使用小写字母
- 单词间使用下划线连接
- 测试文件以test_开头
- 配置文件使用全小写

### 2.2 变量命名
- 使用小写字母
- 单词间使用下划线连接
- 常量使用大写字母
- 私有变量以单下划线开头

### 2.3 类命名
- 使用驼峰命名法
- 模型类使用单数形式
- 工具类以Utils结尾
- 异常类以Error结尾

## 3. 注释规范

### 3.1 文件注释
```python
"""
模块描述
作者：xxx
创建时间：YYYY-MM-DD
最后修改：YYYY-MM-DD
"""
```

### 3.2 函数注释
```python
def function_name(param1: type1, param2: type2) -> return_type:
    """
    函数功能描述

    Args:
        param1: 参数1描述
        param2: 参数2描述

    Returns:
        返回值描述

    Raises:
        异常描述
    """
```

### 3.3 类注释
```python
class ClassName:
    """
    类功能描述

    Attributes:
        attr1: 属性1描述
        attr2: 属性2描述
    """
```

## 4. 错误处理规范

### 4.1 HTTP状态码使用
- 200: 成功
- 201: 创建成功
- 400: 请求错误
- 401: 未认证
- 403: 未授权
- 404: 资源不存在
- 422: 数据验证错误
- 500: 服务器错误

### 4.2 错误响应格式
```json
{
    "detail": "错误描述信息",
    "code": "错误代码",
    "timestamp": "错误发生时间"
}
```

## 5. 数据库操作规范

### 5.1 查询操作
- 使用SQLAlchemy ORM
- 复杂查询使用join
- 必须处理查询结果为空的情况
- 使用适当的索引优化查询

### 5.2 事务处理
- 使用with语句管理事务
- 异常时自动回滚
- 批量操作使用事务

## 6. 安全规范

### 6.1 认证授权
- 使用JWT进行身份认证
- 密码必须加密存储
- 敏感信息不得明文传输
- 实现适当的权限控制

### 6.2 数据验证
- 所有输入数据必须验证
- 防止SQL注入
- 防止XSS攻击
- 防止CSRF攻击

## 7. 测试规范

### 7.1 测试文件组织
- 测试文件与源代码文件对应
- 测试类名以Test开头
- 测试方法名以test_开头

### 7.2 测试覆盖
- 单元测试覆盖率要求>80%
- 必须测试异常情况
- 必须测试边界条件
- 关键业务逻辑必须有集成测试

## API路由规范

### 路由定义
1. 在 `app/api/v1` 目录下创建模块文件
2. 使用 `APIRouter` 创建路由
3. 路由路径不应包含重复的前缀

### 路由注册
1. 在 `app/api/v1/api.py` 中注册路由
2. 使用 `prefix` 参数指定路由前缀
3. 使用 `tags` 参数添加API标签

### 示例
```python
# 在模块文件中
router = APIRouter()

@router.get("")
async def get_items():
    return {"items": []}

# 在api.py中
api_router.include_router(items.router, prefix="/items", tags=["items"])
```

## 前端开发规范

### 组件规范
1. 使用Vue 3组合式API
2. 保持组件单一职责
3. 使用TypeScript进行类型检查

### 状态管理
1. 使用Pinia进行状态管理
2. 遵循单一数据源原则
3. 使用适当的模块化

### API调用
1. 使用统一的请求工具
2. 处理错误情况
3. 使用适当的加载状态

### 样式规范
1. 使用SCSS预处理器
2. 遵循BEM命名规范
3. 保持样式模块化 