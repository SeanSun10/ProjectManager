<template>
  <div class="system-settings">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>系统参数配置</span>
          <el-button type="primary" @click="handleSaveParams">保存配置</el-button>
        </div>
      </template>
      <el-form
        ref="paramsForm"
        :model="systemParams"
        label-width="200px"
      >
        <el-form-item label="系统名称">
          <el-input v-model="systemParams.system_name" />
        </el-form-item>
        <el-form-item label="系统描述">
          <el-input
            v-model="systemParams.system_description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="任务默认优先级">
          <el-select v-model="systemParams.default_task_priority">
            <el-option label="低" value="low" />
            <el-option label="中" value="medium" />
            <el-option label="高" value="high" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务默认状态">
          <el-select v-model="systemParams.default_task_status">
            <el-option label="待处理" value="pending" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        <el-form-item label="允许的文件类型">
          <el-select
            v-model="systemParams.allowed_file_types"
            multiple
            collapse-tags
          >
            <el-option label="图片" value="image/*" />
            <el-option label="文档" value=".doc,.docx,.pdf" />
            <el-option label="表格" value=".xls,.xlsx" />
            <el-option label="压缩包" value=".zip,.rar" />
          </el-select>
        </el-form-item>
        <el-form-item label="最大文件大小(MB)">
          <el-input-number
            v-model="systemParams.max_file_size"
            :min="1"
            :max="100"
          />
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

// 系统参数
const systemParams = ref({
  system_name: '',
  system_description: '',
  default_task_priority: 'medium',
  default_task_status: 'pending',
  allowed_file_types: [],
  max_file_size: 10
})

// 获取系统参数
const fetchSystemParams = async () => {
  try {
    const response = await axios.get('/api/v1/system/params')
    systemParams.value = response.data
  } catch (error) {
    ElMessage.error('获取系统参数失败')
  }
}

// 保存系统参数
const handleSaveParams = async () => {
  try {
    await axios.put('/api/v1/system/params', systemParams.value)
    ElMessage.success('系统参数保存成功')
  } catch (error) {
    ElMessage.error('系统参数保存失败')
  }
}

onMounted(() => {
  fetchSystemParams()
})
</script>

<style scoped>
.system-settings {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style> 