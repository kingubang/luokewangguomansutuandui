import request from './request'
import type { Post, PostListParams, Comment, Team } from './types'

// 获取帖子列表
export const getPostList = (params: PostListParams) => {
  return request.get<{ list: Post[]; total: number; page: number; page_size: number }>('/posts', { params })
}

// 获取帖子详情
export const getPostDetail = (id: number) => {
  return request.get<Post>(`/posts/${id}`)
}

// 创建帖子
export const createPost = (data: { title: string; content: string; images?: string[]; team_id?: number; board_id?: number }) => {
  return request.post<Post>('/posts', data)
}

// 更新帖子
export const updatePost = (id: number, data: Partial<Post>) => {
  return request.put<Post>(`/posts/${id}`, data)
}

// 删除帖子
export const deletePost = (id: number) => {
  return request.delete(`/posts/${id}`)
}

// 点赞帖子
export const likePost = (id: number) => {
  return request.post(`/posts/${id}/like`)
}

// 收藏帖子
export const collectPost = (id: number) => {
  return request.post(`/posts/${id}/collect`)
}

// 获取评论列表
export const getCommentList = (postId: number, page = 1, pageSize = 20) => {
  return request.get<{ list: Comment[]; total: number }>(`/posts/${postId}/comments`, { params: { page, page_size: pageSize } })
}

// 发表评论
export const createComment = (postId: number, data: { content: string; parent_id?: number }) => {
  return request.post<Comment>(`/posts/${postId}/comments`, data)
}

// 删除评论
export const deleteComment = (postId: number, commentId: number) => {
  return request.delete(`/posts/${postId}/comments/${commentId}`)
}

// 创建阵容
export const createTeam = (data: { name: string; pets: number[]; description?: string }) => {
  return request.post<Team>('/teams', data)
}

// 获取我的阵容
export const getMyTeams = () => {
  return request.get<Team[]>('/teams/mine')
}
