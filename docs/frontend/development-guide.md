# 前端开发规范指南

## 1. 组件化规范

### 1.1 组件职责
- 每个组件应该只负责一个特定的功能
- 组件应该保持简单，避免过度复杂化
- 可复用的组件应该放在 `src/components` 目录下
- 页面级组件应该放在 `src/views` 目录下

### 1.2 组件命名
- 组件名使用 PascalCase 命名法
- 文件名与组件名保持一致
- 组件名应该具有描述性，表明其功能

### 1.3 组件结构
```vue
<template>
  <!-- 模板部分 -->
</template>

<script setup>
// 导入部分
// 组件逻辑
</script>

<style scoped>
/* 样式部分 */
</style>
```

## 2. 状态管理规范

### 2.1 Store 组织
- 使用 Pinia 进行状态管理
- 每个功能模块应该有独立的 store
- store 文件应该放在 `src/stores` 目录下
- store 命名应该清晰表明其功能

### 2.2 数据流
- 组件通过 store 获取和修改数据
- 避免组件之间直接传递复杂数据
- 使用计算属性处理派生数据

## 3. 代码组织规范

### 3.1 目录结构
```
src/
  ├── components/     # 可复用组件
  ├── views/          # 页面组件
  ├── stores/         # 状态管理
  ├── constants/      # 常量定义
  ├── utils/          # 工具函数
  ├── api/            # API 接口
  └── assets/         # 静态资源
```

### 3.2 常量管理
- 将常量定义在 `constants` 目录下
- 使用大写字母和下划线命名常量
- 相关的常量应该组织在同一个文件中

### 3.3 工具函数
- 通用的工具函数放在 `utils` 目录下
- 函数应该保持单一职责
- 使用 TypeScript 类型定义

## 4. 样式规范

### 4.1 CSS 命名
- 使用 BEM 命名规范
- 类名应该具有描述性
- 避免使用过于通用的类名

### 4.2 样式组织
- 使用 scoped 样式
- 避免全局样式污染
- 使用 CSS 变量管理主题色

## 5. 性能优化

### 5.1 组件优化
- 使用 `v-if` 和 `v-show` 适当
- 避免不必要的组件重渲染
- 使用 `computed` 缓存计算结果

### 5.2 数据优化
- 合理使用分页
- 避免一次性加载过多数据
- 使用防抖和节流处理频繁操作

## 6. 错误处理

### 6.1 错误捕获
- 使用 try-catch 处理异步操作
- 提供友好的错误提示
- 记录错误日志

### 6.2 用户反馈
- 使用 Element Plus 的消息提示
- 提供清晰的操作反馈
- 保持错误信息的一致性

## 7. 代码质量

### 7.1 代码风格
- 使用 ESLint 进行代码检查
- 遵循 Vue 3 最佳实践
- 保持代码格式一致

### 7.2 注释规范
- 为复杂逻辑添加注释
- 使用 JSDoc 格式注释
- 保持注释的及时更新

## 8. 测试规范

### 8.1 单元测试
- 为关键功能编写测试
- 使用 Jest 进行测试
- 保持测试覆盖率

### 8.2 组件测试
- 测试组件的各种状态
- 模拟用户交互
- 验证组件行为 