import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'
import Layout from '../components/Layout.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: {
      title: '登录'
    }
  },
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('../views/Home.vue'),
        meta: {
          title: '首页',
          requiresAuth: true
        }
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('../views/Projects.vue'),
        meta: {
          title: '项目管理',
          requiresAuth: true
        }
      },
      {
        path: 'tasks',
        name: 'Tasks',
        component: () => import('../views/Tasks.vue'),
        meta: {
          title: '任务管理',
          requiresAuth: true
        }
      },
      {
        path: 'projects/:projectId',
        name: 'ProjectDetail',
        component: () => import('@/views/ProjectDetail.vue'),
        meta: {
          title: '项目详情',
          requiresAuth: true,
          keepAlive: false
        },
        children: [
          {
            path: '',
            name: 'ProjectOverview',
            component: () => import('@/views/ProjectOverview.vue'),
            props: true,
            meta: {
              title: '项目概览',
              requiresAuth: true,
              keepAlive: false
            }
          },
          {
            path: 'tasks',
            name: 'ProjectTasks',
            component: () => import('@/views/TaskList.vue'),
            props: true,
            meta: {
              title: '任务列表',
              requiresAuth: true,
              keepAlive: false
            }
          },
          {
            path: 'tasks/:taskId',
            name: 'TaskDetail',
            component: () => import('@/views/TaskDetail.vue'),
            props: true,
            meta: {
              title: '任务详情',
              requiresAuth: true,
              keepAlive: false
            }
          },
          {
            path: 'sprints',
            name: 'ProjectSprints',
            component: () => import('../views/ProjectSprints.vue'),
            props: true,
            meta: {
              title: '迭代管理',
              requiresAuth: true,
              keepAlive: false
            }
          },
          {
            path: 'costs',
            name: 'ProjectCosts',
            component: () => import('@/views/ProjectCosts.vue'),
            props: true,
            meta: {
              title: '成本管理',
              requiresAuth: true,
              keepAlive: false
            }
          }
        ]
      },
      {
        path: 'sprints',
        name: 'Sprints',
        component: () => import('../views/Sprints.vue'),
        meta: {
          title: '迭代管理',
          requiresAuth: true
        }
      },
      {
        path: 'statistics',
        name: 'Statistics',
        component: () => import('../views/Statistics.vue'),
        meta: {
          title: '统计分析',
          requiresAuth: true
        }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/UserProfile.vue'),
        meta: {
          title: '个人中心',
          requiresAuth: true
        }
      },
      {
        path: '/team-members',
        name: 'TeamMembers',
        component: () => import('../views/TeamMembers.vue'),
        meta: {
          title: '团队成员管理',
          requiresAuth: true
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 项目管理系统` : '项目管理系统'
  
  // 检查是否需要登录
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else {
    next()
  }
})

export default router 