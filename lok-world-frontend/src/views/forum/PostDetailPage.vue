<template>
  <div class="post-detail-page">
    <van-nav-bar title="帖子详情" fixed placeholder>
      <template #left>
        <van-icon name="arrow-left" @click="$router.back()" />
      </template>
      <template #right>
        <van-icon name="ellipsis" @click="showActions" />
      </template>
    </van-nav-bar>
    
    <van-loading v-if="loading" vertical>加载中...</van-loading>
    
    <div v-else-if="post" class="post-content">
      <!-- 帖子主体 -->
      <div class="post-main">
        <div class="post-header">
          <img :src="post.user.avatar" :alt="post.user.username" class="avatar" />
          <div class="user-info">
            <div class="user-row">
              <span class="username">{{ post.user.username }}</span>
              <van-tag v-if="post.user.vip_level > 0" type="warning" size="small">VIP</van-tag>
            </div>
            <span class="time">{{ formatTime(post.created_at) }}</span>
          </div>
        </div>
        
        <h1 class="post-title">{{ post.title }}</h1>
        
        <div class="post-body">
          <p class="post-text">{{ post.content }}</p>
          
          <!-- 阵容卡片 -->
          <TeamCard v-if="post.team" :team="post.team" />
          
          <!-- 图片 -->
          <div v-if="post.images?.length" class="post-images">
            <van-image
              v-for="(img, index) in post.images"
              :key="index"
              :src="img"
              fit="cover"
              class="post-image"
              width="100"
              height="100"
              @click="previewImage(index)"
            />
          </div>
        </div>
        
        <div class="post-footer">
          <div class="action-item" :class="{ active: post.is_liked }" @click="handleLike">
            <van-icon :name="post.is_liked ? 'like' : 'like-o'" />
            <span>{{ post.likes_count }}</span>
          </div>
          <div class="action-item" :class="{ active: post.is_collected }" @click="handleCollect">
            <van-icon :name="post.is_collected ? 'star' : 'star-o'" />
            <span>收藏</span>
          </div>
          <div class="action-item" @click="sharePost">
            <van-icon name="share-o" />
            <span>分享</span>
          </div>
        </div>
      </div>
      
      <!-- 评论区域 -->
      <div class="comments-section">
        <h3 class="section-title">评论 ({{ post.comments_count }})</h3>
        
        <van-list
          v-model:loading="commentLoading"
          :finished="commentFinished"
          @load="loadComments"
        >
          <div v-for="comment in comments" :key="comment.id" class="comment-item">
            <img :src="comment.user.avatar" class="comment-avatar" />
            <div class="comment-body">
              <div class="comment-header">
                <span class="comment-username">{{ comment.user.username }}</span>
                <van-tag v-if="comment.user.vip_level > 0" type="warning" size="small">VIP</van-tag>
                <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
              </div>
              <p class="comment-content">{{ comment.content }}</p>
              <div class="comment-actions">
                <span @click="replyComment(comment)">回复</span>
                <span @click="likeComment(comment)">
                  <van-icon :name="comment.is_liked ? 'like' : 'like-o'" size="14" />
                  {{ comment.likes_count }}
                </span>
              </div>
              
              <!-- 楼中楼 -->
              <div v-if="comment.parent" class="sub-comment">
                <span class="sub-username">{{ comment.parent.user.username }}</span>
                <span>：{{ comment.parent.content }}</span>
              </div>
            </div>
          </div>
        </van-list>
      </div>
    </div>
    
    <!-- 底部评论输入 -->
    <div class="comment-input-bar">
      <van-field
        v-model="commentText"
        placeholder="写下你的评论..."
        @click="checkLogin"
      >
        <template #button>
          <van-button size="small" type="primary" @click="submitComment">发送</van-button>
        </template>
      </van-field>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast, showActionSheet, ImagePreview } from 'vant'
import { getPostDetail, getCommentList, createComment, likePost, collectPost as apiCollectPost } from '@/api/forum'
import { useUserStore } from '@/stores/user'
import TeamCard from '@/components/TeamCard.vue'
import type { Post, Comment } from '@/api/types'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const post = ref<Post | null>(null)
const comments = ref<Comment[]>([])
const commentLoading = ref(false)
const commentFinished = ref(false)
const commentPage = ref(1)
const commentText = ref('')
const replyTo = ref<Comment | null>(null)

