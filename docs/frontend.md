# 前端开发规范文档

## 1. Vue.js开发规范

### 1.1 项目结构
```
frontend/
├── public/              # 静态资源
├── src/
│   ├── assets/         # 项目资源
│   ├── components/     # 公共组件
│   │   ├── Layout.vue  # 全局布局组件
│   │   └── ...
│   ├── views/          # 页面组件
│   ├── router/         # 路由配置
│   ├── stores/         # Pinia状态管理
│   │   ├── layout.js   # 布局状态管理
│   │   └── ...
│   ├── utils/          # 工具函数
│   ├── api/            # API接口
│   ├── styles/         # 全局样式
│   ├── App.vue         # 根组件
│   └── main.js         # 入口文件
```

### 1.2 组件规范
- 使用组合式API (Composition API)
- 组件名使用PascalCase
- 组件文件名与组件名保持一致
- 视图组件（views目录下的组件）采用简单明了的命名，不添加View后缀
  - 正确示例：`Login.vue`, `Home.vue`, `ProjectDetail.vue`
  - 错误示例：`LoginView.vue`, `HomeView.vue`, `ProjectDetailView.vue`
- Props定义必须包含类型和默认值
- 事件名使用kebab-case
- 组件必须包含name属性

### 1.3 代码风格
- 使用ESLint + Prettier
- 缩进使用2个空格
- 字符串使用单引号
- 行末不添加分号
- 使用箭头函数
- 使用const/let替代var

### 1.4 状态管理
- 使用Pinia进行状态管理
- Store命名使用camelCase
- 状态必须定义类型
- 修改状态必须通过actions
- 异步操作使用async/await

## 2. 组件开发规范

### 2.1 布局规范
- 使用统一的 `Layout.vue` 作为全局布局组件
- 布局相关的状态管理统一放在 `stores/layout.js` 中
- 菜单配置统一在 `layoutStore` 中管理
- 布局组件结构：
  ```vue
  <template>
    <el-container class="layout-container">
      <!-- 侧边栏 -->
      <el-aside :width="layoutStore.isCollapsed ? '64px' : '200px'">
        <div class="logo-container">
          <img src="@/assets/logo.svg" alt="Logo" class="logo" />
          <span class="logo-text" v-show="!layoutStore.isCollapsed">项目管理系统</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="side-menu"
          :collapse="layoutStore.isCollapsed"
          router
        >
          <el-menu-item 
            v-for="item in layoutStore.menuItems"
            :key="item.path"
            :index="item.path"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <template #title>{{ item.title }}</template>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部导航 -->
        <el-header>
          <div class="header-content">
            <!-- 折叠按钮 -->
            <div class="header-left">
              <el-button
                class="collapse-btn"
                @click="layoutStore.toggleCollapse"
              >
                <el-icon>
                  <component :is="layoutStore.isCollapsed ? 'Expand' : 'Fold'" />
                </el-icon>
              </el-button>
              <!-- 面包屑导航 -->
              <el-breadcrumb>
                <el-breadcrumb-item 
                  v-for="item in layoutStore.breadcrumbs"
                  :key="item.path"
                  :to="{ path: item.path }"
                >
                  {{ item.title }}
                </el-breadcrumb-item>
              </el-breadcrumb>
            </div>
            <!-- 用户信息 -->
            <div class="user-info">
              <!-- 用户信息内容 -->
            </div>
          </div>
        </el-header>
        
        <!-- 内容区 -->
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </template>
  ```
- 布局组件功能：
  - 响应式侧边栏，支持折叠展开
  - 动态面包屑导航，自动根据路由更新
  - 用户信息展示与操作（登出、设置等）
  - 权限控制的菜单项显示
  - 路由切换时的加载状态

### 2.2 菜单配置规范
- 菜单配置统一在 `layoutStore` 中管理
- 菜单项配置应包含：
  ```javascript
  {
    path: '/path',        // 路由路径
    title: '菜单标题',    // 菜单显示文本
    icon: 'IconName'      // Element Plus 图标名称
  }
  ```
- 菜单项顺序应遵循业务逻辑和用户使用频率
- 新增菜单项时，需要同时更新：
  1. `layoutStore` 中的 `menuItems` 数组
  2. `router/index.js` 中的路由配置
  3. 对应的视图组件

