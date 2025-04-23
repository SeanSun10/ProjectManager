<template>
  <div class="user-profile">
    <el-row :gutter="20">
      <!-- 个人信息 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>个人信息</span>
              <el-button type="primary" @click="handleEditProfile">编辑</el-button>
            </div>
          </template>
          <div class="profile-info">
            <div class="avatar-container">
              <el-avatar :size="100" :src="user.avatar" />
            </div>
            <el-descriptions :column="1" border>
              <el-descriptions-item label="用户名">{{ user.username }}</el-descriptions-item>
              <el-descriptions-item label="邮箱">{{ user.email }}</el-descriptions-item>
              <el-descriptions-item label="角色">
                <el-tag :type="user.is_superuser ? 'danger' : 'primary'">
                  {{ user.is_superuser ? '管理员' : '普通用户' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="注册时间">{{ formatDate(user.created_at) }}</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>

      <!-- 修改密码 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>修改密码</span>
            </div>
          </template>
          <el-form
            ref="passwordForm"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px"
          >
            <el-form-item label="原密码" prop="old_password">
              <el-input
                v-model="passwordForm.old_password"
                type="password"
                show-password
              />
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
              <el-input
                v-model="passwordForm.new_password"
                type="password"
                show-password
              />
            </el-form-item>
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input
                v-model="passwordForm.confirm_password"
                type="password"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleChangePassword">修改密码</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- 任务统计 -->
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>任务统计</span>
            </div>
          </template>
          <div class="task-stats">
            <div class="stat-item">
              <div class="stat-value">{{ taskStats.total }}</div>
              <div class="stat-label">总任务数</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ taskStats.completed }}</div>
              <div class="stat-label">已完成</div>
            </div>
            <div class="stat-item">
              <div class="stat-value">{{ taskStats.in_progress }}</div>
              <div class="stat-label">进行中</div>
            </div>
          </div>
          <div class="task-chart">
            <el-progress
              type="dashboard"
              :percentage="completionRate"
              :color="getCompletionColor"
            >
              <template #default="{ percentage }">
                <span class="percentage-value">{{ percentage }}%</span>
                <span class="percentage-label">完成率</span>
              </template>
            </el-progress>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 编辑个人信息对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑个人信息"
      width="500px"
    >
      <el-form
        ref="profileForm"
        :model="profileForm"
        :rules="profileRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="profileForm.username" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="profileForm.email" />
        </el-form-item>
        <el-form-item label="头像">
          <el-upload
            class="avatar-uploader"
            action="/api/v1/users/avatar"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <img v-if="profileForm.avatar" :src="profileForm.avatar" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showEditDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSaveProfile">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'

// 用户数据
const user = ref({})
const taskStats = ref({
  total: 0,
  completed: 0,
  in_progress: 0
})

// 表单数据
const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const profileForm = ref({
  username: '',
  email: '',
  avatar: ''
})

// 对话框控制
const showEditDialog = ref(false)

// 表单验证规则
const passwordRules = {
  old_password: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const profileRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ]
}

// 计算属性
const completionRate = computed(() => {
  if (taskStats.value.total === 0) return 0
  return Math.round((taskStats.value.completed / taskStats.value.total) * 100)
})

// 工具函数
const getCompletionColor = (percentage) => {
  if (percentage < 30) return '#F56C6C'
  if (percentage < 70) return '#E6A23C'
  return '#67C23A'
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString()
}

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const response = await axios.get('/api/v1/users/me')
    user.value = response.data
    profileForm.value = { ...response.data }
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  }
}

// 获取任务统计
const fetchTaskStats = async () => {
  try {
    const response = await axios.get('/api/v1/users/task-stats')
    taskStats.value = response.data
  } catch (error) {
    ElMessage.error('获取任务统计失败')
  }
}

// 修改密码
const handleChangePassword = async () => {
  try {
    await axios.post('/api/v1/users/change-password', {
      old_password: passwordForm.value.old_password,
      new_password: passwordForm.value.new_password
    })
    ElMessage.success('密码修改成功')
    passwordForm.value = {
      old_password: '',
      new_password: '',
      confirm_password: ''
    }
  } catch (error) {
    ElMessage.error('密码修改失败')
  }
}

// 编辑个人信息
const handleEditProfile = () => {
  showEditDialog.value = true
}

const handleSaveProfile = async () => {
  try {
    await axios.put('/api/v1/users/me', profileForm.value)
    ElMessage.success('个人信息更新成功')
    showEditDialog.value = false
    fetchUserInfo()
  } catch (error) {
    ElMessage.error('个人信息更新失败')
  }
}

// 头像上传
const beforeAvatarUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }
  return true
}

const handleAvatarSuccess = (response) => {
  profileForm.value.avatar = response.url
  ElMessage.success('头像上传成功')
}

onMounted(() => {
  fetchUserInfo()
  fetchTaskStats()
})
</script>

<style scoped>
.user-profile {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-info {
  text-align: center;
}

.avatar-container {
  margin-bottom: 20px;
}

.task-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.task-chart {
  display: flex;
  justify-content: center;
}

.percentage-value {
  font-size: 24px;
  font-weight: bold;
}

.percentage-label {
  font-size: 14px;
  color: #909399;
}

.avatar-uploader {
  text-align: center;
}

.avatar-uploader .avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.avatar-uploader .avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 50%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 