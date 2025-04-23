import dayjs from 'dayjs'

export const formatDate = (date) => {
  if (!date) return ''
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

export const formatDateOnly = (date) => {
  if (!date) return ''
  return dayjs(date).format('YYYY-MM-DD')
}

export const formatTimeOnly = (date) => {
  if (!date) return ''
  return dayjs(date).format('HH:mm')
}

export const isBeforeToday = (date) => {
  if (!date) return false
  return dayjs(date).isBefore(dayjs(), 'day')
}

export const isAfterToday = (date) => {
  if (!date) return false
  return dayjs(date).isAfter(dayjs(), 'day')
}

export const isToday = (date) => {
  if (!date) return false
  return dayjs(date).isSame(dayjs(), 'day')
} 