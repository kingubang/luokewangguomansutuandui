<template>
  <div class="login-page">
    <div class="login-header">
      <img src="/images/logo.png" alt="洛克世界频道" class="logo" />
      <h1>洛克世界频道</h1>
      <p>洛克王国玩家的聚集地</p>
    </div>
    
    <div class="login-form">
      <van-tabs v-model:active="activeTab">
        <van-tab title="账号登录" name="account">
          <van-form @submit="handleAccountLogin">
            <van-field
              v-model="accountForm.username"
              name="username"
              label="用户名"
              placeholder="请输入用户名"
              :rules="[{ required: true, message: '请输入用户名' }]"
            />
            <van-field
              v-model="accountForm.password"
              type="password"
              name="password"
              label="密码"
              placeholder="请输入密码"
              :rules="[{ required: true, message: '请输入密码' }]"
            />
            <div class="form-actions">
              <span class="forgot-link">忘记密码？</span>
            </div>
            <van-button type="primary" block round native-type="submit" :loading="loading">登录</van-button>
          </van-form>
        </van-tab>
      </van-tabs>
      
      <div class="divider">
        <span>其他登录方式</span>
      </div>
      
      <div class="oauth-buttons">
        <div class="oauth-btn" @click="handleWechatLogin">
          <img src="/images/wechat.png" alt="微信" />
          <span>微信登录</span>
        </div>
        <div class="oauth-btn" @click="handleQQLogin">
          <img src="/images/qq.png" alt="QQ" />
          <span>QQ登录</span>
        </div>
      </div>
    </div>
    
    <div class="login-footer">
      <span>登录即表示同意</span>
      <a href="#">《用户协议》</a>
      <span>和</span>
      <a href="#">《隐私政策》</a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { showToast } from 'vant'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeTab = ref('account')
const loading = ref(false)

const accountForm = ref({
  username: '',
  password: ''
})

const handleAccountLogin = async () => {
  loading.value = true
  try {
    const success = await authStore.login(accountForm.value.username, accountForm.value.password)
    if (success) {
      showToast('登录成功')
      const redirect = route.query.redirect as string || '/'
      router.replace(redirect)
    } else {
      showToast('登录失败')
    }
  } finally {
    loading.value = false
  }
}

const handleWechatLogin = () => {
  // 唤起微信授权
  // 实际项目中需要通过后端获取授权链接
  const appId = 'your-wechat-app-id'
  const redirectUri = encodeURIComponent(`${location.origin}/oauth/wechat/callback`)
  const state = authStore.generateOAuthState()
  location.href = `https://open.weixin.qq.com/connect/qrconnect?appid=${appId}&redirect_uri=${redirectUri}&response_type=code&scope=snsapi_login&state=${state}#wechat_redirect`
}

const handleQQLogin = () => {
  // 唤起QQ授权
  const appId = 'your-qq-app-id'
  const redirectUri = encodeURIComponent(`${location.origin}/oauth/qq/callback`)
  const state = authStore.generateOAuthState()
  location.href = `https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=${appId}&redirect_uri=${redirectUri}&state=${state}`
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(180deg, #FF6B35 0%, #FF8C42 100%);
  padding: 40px 24px;
}

.login-header {
  text-align: center;
  color: #fff;
  padding: 40px 0;
}

.logo {
  width: 80px;
  height: 80px;
  background: #fff;
  border-radius: 20px;
  margin-bottom: 16px;
}

.login-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.login-header p {
  font-size: 14px;
  opacity: 0.9;
}

.login-form {
  background: #fff;
  border-radius: 16px;
  padding: 24px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.forgot-link {
  color: #FF6B35;
  font-size: 14px;
}

.divider {
  display: flex;
  align-items: center;
  margin: 24px 0;
  color: #999;
  font-size: 12px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #eee;
}

.divider span {
  padding: 0 16px;
}

.oauth-buttons {
  display: flex;
  justify-content: center;
  gap: 40px;
}

.oauth-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.oauth-btn img {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

.oauth-btn span {
  font-size: 12px;
  color: #666;
}

.login-footer {
  position: fixed;
  bottom: 20px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

.login-footer a {
  color: #fff;
  text-decoration: underline;
}
</style>
