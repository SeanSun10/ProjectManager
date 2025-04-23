<template>
  <el-menu
    :default-active="activeMenu"
    class="el-menu-vertical"
    :router="true"
    :collapse="isCollapse"
  >
    <el-menu-item index="/projects">
      <el-icon><Document /></el-icon>
      <template #title>项目管理</template>
    </el-menu-item>
    <el-menu-item index="/tasks">
      <el-icon><List /></el-icon>
      <template #title>任务管理</template>
    </el-menu-item>
    <el-menu-item index="/statistics">
      <el-icon><DataLine /></el-icon>
      <template #title>统计分析</template>
    </el-menu-item>
    <el-menu-item index="/profile">
      <el-icon><User /></el-icon>
      <template #title>个人中心</template>
    </el-menu-item>
    <el-menu-item 
      v-if="userStore.userInfo?.is_superuser"
      index="/system-settings"
    >
      <el-icon><Setting /></el-icon>
      <template #title>系统设置</template>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { Document, List, DataLine, User, Setting } from '@element-plus/icons-vue'

const route = useRoute()
const userStore = useUserStore()
const isCollapse = ref(false)

const activeMenu = computed(() => {
  return route.path
})
</script>

<style scoped>
.el-menu-vertical {
  height: 100%;
  border-right: none;
}
</style> 