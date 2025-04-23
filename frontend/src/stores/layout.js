import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useLayoutStore = defineStore('layout', () => {
  // 菜单配置
  const menuItems = [
    { path: '/', title: '首页', icon: 'House' },
    { path: '/projects', title: '项目管理', icon: 'Folder' },
    { path: '/tasks', title: '任务管理', icon: 'List' },
    { path: '/sprints', title: '迭代管理', icon: 'Timer' },
    { path: '/statistics', title: '统计分析', icon: 'DataLine' },
    { path: '/team-members', title: '团队成员管理', icon: 'User' }
  ]

  // 侧边栏折叠状态
  const isCollapsed = ref(false)
  
  // 面包屑数据
  const breadcrumbs = ref([])

  // 切换侧边栏状态
  const toggleCollapse = () => {
    isCollapsed.value = !isCollapsed.value
  }

  // 更新面包屑
  const updateBreadcrumbs = (route) => {
    const crumbs = []
    crumbs.push({ title: '首页', path: '/' })
    
    if (route.meta.title) {
      crumbs.push({
        title: route.meta.title,
        path: route.path
      })
    }
    
    breadcrumbs.value = crumbs
  }

  return {
    menuItems,
    isCollapsed,
    breadcrumbs,
    toggleCollapse,
    updateBreadcrumbs
  }
}) 