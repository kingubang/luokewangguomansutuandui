import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/api/types'

export const useUserStore = defineStore('user', () => {
  // State
  const userInfo = ref<UserInfo | null>(null)
  const isLoggedIn = computed(() => !!userInfo.value)
  
  // Getters
  const userId = computed(() => userInfo.value?.id)
  const isVip = computed(() => (userInfo.value?.vip_level ?? 0) > 0)
  const vipLevel = computed(() => userInfo.value?.vip_level ?? 0)
  
  // Actions
  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
  }
  
  const clearUserInfo = () => {
    userInfo.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }
  
  // 初始化（从localStorage恢复）
  const init = () => {
    const token = localStorage.getItem('access_token')
    if (token && userInfo.value) {
      // Token存在但用户信息为空，后续由请求拦截器处理
    }
  }
  
  return {
    userInfo,
    isLoggedIn,
    userId,
    isVip,
    vipLevel,
    setUserInfo,
    clearUserInfo,
    init
  }
})
