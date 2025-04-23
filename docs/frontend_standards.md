# 前端开发规范

## Vue 组件开发规范

### 1. 组件设计原则

#### 1.1 状态管理
- 使用组合式 API 时，将相关的状态和逻辑组织在一起
- 使用 `reactive` 管理复杂状态，使用 `ref` 管理简单状态
- 避免在异步函数内部注册生命周期钩子
- 在组件卸载时正确清理所有资源

#### 1.2 组件接口
- 使用 `v-model` 时遵循 Vue 3 规范（`modelValue` 和 `update:modelValue`）
- 为组件属性提供完整的默认值结构
- 使用可选链操作符处理可能的空值
- 添加适当的类型定义和验证

#### 1.3 错误处理
- 为所有异步操作添加 `try/catch/finally` 块
- 使用统一的错误提示方式
- 确保在错误发生后正确重置状态
- 添加适当的错误日志记录

### 2. 性能优化指南

#### 2.1 资源管理
- 及时清理不再使用的资源（事件监听器、定时器、观察者等）
- 使用 `onBeforeUnmount` 统一处理资源清理
- 避免内存泄漏

#### 2.2 状态更新
- 避免不必要的状态更新
- 合理使用计算属性和监听器
- 优化状态更新逻辑
- 使用防抖和节流处理频繁的状态更新

#### 2.3 组件渲染
- 合理使用 `v-show` 和 `v-if`
- 优化条件渲染逻辑
- 避免不必要的组件重渲染

### 3. 代码组织规范

#### 3.1 文件结构
- 保持文件结构清晰
- 相关功能代码分组存放
- 使用有意义的文件名和目录名

#### 3.2 代码格式
- 使用统一的代码格式化工具
- 保持一致的缩进和空格使用
- 合理使用空行分隔代码块

#### 3.3 注释规范
- 为复杂逻辑添加适当的注释
- 使用清晰的注释说明代码意图
- 保持注释的及时更新

### 4. 最佳实践示例

#### 4.1 组件状态管理
```javascript
// 使用 reactive 管理复杂状态
const state = reactive({
  loading: false,
  submitting: false,
  dialogVisible: false,
  isActive: false
})

// 使用 ref 管理简单状态
const count = ref(0)
```

#### 4.2 错误处理
```javascript
try {
  state.loading = true
  await someAsyncOperation()
} catch (error) {
  console.error('操作失败:', error)
  ElMessage.error('操作失败')
} finally {
  state.loading = false
}
```

#### 4.3 资源清理
```javascript
onBeforeUnmount(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
    resizeHandler = null
  }
})
```

#### 4.4 属性验证
```javascript
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  data: {
    type: Object,
    default: () => ({
      id: null,
      name: '',
      description: ''
    })
  }
})
```

### 5. 工具和库的使用规范

#### 5.1 Element Plus
- 遵循 Element Plus 的设计规范
- 合理使用组件提供的属性和事件
- 保持样式的一致性

#### 5.2 ECharts
- 正确处理图表容器的初始化
- 优化图表数据的更新逻辑
- 及时清理图表实例

#### 5.3 Vue Router
- 合理使用路由守卫
- 优化路由懒加载
- 正确处理路由参数

### 6. 测试规范

#### 6.1 单元测试
- 为关键功能编写单元测试
- 使用有意义的测试用例名称
- 保持测试代码的可维护性

#### 6.2 集成测试
- 测试组件间的交互
- 验证数据流
- 确保功能完整性

### 7. 文档规范

#### 7.1 代码注释
- 使用 JSDoc 格式的注释
- 为公共 API 添加文档
- 保持注释的准确性

#### 7.2 组件文档
- 提供组件的使用说明
- 列出所有属性和事件
- 包含示例代码

### 8. 版本控制规范

#### 8.1 提交信息
- 使用清晰的提交信息
- 遵循约定的提交格式
- 关联相关的 issue

#### 8.2 分支管理
- 遵循 Git Flow 工作流
- 合理使用分支
- 保持代码库的整洁 