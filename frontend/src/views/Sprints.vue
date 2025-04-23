<template>
  <div class="sprints-container">
    <div class="header">
      <h2>迭代管理</h2>
      <el-button type="primary" @click="handleAddSprint">
        新建迭代
      </el-button>
    </div>

    <el-table
      :data="sprints"
      style="width: 100%"
      v-loading="loading"
    >
      <el-table-column prop="name" label="迭代名称" />
      <el-table-column prop="description" label="迭代描述" />
      <el-table-column prop="start_date" label="开始日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.start_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="end_date" label="结束日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.end_date) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="project.name" label="所属项目" />
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button type="primary" link @click="handleEditSprint(row)">
            编辑
          </el-button>
          <el-button type="danger" link @click="handleDeleteSprint(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'add' ? '新建迭代' : '编辑迭代'"
      width="500px"
    >
      <el-form
        ref="sprintForm"
        :model="sprintForm"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="迭代名称" prop="name">
          <el-input v-model="sprintForm.name" placeholder="请输入迭代名称" />
        </el-form-item>
        <el-form-item label="迭代描述" prop="description">
          <el-input
            v-model="sprintForm.description"
            type="textarea"
            placeholder="请输入迭代描述"
          />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker
            v-model="sprintForm.start_date"
            type="date"
            placeholder="请选择开始日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker
            v-model="sprintForm.end_date"
            type="date"
            placeholder="请选择结束日期"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="sprintForm.status" placeholder="请选择状态">
            <el-option
              v-for="item in statusOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="所属项目" prop="project_id">
          <el-select v-model="sprintForm.project_id" placeholder="请选择项目">
            <el-option
              v-for="project in projects"
              :key="project.id"
              :label="project.name"
              :value="project.id"
            />
          </el-select>
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
import request from '../utils/request'

const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('add')
const submitting = ref(false)
const sprints = ref([])
const projects = ref([])

const sprintForm = reactive({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'planned',
  project_id: ''
})

const statusOptions = [
  { value: 'planned', label: '计划中' },
  { value: 'in_progress', label: '进行中' },
  { value: 'completed', label: '已完成' }
]

const rules = {
  name: [
    { required: true, message: '请输入迭代名称', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入迭代描述', trigger: 'blur' }
  ],
  start_date: [
    { required: true, message: '请选择开始日期', trigger: 'change' }
  ],
  end_date: [
    { required: true, message: '请选择结束日期', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  project_id: [
    { required: true, message: '请选择所属项目', trigger: 'change' }
  ]
}

const fetchSprints = async () => {
  try {
    loading.value = true
    const response = await request.get('/sprints')
    sprints.value = response
  } catch (error) {
    ElMessage.error('获取迭代列表失败')
  } finally {
    loading.value = false
  }
}

const fetchProjects = async () => {
  try {
    const response = await request.get('/projects')
    projects.value = response
  } catch (error) {
    ElMessage.error('获取项目列表失败')
  }
}

const handleAddSprint = () => {
  dialogType.value = 'add'
  Object.assign(sprintForm, {
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    status: 'planned',
    project_id: ''
  })
  dialogVisible.value = true
}

const handleEditSprint = (row) => {
  dialogType.value = 'edit'
  Object.assign(sprintForm, row)
  dialogVisible.value = true
}

const handleDeleteSprint = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该迭代吗？', '提示', {
      type: 'warning'
    })
    await request.delete(`/sprints/${row.id}`)
    ElMessage.success('删除成功')
    fetchSprints()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  try {
    submitting.value = true
    if (dialogType.value === 'add') {
      await request.post('/sprints', sprintForm)
      ElMessage.success('创建成功')
    } else {
      await request.put(`/sprints/${sprintForm.id}`, sprintForm)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    fetchSprints()
  } catch (error) {
    ElMessage.error(dialogType.value === 'add' ? '创建失败' : '更新失败')
  } finally {
    submitting.value = false
  }
}

const getStatusType = (status) => {
  const types = {
    planned: 'info',
    in_progress: 'warning',
    completed: 'success'
  }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = {
    planned: '计划中',
    in_progress: '进行中',
    completed: '已完成'
  }
  return texts[status] || status
}

const formatDate = (date) => {
  return date ? new Date(date).toLocaleDateString() : ''
}

onMounted(() => {
  fetchSprints()
  fetchProjects()
})
</script>

<style scoped>
.sprints-container {
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