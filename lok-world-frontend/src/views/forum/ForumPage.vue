<template>
  <div class="forum-page">
    <van-nav-bar title="论坛" fixed placeholder>
      <template #left>
        <van-icon name="arrow-left" @click="$router.back()" />
      </template>
      <template #right>
        <van-icon name="search" size="20" @click="showSearch = true" />
      </template>
    </van-nav-bar>
    
    <!-- 版块选择 -->
    <van-tabs v-model:active="activeBoard" sticky offset-top="46">
      <van-tab title="全部" name="" />
      <van-tab v-for="board in boards" :key="board.id" :title="board.name" :name="board.id" />
    </van-tabs>
    
    <!-- 帖子列表 -->
    <div class="post-list">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="loadMore"
      >
        <PostCard v-for="post in postList" :key="post.id" :post="post" />
      </van-list>
    </div>
    
    <!-- 发布按钮 -->
    <van-button
      type="primary"
      round
      size="large"
      class="publish-btn"
      icon="edit"
      @click="goCreate"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { getPostList } from '@/api/forum'
import PostCard from '@/components/PostCard.vue'
import type { Post } from '@/api/types'

const router = useRouter()

// 状态
const boards = ref([
  { id: 1, name: '攻略' },
  { id: 2, name: '讨论' },
  { id: 3, name: '阵容' },
  { id: 4, name: '交易' },
  { id: 5, name: '求助' }
])
const activeBoard = ref('')
const postList = ref<Post[]>([])
const loading = ref(false)
const finished = ref(false)
const showSearch = ref(false)
const page = ref(1)
const pageSize = 20

// 方法
const loadPosts = async (reset = false) => {
  if (reset) {
    page.value = 1
    finished.value = false
  }
  
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize,
      board_id: activeBoard.value || undefined
    }
    const res: any = await getPostList(params)
    const list = res.data?.list || []
    
    if (reset) {
      postList.value = list
    } else {
      postList.value.push(...list)
    }
    
    if (list.length < pageSize) {
      finished.value = true
    } else {
      page.value++
    }
  } catch (error) {
    console.error('加载帖子失败:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  if (!loading.value && !finished.value) {
    loadPosts()
  }
}

const goCreate = () => {
  router.push('/forum/create')
}

// 监听版块变化
watch(activeBoard, () => {
  loadPosts(true)
})

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.forum-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 70px;
}

.post-list {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.publish-btn {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
  z-index: 100;
}
</style>
