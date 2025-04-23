<template>
  <div class="project-costs">
    <el-card class="cost-header">
      <template #header>
        <div class="card-header">
          <span>成本管理</span>
          <el-button type="primary" @click="handleCreateCost">
            记录成本
          </el-button>
        </div>
      </template>
    </el-card>

    <!-- 成本统计卡片 -->
    <el-row :gutter="20" class="cost-stats">
      <el-col :span="8">
        <el-card class="cost-card">
          <template #header>
            <div class="card-header">
              <span>固定成本</span>
            </div>
          </template>
          <div class="cost-amount">¥{{ costStats.fixed.toFixed(2) }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="cost-card">
          <template #header>
            <div class="card-header">
              <span>人力成本</span>
            </div>
          </template>
          <div class="cost-amount">¥{{ costStats.human.toFixed(2) }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="cost-card">
          <template #header>
            <div class="card-header">
              <span>其他成本</span>
            </div>
          </template>
          <div class="cost-amount">¥{{ costStats.other.toFixed(2) }}</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 成本记录列表 -->
    <el-card class="cost-list" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>成本记录</span>
          <el-button type="primary" @click="handleCreateCost">
            添加成本
          </el-button>
        </div>
      </template>
      <el-empty v-if="!costs.length" description="暂无成本记录" />
      <el-table v-else :data="costs" style="width: 100%">
        <el-table-column prop="date" label="日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.date) }}
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getCostTypeTag(row.type)">
              {{ getCostTypeText(row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额" width="120">
          <template #default="{ row }">
            ¥{{ row.amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button-group>
              <el-button type="primary" link @click="handleEditCost(row)">
                编辑
              </el-button>
              <el-button type="danger" link @click="handleDeleteCost(row)">
                删除
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建/编辑成本对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '添加成本' : '编辑成本'"
      width="500px"
    >
      <el-form
        ref="costFormRef"
        :model="costForm"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="类型" prop="type">
          <el-select v-model="costForm.type" placeholder="请选择成本类型" style="width: 100%">
            <el-option label="固定成本" value="FIXED" />
            <el-option label="人力成本" value="HUMAN" />
            <el-option label="其他成本" value="OTHER" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input-number
            v-model="costForm.amount"
            :precision="2"
            :step="100"
            :min="0"
          />
        </el-form-item>
        <el-form-item label="日期" prop="date">
          <el-date-picker
            v-model="costForm.date"
            type="date"
            placeholder="选择日期"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="costForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入成本描述"
          />
        </el-form-item>
      </el-form>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { formatDate } from '@/utils/date'
import { useCostStore } from '@/stores/cost'

const route = useRoute()
const costStore = useCostStore()
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const costFormRef = ref(null)

const projectId = computed(() => Number(route.params.projectId))

const costs = computed(() => costStore.costs)
const costStats = computed(() => costStore.costStats)

const costForm = reactive({
  type: 'FIXED',
  amount: 0,
  date: new Date(),
  description: ''
})

const rules = {
  type: [
    { required: true, message: '请选择成本类型', trigger: 'change' }
  ],
  amount: [
    { required: true, message: '请输入金额', trigger: 'blur' },
    { type: 'number', message: '金额必须为数字', trigger: ['blur', 'change'] }
  ],
  date: [
    { required: true, message: '请选择日期', trigger: 'change' }
  ],
  description: [
    { required: true, message: '请输入成本描述', trigger: 'blur' }
  ]
}

// 获取成本类型对应的标签类型
const getCostTypeTag = (type) => {
  const types = {
    'FIXED': 'info',
    'HUMAN': 'primary',
    'OTHER': 'warning'
  }
  return types[type] || 'info'
}

// 获取成本类型对应的文本
const getCostTypeText = (type) => {
  const texts = {
    'FIXED': '固定成本',
    'HUMAN': '人力成本',
    'OTHER': '其他成本'
  }
  return texts[type] || type
}

// 创建成本记录
const handleCreateCost = () => {
  dialogType.value = 'create'
  Object.assign(costForm, {
    type: 'FIXED',
    amount: 0,
    date: new Date(),
    description: ''
  })
  dialogVisible.value = true
}

// 编辑成本记录
const handleEditCost = (cost) => {
  dialogType.value = 'edit'
  Object.assign(costForm, {
    id: cost.id,
    type: cost.type,
    amount: cost.amount,
    date: cost.date ? new Date(cost.date) : new Date(),
    description: cost.description
  })
  dialogVisible.value = true
}

// 删除成本记录
const handleDeleteCost = async (cost) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该成本记录吗？删除后无法恢复。',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await costStore.deleteCost(cost.id)
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除成本记录失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!costFormRef.value) return
  
  await costFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        loading.value = true
        const formData = {
          ...costForm,
          project_id: projectId.value,
          record_date: costForm.date ? new Date(costForm.date).toISOString() : null,
          cost_type: costForm.type.toLowerCase()
        }
        
        if (dialogType.value === 'create') {
          await costStore.createCost(formData)
          ElMessage.success('创建成功')
        } else {
          await costStore.updateCost(costForm.id, formData)
          ElMessage.success('更新成功')
        }
        
        dialogVisible.value = false
        await fetchCosts()
      } catch (error) {
        console.error('保存成本记录失败:', error)
        ElMessage.error('保存失败')
      } finally {
        loading.value = false
      }
    }
  })
}

// 获取成本列表和统计
const fetchCosts = async () => {
  try {
    loading.value = true
    await Promise.all([
      costStore.fetchCostsByProject(projectId.value),
      costStore.fetchCostStats(projectId.value)
    ])
  } catch (error) {
    console.error('获取成本数据失败:', error)
    ElMessage.error('获取成本数据失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCosts()
})
</script>

<style scoped>
.project-costs {
  padding: 20px;
}

.cost-header {
  margin-bottom: 20px;
}

.cost-stats {
  margin-bottom: 20px;
}

.cost-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cost-amount {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  text-align: center;
}

.cost-list {
  margin-bottom: 20px;
}
</style> 