const formatTime = (time: string) => dayjs(time).fromNow()

const checkLogin = () => {
  if (!userStore.isLoggedIn) {
    router.push({ name: 'Login', query: { redirect: route.fullPath } })
  }
}

const loadPostDetail = async () => {
  const id = Number(route.params.id)
  loading.value = true
  try {
    const res: any = await getPostDetail(id)
    post.value = res.data
  } catch (error) {
    showToast('加载失败')
  } finally {
    loading.value = false
  }
}

const loadComments = async () => {
  if (!post.value) return
  
  commentLoading.value = true
  try {
    const res: any = await getCommentList(post.value.id, commentPage.value)
    const list = res.data?.list || []
    
    comments.value.push(...list)
    commentPage.value++
    
    if (list.length < 20) {
      commentFinished.value = true
    }
  } catch (error) {
    console.error('加载评论失败:', error)
  } finally {
    commentLoading.value = false
  }
}

const submitComment = async () => {
  if (!commentText.value.trim()) return
  if (!userStore.isLoggedIn) {
    checkLogin()
    return
  }
  
  try {
    const res: any = await createComment(post.value!.id, {
      content: commentText.value,
      parent_id: replyTo.value?.id
    })
    comments.value.unshift(res.data)
    post.value!.comments_count++
    commentText.value = ''
    replyTo.value = null
    showToast('评论成功')
  } catch {
    showToast('评论失败')
  }
}

const handleLike = async () => {
  if (!userStore.isLoggedIn) {
    checkLogin()
    return
  }
  try {
    await likePost(post.value!.id)
    post.value!.is_liked = !post.value!.is_liked
    post.value!.likes_count += post.value!.is_liked ? 1 : -1
  } catch {
    showToast('操作失败')
  }
}

const handleCollect = async () => {
  if (!userStore.isLoggedIn) {
    checkLogin()
    return
  }
  try {
    await apiCollectPost(post.value!.id)
    post.value!.is_collected = !post.value!.is_collected
    showToast(post.value!.is_collected ? '已收藏' : '已取消收藏')
  } catch {
    showToast('操作失败')
  }
}

const replyComment = (comment: Comment) => {
  replyTo.value = comment
  // 聚焦输入框
}

const likeComment = async (comment: Comment) => {
  // 实现评论点赞
}

const previewImage = (index: number) => {
  if (post.value?.images) {
    ImagePreview({
      images: post.value.images,
      startPosition: index
    })
  }
}

const sharePost = () => {
  // 分享功能
}

const showActions = () => {
  showActionSheet({
    actions: [
      { name: '举报', color: '#ee0a24' },
      { name: '复制链接' },
      { name: '刷新' }
    ]
  })
}

onMounted(() => {
  loadPostDetail()
})
</script>

<style scoped>
.post-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 60px;
}

.post-content {
  padding-top: 46px;
}

.post-main {
  background: #fff;
  padding: 16px;
  margin-bottom: 10px;
}

.post-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
}

.user-info {
  flex: 1;
}

.user-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-weight: 600;
  color: #333;
}

.time {
  font-size: 12px;
  color: #999;
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 16px 0;
}

.post-text {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
}

.post-images {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.post-footer {
  display: flex;
  justify-content: space-around;
  padding-top: 16px;
  margin-top: 16px;
  border-top: 1px solid #f5f5f5;
}

.action-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #666;
}

.action-item.active {
  color: #FF6B35;
}

.comments-section {
  background: #fff;
  padding: 16px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.comment-item {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.comment-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.comment-username {
  font-size: 13px;
  font-weight: 500;
  color: #333;
}

.comment-time {
  font-size: 11px;
  color: #999;
}

.comment-content {
  font-size: 14px;
  line-height: 1.5;
  color: #333;
}

.comment-actions {
  display: flex;
  gap: 16px;
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}

.sub-comment {
  background: #f5f5f5;
  padding: 8px;
  border-radius: 4px;
  margin-top: 8px;
  font-size: 13px;
  color: #666;
}

.sub-username {
  color: #FF6B35;
}

.comment-input-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 8px 16px;
  border-top: 1px solid #f5f5f5;
}
</style>
