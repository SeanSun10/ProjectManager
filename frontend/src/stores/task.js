import { defineStore } from 'pinia'
import request from '@/utils/request'

export const useTaskStore = defineStore('task', {
  state: () => ({
    tasks: [],
    loading: false,
    error: null,
    currentProjectId: null
  }),

  actions: {
    async fetchTasks(projectId) {
      if (!projectId) {
        this.tasks = []
        this.currentProjectId = null
        return
      }
      
      this.loading = true
      this.error = null
      this.currentProjectId = projectId
      
      try {
        const response = await request.get(`/tasks?project_id=${projectId}`)
        this.tasks = Array.isArray(response) ? response : []
      } catch (error) {
        this.error = error.response?.data?.message || error.message || '获取任务列表失败'
        this.tasks = []
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchTask(taskId) {
      this.loading = true
      try {
        const response = await request.get(`/tasks/${taskId}`)
        return response
      } catch (error) {
        console.error('获取任务详情失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createTask(taskData) {
      if (!this.currentProjectId) {
        throw new Error('请先选择项目')
      }
      
      try {
        const response = await request.post('/tasks', {
          ...taskData,
          project_id: this.currentProjectId
        })
        if (response && typeof response === 'object') {
          this.tasks.push(response)
        }
        return response
      } catch (error) {
        throw error
      }
    },

    async updateTask(taskId, taskData) {
      if (!this.currentProjectId) {
        throw new Error('未选择项目')
      }
      
      try {
        const response = await request.put(`/tasks/${taskId}`, {
          ...taskData,
          project_id: this.currentProjectId
        })
        if (response && typeof response === 'object') {
          const index = this.tasks.findIndex(task => task.id === taskId)
          if (index !== -1) {
            this.tasks[index] = response
          }
        }
        return response
      } catch (error) {
        throw error
      }
    },

    async deleteTask(taskId) {
      if (!this.currentProjectId) {
        throw new Error('未选择项目')
      }
      
      try {
        await request.delete(`/tasks/${taskId}`, {
          params: {
            project_id: this.currentProjectId
          }
        })
        this.tasks = this.tasks.filter(task => task.id !== taskId)
      } catch (error) {
        throw error
      }
    },

    clearTasks() {
      this.tasks = []
      this.currentProjectId = null
      this.error = null
    }
  }
}) 