import request from './request'
import type { UserInfo, LoginParams } from './types'

// 用户登录
export const login = (data: LoginParams) => {
  return request.post<{ access_token: string; refresh_token: string; user: UserInfo }>('/auth/login', data)
}

// 微信登录
export const loginWithWechat = (code: string) => {
  return request.post<{ access_token: string; refresh_token: string; user: UserInfo }>('/auth/wechat', { code })
}

// QQ登录
export const loginWithQQ = (code: string) => {
  return request.post<{ access_token: string; refresh_token: string; user: UserInfo }>('/auth/qq', { code })
}

// 获取用户信息
export const getUserInfo = () => {
  return request.get<UserInfo>('/user/info')
}

// 更新用户信息
export const updateUserInfo = (data: Partial<UserInfo>) => {
  return request.put<UserInfo>('/user/info', data)
}

// 上传头像
export const uploadAvatar = (file: File) => {
  const formData = new FormData()
  formData.append('avatar', file)
  return request.post<{ avatar_url: string }>('/user/avatar', formData)
}

// 关注用户
export const followUser = (userId: number) => {
  return request.post(`/user/follow/${userId}`)
}

// 取消关注
export const unfollowUser = (userId: number) => {
  return request.delete(`/user/follow/${userId}`)
}
