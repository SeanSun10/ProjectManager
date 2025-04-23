<template>
  <div class="statistics-container">
    <!-- 顶部标题栏 -->
    <div class="header">
      <div class="title-section">
        <h1>项目数据驾驶舱</h1>
        <span class="subtitle">实时数据分析与监控</span>
      </div>
      <div class="time-section">
        <i class="el-icon-time"></i>
        <span>{{ currentTime }}</span>
      </div>
    </div>

    <!-- 数据卡片网格 -->
    <div class="dashboard-grid">
      <!-- 任务完成率卡片 -->
      <div class="dashboard-card">
        <div class="card-header">
          <h3><i class="el-icon-s-data"></i>任务完成率</h3>
        </div>
        <div class="card-body">
          <div class="progress-section">
            <el-progress
              type="dashboard"
              :percentage="taskCompletionRate"
              :color="getCompletionColor"
              :stroke-width="10"
            >
              <template #default="{ percentage }">
                <div class="progress-info">
                  <span class="percentage">{{ percentage }}%</span>
                  <span class="label">完成率</span>
                </div>
              </template>
            </el-progress>
          </div>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="label">总任务</span>
              <span class="value">{{ totalTasks }}</span>
            </div>
            <div class="stat-item">
              <span class="label">已完成</span>
              <span class="value">{{ completedTasks }}</span>
            </div>
            <div class="stat-item">
              <span class="label">进行中</span>
              <span class="value">{{ inProgressTasks }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 项目进度卡片 -->
      <div class="dashboard-card">
        <div class="card-header">
          <h3><i class="el-icon-s-management"></i>项目进度</h3>
        </div>
        <div class="card-body">
          <div class="progress-section">
            <el-progress
              type="circle"
              :percentage="projectProgress"
              :color="getProgressColor"
              :stroke-width="10"
            >
              <template #default="{ percentage }">
                <div class="progress-info">
                  <span class="percentage">{{ percentage }}%</span>
                  <span class="label">进度</span>
                </div>
              </template>
            </el-progress>
          </div>
          <div class="project-info">
            <div class="info-item">
              <span class="label">开始日期</span>
              <span class="value">{{ formatDate(projectStartDate) }}</span>
            </div>
            <div class="info-item">
              <span class="label">结束日期</span>
              <span class="value">{{ formatDate(projectEndDate) }}</span>
            </div>
            <div class="info-item">
              <span class="label">剩余天数</span>
              <span class="value highlight">{{ remainingDays }}天</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 工时统计卡片 -->
      <div class="dashboard-card">
        <div class="card-header">
          <h3><i class="el-icon-time"></i>工时统计</h3>
        </div>
        <div class="card-body">
          <div class="hours-stats">
            <div class="hours-item">
              <div class="hours-info">
                <span class="label">预估总工时</span>
                <span class="value">{{ totalEstimatedHours }}h</span>
              </div>
              <el-progress 
                :percentage="100"
                :stroke-width="8"
                :show-text="false"
                status="warning"
              />
            </div>
            <div class="hours-item">
              <div class="hours-info">
                <span class="label">实际总工时</span>
                <span class="value">{{ totalActualHours }}h</span>
              </div>
              <el-progress 
                :percentage="totalEstimatedHours ? (totalActualHours / totalEstimatedHours) * 100 : 0"
                :stroke-width="8"
                :show-text="false"
                status="success"
              />
            </div>
            <div class="hours-deviation">
              <span class="label">工时偏差</span>
              <span class="value" :class="getHoursDeviationClass">
                {{ hoursDeviation }}%
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 任务状态分布卡片 -->
      <div class="dashboard-card">
        <div class="card-header">
          <h3><i class="el-icon-s-grid"></i>任务状态分布</h3>
        </div>
        <div class="card-body">
          <el-table
            :data="statusDistribution"
            style="width: 100%"
            @row-click="handleStatusClick"
          >
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="数量" />
            <el-table-column prop="percentage" label="占比">
              <template #default="{ row }">
                <div class="percentage-bar">
                  <div class="bar">
                    <div 
                      class="bar-fill" 
                      :style="{ width: row.percentage + '%' }"
                      :class="getStatusType(row.status)"
                    ></div>
                  </div>
                  <span>{{ row.percentage }}%</span>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '../utils/request'

const router = useRouter()
const currentTime = ref('')

// 统计数据
const totalTasks = ref(0)
const completedTasks = ref(0)
const inProgressTasks = ref(0)
const totalEstimatedHours = ref(0)
const totalActualHours = ref(0)
const projectStartDate = ref(null)
const projectEndDate = ref(null)
const statusDistribution = ref([])

// 计算属性
const taskCompletionRate = computed(() => {
  if (totalTasks.value === 0) return 0
  const rate = (completedTasks.value / totalTasks.value) * 100
  return Math.round(rate) || 0
})

const hoursDeviation = computed(() => {
  if (totalEstimatedHours.value === 0) return 0
  const deviation = ((totalActualHours.value - totalEstimatedHours.value) / totalEstimatedHours.value) * 100
  return Math.round(deviation) || 0
})

const projectProgress = computed(() => {
  if (!projectStartDate.value || !projectEndDate.value) return 0
  const totalDays = Math.ceil((new Date(projectEndDate.value) - new Date(projectStartDate.value)) / (1000 * 60 * 60 * 24))
  const remainingDays = Math.ceil((new Date(projectEndDate.value) - new Date()) / (1000 * 60 * 60 * 24))
  const progress = ((totalDays - remainingDays) / totalDays) * 100
  return Math.round(progress) || 0
})

const remainingDays = computed(() => {
  if (!projectEndDate.value) return 0
  return Math.ceil((new Date(projectEndDate.value) - new Date()) / (1000 * 60 * 60 * 24))
})

// 工具函数
const getCompletionColor = (percentage) => {
  if (percentage < 30) return '#F56C6C'
  if (percentage < 70) return '#E6A23C'
  return '#67C23A'
}

const getProgressColor = (percentage) => {
  if (percentage < 30) return '#F56C6C'
  if (percentage < 70) return '#E6A23C'
  return '#67C23A'
}

const getHoursDeviationClass = computed(() => {
  if (hoursDeviation.value > 0) return 'deviation-positive'
  if (hoursDeviation.value < 0) return 'deviation-negative'
  return ''
})

const getStatusType = (status) => {
  const statusMap = {
    'todo': 'info',
    'in_progress': 'warning',
    'review': 'primary',
    'done': 'success'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    'todo': '待办',
    'in_progress': '进行中',
    'review': '评审中',
    'done': '已完成'
  }
  return statusMap[status] || status
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString()
}

// 导航函数
const navigateToTasks = (status = '') => {
  router.push({ path: '/tasks', query: { status } })
}

const navigateToProjects = () => {
  router.push('/projects')
}

const handleStatusClick = (row) => {
  navigateToTasks(row.status)
}

// 更新时间
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString()
}

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const response = await request.get('statistics')
    const data = response
    
    totalTasks.value = data.total_tasks
    completedTasks.value = data.completed_tasks
    inProgressTasks.value = data.in_progress_tasks
    totalEstimatedHours.value = data.total_estimated_hours
    totalActualHours.value = data.total_actual_hours
    projectStartDate.value = data.project_start_date
    projectEndDate.value = data.project_end_date
    statusDistribution.value = data.status_distribution
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  }
}

