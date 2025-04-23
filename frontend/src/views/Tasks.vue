<template>
  <div class="tasks-container">
    <div class="page-header">
      <h2 class="page-title">任务管理</h2>
      <el-button type="primary" class="create-btn" @click="showAddTaskDialog = true">
        <el-icon><Plus /></el-icon>
        新建任务
      </el-button>
    </div>

    <el-card class="main-card" shadow="never">
      <!-- 筛选条件 -->
      <TaskFilter
        :show-project="true"
        :projects="projects"
        @filter="handleFilter"
      />

      <!-- 任务列表 -->
      <TaskTable
        :tasks="filteredTasks"
        :loading="taskStore.loading"
        :show-project="true"
        @edit="handleEdit"
        @delete="handleDelete"
      />

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          class="pagination"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑任务对话框 -->
    <el-dialog
      :title="isEdit ? '编辑任务' : '创建任务'"
      v-model="showAddTaskDialog"
      width="600px"
      class="task-dialog"
    >
      <TaskForm
        ref="taskFormRef"
        :initial-data="taskForm"
        :team-members="teamMembers"
        :sprints="sprints"
      />
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddTaskDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import { useTaskStore } from '@/stores/task'
import { useProjectStore } from '@/stores/project'
import { useTeamMemberStore } from '@/stores/teamMember'
import { useSprintStore } from '@/stores/sprint'
import { ElMessage, ElMessageBox } from 'element-plus'
import TaskFilter from '@/components/TaskFilter.vue'
import TaskTable from '@/components/TaskTable.vue'
import TaskForm from '@/components/TaskForm.vue'
import { DEFAULT_TASK_FORM } from '@/constants/task'

const taskStore = useTaskStore()
const projectStore = useProjectStore()
const teamMemberStore = useTeamMemberStore()
const sprintStore = useSprintStore()

const showAddTaskDialog = ref(false)
const isEdit = ref(false)
const taskFormRef = ref(null)
const taskForm = ref({ ...DEFAULT_TASK_FORM })

// 计算属性
const projects = computed(() => projectStore.projects)
const teamMembers = computed(() => teamMemberStore.teamMembers)
const sprints = computed(() => sprintStore.sprints)

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 筛选条件
const filterConditions = ref({
  project_id: null,
  status: null,
  priority: null
})

// 计算属性：过滤后的任务列表
const filteredTasks = computed(() => {
  let result = taskStore.tasks

  if (filterConditions.value.project_id) {
    result = result.filter(task => task.project_id === filterConditions.value.project_id)
  }

  if (filterConditions.value.status) {
    result = result.filter(task => task.status === filterConditions.value.status)
  }

  if (filterConditions.value.priority) {
    result = result.filter(task => task.priority === filterConditions.value.priority)
  }

  total.value = result.length
  
  // 分页
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return result.slice(start, end)
})

// 处理筛选
const handleFilter = (filters) => {
  filterConditions.value = filters
  currentPage.value = 1
  fetchTasks()
}

// 处理分页大小变化
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchTasks()
}

// 处理页码变化
const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchTasks()
}

const handleEdit = (row) => {
  isEdit.value = true
  taskForm.value = { ...row }
  showAddTaskDialog.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该任务吗？', '提示', {
      type: 'warning'
    })
    await taskStore.deleteTask(row.id)
    ElMessage.success('删除成功')
    await fetchTasks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!taskFormRef.value) return
  
  const valid = await taskFormRef.value.validate()
  if (valid) {
    try {
      const formData = taskFormRef.value.getForm()
      
      if (isEdit.value) {
        await taskStore.updateTask(formData.id, formData)
        ElMessage.success('更新成功')
      } else {
        await taskStore.createTask(formData)
        ElMessage.success('创建成功')
      }
      showAddTaskDialog.value = false
      taskForm.value = { ...DEFAULT_TASK_FORM }
      await fetchTasks()
    } catch (error) {
      ElMessage.error(error.message || '操作失败')
    }
  }
}

// 获取任务列表
const fetchTasks = async () => {
  try {
    await taskStore.fetchTasks(filterConditions.value.project_id)
  } catch (error) {
    console.error('获取任务列表失败:', error)
    ElMessage.error('获取任务列表失败')
  }
}

onMounted(async () => {
  try {
    await Promise.all([
      projectStore.fetchProjects(),
      teamMemberStore.fetchTeamMembers()
    ])
    // 如果有项目数据，默认选择第一个项目
    if (projectStore.projects.length > 0) {
      filterConditions.value.project_id = projectStore.projects[0].id
    }
    await fetchTasks()
  } catch (error) {
    console.error('初始化数据失败:', error)
    ElMessage.error('加载数据失败，请刷新页面重试')
  }
})
</script>

<style scoped>
.tasks-container {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.create-btn {
  display: flex;
  align-items: center;
  gap: 8px;
}

.main-card {
  border-radius: 8px;
  border: none;
  background-color: #fff;
}

.pagination-section {
  padding: 16px 24px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: flex-end;
}

.pagination {
  margin-top: 0;
}

.task-dialog :deep(.el-dialog__body) {
  padding: 20px 24px;
}

.task-dialog :deep(.el-form-item) {
  margin-bottom: 20px;
}

.task-dialog :deep(.el-dialog__footer) {
  padding: 16px 24px;
  border-top: 1px solid #ebeef5;
}
</style> 