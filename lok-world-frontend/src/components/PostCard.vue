<template>
  <div class="post-card" @click="goDetail">
    <div class="post-header">
      <img :src="post.user.avatar" :alt="post.user.username" class="avatar" />
      <div class="user-info">
        <span class="username">{{ post.user.username }}</span>
        <span class="time">{{ formatTime(post.created_at) }}</span>
      </div>
      <van-tag v-if="post.user.vip_level > 0" type="warning" size="small">VIP</van-tag>
    </div>
    
    <div class="post-content">
      <h3 class="post-title">{{ post.title }}</h3>
      <p class="post-text">{{ post.content }}</p>
      
      <!-- 阵容卡片 -->
      <TeamCard v-if="post.team" :team="post.team" />
      
      <!-- 图片 -->
      <div v-if="post.images?.length" class="post-images">
        <van-image
          v-for="(img, index) in post.images.slice(0, 3)"
          :key="index"
          :src="img"
          fit="cover"
          class="post-image"
          @click.stop="previewImage(index)"
        />
        <span v-if="post.images.length > 3" class="more-images">+{{ post.images.length - 3 }}</span>
      </div>
    </div>
    
    <div class="post-footer">
      <div class="action-item" @click.stop="handleLike">
        <van-icon :name="post.is_liked ? 'like' : 'like-o'" :color="post.is_liked ? '#FF6B35' : '#999'" />
        <span>{{ post.likes_count }}</span>
      </div>
      <div class="action-item" @click.stop="goDetail">
        <van-icon name="comment-o" color="#999" />
        <span>{{ post.comments_count }}</span>
      </div>
      <div class="action-item" @click.stop="handleCollect">
        <van-icon :name="post.is_collected ? 'star' : 'star-o'" :color="post.is_collected ? '#FFD700' : '#999'" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { likePost, collectPost } from '@/api/forum'
import type { Post } from '@/api/types'
import TeamCard from './TeamCard.vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

const props = defineProps<{
  post: Post
}>()

const router = useRouter()

const formatTime = (time: string) => {
  return dayjs(time).fromNow()
}

const goDetail = () => {
  router.push(`/forum/post/${props.post.id}`)
}

const previewImage = (index: number) => {
  // 图片预览
  console.log('preview', index)
}

const handleLike = async () => {
  try {
    await likePost(props.post.id)
    props.post.is_liked = !props.post.is_liked
    props.post.likes_count += props.post.is_liked ? 1 : -1
  } catch {
    showToast('操作失败')
  }
}

const handleCollect = async () => {
  try {
    await collectPost(props.post.id)
    props.post.is_collected = !props.post.is_collected
    showToast(props.post.is_collected ? '已收藏' : '已取消收藏')
  } catch {
    showToast('操作失败')
  }
}
</script>

<style scoped>
.post-card {
  background: #fff;
  border-radius: 8px;
  padding: 12px;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
}

.user-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.time {
  font-size: 12px;
  color: #999;
}

.post-content {
  margin-top: 10px;
}

.post-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.post-text {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-images {
  display: flex;
  gap: 6px;
  margin-top: 10px;
}

.post-image {
  width: 100px;
  height: 100px;
  border-radius: 4px;
}

.more-images {
  width: 100px;
  height: 100px;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.post-footer {
  display: flex;
  gap: 24px;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f5f5f5;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #999;
}
</style>
