<template>
  <div class="team-editor">
    <van-field v-model="teamName" label="阵容名称" placeholder="给阵容起个名字" />
    
    <div class="pet-selector">
      <div class="section-header">
        <span>选择宠物</span>
        <span class="pet-count">{{ selectedPets.length }}/6</span>
      </div>
      
      <van-search
        v-model="keyword"
        placeholder="搜索宠物"
        @search="searchPet"
      />
      
      <div class="pet-grid">
        <div
          v-for="pet in searchResults"
          :key="pet.id"
          class="pet-option"
          :class="{ selected: isSelected(pet.id) }"
          @click="togglePet(pet)"
        >
          <img :src="pet.image_url" class="pet-icon" />
          <span class="pet-name">{{ pet.name }}</span>
          <van-icon v-if="isSelected(pet.id)" name="success" class="check-icon" />
        </div>
      </div>
      
      <van-empty v-if="!searchResults.length && keyword" description="未找到相关宠物" />
    </div>
    
    <van-field
      v-model="description"
      type="textarea"
      label="阵容说明"
      placeholder="介绍一下这个阵容的特点..."
      rows="3"
    />
    
    <div class="actions">
      <van-button @click="$emit('cancel')">取消</van-button>
      <van-button type="primary" :disabled="!canSave" @click="handleSave">保存</van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { showToast } from 'vant'
import { searchPets, createTeam } from '@/api/forum'
import type { Pet } from '@/api/types'

const emit = defineEmits<{
  (e: 'save', team: any): void
  (e: 'cancel'): void
}>()

const teamName = ref('')
const description = ref('')
const keyword = ref('')
const searchResults = ref<Pet[]>([])
const selectedPets = ref<Pet[]>([])

const canSave = computed(() => {
  return teamName.value.trim() && selectedPets.value.length >= 1
})

const searchPet = async () => {
  if (!keyword.value.trim()) return
  
  try {
    const res: any = await searchPets(keyword.value)
    searchResults.value = res.data || []
  } catch (error) {
    console.error('搜索失败:', error)
  }
}

const isSelected = (petId: number) => {
  return selectedPets.value.some(p => p.id === petId)
}

const togglePet = (pet: Pet) => {
  if (isSelected(pet.id)) {
    selectedPets.value = selectedPets.value.filter(p => p.id !== pet.id)
  } else if (selectedPets.value.length < 6) {
    selectedPets.value.push(pet)
  } else {
    showToast('最多选择6只宠物')
  }
}

const handleSave = async () => {
  try {
    const res: any = await createTeam({
      name: teamName.value,
      pets: selectedPets.value.map(p => p.id),
      description: description.value || undefined
    })
    emit('save', res.data)
    showToast('阵容创建成功')
  } catch (error) {
    showToast('创建失败')
  }
}
</script>

<style scoped>
.team-editor {
  padding: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  font-weight: 600;
}

.pet-count {
  color: #FF6B35;
  font-weight: normal;
}

.pet-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  padding: 12px 0;
}

.pet-option {
  position: relative;
  background: #f5f5f5;
  padding: 12px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  border: 2px solid transparent;
}

.pet-option.selected {
  border-color: #FF6B35;
  background: #FFF7F0;
}

.pet-icon {
  width: 50px;
  height: 50px;
  object-fit: contain;
}

.pet-name {
  font-size: 12px;
  color: #666;
}

.check-icon {
  position: absolute;
  top: 4px;
  right: 4px;
  color: #FF6B35;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

.actions .van-button {
  flex: 1;
}
</style>
