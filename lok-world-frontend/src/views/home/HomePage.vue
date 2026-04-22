<template>
  <div class="home-page">
    <!-- 顶部导航 -->
    <van-nav-bar title="洛克世界频道" fixed placeholder>
      <template #right>
        <van-icon name="search" size="20" @click="goSearch" />
      </template>
    </van-nav-bar>
    
    <!-- Banner轮播 -->
    <van-swipe class="banner" :autoplay="3000" indicator-color="#FF6B35">
      <van-swipe-item v-for="(banner, index) in banners" :key="index">
        <img :src="banner.image" :alt="banner.title" @error="handleImageError" />
      </van-swipe-item>
    </van-swipe>
    
    <!-- 快捷入口 -->
    <van-grid class="quick-entry" :column-num="4" :gutter="10">
      <van-grid-item v-for="item in quickEntries" :key="item.icon" :icon="item.icon" :text="item.text" @click="handleEntry(item)" />
    </van-grid>
    
    <!-- 热门宠物 -->
    <div class="section">
      <div class="section-header">
        <span class="section-title">🔥 热门宠物</span>
        <van-button size="small" text="更多" @click="$router.push('/pet')" />
      </div>
      <van-swipe class="pet-swipe" :width="120" :height="150" :show-indications="false" :loop="false">
        <van-swipe-item v-for="pet in hotPets" :key="pet.id" @click="goPetDetail(pet.id)">
          <div class="pet-card">
            <img :src="pet.image_url" :alt="pet.name" class="pet-image" @error="handleImageError" />
            <span class="pet-name">{{ pet.name }}</span>
          </div>
        </van-swipe-item>
      </van-swipe>
    </div>
    
    <!-- 最新帖子 -->
    <div class="section">
      <div class="section-header">
        <span class="section-title">📝 最新帖子</span>
        <van-button size="small" text="更多" @click="$router.push('/forum')" />
      </div>
      <div class="post-list">
        <PostCard v-for="post in latestPosts" :key="post.id" :post="post" />
      </div>
    </div>
    
    <!-- 世界频道入口 -->
    <div class="channel-entry" @click="$router.push('/channel')">
      <van-icon name="chat-o" size="24" color="#FF6B35" />
      <span>世界频道</span>
      <van-badge :content="unreadCount > 99 ? '99+' : unreadCount" :show-zero="false" />
      <van-icon name="arrow" size="16" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getPetList } from '@/api/pet'
import { getPostList } from '@/api/forum'
import PostCard from '@/components/PostCard.vue'
import type { Pet, Post } from '@/api/types'

const router = useRouter()

// 数据
const banners = ref([
  { title: '欢迎来到洛克世界', image: '/images/banner1.jpg' },
  { title: '新宠物上线', image: '/images/banner2.jpg' }
])

const quickEntries = [
  { icon: 'search', text: '宠物查询', route: '/pet' },
  { icon: 'chart-trending-o', text: '宠物对比', route: '/pet/compare' },
  { icon: 'edit', text: '发布帖子', route: '/forum/create' },
  { icon: 'user-o', text: '个人中心', route: '/user' }
]

const hotPets = ref<Pet[]>([])
const latestPosts = ref<Post[]>([])
const unreadCount = ref(5)

// 方法
const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.src = '/images/default-pet.png'
}

const goSearch = () => {
  router.push('/pet')
}

const handleEntry = (item: { route: string }) => {
  router.push(item.route)
}

const goPetDetail = (id: number) => {
  router.push(`/pet/${id}`)
}

const loadData = async () => {
  try {
    // 加载热门宠物
    const petRes: any = await getPetList({ page: 1, page_size: 10 })
    hotPets.value = petRes.data.list || []
    
    // 加载最新帖子
    const postRes: any = await getPostList({ page: 1, page_size: 5 })
    latestPosts.value = postRes.data.list || []
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 70px;
}

.banner {
  height: 180px;
}

.banner img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.quick-entry {
  background: #fff;
  padding: 12px 0;
}

.section {
  background: #fff;
  margin-top: 10px;
  padding: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.pet-swipe {
  height: 160px;
}

.pet-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px;
}

.pet-image {
  width: 100px;
  height: 100px;
  object-fit: contain;
  background: #f5f5f5;
  border-radius: 8px;
}

.pet-name {
  margin-top: 8px;
  font-size: 12px;
  color: #666;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.channel-entry {
  position: fixed;
  bottom: 16px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff;
  padding: 10px 20px;
  border-radius: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
}

.channel-entry span {
  font-size: 14px;
  color: #333;
}
</style>
