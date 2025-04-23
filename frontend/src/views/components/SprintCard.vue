<template>
  <el-card class="sprint-card">
    <template #header>
      <div class="sprint-card-header">
        <h3>{{ sprint.name }}</h3>
        <div class="sprint-actions">
          <el-tag :type="getSprintStatusType(sprint.status)">
            {{ getSprintStatusText(sprint.status) }}
          </el-tag>
          <el-button-group>
            <el-button type="primary" link @click="$emit('edit', sprint)">
              编辑
            </el-button>
            <el-button type="danger" link @click="$emit('delete', sprint)">
              删除
            </el-button>
          </el-button-group>
        </div>
      </div>
    </template>
    
    <div class="sprint-content">
      <p class="sprint-description">{{ sprint.description }}</p>
      <div class="sprint-info">
        <div class="info-item">
          <span class="label">开始日期：</span>
          <span>{{ formatDate(sprint.start_date) }}</span>
        </div>
        <div class="info-item">
          <span class="label">结束日期：</span>
          <span>{{ formatDate(sprint.end_date) }}</span>
        </div>
        <div class="info-item">
          <span class="label">任务数：</span>
          <span>{{ sprint.task_count || 0 }}</span>
        </div>
        <div class="info-item">
          <span class="label">完成率：</span>
          <el-progress 
            :percentage="sprint.completion_rate || 0" 
            :status="getProgressStatus(sprint.completion_rate)"
          />
        </div>
      </div>
      
      <!-- 任务列表 -->
      <div class="sprint-tasks">
        <div class="tasks-header">
          <h4>任务列表</h4>
          <el-button type="primary" link @click="$emit('add-task', sprint)">
            添加任务
          </el-button>
        </div>
        <el-table
          :data="sprint.tasks"
          style="width: 100%"
          v-loading="loading"
        >
          <el-table-column prop="title" label="任务标题" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getTaskStatusType(row.status)">
                {{ getTaskStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="priority" label="优先级" width="100">
            <template #default="{ row }">
              <el-tag :type="getTaskPriorityType(row.priority)">
                {{ getTaskPriorityText(row.priority) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="assignee.name" label="负责人" width="120" />
          <el-table-column prop="estimated_hours" label="预估工时" width="100" />
          <el-table-column prop="actual_hours" label="实际工时" width="100" />
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button type="primary" link @click="$emit('edit-task', row)">
                编辑
              </el-button>
              <el-button type="danger" link @click="$emit('remove-task', sprint, row)">
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 任务统计 -->
      <div class="sprint-stats">
        <div class="stats-header">
          <h4>任务统计</h4>
        </div>
        <div class="stats-content">
          <div class="stats-item">
            <div class="stats-label">总任务数</div>
            <div class="stats-value">{{ sprint.task_count || 0 }}</div>
          </div>
          <div class="stats-item">
            <div class="stats-label">已完成</div>
            <div class="stats-value">{{ getCompletedTaskCount(sprint) }}</div>
          </div>
          <div class="stats-item">
            <div class="stats-label">进行中</div>
            <div class="stats-value">{{ getInProgressTaskCount(sprint) }}</div>
          </div>
          <div class="stats-item">
            <div class="stats-label">待办</div>
            <div class="stats-value">{{ getTodoTaskCount(sprint) }}</div>
          </div>
        </div>
        
        <!-- 工时统计 -->
        <div class="hours-stats">
          <div class="stats-item">
            <div class="stats-label">预估总工时</div>
            <div class="stats-value">{{ getTotalEstimatedHours(sprint) }}h</div>
          </div>
          <div class="stats-item">
            <div class="stats-label">实际总工时</div>
            <div class="stats-value">{{ getTotalActualHours(sprint) }}h</div>
          </div>
          <div class="stats-item">
            <div class="stats-label">工时偏差</div>
            <div class="stats-value" :class="getHoursDeviationClass(sprint)">
              {{ getHoursDeviation(sprint) }}h
            </div>
          </div>
        </div>
        
        <!-- 燃尽图 -->
        <div class="burn-down-chart">
          <div class="chart-header">
            <h4>燃尽图</h4>
          </div>
          <div class="chart-container" ref="chartRef"></div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { formatDate } from '@/utils/date'
import * as echarts from 'echarts'

const props = defineProps({
  sprint: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['edit', 'delete', 'add-task', 'edit-task', 'remove-task'])

const chartRef = ref(null)
let chart = null
let resizeObserver = null
let resizeHandler = null

// 工具函数
const getSprintStatusType = (status) => {
  const types = {
    'PLANNING': 'info',
    'IN_PROGRESS': 'primary',
    'COMPLETED': 'success'
  }
  return types[status] || 'info'
}

const getSprintStatusText = (status) => {
  const texts = {
    'PLANNING': '规划中',
    'IN_PROGRESS': '进行中',
    'COMPLETED': '已完成'
  }
  return texts[status] || status
}

const getProgressStatus = (rate) => {
  if (rate >= 100) return 'success'
  if (rate >= 80) return 'warning'
  return ''
}

const getTaskStatusType = (status) => {
  const types = {
    'TODO': 'info',
    'IN_PROGRESS': 'warning',
    'REVIEW': 'primary',
    'DONE': 'success'
  }
  return types[status] || 'info'
}

const getTaskStatusText = (status) => {
  const texts = {
    'TODO': '待办',
    'IN_PROGRESS': '进行中',
    'REVIEW': '评审中',
    'DONE': '已完成'
  }
  return texts[status] || status
}

const getTaskPriorityType = (priority) => {
  const types = {
    'LOW': 'info',
    'MEDIUM': 'warning',
    'HIGH': 'danger',
    'URGENT': 'danger'
  }
  return types[priority] || 'info'
}

const getTaskPriorityText = (priority) => {
  const texts = {
    'LOW': '低',
    'MEDIUM': '中',
    'HIGH': '高',
    'URGENT': '紧急'
  }
  return texts[priority] || priority
}

const getCompletedTaskCount = (sprint) => {
  return sprint.tasks?.filter(task => task.status === 'DONE').length || 0
}

const getInProgressTaskCount = (sprint) => {
  return sprint.tasks?.filter(task => task.status === 'IN_PROGRESS').length || 0
}

const getTodoTaskCount = (sprint) => {
  return sprint.tasks?.filter(task => task.status === 'TODO').length || 0
}

const getTotalEstimatedHours = (sprint) => {
  return sprint.tasks?.reduce((sum, task) => sum + (task.estimated_hours || 0), 0) || 0
}

const getTotalActualHours = (sprint) => {
  return sprint.tasks?.reduce((sum, task) => sum + (task.actual_hours || 0), 0) || 0
}

const getHoursDeviation = (sprint) => {
  const estimated = getTotalEstimatedHours(sprint)
  const actual = getTotalActualHours(sprint)
  return actual - estimated
}

const getHoursDeviationClass = (sprint) => {
  const deviation = getHoursDeviation(sprint)
  return {
    'positive': deviation > 0,
    'negative': deviation < 0
  }
}

// 等待容器元素准备好
const waitForContainer = async () => {
  let retryCount = 0
  const maxRetries = 30
  const waitTime = 100
  
  while (retryCount < maxRetries) {
    await nextTick()
    if (chartRef.value && chartRef.value instanceof Element) {
      const container = chartRef.value
      const rect = container.getBoundingClientRect()
      if (rect.width > 0 && rect.height > 0) {
        return container
      }
    }
    retryCount++
    await new Promise(resolve => setTimeout(resolve, waitTime))
  }
  
  console.warn('等待容器元素超时')
  return null
}

// 初始化图表
const initChart = async () => {
  if (!props.sprint?.start_date || !props.sprint?.end_date) {
    return
  }

  const container = await waitForContainer()
  if (!container) return
  
  try {
    if (!resizeObserver) {
      resizeObserver = new ResizeObserver(async (entries) => {
        for (const entry of entries) {
          const { width, height } = entry.contentRect
          if (width > 0 && height > 0) {
            if (!chart) {
              await createChart()
            } else {
              chart.resize()
            }
          }
        }
      })
    }

    resizeObserver.observe(container)
  } catch (error) {
    console.error('ResizeObserver 初始化失败:', error)
  }
}

// 创建图表
const createChart = async () => {
  const container = await waitForContainer()
  if (!container) return
  
  try {
    await nextTick()

    if (chart) {
      chart.dispose()
      chart = null
    }

    const rect = container.getBoundingClientRect()
    chart = echarts.init(container, null, {
      renderer: 'canvas',
      width: rect.width,
      height: rect.height
    })

    const startDate = new Date(props.sprint.start_date)
    const endDate = new Date(props.sprint.end_date)
    const totalDays = Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24))
    const totalTasks = props.sprint.task_count || 0

    const xAxisData = []
    const idealLineData = []
    const actualLineData = []

    for (let i = 0; i <= totalDays; i++) {
      const date = new Date(startDate)
      date.setDate(date.getDate() + i)
      xAxisData.push(date.toLocaleDateString())

      idealLineData.push(totalTasks * (1 - i / totalDays))

      const completedTasks = props.sprint.tasks?.filter(task => {
        const taskDate = new Date(task.updated_at)
        return task.status === 'DONE' && taskDate <= date
      }).length || 0
      actualLineData.push(totalTasks - completedTasks)
    }

    const option = {
      tooltip: {
        trigger: 'axis',
        formatter: function(params) {
          const date = params[0].name
          const ideal = params[0].value
          const actual = params[1].value
          return `日期：${date}<br/>理想剩余：${ideal}<br/>实际剩余：${actual}`
        }
      },
      legend: {
        data: ['理想线', '实际线']
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: xAxisData,
        axisLabel: {
          rotate: 45
        }
      },
      yAxis: {
        type: 'value',
        name: '剩余任务数',
        minInterval: 1
      },
      series: [
        {
          name: '理想线',
          type: 'line',
          data: idealLineData,
          itemStyle: {
            color: '#409EFF'
          },
          lineStyle: {
            type: 'dashed'
          }
        },
        {
          name: '实际线',
          type: 'line',
          data: actualLineData,
          itemStyle: {
            color: '#67C23A'
          }
        }
      ]
    }

    chart.setOption(option)

    resizeHandler = () => {
      if (chart) {
        chart.resize()
      }
    }
    window.addEventListener('resize', resizeHandler)

  } catch (error) {
    console.error('创建图表失败:', error)
  }
}

// 监听迭代数据变化
watch(
  () => props.sprint,
  async (newVal) => {
    if (newVal?.start_date && newVal?.end_date) {
      await initChart()
    }
  },
  { deep: true }
)

// 生命周期钩子
onMounted(async () => {
  if (props.sprint?.start_date && props.sprint?.end_date) {
    await initChart()
  }
})

onBeforeUnmount(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
  if (resizeObserver) {
    resizeObserver.disconnect()
    resizeObserver = null
  }
  if (resizeHandler) {
    window.removeEventListener('resize', resizeHandler)
    resizeHandler = null
  }
})
</script>

<style scoped>
.sprint-card {
  margin-bottom: 10px;
}

.sprint-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sprint-card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.sprint-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.sprint-content {
  color: #606266;
}

.sprint-description {
  margin: 10px 0;
  line-height: 1.6;
}

.sprint-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-top: 10px;
}

.info-item {
  display: flex;
  align-items: center;
}

.info-item .label {
  color: #909399;
  margin-right: 5px;
}

.sprint-tasks {
  margin-top: 20px;
  border-top: 1px solid #EBEEF5;
  padding-top: 20px;
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.tasks-header h4 {
  margin: 0;
  color: #303133;
}

.sprint-stats {
  margin-top: 20px;
  border-top: 1px solid #EBEEF5;
  padding-top: 20px;
}

.stats-header {
  margin-bottom: 15px;
}

.stats-header h4 {
  margin: 0;
  color: #303133;
}

.stats-content {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.stats-item {
  text-align: center;
  padding: 10px;
  background-color: #F5F7FA;
  border-radius: 4px;
}

.stats-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.stats-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.stats-value.positive {
  color: #F56C6C;
}

.stats-value.negative {
  color: #67C23A;
}

.hours-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.burn-down-chart {
  margin-top: 20px;
}

.chart-header {
  margin-bottom: 15px;
}

.chart-header h4 {
  margin: 0;
  color: #303133;
}

.chart-container {
  width: 100%;
  height: 300px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style> 