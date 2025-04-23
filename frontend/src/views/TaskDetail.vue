<template>
  <div class="task-detail">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>{{ task?.title }}</h2>
          <el-button type="primary" @click="showEditDialog">编辑任务</el-button>
        </div>
      </template>
      
      <div class="task-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(task?.status)">{{ task?.status }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="优先级">
            <el-tag :type="getPriorityType(task?.priority)">{{ task?.priority }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="预计工时">
            {{ task?.estimated_hours }} 小时
          </el-descriptions-item>
          <el-descriptions-item label="实际工时">
            {{ task?.actual_hours }} 小时
          </el-descriptions-item>
          <el-descriptions-item label="截止日期">
            {{ formatDate(task?.due_date) }}
          </el-descriptions-item>
          <el-descriptions-item label="负责人">
            {{ task?.assignee?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="描述" :span="2">
            {{ task?.description }}
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <!-- 编辑任务对话框 -->
      <el-dialog
        v-model="dialogVisible"
        title="编辑任务"
        width="50%"
        :before-close="handleClose"
      >
        <el-form
          ref="formRef"
          :model="form"
          :rules="rules"
          label-width="120px"
          class="task-form"
        >
          <el-form-item label="标题" prop="title">
            <el-input v-model="form.title" />
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="form.description"
              type="textarea"
              :rows="3"
            />
          </el-form-item>
          <el-form-item label="状态" prop="status">
            <el-select v-model="form.status" placeholder="请选择状态">
              <el-option label="待处理" value="TODO" />
              <el-option label="进行中" value="IN_PROGRESS" />
              <el-option label="已完成" value="DONE" />
            </el-select>
          </el-form-item>
          <el-form-item label="优先级" prop="priority">
            <el-select v-model="form.priority" placeholder="请选择优先级">
              <el-option label="低" value="LOW" />
              <el-option label="中" value="MEDIUM" />
              <el-option label="高" value="HIGH" />
            </el-select>
          </el-form-item>
          <el-form-item label="预计工时" prop="estimated_hours">
            <el-input-number
              v-model="form.estimated_hours"
              :min="0"
              :precision="1"
            />
          </el-form-item>
          <el-form-item label="实际工时" prop="actual_hours">
            <el-input-number
              v-model="form.actual_hours"
              :min="0"
              :precision="1"
            />
          </el-form-item>
          <el-form-item label="截止日期" prop="due_date">
            <el-date-picker
              v-model="form.due_date"
              type="datetime"
              placeholder="选择截止日期"
            />
          </el-form-item>
        </el-form>
        <template #footer>
          <span class="dialog-footer">
            <el-button @click="dialogVisible = false">取消</el-button>
            <el-button type="primary" @click="submitForm">
              确认
            </el-button>
          </span>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useTaskStore } from '@/stores/task'
import { useTeamMemberStore } from '@/stores/teamMember'
import { useSprintStore } from '@/stores/sprint'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatDate } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const taskStore = useTaskStore()
const teamMemberStore = useTeamMemberStore()
const sprintStore = useSprintStore()

const task = ref(null)
const loading = ref(false)
const dialogVisible = ref(false)
const formRef = ref(null)

const form = ref({
  title: '',
  description: '',
  status: '',
  priority: '',
  estimated_hours: 0,
  actual_hours: 0,
  due_date: null
})

const rules = {
  title: [{ required: true, message: '请输入任务标题', trigger: 'blur' }],
  status: [{ required: true, message: '请选择任务状态', trigger: 'change' }],
  priority: [{ required: true, message: '请选择任务优先级', trigger: 'change' }]
}

const getStatusType = (status) => {
  const types = {
    'TODO': 'info',
    'IN_PROGRESS': 'warning',
    'DONE': 'success'
  }
  return types[status] || 'info'
}

const getPriorityType = (priority) => {
  const types = {
    'LOW': 'info',
    'MEDIUM': 'warning',
    'HIGH': 'danger'
  }
  return types[priority] || 'info'
}

const showEditDialog = () => {
  form.value = {
    ...task.value,
    due_date: task.value.due_date ? new Date(task.value.due_date) : null
  }
  dialogVisible.value = true
}

const handleClose = (done) => {
  ElMessageBox.confirm('确认关闭？未保存的更改将会丢失')
    .then(() => {
      done()
    })
    .catch(() => {})
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        loading.value = true
        await taskStore.updateTask(task.value.id, form.value)
        task.value = await taskStore.fetchTask(task.value.id)
        dialogVisible.value = false
        ElMessage.success('更新成功')
      } catch (error) {
        ElMessage.error('更新失败：' + error.message)
      } finally {
        loading.value = false
      }
    }
  })
}

const fetchTaskDetail = async () => {
  try {
    const taskId = route.params.taskId
    if (!taskId) {
      ElMessage.error('任务ID不能为空')
      return
    }
    loading.value = true
    const taskData = await taskStore.fetchTask(taskId)
    task.value = taskData
    form.value = {
      ...taskData,
      due_date: taskData.due_date ? new Date(taskData.due_date) : null
    }
  } catch (error) {
    console.error('获取任务详情失败:', error)
    ElMessage.error('获取任务详情失败：' + (error.message || '未知错误'))
    router.back()
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    await Promise.all([
      fetchTaskDetail(),
      teamMemberStore.fetchTeamMembers(),
      sprintStore.fetchSprintsByProject(route.params.projectId)
    ])
  } catch (error) {
    console.error('初始化数据失败:', error)
    ElMessage.error('加载数据失败，请刷新页面重试')
  }
})
</script>

<style scoped>
.task-detail {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.task-info {
  margin-top: 20px;
}

.task-form {
  margin: 20px 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 