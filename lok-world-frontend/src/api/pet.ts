import request from './request'
import type { Pet, PetListParams } from './types'

// 获取宠物列表
export const getPetList = (params: PetListParams) => {
  return request.get<{ list: Pet[]; total: number; page: number; page_size: number }>('/pets', { params })
}

// 获取宠物详情
export const getPetDetail = (id: number) => {
  return request.get<Pet>(`/pets/${id}`)
}

// 搜索宠物
export const searchPets = (keyword: string) => {
  return request.get<Pet[]>('/pets/search', { params: { keyword } })
}

// 获取宠物对比数据
export const comparePets = (ids: number[]) => {
  return request.post<{ pets: Pet[] }>('/pets/compare', { ids })
}
