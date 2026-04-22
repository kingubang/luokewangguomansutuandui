import request from './request'
import type { ChannelMessage } from './types'

// 获取历史消息
export const getHistoryMessages = (limit = 50) => {
  return request.get<ChannelMessage[]>('/channel/history', { params: { limit } })
}

// 发送消息
export const sendMessage = (content: string) => {
  return request.post<ChannelMessage>('/channel/send', { content })
}

// WebSocket连接地址
export const getWebSocketUrl = () => {
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'ws://localhost:8000'
  return `${baseUrl.replace('http', 'ws')}/channel/ws?token=${localStorage.getItem('access_token')}`
}
