import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'

export const useCostStore = defineStore('cost', () => {
  // 状态
  const costs = ref([])
  const costStats = ref({
    fixed: 0,
    human: 0,
    other: 0
  })
  const loading = ref(false)
  const error = ref(null)

  // 获取项目下的成本列表
  const fetchCostsByProject = async (projectId) => {
    if (!projectId) {
      console.error('项目ID不能为空')
      throw new Error('项目ID不能为空')
    }

    try {
      loading.value = true
      error.value = null
      const response = await request.get(`costs/project/${projectId}`)
      costs.value = Array.isArray(response) ? response : []
      return costs.value
    } catch (err) {
      console.error('获取成本列表失败:', err)
      error.value = err.response?.data?.detail || err.message
      costs.value = []
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取成本统计
  const fetchCostStats = async (projectId) => {
    if (!projectId) {
      console.error('项目ID不能为空')
      throw new Error('项目ID不能为空')
    }

    try {
      loading.value = true
      error.value = null
      const response = await request.get(`costs/project/${projectId}/stats`)
      costStats.value = response || {
        fixed: 0,
        human: 0,
        other: 0
      }
      return costStats.value
    } catch (err) {
      console.error('获取成本统计失败:', err)
      error.value = err.response?.data?.detail || err.message
      costStats.value = {
        fixed: 0,
        human: 0,
        other: 0
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  // 创建成本记录
  const createCost = async (costData) => {
    try {
      loading.value = true
      error.value = null
      const response = await request.post('costs', costData)
      costs.value.push(response)
      return response
    } catch (err) {
      console.error('创建成本记录失败:', err)
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新成本记录
  const updateCost = async (costId, costData) => {
    try {
      loading.value = true
      error.value = null
      const response = await request.put(`costs/${costId}`, costData)
      const index = costs.value.findIndex(c => c.id === costId)
      if (index !== -1) {
        costs.value[index] = response
      }
      return response
    } catch (err) {
      console.error('更新成本记录失败:', err)
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 删除成本记录
  const deleteCost = async (costId) => {
    try {
      loading.value = true
      error.value = null
      await request.delete(`costs/${costId}`)
      costs.value = costs.value.filter(c => c.id !== costId)
      return true
    } catch (err) {
      console.error('删除成本记录失败:', err)
      error.value = err.response?.data?.detail || err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  // 重置状态
  const reset = () => {
    costs.value = []
    costStats.value = {
      fixed: 0,
      human: 0,
      other: 0
    }
    loading.value = false
    error.value = null
  }

  return {
    // 状态
    costs,
    costStats,
    loading,
    error,
    // 方法
    fetchCostsByProject,
    fetchCostStats,
    createCost,
    updateCost,
    deleteCost,
    reset
  }
}) 