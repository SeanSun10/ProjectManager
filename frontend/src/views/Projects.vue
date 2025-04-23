<template>
  <div class="projects-container">
    <div class="header">
      <h2>项目管理</h2>
      <el-button type="primary" @click="handleAddProject">
        新建项目
      </el-button>
    </div>

    <el-table
      :data="projects"
      style="width: 100%"
      v-loading="loading"
      :empty-text="loading ? '加载中...' : '暂无项目数据'"
    >
      <el-table-column prop="name" label="项目名称" min-width="150">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleViewProject(row)">
            {{ row.name }}
          </el-button>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="项目描述" min-width="200" show-overflow-tooltip />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="fixed_cost_monthly" label="固定月成本" width="120">
        <template #default="{ row }">
          ¥{{ row.fixed_cost_monthly?.toFixed(2) || '0.00' }}
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleViewProject(row)">
            概览
          </el-button>
          <el-button type="primary" link @click="handleEditProject(row)">
            编辑
          </el-button>
          <el-button type="danger" link @click="handleDeleteProject(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新建项目' : '编辑项目'"
      width="500px"
    >
      <el-form
        ref="projectFormRef"
        :model="projectForm"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="projectForm.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            placeholder="请输入项目描述"
          />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="projectForm.start_date" type="date" placeholder="选择开始日期" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="projectForm.end_date" type="date" placeholder="选择结束日期" />
        </el-form-item>
        <el-form-item label="项目状态" prop="status">
          <el-select v-model="projectForm.status" placeholder="选择项目状态">
            <el-option label="规划中" value="PLANNING" />
            <el-option label="进行中" value="IN_PROGRESS" />
            <el-option label="已完成" value="COMPLETED" />
            <el-option label="已取消" value="CANCELLED" />
            <el-option label="已暂停" value="ON_HOLD" />
          </el-select>
        </el-form-item>
        <el-form-item label="固定月成本" prop="fixed_cost_monthly">
          <el-input 
            v-model.number="projectForm.fixed_cost_monthly" 
            type="number" 
            placeholder="请输入固定月成本" 
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import request from '../utils/request'

const router = useRouter()
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('add')
const submitting = ref(false)
const projects = ref([])
const projectFormRef = ref(null)

const projectForm = reactive({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'PLANNING',
  fixed_cost_monthly: 0
})

const rules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入项目描述', trigger: 'blur' }
  ],
  start_date: [
    { required: true, message: '请选择开始日期', trigger: 'change' }
  ],
  end_date: [
    { required: true, message: '请选择结束日期', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择项目状态', trigger: 'change' }
  ],
  fixed_cost_monthly: [
    { required: true, message: '请输入固定月成本', trigger: 'blur' },
    { type: 'number', message: '成本必须为数字', trigger: ['blur', 'change'] }
  ]
}

const fetchProjects = async () => {
  try {
    loading.value = true
    const response = await request.get('projects/')
    projects.value = Array.isArray(response) ? response : []
    if (projects.value.length === 0) {
      ElMessage.info('暂无项目数据')
    }
  } catch (error) {
    console.error('获取项目列表失败:', error)
    ElMessage.error('获取项目列表失败')
    projects.value = []
  } finally {
    loading.value = false
  }
}

const handleViewProject = (row) => {
  router.push(`/projects/${row.id}`)
}

const handleAddProject = () => {
  dialogType.value = 'add'
  projectForm.name = ''
  projectForm.description = ''
  projectForm.start_date = ''
  projectForm.end_date = ''
  projectForm.status = 'PLANNING'
  projectForm.fixed_cost_monthly = 0
  dialogVisible.value = true
}

const handleEditProject = (row) => {
  dialogType.value = 'edit'
  projectForm.name = row.name
  projectForm.description = row.description
  projectForm.start_date = row.start_date
  projectForm.end_date = row.end_date
  projectForm.status = row.status
  projectForm.fixed_cost_monthly = row.fixed_cost_monthly
  projectForm.id = row.id
  dialogVisible.value = true
}

const handleDeleteProject = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {
      type: 'warning'
    })
    await request.delete(`projects/${row.id}/`)
    ElMessage.success('删除成功')
    fetchProjects()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!projectFormRef.value) return
  
  await projectFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitting.value = true
        const formData = {
          name: projectForm.name,
          description: projectForm.description,
          status: projectForm.status,
          fixed_cost_monthly: Number(projectForm.fixed_cost_monthly),
          start_date: projectForm.start_date ? new Date(projectForm.start_date).toISOString() : null,
          end_date: projectForm.end_date ? new Date(projectForm.end_date).toISOString() : null
        }
        
        if (dialogType.value === 'add') {
          await request.post('projects/', formData)
          ElMessage.success('创建成功')
        } else {
          await request.put(`projects/${projectForm.id}/`, formData)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchProjects()
      } catch (error) {
        console.error('提交失败:', error)
        ElMessage.error(dialogType.value === 'add' ? '创建失败' : '更新失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

const getStatusType = (status) => {
  const statusMap = {
    'PLANNING': 'info',
    'IN_PROGRESS': 'primary',
    'COMPLETED': 'success',
    'ON_HOLD': 'warning'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    'PLANNING': '规划中',
    'IN_PROGRESS': '进行中',
    'COMPLETED': '已完成',
    'ON_HOLD': '已暂停'
  }
  return statusMap[status] || status
}

onMounted(() => {
  fetchProjects()
})
</script>

<style scoped>
.projects-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  color: #303133;
}
</style> 