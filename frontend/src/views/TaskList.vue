<template>
  <div class="task-list">
    <div class="header">
      <h2>任务列表</h2>
      <el-button type="primary" @click="showCreateDialog">新建任务</el-button>
    </div>

    <el-table
      v-loading="taskStore.loading"
      :data="taskStore.tasks"
      style="width: 100%"
    >
      <el-table-column prop="title" label="标题" />
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="TASK_STATUS_TYPE[row.status]">
            {{ TASK_STATUS_MAP[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="priority" label="优先级">
        <template #default="{ row }">
          <el-tag :type="TASK_PRIORITY_TYPE[row.priority]">
            {{ TASK_PRIORITY_MAP[row.priority] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="assignee.name" label="负责人" />
      <el-table-column prop="estimated_hours" label="预计工时" />
      <el-table-column prop="actual_hours" label="实际工时" />
      <el-table-column prop="due_date" label="截止日期">
        <template #default="{ row }">
          {{ formatDate(row.due_date) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button
              size="small"
              @click="handleView(row)"
            >
              查看
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑任务对话框 -->
    <el-dialog
      :title="dialogType === 'create' ? '新建任务' : '编辑任务'"
      v-model="dialogVisible"
      width="50%"
    >
      <TaskForm
        ref="taskFormRef"
        :initial-data="taskForm"
        :team-members="teamMembers"
        :sprints="sprints"
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue'
import { useTaskStore } from '@/stores/task'
import { useTeamMemberStore } from '@/stores/teamMember'
import { useSprintStore } from '@/stores/sprint'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatDate } from '@/utils/date'
import { useRouter, useRoute } from 'vue-router'
import TaskForm from '@/components/TaskForm.vue'
import {
  TASK_STATUS_TYPE,
  TASK_STATUS_MAP,
  TASK_PRIORITY_TYPE,
  TASK_PRIORITY_MAP,
  DEFAULT_TASK_FORM
} from '@/constants/task'

const props = defineProps({
  projectId: {
    type: Number,
    required: true
  }
})

const taskStore = useTaskStore()
const teamMemberStore = useTeamMemberStore()
const sprintStore = useSprintStore()
const dialogVisible = ref(false)
const dialogType = ref('create')
const taskForm = ref({ ...DEFAULT_TASK_FORM })
const taskFormRef = ref(null)

const router = useRouter()
const route = useRoute()

const teamMembers = computed(() => teamMemberStore.teamMembers)
const sprints = computed(() => sprintStore.sprints)

// 监听路由参数变化
watch(
  () => route.params.projectId,
  (newProjectId, oldProjectId) => {
    if (newProjectId && newProjectId !== oldProjectId) {
      taskStore.fetchTasks(Number(newProjectId))
    }
  },
  { immediate: true }
)

// 监听项目ID变化
watch(
  () => props.projectId,
  async (newProjectId, oldProjectId) => {
    if (newProjectId && newProjectId !== oldProjectId) {
      await Promise.all([
        taskStore.fetchTasks(newProjectId),
        teamMemberStore.fetchTeamMembers(),
        sprintStore.fetchSprintsByProject(newProjectId)
      ])
    }
  },
  { immediate: true }
)

const showCreateDialog = async () => {
  dialogType.value = 'create'
  taskForm.value = { ...DEFAULT_TASK_FORM }
  
  try {
    await Promise.all([
      teamMemberStore.fetchTeamMembers(),
      sprintStore.fetchSprintsByProject(props.projectId)
    ])
    
    if (teamMemberStore.teamMembers.length > 0) {
      dialogVisible.value = true
    } else {
      ElMessage.warning('暂无可选的团队成员，请先添加团队成员')
    }
  } catch (error) {
    ElMessage.error('加载数据失败，请重试')
  }
}

const handleView = (row) => {
  router.push(`/projects/${props.projectId}/tasks/${row.id}`)
}

const handleEdit = async (row) => {
  dialogType.value = 'edit'
  taskForm.value = {
    ...row,
    due_date: row.due_date ? new Date(row.due_date) : null
  }
  
  try {
    await Promise.all([
      teamMemberStore.fetchTeamMembers(),
      sprintStore.fetchSprintsByProject(props.projectId)
    ])
    dialogVisible.value = true
  } catch (error) {
    ElMessage.error('加载数据失败，请重试')
  }
}

const handleSubmit = async () => {
  if (!taskFormRef.value) return
  
  const valid = await taskFormRef.value.validate()
  if (valid) {
    try {
      const formData = taskFormRef.value.getForm()
      
      if (dialogType.value === 'create') {
        await taskStore.createTask({
          ...formData,
          project_id: props.projectId
        })
        ElMessage.success('创建任务成功')
      } else {
        await taskStore.updateTask(formData.id, {
          ...formData,
          project_id: props.projectId
        })
        ElMessage.success('更新任务成功')
      }
      dialogVisible.value = false
      await taskStore.fetchTasks(props.projectId)
    } catch (error) {
      ElMessage.error(error.message || '操作失败')
    }
  }
}

const handleDelete = async (task) => {
  try {
    await ElMessageBox.confirm('确定要删除该任务吗？', '提示', {
      type: 'warning'
    })
    await taskStore.deleteTask(task.id)
    ElMessage.success('删除任务成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

onMounted(async () => {
  if (props.projectId) {
    await Promise.all([
      taskStore.fetchTasks(props.projectId),
      teamMemberStore.fetchTeamMembers(),
      sprintStore.fetchSprintsByProject(props.projectId)
    ])
  }
})

onBeforeUnmount(() => {
  taskStore.clearTasks()
})
</script>

<style scoped>
.task-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 