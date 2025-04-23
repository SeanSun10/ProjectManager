import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'

// 配置 axios
axios.defaults.withCredentials = true
axios.defaults.timeout = 10000

// 添加请求拦截器
axios.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    return config
  },
  error => {
    // 对请求错误做些什么
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 添加响应拦截器
axios.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    return response
  },
  error => {
    if (error.response) {
      // 请求已发出，但服务器响应的状态码不在 2xx 范围内
      console.error('Error response:', error.response)
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      console.error('Error request:', error.request)
      // 如果是连接被拒绝，可能是后端服务器未启动
      if (error.code === 'ECONNREFUSED') {
        console.error('后端服务器可能未启动，请检查后端服务是否正在运行')
      }
    } else {
      // 发送请求时出了点问题
      console.error('Error message:', error.message)
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

app.mount('#app')
