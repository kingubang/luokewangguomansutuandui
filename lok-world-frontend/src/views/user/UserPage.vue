<template>
  <div class="user-page">
    <van-nav-bar title="我的" fixed placeholder />
    
    <!-- 用户信息卡片 -->
    <div class="user-card">
      <div v-if="userStore.isLoggedIn" class="user-info">
        <img :src="userStore.userInfo?.avatar || '/images/default-avatar.png'" class="avatar" />
        <div class="info">
          <div class="username-row">
            <span class="username">{{ userStore.userInfo?.username }}</span>
            <van-tag v-if="userStore.isVip" type="warning">VIP {{ userStore.vipLevel }}</van-tag>
          </div>
          <span class="user-id">ID: {{ userStore.userId }}</span>
        </div>
        <van-button size="small" plain @click="$router.push('/user/profile')">编辑</van-button>
      </div>
      <div v-else class="login-prompt" @click="$router.push('/user/login')">
        <img src="/images/default-avatar.png" class="avatar" />
        <span>点击登录</span>
      </div>
    </div>
    
    <!-- 数据统计 -->
    <van-grid class="stats-grid" :column-num="4">
      <van-grid-item>
        <span class="stat-value">0</span>
        <span class="stat-label">发帖</span>
      </van-grid-item>
      <van-grid-item>
        <span class="stat-value">0</span>
        <span class="stat-label">关注</span>
      </van-grid-item>
      <van-grid-item>
        <span class="stat-value">0</span>
        <span class="stat-label">粉丝</span>
      </van-grid-item>
      <van-grid-item>
        <span class="stat-value">0</span>
        <span class="stat-label">收藏</span>
      </van-grid-item>
    </van-grid>
    
    <!-- 功能菜单 -->
    <van-cell-group class="menu-group" title="我的内容">
      <van-cell title="我的帖子" is-link icon="orders-o" />
      <van-cell title="我的评论" is-link icon="comment-o" />
      <van-cell title="我的收藏" is-link icon="star-o" />
      <van-cell title="我的阵容" is-link icon="friends-o" @click="$router.push('/user/teams')" />
    </van-cell-group>
    
    <van-cell-group class="menu-group" title="增值服务">
      <van-cell title="开通VIP" is-link icon="vip-card-o" @click="openVip" />
    </van-cell-group>
    
    <van-cell-group class="menu-group" title="设置">
      <van-cell title="账号设置" is-link icon="setting-o" />
      <van-cell title="通知设置" is-link icon="bell-o" />
      <van-cell title="关于我们" is-link icon="info-o" />
      <van-cell title="退出登录" is-link icon="close" @click="handleLogout" />
    </van-cell-group>
  </div>
</template>

<script setup lang="ts">
import { showToast, showConfirmDialog } from 'vant'
import { useUserStore } from '@/stores/user'
import { useAuthStore } from '@/stores/auth'

const userStore = useUserStore()
const authStore = useAuthStore()

const openVip = () => {
  showToast('VIP功能开发中')
}

const handleLogout = async () => {
  await showConfirmDialog({
    title: '确认退出',
    message: '确定要退出登录吗？'
  })
  authStore.logout()
  showToast('已退出登录')
}
</script>

<style scoped>
.user-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-top: 46px;
}

.user-card {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  padding: 24px 16px;
  color: #fff;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 2px solid #fff;
}

.info {
  flex: 1;
}

.username-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-size: 18px;
  font-weight: 600;
}

.user-id {
  font-size: 12px;
  opacity: 0.8;
}

.login-prompt {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stats-grid {
  background: #fff;
}

.stat-value {
  font-size: 18px;
  font-weight: 600;
  color: #FF6B35;
}

.stat-label {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.menu-group {
  margin-top: 10px;
}
</style>
