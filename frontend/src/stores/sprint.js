import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'

export const useSprintStore = defineStore('sprint', () => {
  // 状态
  const sprints = ref([])
  const currentSprint = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // 获取项目下的迭代列表
  const fetchSprintsByProject = async (projectId) => {
    if (!projectId) {
      console.error('项目ID不能为空')
      throw new Error('项目ID不能为空')
    }

    try {
      loading.value = true
      error.value = null
      const response = await request.get(`sprints/project/${projectId}`)
      sprints.value = Array.isArray(response) ? response : []
      return sprints.value
    } catch (err) {
      console.error('获取迭代列表失败:', err)
      error.value = err.response?.data?.detail || err.message
      sprints.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取迭代详情
  const fetchSprint = async (sprintId) => {
    if (!sprintId) {
      console.error('迭代ID不能为空')
      throw new Error('迭代ID不能为空')
    }

    try {
      loading.value = true
      error.value = null
      const response = await request.get(`sprints/${sprintId}`)
      currentSprint.value = response
      return response
    } catch (err) {
      console.error('获取迭代详情失败:', err)
      error.value = err.response?.data?.detail || err.message
      currentSprint.value = null
      throw err
    } finally {
      loading.value = false
    }
  }

  // 创建迭代
  const createSprint = async (sprintData) => {
    try {
      loading.value = true
      error.value = null
      const response = await request.post('sprints', sprintData)
      sprints.value.push(response)
      return response
    } catch (err) {
      console.error('创建迭代失败:', err)
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新迭代
  const updateSprint = async (sprintId, sprintData) => {
    try {
      loading.value = true
      error.value = null
      const response = await request.put(`sprints/${sprintId}`, sprintData)
      const index = sprints.value.findIndex(s => s.id === sprintId)
      if (index !== -1) {
        sprints.value[index] = response
      }
      if (currentSprint.value?.id === sprintId) {
        currentSprint.value = response
      }
      return response
    } catch (err) {
      console.error('更新迭代失败:', err)
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 删除迭代
  const deleteSprint = async (sprintId) => {
    try {
      loading.value = true
      error.value = null
      await request.delete(`sprints/${sprintId}`)
      sprints.value = sprints.value.filter(s => s.id !== sprintId)
      if (currentSprint.value?.id === sprintId) {
        currentSprint.value = null
      }
      return true
    } catch (err) {
      console.error('删除迭代失败:', err)
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 重置状态
  const reset = () => {
    sprints.value = []
    currentSprint.value = null
    loading.value = false
    error.value = null
  }

  return {
    // 状态
    sprints,
    currentSprint,
    loading,
    error,
    // 方法
    fetchSprintsByProject,
    fetchSprint,
    createSprint,
    updateSprint,
    deleteSprint,
    reset
  }
}) 