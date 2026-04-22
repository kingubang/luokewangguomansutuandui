<template>
  <div class="channel-page">
    <van-nav-bar title="世界频道" fixed placeholder>
      <template #left>
        <van-icon name="arrow-left" @click="$router.back()" />
      </template>
      <template #right>
        <van-icon name="setting-o" @click="showSettings = true" />
      </template>
    </van-nav-bar>
    
    <!-- 消息列表 -->
    <div class="message-list" ref="messageListRef">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message-item"
        :class="{ 'my-message': msg.user_id === userStore.userId }"
      >
        <img v-if="msg.user_id !== userStore.userId" :src="msg.user.avatar" class="avatar" />
        <div class="message-content">
          <div v-if="msg.user_id !== userStore.userId" class="message-header">
            <span class="username">{{ msg.user.username }}</span>
            <van-tag v-if="msg.user.vip_level > 0" type="warning" size="small">VIP</van-tag>
          </div>
          <div class="message-bubble">
            <span class="message-text">{{ msg.content }}</span>
          </div>
          <span class="message-time">{{ formatTime(msg.created_at) }}</span>
        </div>
      </div>
      
      <van-empty v-if="!messages.length && !loading" description="暂无消息，快来发言吧~" />
      <van-loading v-if="loading" class="loading" />
    </div>
    
    <!-- 输入框 -->
    <div class="input-bar">
      <van-field
        v-model="inputText"
        placeholder="说点什么..."
        @keyup.enter="sendMessage"
      >
        <template #button>
          <van-icon name="send" color="#FF6B35" size="20" @click="sendMessage" />
        </template>
      </van-field>
    </div>
    
    <!-- 设置弹窗 -->
    <van-popup v-model:show="showSettings" position="bottom">
      <van-cell-group title="频道设置">
        <van-cell title="屏蔽用户" is-link />
        <van-cell title="举报" is-link />
        <van-cell title="清空历史" is-link @click="clearHistory" />
      </van-cell-group>
    </van-popup>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { showToast } from 'vant'
import { getHistoryMessages, sendMessage as apiSendMessage, getWebSocketUrl } from '@/api/channel'
import { useUserStore } from '@/stores/user'
import type { ChannelMessage } from '@/api/types'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

const userStore = useUserStore()

const messages = ref<ChannelMessage[]>([])
const inputText = ref('')
const loading = ref(false)
const showSettings = ref(false)
const messageListRef = ref<HTMLElement | null>(null)
let ws: WebSocket | null = null

const formatTime = (time: string) => dayjs(time).fromNow()

const scrollToBottom = () => {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

const loadHistory = async () => {
  loading.value = true
  try {
    const res: any = await getHistoryMessages(50)
    messages.value = res.data || []
    scrollToBottom()
  } catch (error) {
    console.error('加载历史消息失败:', error)
  } finally {
    loading.value = false
  }
}

const connectWebSocket = () => {
  if (!userStore.isLoggedIn) return
  
  const wsUrl = getWebSocketUrl()
  ws = new WebSocket(wsUrl)
  
  ws.onopen = () => {
    console.log('WebSocket connected')
  }
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'message') {
      messages.value.push(data.data)
      scrollToBottom()
    }
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
  
  ws.onclose = () => {
    console.log('WebSocket closed, reconnecting...')
    setTimeout(connectWebSocket, 3000)
  }
}

const sendMessage = async () => {
  if (!inputText.value.trim()) return
  
  try {
    // 如果WebSocket已连接，优先使用WebSocket发送
    if (ws?.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'message', content: inputText.value }))
    } else {
      // 否则调用API
      const res: any = await apiSendMessage(inputText.value)
      messages.value.push(res.data)
    }
    inputText.value = ''
    scrollToBottom()
  } catch (error) {
    showToast('发送失败')
  }
}

const clearHistory = () => {
  messages.value = []
  showSettings.value = false
  showToast('已清空')
}

onMounted(() => {
  loadHistory()
  connectWebSocket()
})

onUnmounted(() => {
  ws?.close()
})
</script>

<style scoped>
.channel-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  padding-bottom: 60px;
}

.message-item {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
}

.message-item.my-message {
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  flex-shrink: 0;
}

.message-content {
  max-width: 70%;
}

.message-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 4px;
}

.username {
  font-size: 12px;
  color: #666;
}

.message-bubble {
  background: #fff;
  padding: 10px 14px;
  border-radius: 12px;
  border-top-left-radius: 4px;
}

.my-message .message-bubble {
  background: #FF6B35;
  color: #fff;
  border-top-left-radius: 12px;
  border-top-right-radius: 4px;
}

.message-text {
  font-size: 14px;
  line-height: 1.4;
}

.message-time {
  font-size: 11px;
  color: #999;
  margin-top: 4px;
  display: block;
}

.my-message .message-time {
  text-align: right;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 16px;
}

.input-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #fff;
  padding: 8px 16px;
  border-top: 1px solid #f5f5f5;
}
</style>
