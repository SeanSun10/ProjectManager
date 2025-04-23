export const TASK_STATUS = {
  TODO: 'TODO',
  IN_PROGRESS: 'IN_PROGRESS',
  REVIEW: 'REVIEW',
  DONE: 'DONE'
}

export const TASK_STATUS_MAP = {
  [TASK_STATUS.TODO]: '待办',
  [TASK_STATUS.IN_PROGRESS]: '进行中',
  [TASK_STATUS.REVIEW]: '评审中',
  [TASK_STATUS.DONE]: '已完成'
}

export const TASK_STATUS_TYPE = {
  [TASK_STATUS.TODO]: 'info',
  [TASK_STATUS.IN_PROGRESS]: 'warning',
  [TASK_STATUS.REVIEW]: 'primary',
  [TASK_STATUS.DONE]: 'success'
}

export const TASK_PRIORITY = {
  LOW: 'LOW',
  MEDIUM: 'MEDIUM',
  HIGH: 'HIGH',
  URGENT: 'URGENT'
}

export const TASK_PRIORITY_MAP = {
  [TASK_PRIORITY.LOW]: '低',
  [TASK_PRIORITY.MEDIUM]: '中',
  [TASK_PRIORITY.HIGH]: '高',
  [TASK_PRIORITY.URGENT]: '紧急'
}

export const TASK_PRIORITY_TYPE = {
  [TASK_PRIORITY.LOW]: 'info',
  [TASK_PRIORITY.MEDIUM]: 'warning',
  [TASK_PRIORITY.HIGH]: 'danger',
  [TASK_PRIORITY.URGENT]: 'danger'
}

export const DEFAULT_TASK_FORM = {
  title: '',
  description: '',
  status: TASK_STATUS.TODO,
  priority: TASK_PRIORITY.MEDIUM,
  assignee_id: null,
  sprint_id: null,
  estimated_hours: 0,
  actual_hours: 0,
  due_date: null
}

export const TASK_FORM_RULES = {
  title: [{ required: true, message: '请输入任务标题', trigger: 'blur' }],
  status: [{ required: true, message: '请选择任务状态', trigger: 'change' }],
  priority: [{ required: true, message: '请选择任务优先级', trigger: 'change' }],
  assignee_id: [{ required: true, message: '请选择负责人', trigger: 'change' }]
} 