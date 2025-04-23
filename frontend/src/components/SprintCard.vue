<template>
  <el-card class="sprint-card">
    <div class="sprint-card-header">
      <h3>{{ sprint.name }}</h3>
      <div class="sprint-actions">
        <el-button type="primary" size="small" @click="$emit('edit', sprint)">编辑</el-button>
        <el-button type="danger" size="small" @click="$emit('delete', sprint)">删除</el-button>
      </div>
    </div>
    
    <div class="sprint-content">
      <div class="sprint-description">{{ sprint.description }}</div>
      
      <div class="sprint-info">
        <div class="info-item">
          <span class="label">开始日期：</span>
          <span>{{ sprint.start_date ? new Date(sprint.start_date).toLocaleDateString() : '未设置' }}</span>
        </div>
        <div class="info-item">
          <span class="label">结束日期：</span>
          <span>{{ sprint.end_date ? new Date(sprint.end_date).toLocaleDateString() : '未设置' }}</span>
        </div>
        <div class="info-item">
          <span class="label">状态：</span>
          <el-tag :type="getSprintStatusType(sprint.status)">
            {{ getSprintStatusText(sprint.status) }}
          </el-tag>
        </div>
      </div>
    </div>
    
    <slot></slot>
  </el-card>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  sprint: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['edit', 'delete'])

// 获取迭代状态对应的类型
const getSprintStatusType = (status) => {
  const types = {
    'PLANNING': 'info',
    'ACTIVE': 'success',
    'COMPLETED': 'primary',
    'CANCELLED': 'danger'
  }
  return types[status] || 'info'
}

// 获取迭代状态对应的文本
const getSprintStatusText = (status) => {
  const texts = {
    'PLANNING': '规划中',
    'ACTIVE': '进行中',
    'COMPLETED': '已完成',
    'CANCELLED': '已取消'
  }
  return texts[status] || status
}
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
</style> 