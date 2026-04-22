<template>
  <div class="profile-page">
    <van-nav-bar title="编辑资料" fixed placeholder>
      <template #left>
        <van-icon name="arrow-left" @click="$router.back()" />
      </template>
      <template #right>
        <van-button type="primary" size="small" :loading="saving" @click="handleSave">保存</van-button>
      </template>
    </van-nav-bar>
    
    <div class="profile-content">
      <!-- 头像 -->
      <div class="avatar-section">
        <img :src="form.avatar || '/images/default-avatar.png'" class="avatar" />
        <van-button size="small" @click="showAvatarPicker = true">更换头像</van-button>
      </div>
      
      <!-- 表单 -->
      <van-cell-group>
        <van-field
          v-model="form.username"
          label="用户名"
          placeholder="请输入用户名"
        />
        <van-field
          v-model="form.bio"
          type="textarea"
          label="个人简介"
          placeholder="介绍一下自己吧~"
          rows="3"
        />
      </van-cell-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { getUserInfo, updateUserInfo, uploadAvatar } from '@/api/user'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const saving = ref(false)
const showAvatarPicker = ref(false)

const form = ref({
  username: '',
  bio: '',
  avatar: ''
})

const loadProfile = async () => {
  if (!userStore.isLoggedIn) return
  
  try {
    const res: any = await getUserInfo()
    form.value = {
      username: res.data.username,
      bio: res.data.bio || '',
      avatar: res.data.avatar
    }
  } catch (error) {
    showToast('加载失败')
  }
}

const handleSave = async () => {
  saving.value = true
  try {
    await updateUserInfo({
      username: form.value.username,
      bio: form.value.bio
    } as any)
    userStore.setUserInfo({ ...userStore.userInfo!, ...form.value } as any)
    showToast('保存成功')
    router.back()
  } catch {
    showToast('保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.profile-content {
  padding-top: 46px;
}

.avatar-section {
  background: #fff;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}
</style>
