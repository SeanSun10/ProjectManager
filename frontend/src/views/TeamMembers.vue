<template>
  <div class="team-members">
    <el-card class="header-card">
      <template #header>
        <div class="card-header">
          <span>团队成员管理</span>
          <el-button type="primary" @click="handleCreate">
            添加成员
          </el-button>
        </div>
      </template>
    </el-card>

    <!-- 成员列表 -->
    <el-card class="list-card">
      <el-table
        :data="teamMembers"
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="role" label="角色" />
        <el-table-column prop="monthly_salary" label="月薪">
          <template #default="{ row }">
            ¥{{ row.monthly_salary.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="join_date" label="加入日期">
          <template #default="{ row }">
            {{ formatDate(row.join_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="leave_date" label="离职日期">
          <template #default="{ row }">
            {{ row.leave_date ? formatDate(row.leave_date) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" link @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '添加成员' : '编辑成员'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-input v-model="form.role" />
        </el-form-item>
        <el-form-item label="月薪" prop="monthly_salary">
          <el-input-number
            v-model="form.monthly_salary"
            :min="0"
            :precision="2"
            :step="1000"
          />
        </el-form-item>
        <el-form-item label="加入日期" prop="join_date">
          <el-date-picker
            v-model="form.join_date"
            type="date"
            placeholder="选择日期"
          />
        </el-form-item>
        <el-form-item label="离职日期" prop="leave_date">
          <el-date-picker
            v-model="form.leave_date"
            type="date"
            placeholder="选择日期"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '../utils/request'
import { formatDate } from '../utils/date'

const loading = ref(false)
const teamMembers = ref([])
const dialogVisible = ref(false)
const dialogType = ref('create')
const formRef = ref(null)
const form = ref({
  name: '',
  role: '',
  monthly_salary: 0,
  join_date: new Date(),
  leave_date: null
})

const rules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  role: [{ required: true, message: '请输入角色', trigger: 'blur' }],
  monthly_salary: [{ required: true, message: '请输入月薪', trigger: 'blur' }],
  join_date: [{ required: true, message: '请选择加入日期', trigger: 'change' }]
}

// 获取团队成员列表
const fetchTeamMembers = async () => {
  try {
    loading.value = true
    const response = await request.get('/team-members')
    teamMembers.value = response
  } catch (error) {
    console.error('获取团队成员列表失败:', error)
    ElMessage.error('获取团队成员列表失败')
  } finally {
    loading.value = false
  }
}

// 创建成员
const handleCreate = () => {
  dialogType.value = 'create'
  form.value = {
    name: '',
    role: '',
    monthly_salary: 0,
    join_date: new Date(),
    leave_date: null
  }
  dialogVisible.value = true
}

// 编辑成员
const handleEdit = (row) => {
  dialogType.value = 'edit'
  form.value = { ...row }
  dialogVisible.value = true
}

// 删除成员
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该成员吗？', '提示', {
      type: 'warning'
    })
    
    await request.delete(`/team-members/${row.id}`)
    ElMessage.success('删除成功')
    fetchTeamMembers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除成员失败:', error)
      ElMessage.error('删除成员失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    if (dialogType.value === 'create') {
      await request.post('/team-members', form.value)
      ElMessage.success('添加成功')
    } else {
      await request.put(`/team-members/${form.value.id}`, form.value)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    fetchTeamMembers()
  } catch (error) {
    console.error('提交表单失败:', error)
    ElMessage.error('提交表单失败')
  }
}

onMounted(() => {
  fetchTeamMembers()
})
</script>

<style scoped>
.team-members {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.list-card {
  margin-bottom: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 