// 用户相关
export interface UserInfo {
  id: number
  username: string
  avatar: string
  vip_level: number
  vip_expire_at?: string
  created_at: string
}

export interface LoginParams {
  username: string
  password: string
}

// 宠物相关
export interface Pet {
  id: number
  name: string
  category: string
  image_url: string
  bloodline: string
  stats: {
    hp: number
    attack: number
    defense: number
    magic_attack: number
    magic_defense: number
    speed: number
  }
  recommended_nature: string[]
  recommended_talent: string[]
  recommended_skills: string[]
  capture_location: string
  capture_condition: string
  capture_time: string
  can_evolve: boolean
  evolution_forms?: { id: number; name: string; condition: string }[]
  has_albinism: boolean
  albinism_image?: string
}

export interface PetListParams {
  page?: number
  page_size?: number
  category?: string
  keyword?: string
}

// 论坛相关
export interface Post {
  id: number
  user_id: number
  user: UserInfo
  title: string
  content: string
  images: string[]
  team_id?: number
  team?: Team
  board_id: number
  board_name?: string
  likes_count: number
  comments_count: number
  is_liked: boolean
  is_collected: boolean
  created_at: string
}

export interface PostListParams {
  page?: number
  page_size?: number
  board_id?: number
  user_id?: number
}

export interface Comment {
  id: number
  post_id: number
  user_id: number
  user: UserInfo
  content: string
  parent_id?: number
  parent?: Comment
  likes_count: number
  created_at: string
}

export interface Team {
  id: number
  user_id: number
  name: string
  pets: Pet[]
  description?: string
  created_at: string
}

// 世界频道
export interface ChannelMessage {
  id: number
  user_id: number
  user: UserInfo
  content: string
  created_at: string
}
