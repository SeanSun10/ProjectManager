<template>
  <div class="filter-section">
    <el-form :inline="true" :model="filterForm" class="filter-form">
      <el-form-item v-if="showProject" label="项目" class="filter-item">
        <el-select
          v-model="filterForm.project_id"
          placeholder="选择项目"
          clearable
          @change="handleFilterChange"
          class="filter-select"
        >
          <el-option
            v-for="project in projects"
            :key="project.id"
            :label="project.name"
            :value="project.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" class="filter-item">
        <el-select
          v-model="filterForm.status"
          placeholder="选择状态"
          clearable
          @change="handleFilterChange"
          class="filter-select"
        >
          <el-option
            v-for="[key, value] in Object.entries(TASK_STATUS_MAP)"
            :key="key"
            :label="value"
            :value="key"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="优先级" class="filter-item">
        <el-select
          v-model="filterForm.priority"
          placeholder="选择优先级"
          clearable
          @change="handleFilterChange"
          class="filter-select"
        >
          <el-option
            v-for="[key, value] in Object.entries(TASK_PRIORITY_MAP)"
            :key="key"
            :label="value"
            :value="key"
          />
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { TASK_STATUS_MAP, TASK_PRIORITY_MAP } from '@/constants/task'

const props = defineProps({
  showProject: {
    type: Boolean,
    default: false
  },
  projects: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['filter'])

const filterForm = ref({
  project_id: null,
  status: null,
  priority: null
})

const handleFilterChange = () => {
  emit('filter', { ...filterForm.value })
}

// 监听项目列表变化，如果只有一个项目，自动选择
watch(() => props.projects, (newProjects) => {
  if (newProjects.length === 1) {
    filterForm.value.project_id = newProjects[0].id
    handleFilterChange()
  }
}, { immediate: true })
</script>

<style scoped>
.filter-section {
  padding: 16px 24px;
  border-bottom: 1px solid #ebeef5;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-item {
  margin-bottom: 0;
}

.filter-select {
  width: 200px;
}
</style> 