<template>
  <div class="pet-detail-page">
    <van-nav-bar title="宠物详情" fixed placeholder>
      <template #left>
        <van-icon name="arrow-left" @click="$router.back()" />
      </template>
      <template #right>
        <van-icon name="chart-trending-o" size="20" @click="addToCompare" />
      </template>
    </van-nav-bar>
    
    <van-loading v-if="loading" vertical>加载中...</van-loading>
    
    <div v-else-if="pet" class="pet-content">
      <!-- 基础信息 -->
      <div class="section pet-header">
        <img :src="pet.image_url" :alt="pet.name" class="pet-image" @error="handleImageError" />
        <div v-if="pet.has_albinism" class="albinism-tag">异色</div>
        <h2 class="pet-name">{{ pet.name }}</h2>
        <div class="pet-tags">
          <van-tag type="primary">{{ pet.category }}</van-tag>
          <van-tag>{{ pet.bloodline }}</van-tag>
        </div>
      </div>
      
      <!-- 资质值 -->
      <div class="section">
        <h3 class="section-title">📊 资质值</h3>
        <div class="stats-grid">
          <div v-for="(value, key) in pet.stats" :key="key" class="stat-item">
            <span class="stat-label">{{ statLabels[key] }}</span>
            <van-progress
              :percentage="(value / 400) * 100"
              :pivot-text="value.toString()"
              :color="getStatColor(value)"
            />
          </div>
        </div>
      </div>
      
      <!-- 培养推荐 -->
      <div class="section">
        <h3 class="section-title">🎯 培养推荐</h3>
        <div class="recommend-card">
          <div class="recommend-item">
            <span class="recommend-label">推荐性格</span>
            <div class="recommend-tags">
              <van-tag v-for="n in pet.recommended_nature" :key="n" type="warning">{{ n }}</van-tag>
            </div>
          </div>
          <div class="recommend-item">
            <span class="recommend-label">推荐天分</span>
            <div class="recommend-tags">
              <van-tag v-for="t in pet.recommended_talent" :key="t" type="success">{{ t }}</van-tag>
            </div>
          </div>
          <div class="recommend-item">
            <span class="recommend-label">推荐技能</span>
            <div class="skill-list">
              <span v-for="s in pet.recommended_skills" :key="s" class="skill-tag">{{ s }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 捕获相关 -->
      <div class="section">
        <h3 class="section-title">📍 捕获信息</h3>
        <van-cell-group>
          <van-cell title="捕获地点" :value="pet.capture_location" />
          <van-cell title="捕获条件" :value="pet.capture_condition" />
          <van-cell title="捕获时间" :value="pet.capture_time" />
        </van-cell-group>
      </div>
      
      <!-- 进阶相关 -->
      <div v-if="pet.can_evolve" class="section">
        <h3 class="section-title">⬆️ 进阶信息</h3>
        <van-cell-group>
          <van-cell title="可进阶形态" :value="pet.evolution_forms?.map(e => e.name).join('、') || '无'" />
          <van-cell title="进阶条件" :value="pet.evolution_forms?.[0]?.condition || '未知'" />
        </van-cell-group>
        <div v-if="pet.evolution_forms?.length" class="evolution-chain">
          <img :src="pet.image_url" class="evo-pet" />
          <van-icon name="arrow" />
          <img
            v-for="evo in pet.evolution_forms"
            :key="evo.id"
            :src="getEvoImage(evo.id)"
            class="evo-pet"
            @click="goEvoPet(evo.id)"
          />
        </div>
      </div>
      
      <!-- 异色相关 -->
      <div v-if="pet.has_albinism" class="section">
        <h3 class="section-title">🌈 异色形态</h3>
        <img :src="pet.albinism_image" class="albinism-image" @error="handleImageError" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from 'vant'
import { getPetDetail } from '@/api/pet'
import { usePetStore } from '@/stores/pet'
import type { Pet } from '@/api/types'

const route = useRoute()
const router = useRouter()
const petStore = usePetStore()

const loading = ref(true)
const pet = ref<Pet | null>(null)

const statLabels: Record<string, string> = {
  hp: 'HP',
  attack: '攻击',
  defense: '防御',
  magic_attack: '魔攻',
  magic_defense: '魔防',
  speed: '速度'
}

const getStatColor = (value: number) => {
  if (value >= 350) return '#FF6B35'
  if (value >= 300) return '#07c160'
  if (value >= 250) return '#1989fa'
  return '#999'
}

const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.src = '/images/default-pet.png'
}

const getEvoImage = (id: number) => {
  return `/images/pet/${id}.png`
}

const goEvoPet = (id: number) => {
  router.push(`/pet/${id}`)
}

const addToCompare = () => {
  if (pet.value) {
    if (petStore.comparePets.length >= 2) {
      showToast('对比栏已满')
      return
    }
    petStore.addToCompare(pet.value)
    showToast('已添加到对比栏')
  }
}

const loadPetDetail = async () => {
  const id = Number(route.params.id)
  loading.value = true
  try {
    const res: any = await getPetDetail(id)
    pet.value = res.data
  } catch (error) {
    console.error('加载宠物详情失败:', error)
    showToast('加载失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadPetDetail()
})
</script>

<style scoped>
.pet-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.pet-content {
  padding-top: 46px;
}

.section {
  background: #fff;
  margin-bottom: 10px;
  padding: 16px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.pet-header {
  text-align: center;
}

.pet-image {
  width: 200px;
  height: 200px;
  object-fit: contain;
  margin: 0 auto;
}

.pet-name {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin: 12px 0;
}

.pet-tags {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.albinism-tag {
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  color: #fff;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.stats-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-label {
  width: 50px;
  font-size: 13px;
  color: #666;
}

.recommend-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.recommend-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.recommend-label {
  font-size: 13px;
  color: #666;
  min-width: 70px;
}

.recommend-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.skill-tag {
  background: #f5f5f5;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

.evolution-chain {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
}

.evo-pet {
  width: 60px;
  height: 60px;
  object-fit: contain;
  background: #f5f5f5;
  border-radius: 8px;
  cursor: pointer;
}

.albinism-image {
  width: 100%;
  max-width: 200px;
  display: block;
  margin: 0 auto;
  border-radius: 8px;
}
</style>
