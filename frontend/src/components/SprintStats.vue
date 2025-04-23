<template>
  <div class="sprint-stats">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ totalTasks }}</div>
            <div class="stat-label">总任务数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ completedTasks }}</div>
            <div class="stat-label">已完成</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ inProgressTasks }}</div>
            <div class="stat-label">进行中</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-item">
            <div class="stat-value">{{ todoTasks }}</div>
            <div class="stat-label">待处理</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue'

const props = defineProps({
  tasks: {
    type: Array,
    required: true,
    default: () => []
  }
})

const totalTasks = computed(() => props.tasks.length)

const completedTasks = computed(() => 
  props.tasks.filter(task => task.status === 'COMPLETED').length
)

const inProgressTasks = computed(() => 
  props.tasks.filter(task => task.status === 'IN_PROGRESS').length
)

const todoTasks = computed(() => 
  props.tasks.filter(task => task.status === 'TODO').length
)
</script>

<style scoped>
.sprint-stats {
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
  padding: 10px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}
</style> 