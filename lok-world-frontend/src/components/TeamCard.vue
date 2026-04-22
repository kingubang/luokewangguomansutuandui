<template>
  <div class="team-card" @click="goDetail">
    <div class="team-header">
      <van-icon name="friends-o" color="#FF6B35" />
      <span class="team-name">{{ team.name }}</span>
    </div>
    <div class="team-pets">
      <div v-for="pet in team.pets" :key="pet.id" class="pet-item">
        <img :src="pet.image_url" :alt="pet.name" class="pet-icon" />
        <span class="pet-name">{{ pet.name }}</span>
      </div>
    </div>
    <p v-if="team.description" class="team-desc">{{ team.description }}</p>
  </div>
</template>

<script setup lang="ts">
import type { Team } from '@/api/types'

defineProps<{
  team: Team
}>()

const goDetail = () => {
  // 跳转阵容详情
}
</script>

<style scoped>
.team-card {
  background: #FFF7F0;
  border: 1px solid #FFE4D6;
  border-radius: 8px;
  padding: 10px;
  margin-top: 10px;
}

.team-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.team-name {
  font-size: 13px;
  font-weight: 600;
  color: #FF6B35;
}

.team-pets {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.pet-item {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #fff;
  padding: 4px 8px;
  border-radius: 16px;
}

.pet-icon {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.pet-name {
  font-size: 12px;
  color: #666;
}

.team-desc {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}
</style>
