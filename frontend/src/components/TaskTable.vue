<template>
  <div class="task-table-wrapper">
    <el-table
      v-loading="loading"
      :data="tasks"
      style="width: 100%"
      :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
    >
      <el-table-column prop="title" label="任务标题" min-width="200">
        <template #default="{ row }">
          <div class="task-title">
            <span class="title-text">{{ row.title }}</span>
            <el-tag
              :type="TASK_PRIORITY_TYPE[row.priority]"
              size="small"
              class="priority-tag"
            >
              {{ TASK_PRIORITY_MAP[row.priority] }}
            </el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="TASK_STATUS_TYPE[row.status]" class="status-tag">
            {{ TASK_STATUS_MAP[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column 
        v-if="showProject" 
        prop="project.name" 
        label="所属项目" 
        width="150" 
      />
      <el-table-column prop="assignee.name" label="负责人" width="120" />
      <el-table-column label="工时" width="180">
        <template #default="{ row }">
          <div class="hours-info">
            <span class="estimated">预计: {{ row.estimated_hours }}h</span>
            <span class="actual">实际: {{ row.actual_hours }}h</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <div class="action-buttons">
            <el-button
              v-if="showView"
              size="small"
              @click="$emit('view', row)"
            >
              查看
            </el-button>
            <el-button
              type="primary"
              size="small"
              @click="$emit('edit', row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="$emit('delete', row)"
            >
              删除
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import {
  TASK_STATUS_MAP,
  TASK_STATUS_TYPE,
  TASK_PRIORITY_MAP,
  TASK_PRIORITY_TYPE
} from '@/constants/task'

defineProps({
  tasks: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  showProject: {
    type: Boolean,
    default: false
  },
  showView: {
    type: Boolean,
    default: false
  }
})

defineEmits(['view', 'edit', 'delete'])
</script>

<style scoped>
.task-table-wrapper {
  width: 100%;
}

.task-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-text {
  font-weight: 500;
}

.priority-tag {
  font-size: 12px;
}

.status-tag {
  font-size: 12px;
}

.hours-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.estimated {
  color: #909399;
  font-size: 13px;
}

.actual {
  color: #67c23a;
  font-size: 13px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}
</style> 