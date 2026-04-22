import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login as apiLogin, loginWithWechat, loginWithQQ } from '@/api/user'
import { useUserStore } from './user'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const userStore = useUserStore()
  
  // State
  const isLoading = ref(false)
  const oauthState = ref('')
  
  // Actions
  const login = async (username: string, password: string) => {
    isLoading.value = true
    try {
      const res: any = await apiLogin({ username, password })
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('refresh_token', res.data.refresh_token)
      userStore.setUserInfo(res.data.user)
      return true
    } catch (error) {
      console.error('登录失败:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  const loginByWechat = async (code: string) => {
    isLoading.value = true
    try {
      const res: any = await loginWithWechat(code)
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('refresh_token', res.data.refresh_token)
      userStore.setUserInfo(res.data.user)
      return true
    } catch (error) {
      console.error('微信登录失败:', error)
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  const loginByQQ = async (code: string) => {
    isLoading.value = true
    try {
      const res: any = await loginWithQQ(code)
      localStorage.setItem('access_token', res.data.access_token)
      localStorage.setItem('refresh_token', res.data.refresh_token)
      userStore.setUserInfo(res.data.user)
      return true
    } catch (error) {
      console.error('QQ登录失败:', error)
      return false
    } finally
    } finally {
      isLoading.value = false
    }
  }
  
  const logout = () => {
    userStore.clearUserInfo()
    router.push({ name: 'Home' })
  }
  
  // 生成OAuth state
  const generateOAuthState = () => {
    oauthState.value = Math.random().toString(36).substring(2, 15)
    return oauthState.value
  }
  
  return {
    isLoading,
    oauthState,
    login,
    loginByWechat,
    loginByQQ,
    logout,
    generateOAuthState
  }
})
