<template>
  <div class="project-sprints" v-show="state.isActive">
    <el-card class="sprint-header">
      <template #header>
        <div class="card-header">
          <span>迭代管理</span>
          <el-button type="primary" @click="handleCreateSprint">
            创建迭代
          </el-button>
        </div>
      </template>
    </el-card>

    <el-card class="sprint-list" v-loading="state.loading">
      <el-empty v-if="!sprints.length" description="暂无迭代" />
      <el-timeline v-else>
        <el-timeline-item
          v-for="sprint in sprints"
          :key="sprint.id"
          :type="getSprintStatusType(sprint.status)"
          :timestamp="formatDate(sprint.start_date)"
          placement="top"
        >
          <sprint-card
            :sprint="sprint"
            :loading="state.loading"
            @edit="handleEditSprint"
            @delete="handleDeleteSprint"
            @add-task="handleAddTask"
            @edit-task="handleEditTask"
            @remove-task="handleRemoveTask"
          />
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <!-- 创建/编辑迭代对话框 -->
    <sprint-dialog
      v-model="state.dialogVisible"
      :sprint="sprintForm"
      @submit="handleSubmit"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch, onBeforeUnmount, nextTick, onActivated, onDeactivated } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatDate } from '@/utils/date'
import { useSprintStore } from '@/stores/sprint'
import { useTaskStore } from '@/stores/task'
import SprintCard from './components/SprintCard.vue'
import SprintDialog from './components/SprintDialog.vue'

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
})

const route = useRoute()
const sprintStore = useSprintStore()
const taskStore = useTaskStore()

// 状态管理
const state = reactive({
  loading: false,
  submitting: false,
  dialogVisible: false,
  isActive: false,
  isInitialized: false
})

// 表单数据
const sprintForm = reactive({
  id: null,
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'PLANNING'
})

// 表单验证规则
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
    { required: true, message: '请选择迭代状态', trigger: 'change' }
  ]
}

// 计算属性
const sprints = computed(() => sprintStore.sprints)

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

// 事件处理函数
const handleCreateSprint = () => {
  Object.assign(sprintForm, {
    id: null,
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    status: 'PLANNING'
  })
  state.dialogVisible = true
}

const handleEditSprint = (sprint) => {
  Object.assign(sprintForm, {
    id: sprint.id,
    name: sprint.name,
    description: sprint.description,
    start_date: sprint.start_date,
    end_date: sprint.end_date,
    status: sprint.status
  })
  state.dialogVisible = true
}

const handleDeleteSprint = async (sprint) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该迭代吗？删除后无法恢复。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    state.loading = true
    await sprintStore.deleteSprint(sprint.id)
    ElMessage.success('删除成功')
    await fetchSprints()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除迭代失败:', error)
      ElMessage.error('删除失败')
    }
  } finally {
    state.loading = false
  }
}

const handleSubmit = async (formData) => {
  try {
    state.submitting = true
    const data = {
      ...formData,
      project_id: props.projectId
    }
    
    if (formData.id) {
      await sprintStore.updateSprint(formData.id, data)
      ElMessage.success('更新成功')
    } else {
      await sprintStore.createSprint(data)
      ElMessage.success('创建成功')
    }
    
    state.dialogVisible = false
    await fetchSprints()
  } catch (error) {
    console.error('保存迭代失败:', error)
    ElMessage.error('保存失败')
  } finally {
    state.submitting = false
  }
}

const handleAddTask = async (sprint) => {
  try {
    state.loading = true
    const tasks = await taskStore.fetchTasks(props.projectId)
    const availableTasks = tasks.filter(task => !task.sprint_id)
    
    if (availableTasks.length === 0) {
      ElMessage.warning('没有可添加的任务')
      return
    }
    
    const { value: selectedTaskIds } = await ElMessageBox.prompt(
      '请选择要添加的任务（多个任务ID用逗号分隔）',
      '添加任务',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /^\d+(,\d+)*$/,
        inputErrorMessage: '请输入有效的任务ID'
      }
    )
    
    if (selectedTaskIds) {
      const taskIds = selectedTaskIds.split(',').map(id => parseInt(id.trim()))
      await Promise.all(
        taskIds.map(taskId => 
          taskStore.updateTask(taskId, { sprint_id: sprint.id })
        )
      )
      ElMessage.success('添加任务成功')
      await fetchSprints()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('添加任务失败:', error)
      ElMessage.error('添加任务失败')
    }
  } finally {
    state.loading = false
  }
}

const handleEditTask = async (task) => {
  try {
    state.loading = true
    await taskStore.updateTask(task.id, task)
    ElMessage.success('更新任务成功')
    await fetchSprints()
  } catch (error) {
    console.error('更新任务失败:', error)
    ElMessage.error('更新任务失败')
  } finally {
    state.loading = false
  }
}

const handleRemoveTask = async (sprint, task) => {
  try {
    await ElMessageBox.confirm(
      '确定要从迭代中移除该任务吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    state.loading = true
    await taskStore.updateTask(task.id, { sprint_id: null })
    ElMessage.success('移除任务成功')
    await fetchSprints()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('移除任务失败:', error)
      ElMessage.error('移除任务失败')
    }
  } finally {
    state.loading = false
  }
}

// 数据获取
const fetchSprints = async () => {
  try {
    state.loading = true
    await sprintStore.fetchSprintsByProject(props.projectId)
  } catch (error) {
    console.error('获取迭代列表失败:', error)
    ElMessage.error('获取迭代列表失败')
  } finally {
    state.loading = false
  }
}

// 生命周期钩子
onMounted(async () => {
  state.isActive = true
  await fetchSprints()
  state.isInitialized = true
})

onActivated(() => {
  state.isActive = true
})

onDeactivated(() => {
  state.isActive = false
})

onBeforeUnmount(() => {
  state.isActive = false
  sprintStore.reset()
})
</script>

<style scoped>
.project-sprints {
  padding: 20px;
}

.sprint-header {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sprint-list {
  margin-bottom: 20px;
}
</style> 