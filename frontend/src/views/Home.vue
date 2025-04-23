<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>项目统计</span>
              <el-button type="primary" link @click="$router.push('/projects')">
                查看详情
              </el-button>
            </div>
          </template>
          <div class="data-content">
            <el-row>
              <el-col :span="12" class="data-item">
                <div class="data-label">总项目数</div>
                <div class="data-value">{{ statistics.project_count || 0 }}</div>
              </el-col>
              <el-col :span="12" class="data-item">
                <div class="data-label">进行中</div>
                <div class="data-value">{{ statistics.active_project_count || 0 }}</div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>任务统计</span>
              <el-button type="primary" link @click="$router.push('/tasks')">
                查看详情
              </el-button>
            </div>
          </template>
          <div class="data-content">
            <el-row>
              <el-col :span="8" class="data-item">
                <div class="data-label">总任务数</div>
                <div class="data-value">{{ statistics.total_tasks || 0 }}</div>
              </el-col>
              <el-col :span="8" class="data-item">
                <div class="data-label">进行中</div>
                <div class="data-value">{{ statistics.in_progress_tasks || 0 }}</div>
              </el-col>
              <el-col :span="8" class="data-item">
                <div class="data-label">已完成</div>
                <div class="data-value">{{ statistics.completed_tasks || 0 }}</div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="data-card">
          <template #header>
            <div class="card-header">
              <span>工时统计</span>
              <el-button type="primary" link @click="$router.push('/tasks')">
                查看详情
              </el-button>
            </div>
          </template>
          <div class="data-content">
            <el-row>
              <el-col :span="12" class="data-item">
                <div class="data-label">预估工时</div>
                <div class="data-value">{{ statistics.total_estimated_hours || 0 }}</div>
              </el-col>
              <el-col :span="12" class="data-item">
                <div class="data-label">实际工时</div>
                <div class="data-value">{{ statistics.total_actual_hours || 0 }}</div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>任务状态分布</span>
            </div>
          </template>
          <div class="chart-content">
            <el-table
              :data="statistics.status_distribution || []"
              style="width: 100%"
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
                  {{ row.percentage }}%
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="list-card">
          <template #header>
            <div class="card-header">
              <span>最近活动</span>
              <el-button type="primary" link @click="refreshActivities">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          <div class="list-content">
            <el-timeline>
              <el-timeline-item
                v-for="(activity, index) in recentActivities"
                :key="index"
                :timestamp="activity.created_at"
                :type="getActivityType(activity.type)"
              >
                {{ activity.content }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import request from '../utils/request'
import { Refresh } from '@element-plus/icons-vue'

const statistics = ref({
  project_count: 0,
  active_project_count: 0,
  total_tasks: 0,
  completed_tasks: 0,
  in_progress_tasks: 0,
  total_estimated_hours: 0,
  total_actual_hours: 0,
  status_distribution: []
})
const recentActivities = ref([])

// 活动类型映射
const getActivityType = (activityType) => {
  const typeMap = {
    'project_created': 'success',
    'project_updated': 'primary',
    'task_created': 'success',
    'task_updated': 'primary',
    'task_completed': 'success',
    'sprint_started': 'warning',
    'sprint_completed': 'success'
  }
  return typeMap[activityType] || 'info'
}

// 任务状态类型映射
const getStatusType = (status) => {
  const statusMap = {
    'todo': 'info',
    'in_progress': 'warning',
    'review': 'primary',
    'done': 'success'
  }
  return statusMap[status] || 'info'
}

// 任务状态文本映射
const getStatusText = (status) => {
  const statusMap = {
    'todo': '待办',
    'in_progress': '进行中',
    'review': '评审中',
    'done': '已完成'
  }
  return statusMap[status] || status
}

const fetchStatistics = async () => {
  try {
    const response = await request.get('/statistics')
    statistics.value = response
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

const fetchRecentActivities = async () => {
  try {
    const response = await request.get('/activities')
    recentActivities.value = response
  } catch (error) {
    console.error('获取最近活动失败:', error)
  }
}

// 添加定时器变量
let refreshTimer = null

// 修改自动刷新函数
const startAutoRefresh = () => {
  // 清除已存在的定时器
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
  // 每5分钟刷新一次活动数据
  refreshTimer = setInterval(fetchRecentActivities, 5 * 60 * 1000)
}

// 在组件卸载时清除定时器
onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})

// 添加手动刷新按钮
const refreshActivities = () => {
  fetchRecentActivities()
}

onMounted(() => {
  fetchStatistics()
  fetchRecentActivities()
  startAutoRefresh()
})
</script>

<style scoped>
.home-container {
  min-height: 100%;
}

.data-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-content {
  padding: 20px 0;
}

.data-item {
  text-align: center;
}

.data-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.data-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.mt-20 {
  margin-top: 20px;
}

.chart-card,
.list-card {
  height: 400px;
}

.chart-content {
  height: 300px;
}

.list-content {
  height: 320px;
  overflow-y: auto;
}

.list-content :deep(.el-timeline) {
  padding-left: 16px;
}
</style> 