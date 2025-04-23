# 组件接口文档

## SprintCard 组件

### 功能描述
用于显示单个迭代的详细信息，包括基本信息、任务列表、统计数据和燃尽图。

### 属性
| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| sprint | Object | 是 | - | 迭代数据对象 |
| loading | Boolean | 否 | false | 加载状态 |

### 事件
| 事件名 | 参数 | 说明 |
|--------|------|------|
| edit | sprint | 编辑迭代 |
| delete | sprint | 删除迭代 |
| add-task | sprint | 添加任务到迭代 |
| edit-task | task | 编辑任务 |
| remove-task | (sprint, task) | 从迭代中移除任务 |

### 示例
```vue
<sprint-card
  :sprint="sprint"
  :loading="loading"
  @edit="handleEditSprint"
  @delete="handleDeleteSprint"
  @add-task="handleAddTask"
  @edit-task="handleEditTask"
  @remove-task="handleRemoveTask"
/>
```

## SprintDialog 组件

### 功能描述
用于创建和编辑迭代的对话框组件。

### 属性
| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| modelValue | Boolean | 是 | false | 对话框显示状态 |
| sprint | Object | 否 | 见默认值 | 迭代数据对象 |

### 默认值
```javascript
{
  id: null,
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'PLANNING'
}
```

### 事件
| 事件名 | 参数 | 说明 |
|--------|------|------|
| update:modelValue | Boolean | 更新对话框显示状态 |
| submit | Object | 提交表单数据 |

### 表单验证规则
```javascript
{
  name: [
    { required: true, message: '请输入迭代名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入迭代描述', trigger: 'blur' },
    { max: 500, message: '长度不能超过 500 个字符', trigger: 'blur' }
  ],
  start_date: [
    { required: true, message: '请选择开始日期', trigger: 'change' }
  ],
  end_date: [
    { required: true, message: '请选择结束日期', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择迭代状态', trigger: 'change' }
  ]
}
```

### 示例
```vue
<sprint-dialog
  v-model="dialogVisible"
  :sprint="sprintForm"
  @submit="handleSubmit"
/>
```

## ProjectSprints 组件

### 功能描述
用于管理项目迭代列表的组件。

### 属性
| 属性名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| projectId | Number | 是 | - | 项目ID |

### 状态管理
```javascript
const state = reactive({
  loading: false,
  submitting: false,
  dialogVisible: false,
  isActive: false,
  isInitialized: false
})
```

### 数据流
1. 组件挂载时获取迭代列表
2. 支持创建、编辑、删除迭代
3. 支持添加、编辑、移除任务
4. 自动更新迭代统计数据和燃尽图

### 示例
```vue
<project-sprints
  :project-id="projectId"
/>
``` 