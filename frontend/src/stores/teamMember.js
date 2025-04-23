import { defineStore } from 'pinia'
import request from '@/utils/request'

export const useTeamMemberStore = defineStore('teamMember', {
  state: () => ({
    teamMembers: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchTeamMembers() {
      this.loading = true
      this.error = null
      
      try {
        const response = await request.get('/team-members')
        this.teamMembers = Array.isArray(response) ? response : []
      } catch (error) {
        this.error = error.response?.data?.detail || error.message || '获取团队成员失败'
        this.teamMembers = []
        throw error
      } finally {
        this.loading = false
      }
    },

    async createTeamMember(memberData) {
      try {
        const response = await request.post('/team-members', memberData)
        if (response && typeof response === 'object') {
          this.teamMembers.push(response)
        }
        return response
      } catch (error) {
        throw error
      }
    },

    async updateTeamMember(memberId, memberData) {
      try {
        const response = await request.put(`/team-members/${memberId}`, memberData)
        if (response && typeof response === 'object') {
          const index = this.teamMembers.findIndex(member => member.id === memberId)
          if (index !== -1) {
            this.teamMembers[index] = response
          }
        }
        return response
      } catch (error) {
        throw error
      }
    },

    async deleteTeamMember(memberId) {
      try {
        await request.delete(`/team-members/${memberId}`)
        this.teamMembers = this.teamMembers.filter(member => member.id !== memberId)
      } catch (error) {
        throw error
      }
    }
  }
}) 