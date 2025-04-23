import { defineStore } from 'pinia'
import request from '../utils/request'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: null
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  
  actions: {
    async login(username, password) {
      try {
        const params = new URLSearchParams()
        params.append('username', username)
        params.append('password', password)
        
        const response = await request.post('/auth/login', params, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
        
        if (response.access_token) {
          this.token = response.access_token
          localStorage.setItem('token', response.access_token)
          const userInfo = await this.getUserInfo()
          return !!userInfo
        }
        return false
      } catch (error) {
        console.error('Login error:', error)
        return false
      }
    },
    
    async getUserInfo() {
      try {
        const response = await request.get('auth/me')
        this.userInfo = response
        return response
      } catch (error) {
        return null
      }
    },
    
    logout() {
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
    }
  }
}) 