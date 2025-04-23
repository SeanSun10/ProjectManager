<template>
  <div class="project-overview">
    <el-row :gutter="20">
      <!-- 任务统计卡片 -->
      <el-col :span="8">
        <el-card class="stat-card" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span>任务统计</span>
              <el-button type="primary" link @click="refreshStats">
                <el-icon><Refresh /></el-icon>
              </el-button>
            </div>
          </template>
          <el-row class="stat-content">
            <el-col :span="8" class="stat-item">
              <div class="stat-value">{{ projectStats.taskStats.total || 0 }}</div>
              <div class="stat-label">总任务</div>
            </el-col>
            <el-col :span="8" class="stat-item">
              <div class="stat-value">{{ projectStats.taskStats.inProgress || 0 }}</div>
              <div class="stat-label">进行中</div>
            </el-col>
            <el-col :span="8" class="stat-item">
              <div class="stat-value">{{ projectStats.taskStats.completed || 0 }}</div>
              <div class="stat-label">已完成</div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <!-- 工时统计卡片 -->
      <el-col :span="8">
        <el-card class="stat-card" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span>工时统计</span>
            </div>
          </template>
          <el-row class="stat-content">
            <el-col :span="12" class="stat-item">
              <div class="stat-value">{{ projectStats.timeStats.estimated || 0 }}</div>
              <div class="stat-label">预计工时</div>
            </el-col>
            <el-col :span="12" class="stat-item">
              <div class="stat-value">{{ projectStats.timeStats.actual || 0 }}</div>
              <div class="stat-label">实际工时</div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>

      <!-- 成本统计卡片 -->
      <el-col :span="8">
        <el-card class="stat-card" v-loading="loading">
          <template #header>
            <div class="card-header">
              <span>成本统计</span>
            </div>
          </template>
          <el-row class="stat-content">
            <el-col :span="12" class="stat-item">
              <div class="stat-value">¥{{ projectStats.costStats.fixed || 0 }}</div>
              <div class="stat-label">固定成本</div>
            </el-col>
            <el-col :span="12" class="stat-item">
              <div class="stat-value">¥{{ projectStats.costStats.human || 0 }}</div>
              <div class="stat-label">人力成本</div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <!-- 最近活动 -->
    <el-card class="activity-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>最近活动</span>
          <el-button type="primary" link @click="refreshActivities">
            <el-icon><Refresh /></el-icon>
          </el-button>
        </div>
      </template>
      <el-empty v-if="!recentActivities.length" description="暂无活动记录" />
      <el-timeline v-else>
        <el-timeline-item
          v-for="activity in recentActivities"
          :key="activity.id"
          :timestamp="formatDate(activity.created_at)"
          :type="getActivityType(activity.type)"
        >
          {{ activity.content }}
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <!-- 任务完成趋势图 -->
    <el-card class="chart-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>任务完成趋势</span>
          <el-radio-group v-model="chartPeriod" size="small" @change="handlePeriodChange">
            <el-radio-button value="week">周</el-radio-button>
            <el-radio-button value="month">月</el-radio-button>
          </el-radio-group>
        </div>
      </template>
      <div class="chart-container" ref="chartContainer">
        <!-- 这里可以使用 ECharts 或其他图表库来展示趋势图 -->
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProjectStore } from '@/stores/project'
import { formatDate } from '@/utils/date'
import { Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const route = useRoute()
const projectStore = useProjectStore()
const chartPeriod = ref('week')
const chartContainer = ref(null)
const loading = ref(false)

const projectStats = computed(() => projectStore.projectStats || {
  taskStats: { total: 0, inProgress: 0, completed: 0 },
  timeStats: { estimated: 0, actual: 0 },
  costStats: { fixed: 0, human: 0 }
})

const recentActivities = computed(() => projectStore.recentActivities || [])

// 获取活动类型对应的图标样式
const getActivityType = (type) => {
  const types = {
    'task_created': 'primary',
    'task_updated': 'warning',
    'task_completed': 'success',
    'member_added': 'info',
    'cost_recorded': 'danger'
  }
  return types[type] || 'info'
}

// 刷新统计数据
const refreshStats = async () => {
  try {
    loading.value = true
    await projectStore.fetchProjectStats(route.params.projectId)
    ElMessage.success('统计数据已更新')
  } catch (error) {
    ElMessage.error('获取统计数据失败')
  } finally {
    loading.value = false
  }
}

// 刷新活动列表
const refreshActivities = async () => {
  try {
    loading.value = true
    await projectStore.fetchRecentActivities(route.params.projectId)
    ElMessage.success('活动列表已更新')
  } catch (error) {
    ElMessage.error('获取活动列表失败')
  } finally {
    loading.value = false
  }
}

// 处理时间周期变化
const handlePeriodChange = () => {
  // TODO: 根据选择的时间周期更新图表数据
}

// 初始化数据
const initData = async () => {
  if (!route.params.projectId) {
    ElMessage.error('项目ID不存在')
    return
  }

  try {
    loading.value = true
    await Promise.all([
      projectStore.fetchProjectStats(Number(route.params.projectId)),
      projectStore.fetchRecentActivities(Number(route.params.projectId))
    ])
  } catch (error) {
    console.error('初始化数据失败:', error)
    ElMessage.error(error.response?.data?.detail || '初始化数据失败')
  } finally {
    loading.value = false
  }
}

// 添加路由参数监听
watch(() => route.params.projectId, (newId) => {
  if (newId) {
    initData()
  }
}, { immediate: true })

onUnmounted(() => {
  projectStore.reset()
})
</script>

<style scoped>
.project-overview {
  padding: 20px;
}

.stat-card {
  margin-bottom: 20px;
}

.stat-content {
  text-align: center;
}

.stat-item {
  padding: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}

.activity-card {
  margin-bottom: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 300px;
  padding: 20px;
}
</style> 