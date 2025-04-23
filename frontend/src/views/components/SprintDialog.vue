<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑迭代' : '创建迭代'"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      label-position="right"
    >
      <el-form-item label="迭代名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入迭代名称" />
      </el-form-item>
      
      <el-form-item label="迭代描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入迭代描述"
        />
      </el-form-item>
      
      <el-form-item label="开始日期" prop="start_date">
        <el-date-picker
          v-model="form.start_date"
          type="date"
          placeholder="请选择开始日期"
          value-format="YYYY-MM-DD"
          :disabled-date="disabledStartDate"
        />
      </el-form-item>
      
      <el-form-item label="结束日期" prop="end_date">
        <el-date-picker
          v-model="form.end_date"
          type="date"
          placeholder="请选择结束日期"
          value-format="YYYY-MM-DD"
          :disabled-date="disabledEndDate"
        />
      </el-form-item>
      
      <el-form-item label="迭代状态" prop="status">
        <el-select v-model="form.status" placeholder="请选择迭代状态">
          <el-option
            v-for="item in statusOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
    </el-form>
    
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="loading">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  sprint: {
    type: Object,
    default: () => ({
      id: null,
      name: '',
      description: '',
      start_date: '',
      end_date: '',
      status: 'PLANNING'
    })
  }
})

const emit = defineEmits(['update:modelValue', 'submit'])

const dialogVisible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const isEdit = computed(() => !!props.sprint?.id)

const formRef = ref(null)
const loading = ref(false)

const form = reactive({
  id: null,
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  status: 'PLANNING'
})

const rules = {
  name: [
    { required: true, message: '请输入迭代名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入迭代描述', trigger: 'blur' },
    { max: 500, message: '长度不能超过 500 个字符', trigger: 'blur' }
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

const statusOptions = [
  { value: 'PLANNING', label: '规划中' },
  { value: 'IN_PROGRESS', label: '进行中' },
  { value: 'COMPLETED', label: '已完成' }
]

// 禁用开始日期
const disabledStartDate = (time) => {
  if (form.end_date) {
    return time > new Date(form.end_date)
  }
  return false
}

// 禁用结束日期
const disabledEndDate = (time) => {
  if (form.start_date) {
    return time < new Date(form.start_date)
  }
  return false
}

// 初始化表单数据
const initForm = () => {
  if (isEdit.value) {
    Object.assign(form, props.sprint)
  } else {
    Object.assign(form, {
      id: null,
      name: '',
      description: '',
      start_date: '',
      end_date: '',
      status: 'PLANNING'
    })
  }
}

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false
  formRef.value?.resetFields()
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    loading.value = true
    await emit('submit', { ...form })
    
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    handleClose()
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    loading.value = false
  }
}

// 监听对话框显示状态
watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      initForm()
    }
  }
)

// 监听 sprint 属性变化
watch(
  () => props.sprint,
  (newVal) => {
    if (newVal && props.modelValue) {
      initForm()
    }
  },
  { deep: true }
)
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 