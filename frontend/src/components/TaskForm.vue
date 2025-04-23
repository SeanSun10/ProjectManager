<template>
  <el-form
    ref="formRef"
    :model="form"
    :rules="TASK_FORM_RULES"
    label-width="100px"
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
      <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
        <el-option
          v-for="[key, value] in Object.entries(TASK_STATUS_MAP)"
          :key="key"
          :label="value"
          :value="key"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="优先级" prop="priority">
      <el-select v-model="form.priority" placeholder="请选择优先级" style="width: 100%">
        <el-option
          v-for="[key, value] in Object.entries(TASK_PRIORITY_MAP)"
          :key="key"
          :label="value"
          :value="key"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="负责人" prop="assignee_id">
      <el-select v-model="form.assignee_id" placeholder="请选择负责人" style="width: 100%">
        <el-option
          v-for="member in teamMembers"
          :key="member.id"
          :label="member.name"
          :value="member.id"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="所属迭代" prop="sprint_id">
      <el-select v-model="form.sprint_id" placeholder="请选择迭代" style="width: 100%">
        <el-option
          v-for="sprint in sprints"
          :key="sprint.id"
          :label="sprint.name"
          :value="sprint.id"
        />
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
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue'
import {
  TASK_STATUS_MAP,
  TASK_PRIORITY_MAP,
  TASK_FORM_RULES,
  DEFAULT_TASK_FORM
} from '@/constants/task'

const props = defineProps({
  initialData: {
    type: Object,
    default: () => ({ ...DEFAULT_TASK_FORM })
  },
  teamMembers: {
    type: Array,
    default: () => []
  },
  sprints: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:form'])

const formRef = ref(null)
const form = ref({ ...props.initialData })

watch(() => props.initialData, (newVal) => {
  form.value = { ...newVal }
}, { deep: true })

// 暴露表单验证方法
defineExpose({
  validate: () => formRef.value?.validate(),
  getForm: () => form.value
})
</script> 