### 2.3 页面布局规范
- 页面内容应位于 Layout 的 main 区域
- 使用统一的页面结构：
  ```vue
  <template>
    <div class="page-container">
      <!-- 页面标题区 -->
      <div class="page-header">
        <h1>页面标题</h1>
        <div class="page-actions">
          <!-- 页面操作按钮 -->
        </div>
      </div>
      
      <!-- 页面主内容 -->
      <div class="page-content">
        <!-- 内容区域 -->
      </div>
    </div>
  </template>
  ```
- 遵循统一的间距和样式规范
- 适配不同屏幕尺寸

### 2.4 组件结构
```vue
<template>
  <div class="component-name">
    <!-- 模板内容 -->
  </div>
</template>

<script setup>
// 导入
import { ref, onMounted } from 'vue'
import { useStore } from '@/stores/store'

// Props定义
const props = defineProps({
  propName: {
    type: String,
    required: true,
    default: ''
  }
})

// 事件定义
const emit = defineEmits(['eventName'])

// 响应式数据
const data = ref(null)

// 计算属性
const computedData = computed(() => {
  return data.value
})

// 方法
const handleClick = () => {
  emit('eventName', data.value)
}

// 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style scoped>
.component-name {
  /* 样式定义 */
}
</style>
```

### 2.5 组件通信
- 父传子：使用props
- 子传父：使用emit
- 兄弟组件：使用Pinia
- 深层组件：使用provide/inject

## 3. 路由规范

### 3.1 路由配置
- 路由配置示例:
```javascript
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '登录'
    }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/projects',
    children: [
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('@/views/Projects.vue'),
        meta: {
          title: '项目管理',
          requiresAuth: true
        }
      },
      {
        path: 'projects/:id',
        name: 'ProjectDetail',
        component: () => import('@/views/ProjectDetail.vue'),
        meta: {
          title: '项目详情',
          requiresAuth: true
        }
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('@/views/Tasks.vue'),
        meta: {
          title: '任务管理',
          requiresAuth: true
        }
      },
      {
        path: 'tasks/:id',
        name: 'TaskDetail',
        component: () => import('@/views/TaskDetail.vue'),
        meta: {
          title: '任务详情',
          requiresAuth: true
        }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('@/views/Statistics.vue'),
        meta: {
          title: '统计分析',
          requiresAuth: true
        }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/Profile.vue'),
        meta: {
          title: '个人中心',
          requiresAuth: true
        }
      },
      {
        path: 'system-settings',
        name: 'SystemSettings',
        component: () => import('@/views/SystemSettings.vue'),
        meta: {
          title: '系统设置',
          requiresAuth: true,
          requiresAdmin: true
        }
      }
    ]
  }
]
```

### 3.2 路由守卫
- 使用全局前置守卫进行权限控制
- 路由元信息应包含：
  - title: 页面标题
  - requiresAuth: 是否需要登录
  - requiresAdmin: 是否需要管理员权限
  - keepAlive: 是否缓存组件

### 3.3 动态路由
- 动态路由应在用户登录后加载
- 动态路由配置应与后端权限系统保持一致
- 动态路由变更后需要更新菜单配置

## 4. 状态管理规范

### 4.1 Store 结构
```javascript
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useStore = defineStore('storeName', () => {
  // 状态
  const state = ref(null)
  
  // 计算属性
  const computedState = computed(() => {
    return state.value
  })
  
  // 方法
  const action = async () => {
    // 异步操作
  }
  
  return {
    state,
    computedState,
    action
  }
})
```

### 4.2 状态命名
- 状态名应使用 camelCase
- 状态名应具有描述性
- 避免使用过于通用的状态名

### 4.3 状态更新
- 状态更新必须通过 actions
- 异步操作使用 async/await
- 错误处理必须完善
- 状态重置方法必须提供

## 5. 样式规范

### 5.1 CSS 命名
- 使用 BEM 命名规范
- 类名使用 kebab-case
- 避免使用过于通用的类名

### 5.2 样式组织
- 全局样式放在 styles 目录
- 组件样式使用 scoped
- 公共样式使用 mixin
- 主题变量使用 CSS 变量

### 5.3 响应式设计
- 使用 Element Plus 的响应式工具类
- 移动端优先
- 断点设置：
  - xs: < 768px
  - sm: ≥ 768px
  - md: ≥ 992px
  - lg: ≥ 1200px
  - xl: ≥ 1920px

## 6. 性能优化

