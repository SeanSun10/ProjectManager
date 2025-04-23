<template>
  <div class="project-detail">
    <el-card class="project-info" v-loading="loading">
      <template #header>
        <div class="card-header">
          <h2>{{ project?.name }}</h2>
          <div class="header-actions">
            <el-button type="primary" @click="handleEdit">
              编辑项目
            </el-button>
          </div>
        </div>
      </template>
      <div class="project-description">
        {{ project?.description }}
      </div>
    </el-card>

    <el-card class="project-tabs">
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="项目概览" name="overview">
          <router-view v-if="project" :projectId="project.id" />
        </el-tab-pane>
        <el-tab-pane label="任务管理" name="tasks">
          <router-view v-if="project" :projectId="project.id" />
        </el-tab-pane>
        <el-tab-pane label="迭代管理" name="sprints">
          <router-view v-if="project" :projectId="project.id" />
        </el-tab-pane>
        <el-tab-pane label="成本管理" name="costs">
          <router-view v-if="project" :projectId="project.id" />
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      title="编辑项目"
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
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useProjectStore } from '@/stores/project'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

const activeTab = ref('overview')
const dialogVisible = ref(false)
const submitting = ref(false)
const loading = ref(false)
const projectFormRef = ref(null)

const project = computed(() => projectStore.currentProject)
const projectId = computed(() => Number(route.params.projectId))

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

// 根据路由路径设置当前标签
watch(() => route.path, (path) => {
  const pathSegments = path.split('/')
  if (pathSegments.length > 3) {
    activeTab.value = pathSegments[3]
  } else {
    activeTab.value = 'overview'
  }
}, { immediate: true })

// 处理标签切换
const handleTabClick = (tab) => {
  if (!projectId.value) {
    ElMessage.error('项目ID不存在')
    return
  }

  if (tab.props.name === 'overview') {
    router.push(`/projects/${projectId.value}`)
  } else {
    router.push(`/projects/${projectId.value}/${tab.props.name}`)
  }
}

// 获取项目详情
const fetchProject = async () => {
  try {
    loading.value = true
    console.log('[Debug] 当前路由项目ID:', projectId.value)
    
    if (!projectId.value) {
      ElMessage.error('项目ID不存在')
      router.push('/projects')
      return
    }

    await projectStore.fetchProject(projectId.value)
    const currentProject = projectStore.currentProject
    console.log('[Debug] 从 store 获取到的项目数据:', currentProject)
    
    if (!currentProject) {
      console.error('[Debug] 项目数据为空')
      ElMessage.error('项目不存在')
      router.push('/projects')
      return
    }

    // 使用解构赋值来确保所有字段都被正确赋值
    const {
      name,
      description,
      start_date,
      end_date,
      status,
      fixed_cost_monthly
    } = currentProject

    console.log('[Debug] 解构后的项目数据:', {
      name,
      description,
      start_date,
      end_date,
      status,
      fixed_cost_monthly
    })

    // 更新表单数据
    Object.assign(projectForm, {
      name: name || '',
      description: description || '',
      start_date: start_date ? new Date(start_date) : '',
      end_date: end_date ? new Date(end_date) : '',
      status: status || 'PLANNING',
      fixed_cost_monthly: fixed_cost_monthly || 0
    })

    console.log('[Debug] 更新后的表单数据:', projectForm)

  } catch (error) {
    console.error('[Debug] 获取项目详情失败:', error)
    ElMessage.error('获取项目详情失败')
    router.push('/projects')
  } finally {
    loading.value = false
  }
}

// 添加 project 的 watch
watch(() => project.value, (newVal) => {
  if (!newVal) {
    fetchProject()
  }
}, { immediate: true })

// 处理编辑按钮点击
const handleEdit = () => {
  dialogVisible.value = true
}

// 处理表单提交
const handleSubmit = async () => {
  if (!projectFormRef.value) return
  
  await projectFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        submitting.value = true
        const formData = {
          ...projectForm,
          fixed_cost_monthly: Number(projectForm.fixed_cost_monthly),
          start_date: projectForm.start_date ? new Date(projectForm.start_date).toISOString() : null,
          end_date: projectForm.end_date ? new Date(projectForm.end_date).toISOString() : null
        }
        
        await projectStore.updateProject(route.params.projectId, formData)
        ElMessage.success('更新成功')
        dialogVisible.value = false
        await fetchProject()
      } catch (error) {
        console.error('更新项目失败:', error)
        ElMessage.error('更新失败')
      } finally {
        submitting.value = false
      }
    }
  })
}

onMounted(() => {
  fetchProject()
})
</script>

<style scoped>
.project-detail {
  padding: 20px;
}

.project-info {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  color: #303133;
}

.project-description {
  color: #606266;
  line-height: 1.6;
}

.project-tabs {
  margin-bottom: 20px;
}
</style> 