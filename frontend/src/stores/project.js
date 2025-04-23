import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'

export const useProjectStore = defineStore('project', () => {
  // 状态
  const projects = ref([])
  const currentProject = ref(null)
  const projectStats = ref({
    taskStats: {
      total: 0,
      inProgress: 0,
      completed: 0
    },
    timeStats: {
      estimated: 0,
      actual: 0
    },
    costStats: {
      fixed: 0,
      human: 0
    }
  })
  const recentActivities = ref([])
  const loading = ref(false)
  const error = ref(null)

  // 获取项目列表
  const fetchProjects = async () => {
    try {
      loading.value = true
      const response = await request.get('projects')
      // 确保 response 是数组
      projects.value = Array.isArray(response) ? response : []
    } catch (err) {
      error.value = err.message
      projects.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取项目详情
  const fetchProject = async (id) => {
    if (!id) {
      console.error('项目ID不能为空')
      throw new Error('项目ID不能为空')
    }

    try {
      loading.value = true
      error.value = null
      console.log('开始获取项目详情，ID:', id)
      const response = await request.get(`projects/${id}`)
      console.log('获取到的项目数据:', response)
      
      if (!response) {
        throw new Error('未找到项目数据')
      }

      currentProject.value = response
      console.log('更新后的 currentProject:', currentProject.value)
      return response
    } catch (err) {
      console.error('获取项目详情失败:', err)
      error.value = err.response?.data?.detail || err.message
      currentProject.value = null
      throw err
    } finally {
      loading.value = false
    }
  }

  // 创建项目
  const createProject = async (projectData) => {
    try {
      loading.value = true
      const response = await request.post('projects', projectData)
      projects.value.push(response)
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新项目
  const updateProject = async (id, projectData) => {
    try {
      loading.value = true
      const response = await request.put(`projects/${id}`, projectData)
      const index = projects.value.findIndex(p => p.id === id)
      if (index !== -1) {
        projects.value[index] = response
      }
      if (currentProject.value?.id === id) {
        currentProject.value = response
      }
      return response
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 删除项目
  const deleteProject = async (id) => {
    try {
      loading.value = true
      await request.delete(`projects/${id}`)
      projects.value = projects.value.filter(p => p.id !== id)
      if (currentProject.value?.id === id) {
        currentProject.value = null
      }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取项目统计数据
  const fetchProjectStats = async (projectId) => {
    if (!projectId) {
      console.error('项目ID不能为空')
      throw new Error('项目ID不能为空')
    }

    try {
      loading.value = true
      error.value = null
      const response = await request.get(`projects/${projectId}/stats`)
      
      if (!response) {
        throw new Error('未找到项目统计数据')
      }

      projectStats.value = {
        taskStats: {
          total: response.taskStats?.total ?? 0,
          inProgress: response.taskStats?.inProgress ?? 0,
          completed: response.taskStats?.completed ?? 0
        },
        timeStats: {
          estimated: response.timeStats?.estimated ?? 0,
          actual: response.timeStats?.actual ?? 0
        },
        costStats: {
          fixed: response.costStats?.fixed ?? 0,
          human: response.costStats?.human ?? 0
        }
      }
      return projectStats.value
    } catch (err) {
      console.error('获取项目统计数据失败:', err)
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取项目最近活动
  const fetchRecentActivities = async (projectId) => {
    if (!projectId) {
      console.error('项目ID不能为空')
      throw new Error('项目ID不能为空')
    }

    try {
      loading.value = true
      error.value = null
      const response = await request.get(`projects/${projectId}/activities`)
      
      if (!response) {
        throw new Error('未找到项目活动数据')
      }

      recentActivities.value = Array.isArray(response) ? response : []
      return recentActivities.value
    } catch (err) {
      console.error('获取项目活动数据失败:', err)
      error.value = err.response?.data?.detail || err.message
      recentActivities.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  // 重置状态
  const reset = () => {
    projects.value = []
    currentProject.value = null
    projectStats.value = {
      taskStats: { total: 0, inProgress: 0, completed: 0 },
      timeStats: { estimated: 0, actual: 0 },
      costStats: { fixed: 0, human: 0 }
    }
    recentActivities.value = []
    loading.value = false
    error.value = null
  }

  return {
    // 状态
    projects,
    currentProject,
    projectStats,
    recentActivities,
    loading,
    error,
    // 方法
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    fetchProjectStats,
    fetchRecentActivities,
    reset
  }
}) 