### 6.1 代码分割
- 路由组件使用动态导入
- 大型组件使用异步组件
- 第三方库按需加载

### 6.2 缓存策略
- 使用 keep-alive 缓存页面
- 合理使用 localStorage
- 实现数据预加载

### 6.3 资源优化
- 图片使用 webp 格式
- 使用 CDN 加速
- 启用 gzip 压缩

## 7. 测试规范

### 7.1 单元测试
- 使用Vitest
- 测试组件渲染
- 测试事件处理
- 测试状态变化

### 7.2 E2E测试
- 使用Cypress
- 测试用户流程
- 测试表单提交
- 测试页面跳转

## 8. 任务和迭代管理规范

### 8.1 任务管理组件
- 任务列表组件 (`TaskList.vue`)
  - 显示项目所有任务
  - 支持任务创建、编辑、删除
  - 支持任务状态和优先级管理
  - 支持任务分配和工时记录
  - 支持任务与迭代关联

- 任务表单组件
  - 必填字段：标题、状态、优先级、负责人
  - 选填字段：描述、所属迭代、预计工时、实际工时、截止日期
  - 表单验证规则：
    ```javascript
    {
      title: [{ required: true, message: '请输入任务标题', trigger: 'blur' }],
      status: [{ required: true, message: '请选择任务状态', trigger: 'change' }],
      priority: [{ required: true, message: '请选择任务优先级', trigger: 'change' }],
      assignee_id: [{ required: true, message: '请选择负责人', trigger: 'change' }]
    }
    ```

### 8.2 迭代管理组件
- 迭代列表组件 (`ProjectSprints.vue`)
  - 显示项目所有迭代
  - 支持迭代创建、编辑、删除
  - 支持迭代状态管理
  - 支持迭代任务管理
  - 支持迭代统计和燃尽图

- 迭代表单组件
  - 必填字段：名称、描述、开始日期、结束日期、状态
  - 表单验证规则：
    ```javascript
    {
      name: [{ required: true, message: '请输入迭代名称', trigger: 'blur' }],
      description: [{ required: true, message: '请输入迭代描述', trigger: 'blur' }],
      start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
      end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }],
      status: [{ required: true, message: '请选择迭代状态', trigger: 'change' }]
    }
    ```

### 8.3 任务统计功能
- 任务状态统计
  - 总任务数
  - 已完成任务数
  - 进行中任务数
  - 待办任务数

- 工时统计
  - 预估总工时
  - 实际总工时
  - 工时偏差（实际-预估）
  - 偏差样式：正偏差显示红色，负偏差显示绿色

### 8.4 燃尽图实现
- 使用 ECharts 实现燃尽图
- 图表配置：
  ```javascript
  {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['理想线', '实际线']
    },
    xAxis: {
      type: 'category',
      data: xAxisData
    },
    yAxis: {
      type: 'value',
      name: '剩余任务数'
    },
    series: [
      {
        name: '理想线',
        type: 'line',
        data: idealLineData,
        itemStyle: { color: '#409EFF' }
      },
      {
        name: '实际线',
        type: 'line',
        data: actualLineData,
        itemStyle: { color: '#67C23A' }
      }
    ]
  }
  ```

### 8.5 状态管理
- 任务状态管理 (`taskStore`)
  - 任务列表
  - 任务创建
  - 任务更新
  - 任务删除
  - 任务查询

- 迭代状态管理 (`sprintStore`)
  - 迭代列表
  - 迭代创建
  - 迭代更新
  - 迭代删除
  - 迭代查询
  - 迭代任务管理

### 8.6 样式规范
- 任务列表样式
  ```css
  .task-list {
    padding: 20px;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  ```

- 迭代卡片样式
  ```css
  .sprint-card {
    margin-bottom: 10px;
  }
  .sprint-content {
    color: #606266;
  }
  .sprint-stats {
    margin-top: 20px;
    border-top: 1px solid #EBEEF5;
    padding-top: 20px;
  }
  ```

- 统计卡片样式
  ```css
  .stats-item {
    text-align: center;
    padding: 10px;
    background-color: #F5F7FA;
    border-radius: 4px;
  }
  .stats-value {
    font-size: 24px;
    font-weight: bold;
    color: #303133;
  }
  .stats-value.positive {
    color: #F56C6C;
  }
  .stats-value.negative {
    color: #67C23A;
  }
  ``` 