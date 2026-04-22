import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/home/HomePage.vue')
  },
  {
    path: '/pet',
    name: 'PetList',
    component: () => import('@/views/pet/PetListPage.vue')
  },
  {
    path: '/pet/:id',
    name: 'PetDetail',
    component: () => import('@/views/pet/PetDetailPage.vue')
  },
  {
    path: '/pet/compare',
    name: 'PetCompare',
    component: () => import('@/views/pet/PetComparePage.vue')
  },
  {
    path: '/forum',
    name: 'Forum',
    component: () => import('@/views/forum/ForumPage.vue')
  },
  {
    path: '/forum/post/:id',
    name: 'PostDetail',
    component: () => import('@/views/forum/PostDetailPage.vue')
  },
  {
    path: '/forum/create',
    name: 'CreatePost',
    component: () => import('@/views/forum/CreatePostPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/channel',
    name: 'WorldChannel',
    component: () => import('@/views/channel/WorldChannelPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('@/views/user/UserPage.vue')
  },
  {
    path: '/user/login',
    name: 'Login',
    component: () => import('@/views/user/LoginPage.vue')
  },
  {
    path: '/user/profile',
    name: 'Profile',
    component: () => import('@/views/user/ProfilePage.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const userStore = useUserStore()
    if (!userStore.isLoggedIn) {
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }
  next()
})

export default router