onMounted(() => {
  fetchStatistics()
  updateTime()
  setInterval(updateTime, 1000)
})
</script>

<style scoped>
.statistics-container {
  height: 100%;
  padding: 20px;
  background: #f0f2f5;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  background: #fff;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.title-section h1 {
  margin: 0;
  font-size: 24px;
  color: #1890ff;
}

.subtitle {
  color: #8c8c8c;
  font-size: 14px;
  margin-top: 4px;
}

.time-section {
  display: flex;
  align-items: center;
  color: #1890ff;
}

.time-section i {
  margin-right: 8px;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.dashboard-card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  padding: 16px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h3 {
  margin: 0;
  color: #1890ff;
  font-size: 16px;
  display: flex;
  align-items: center;
}

.card-header h3 i {
  margin-right: 8px;
}

.card-body {
  padding: 24px;
}

.progress-section {
  display: flex;
  justify-content: center;
  margin-bottom: 24px;
}

.progress-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.progress-info .percentage {
  font-size: 24px;
  font-weight: bold;
  color: #1890ff;
}

.progress-info .label {
  font-size: 14px;
  color: #8c8c8c;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-item {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  text-align: center;
}

.stat-item .label {
  font-size: 12px;
  color: #8c8c8c;
}

.stat-item .value {
  display: block;
  font-size: 20px;
  font-weight: bold;
  color: #1890ff;
  margin-top: 4px;
}

.project-info {
  display: grid;
  gap: 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 4px;
}

.info-item .label {
  color: #8c8c8c;
}

.info-item .value {
  color: #262626;
}

.info-item .value.highlight {
  color: #1890ff;
  font-weight: bold;
}

.hours-stats {
  display: grid;
  gap: 20px;
}

.hours-item {
  display: grid;
  gap: 8px;
}

.hours-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hours-deviation {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 4px;
  margin-top: 8px;
}

.percentage-bar {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bar {
  flex: 1;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.bar-fill.success { background: #67C23A; }
.bar-fill.warning { background: #E6A23C; }
.bar-fill.info { background: #909399; }
.bar-fill.primary { background: #409EFF; }

:deep(.el-table) {
  background: transparent;
}

:deep(.el-table th) {
  background: #f5f5f5;
}

:deep(.el-table td), :deep(.el-table th) {
  padding: 8px 0;
}

:deep(.el-tag) {
  border-radius: 4px;
}
</style> 