<template>
  <router-view v-slot="{ Component }">
    <component :is="Component" />
  </router-view>
</template>

<style>
:root {
  --el-menu-bg-color: #001529;
  --el-menu-text-color: rgba(255, 255, 255, 0.85);
  --el-menu-active-color: #1890ff;
  --el-menu-hover-bg-color: #1890ff;
}

body {
  margin: 0 !important;
  padding: 0 !important;
  min-width: 100vw !important;
  min-height: 100vh !important;
  overflow: hidden !important;
}

#app {
  margin: 0 !important;
  padding: 0 !important;
  width: 100vw !important;
  min-width: 100vw !important;
  height: 100vh !important;
  min-height: 100vh !important;
  overflow: hidden !important;
}

.el-container.layout-container {
  margin: 0 !important;
  padding: 0 !important;
  width: 100vw !important;
  min-width: 100vw !important;
  height: 100vh !important;
  min-height: 100vh !important;
  display: flex !important;
}

/* Element Plus 布局覆盖 */
.el-container {
  margin: 0 !important;
  padding: 0 !important;
  height: 100% !important;
  width: 100% !important;
}

:deep(.el-aside) {
  padding: 0 !important;
  margin: 0 !important;
  flex-shrink: 0 !important;
  background-color: var(--el-menu-bg-color) !important;
  width: auto !important;
}

:deep(.el-main) {
  padding: 20px !important;
  background-color: #f0f2f5 !important;
  height: calc(100vh - 60px) !important;
  overflow-y: auto !important;
  flex: 1 !important;
}

/* Element Plus 菜单覆盖 */
.el-menu {
  --el-menu-bg-color: var(--el-menu-bg-color);
  --el-menu-text-color: var(--el-menu-text-color);
  --el-menu-active-color: var(--el-menu-active-color);
  --el-menu-hover-bg-color: var(--el-menu-hover-bg-color);
  border-right: none !important;
  width: 100% !important;
}

.el-menu-item {
  font-size: 14px !important;
  font-weight: 500 !important;
  letter-spacing: 0.5px;
  padding-left: 20px !important;
}

.el-menu-item:not(.is-active) {
  color: var(--el-menu-text-color) !important;
}

.el-menu-item.is-active {
  background-color: var(--el-menu-hover-bg-color) !important;
  color: #ffffff !important;
  font-weight: 600 !important;
}

.el-menu-item:hover {
  background-color: var(--el-menu-hover-bg-color) !important;
  color: #ffffff !important;
}

.el-menu-item .el-icon {
  color: inherit;
  font-size: 18px !important;
  margin-right: 10px !important;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

/* 确保 Layout 组件内的元素正确对齐 */
.el-header {
  padding: 0 20px !important;
  margin: 0 !important;
  width: 100% !important;
  background-color: #fff !important;
  border-bottom: 1px solid #e6e6e6 !important;
}
</style>
