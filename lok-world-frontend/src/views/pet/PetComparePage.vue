<template>
  <div class="pet-compare-page">
    <van-nav-bar title="宠物对比" fixed placeholder>
      <template #left>
        <van-icon name="arrow-left" @click="$router.back()" />
      </template>
      <template #right>
        <van-icon name="exchange" @click="switchPets" />
      </template>
    </van-nav-bar>
    
    <div v-if="petStore.canCompare" class="compare-content">
      <!-- 宠物信息对比 -->
      <div class="compare-header">
        <div class="pet-info" v-for="pet in petStore.comparePets" :key="pet.id">
          <img :src="pet.image_url" :alt="pet.name" class="pet-image" @error="handleImageError" />
          <span class="pet-name">{{ pet.name }}</span>
          <van-tag type="primary">{{ pet.category }}</van-tag>
        </div>
      </div>
      
      <!-- 资质对比图 -->
      <div class="stats-compare">
        <h3 class="section-title">📊 资质值对比</h3>
        <div class="radar-chart" ref="radarChartRef"></div>
        
        <!-- 柱状图对比 -->
        <div class="bar-compare">
          <div v-for="(value, key) in compareStats" :key="key" class="stat-row">
            <span class="stat-label">{{ statLabels[key] }}</span>
            <div class="bars">
              <div
                class="bar bar-left"
                :style="{ width: `${(value.pet1 / 400) * 100}%`, background: '#FF6B35' }"
              >
                {{ value.pet1 }}
              </div>
              <div
                class="bar bar-right"
                :style="{ width: `${(value.pet2 / 400) * 100}%`, background: '#1989fa' }"
              >
                {{ value.pet2 }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 其他属性对比 -->
      <div class="other-compare">
        <h3 class="section-title">📋 其他信息</h3>
        <van-cell-group>
          <van-cell title="血脉">
            <template #value>
              <span>{{ petStore.comparePets[0].bloodline }}</span>
              <span>{{ petStore.comparePets[1].bloodline }}</span>
            </template>
          </van-cell>
          <van-cell title="捕获地点">
            <template #value>
              <span>{{ petStore.comparePets[0].capture_location }}</span>
              <span>{{ petStore.comparePets[1].capture_location }}</span>
            </template>
          </van-cell>
          <van-cell title="可进阶">
            <template #value>
              <van-tag :type="petStore.comparePets[0].can_evolve ? 'success' : 'default'">
                {{ petStore.comparePets[0].can_evolve ? '是' : '否' }}
              </van-tag>
              <van-tag :type="petStore.comparePets[1].can_evolve ? 'success' : 'default'">
                {{ petStore.comparePets[1].can_evolve ? '是' : '否' }}
              </van-tag>
            </template>
          </van-cell>
          <van-cell title="异色">
            <template #value>
              <van-tag :type="petStore.comparePets[0].has_albinism ? 'warning' : 'default'">
                {{ petStore.comparePets[0].has_albinism ? '有' : '无' }}
              </van-tag>
              <van-tag :type="petStore.comparePets[1].has_albinism ? 'warning' : 'default'">
                {{ petStore.comparePets[1].has_albinism ? '有' : '无' }}
              </van-tag>
            </template>
          </van-cell>
        </van-cell-group>
      </div>
    </div>
    
    <!-- 空状态 -->
    <van-empty v-else description="请选择两个宠物进行对比" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { usePetStore } from '@/stores/pet'
import type { Pet } from '@/api/types'

const petStore = usePetStore()
const radarChartRef = ref<HTMLElement | null>(null)

const statLabels: Record<string, string> = {
  hp: 'HP',
  attack: '攻击',
  defense: '防御',
  magic_attack: '魔攻',
  magic_defense: '魔防',
  speed: '速度'
}

const compareStats = computed(() => {
  if (petStore.comparePets.length < 2) return {}
  
  const pet1 = petStore.comparePets[0]
  const pet2 = petStore.comparePets[1]
  
  return {
    hp: { pet1: pet1.stats.hp, pet2: pet2.stats.hp },
    attack: { pet1: pet1.stats.attack, pet2: pet2.stats.attack },
    defense: { pet1: pet1.stats.defense, pet2: pet2.stats.defense },
    magic_attack: { pet1: pet1.stats.magic_attack, pet2: pet2.stats.magic_attack },
    magic_defense: { pet1: pet1.stats.magic_defense, pet2: pet2.stats.magic_defense },
    speed: { pet1: pet1.stats.speed, pet2: pet2.stats.speed }
  }
})

const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.src = '/images/default-pet.png'
}

const switchPets = () => {
  if (petStore.comparePets.length === 2) {
    const temp = petStore.comparePets[0]
    petStore.comparePets[0] = petStore.comparePets[1]
    petStore.comparePets[1] = temp
  }
}

onMounted(() => {
  // TODO: 使用 Chart.js 或 VChart 渲染雷达图
})
</script>

<style scoped>
.pet-compare-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 20px;
}

.compare-content {
  padding-top: 46px;
}

.compare-header {
  display: flex;
  justify-content: space-around;
  background: #fff;
  padding: 20px;
}

.pet-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.pet-image {
  width: 120px;
  height: 120px;
  object-fit: contain;
  background: #f5f5f5;
  border-radius: 12px;
}

.pet-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

.stats-compare {
  background: #fff;
  padding: 16px;
  margin-top: 10px;
}

.section-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.radar-chart {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
  border-radius: 8px;
  color: #999;
}

.bar-compare {
  margin-top: 20px;
}

.stat-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.stat-label {
  width: 50px;
  font-size: 13px;
  color: #666;
}

.bars {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.bar {
  height: 20px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 8px;
  color: #fff;
  font-size: 12px;
  min-width: 30px;
}

.other-compare {
  background: #fff;
  padding: 16px;
  margin-top: 10px;
}

:deep(.van-cell__value) {
  display: flex;
  gap: 20px;
  justify-content: flex-end;
}
</style>
