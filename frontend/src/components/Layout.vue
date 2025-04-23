<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="layoutStore.isCollapsed ? '64px' : '200px'" v-if="userStore.isLoggedIn">
      <div class="logo-container">
        <img src="@/assets/logo.svg" alt="Logo" class="logo" />
        <span class="logo-text" v-show="!layoutStore.isCollapsed">项目管理系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="side-menu"
        :collapse="layoutStore.isCollapsed"
        router
      >
        <el-menu-item 
          v-for="item in layoutStore.menuItems"
          :key="item.path"
          :index="item.path"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <template #title>{{ item.title }}</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container class="main-container">
      <!-- 顶部导航 -->
      <el-header v-if="userStore.isLoggedIn">
        <div class="header-content">
          <!-- 折叠按钮 -->
          <div class="header-left">
            <el-button
              class="collapse-btn"
              @click="layoutStore.toggleCollapse"
            >
              <el-icon>
                <component :is="layoutStore.isCollapsed ? 'Expand' : 'Fold'" />
              </el-icon>
            </el-button>
            <!-- 面包屑导航 -->
            <el-breadcrumb>
              <el-breadcrumb-item 
                v-for="item in layoutStore.breadcrumbs"
                :key="item.path"
                :to="{ path: item.path }"
              >
                {{ item.title }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>

          <!-- 用户信息 -->
          <div class="user-info">
            <el-dropdown>
              <span class="user-dropdown">
                <el-avatar :size="32" :src="userStore.userInfo?.avatar">
                  {{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() }}
                </el-avatar>
                <span class="username">{{ userStore.userInfo?.username }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="navigateTo('/profile')">
                    <el-icon><User /></el-icon>个人中心
                  </el-dropdown-item>
                  <el-dropdown-item divided @click="handleLogout">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main>
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  House, Folder, List, Timer, DataLine, 
  User, SwitchButton, Expand, Fold 
} from '@element-plus/icons-vue'
import { useUserStore } from '../stores/user'
import { useLayoutStore } from '../stores/layout'
import { ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const layoutStore = useLayoutStore()

// 当前激活的菜单项
const activeMenu = computed(() => route.path)

// 监听路由变化，更新面包屑
watch(() => route, (newRoute) => {
  layoutStore.updateBreadcrumbs(newRoute)
}, { immediate: true, deep: true })

// 页面跳转
const navigateTo = (path) => {
  router.push(path)
}

// 退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await userStore.logout()
    router.push('/login')
  } catch {
    // 用户取消退出
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh !important;
  width: 100vw !important;
  display: flex !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
}

:deep(.el-aside) {
  flex-shrink: 0 !important;
  transition: width 0.3s;
  background-color: var(--el-menu-bg-color) !important;
  padding: 0 !important;
  margin: 0 !important;
  height: 100vh !important;
  overflow: hidden !important;
}

.main-container {
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  height: 100vh !important;
  overflow: hidden !important;
}

:deep(.el-header) {
  padding: 0 !important;
  margin: 0 !important;
  background-color: #fff !important;
  border-bottom: 1px solid #e6e6e6 !important;
  height: 60px !important;
  flex-shrink: 0 !important;
}

:deep(.el-main) {
  flex: 1 !important;
  padding: 20px !important;
  margin: 0 !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
  height: calc(100vh - 60px) !important;
  background-color: #f0f2f5 !important;
}

.header-content {
  height: 100% !important;
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 0 20px !important;
  margin: 0 !important;
}

.header-left {
  display: flex !important;
  align-items: center !important;
  gap: 16px !important;
}

.collapse-btn {
  padding: 0;
  height: auto;
  border: none;
  background: transparent;
  color: var(--el-text-color-primary);
}

.collapse-btn:hover {
  background: transparent;
  color: var(--el-color-primary);
}

.collapse-btn:focus {
  background: transparent;
  color: var(--el-text-color-primary);
}

.user-info {
  display: flex !important;
  align-items: center !important;
}

.user-dropdown {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
  cursor: pointer !important;
}

.username {
  font-size: 14px !important;
  color: var(--el-text-color-primary) !important;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  background: var(--el-menu-bg-color);
  overflow: hidden;
  margin: 0;
}

.logo {
  height: 32px !important;
  width: 32px !important;
  margin-right: 12px !important;
  flex-shrink: 0 !important;
}

.logo-text {
  color: var(--el-menu-text-color) !important;
  font-size: 16px !important;
  font-weight: bold !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.side-menu {
  height: calc(100vh - 60px) !important;
  border-right: none !important;
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}

:deep(.el-menu) {
  border-right: none !important;
  height: calc(100vh - 60px) !important;
}

:deep(.el-menu--collapse) {
  width: 64px !important;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease !important;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0 !important;
}
</style> 