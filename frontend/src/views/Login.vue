<template>
  <div class="login-container">
    <div class="login-background">
      <div class="circles">
        <div v-for="i in 10" :key="i" class="circle"></div>
      </div>
    </div>
    
    <div class="login-content">
      <div class="login-header">
        <div class="logo">
          <el-icon :size="40"><Monitor /></el-icon>
        </div>
        <h1>项目管理系统</h1>
        <p class="subtitle">Professional Project Management Platform</p>
      </div>

      <div class="login-box">
        <el-form
          ref="loginForm"
          :model="formData"
          :rules="rules"
          class="login-form"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              ref="usernameInput"
              v-model="username"
              placeholder="Username"
              :prefix-icon="User"
              class="custom-input"
              @input="updateUsername"
            />
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              ref="passwordInput"
              v-model="password"
              type="password"
              placeholder="Password"
              :prefix-icon="Lock"
              show-password
              class="custom-input"
              @input="updatePassword"
            />
          </el-form-item>
          <el-form-item>
            <div class="form-footer">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <el-button link>忘记密码？</el-button>
            </div>
          </el-form-item>
          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              class="login-button"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="login-footer">
        <p>© {{ new Date().getFullYear() }} Project Management System. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Monitor } from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const rememberMe = ref(false)
const username = ref('')
const password = ref('')
const usernameInput = ref(null)
const passwordInput = ref(null)
const loginForm = ref(null)

const formData = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const updateUsername = (value) => {
  username.value = value
  formData.username = value
}

const updatePassword = (value) => {
  password.value = value
  formData.password = value
}

const handleLogin = async () => {
  try {
    loading.value = true
    await userStore.login(username.value, password.value)
    if (userStore.isLoggedIn) {
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error('用户名或密码错误')
    }
  } catch (error) {
    ElMessage.error('登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1a1a1a 0%, #0a192f 100%);
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.circles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.circle {
  position: absolute;
  display: block;
  width: 20px;
  height: 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  animation: animate 25s linear infinite;
  bottom: -150px;
  border-radius: 50%;
}

.circle:nth-child(1) { left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
.circle:nth-child(2) { left: 10%; width: 20px; height: 20px; animation-delay: 2s; animation-duration: 12s; }
.circle:nth-child(3) { left: 70%; width: 20px; height: 20px; animation-delay: 4s; }
.circle:nth-child(4) { left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; }
.circle:nth-child(5) { left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
.circle:nth-child(6) { left: 75%; width: 110px; height: 110px; animation-delay: 3s; }
.circle:nth-child(7) { left: 35%; width: 150px; height: 150px; animation-delay: 7s; }
.circle:nth-child(8) { left: 50%; width: 25px; height: 25px; animation-delay: 15s; animation-duration: 45s; }
.circle:nth-child(9) { left: 20%; width: 15px; height: 15px; animation-delay: 2s; animation-duration: 35s; }
.circle:nth-child(10) { left: 85%; width: 150px; height: 150px; animation-delay: 0s; animation-duration: 11s; }

@keyframes animate {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(-1000px) rotate(720deg);
    opacity: 0;
  }
}

.login-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 400px;
  padding: 20px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  margin-bottom: 20px;
}

.logo :deep(.el-icon) {
  color: #409EFF;
  background: rgba(64, 158, 255, 0.1);
  padding: 20px;
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(64, 158, 255, 0.2);
}

.login-header h1 {
  color: #fff;
  font-size: 28px;
  margin: 0;
  margin-bottom: 10px;
}

.subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  margin: 0;
}

.login-box {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  padding: 40px;
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.login-form :deep(.el-input) {
  --el-input-bg-color: rgba(255, 255, 255, 0.1);
  --el-input-border-color: rgba(255, 255, 255, 0.2);
  --el-input-hover-border-color: rgba(255, 255, 255, 0.3);
  --el-input-focus-border-color: #409EFF;
}

.login-form :deep(.el-input__wrapper) {
  box-shadow: none !important;
  background-color: rgba(255, 255, 255, 0.1);
  padding: 0 12px;
}

.login-form :deep(.el-input__inner) {
  color: #fff;
  height: 50px;
  background-color: transparent;
  padding: 0;
  line-height: 50px;
}

.login-form :deep(.el-input__prefix-inner) {
  color: rgba(255, 255, 255, 0.6);
  margin-right: 8px;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-footer :deep(.el-checkbox) {
  color: rgba(255, 255, 255, 0.6);
}

.form-footer :deep(.el-button--text) {
  color: rgba(255, 255, 255, 0.6);
}

.form-footer :deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: #409EFF;
}

.login-button {
  width: 100%;
  height: 50px;
  font-size: 16px;
  background: linear-gradient(45deg, #409EFF, #36cfc9);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(64, 158, 255, 0.3);
}

.login-footer {
  text-align: center;
  margin-top: 40px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-content {
    padding: 20px;
    width: 90%;
  }
  
  .login-box {
    padding: 30px 20px;
  }

  .login-header h1 {
    font-size: 24px;
  }

  .subtitle {
    font-size: 12px;
  }
}

@media (max-height: 600px) {
  .login-header {
    margin-bottom: 20px;
  }

  .logo {
    margin-bottom: 10px;
  }

  .login-box {
    padding: 20px;
  }

  .login-footer {
    margin-top: 20px;
  }
}
</style> 