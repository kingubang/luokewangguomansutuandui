<template>
  <div class="pet-list-page">
    <van-nav-bar title="宠物查询" fixed placeholder>
      <template #left>
        <van-icon name="arrow-left" @click="$router.back()" />
      </template>
    </van-nav-bar>
    
    <!-- 搜索栏 -->
    <div class="search-bar">
      <van-search
        v-model="keyword"
        placeholder="搜索宠物名称"
        shape="round"
        @search="onSearch"
      />
    </div>
    
    <!-- 筛选标签 -->
    <van-tabs v-model:active="activeCategory" sticky offset-top="46">
      <van-tab title="全部" name="" />
      <van-tab v-for="cat in categories" :key="cat" :title="cat" :name="cat" />
    </van-tabs>
    
    <!-- 宠物列表 -->
    <div class="pet-list">
      <van-list
        v-model:loading="loading"
        :finished="finished"
        finished-text="没有更多了"
        @load="loadMore"
      >
        <div class="pet-grid">
          <div
            v-for="pet in petList"
            :key="pet.id"
            class="pet-item"
            @click="goDetail(pet.id)"
          >
            <div class="pet-image-wrapper">
              <img :src="pet.image_url" :alt="pet.name" class="pet-image" @error="handleImageError" />
              <van-badge v-if="pet.has_albinism" content="异色" color="#FF6B35" />
            </div>
            <div class="pet-info">
              <span class="pet-name">{{ pet.name }}</span>
              <span class="pet-category">{{ pet.category }}</span>
            </div>
            <div class="pet-actions">
              <van-icon name="chart-trending-o" size="18" @click.stop="addToCompare(pet)" />
            </div>
          </div>
        </div>
      </van-list>
    </div>
    
    <!-- 对比栏 -->
    <div v-if="petStore.comparePets.length > 0" class="compare-bar">
      <div class="compare-pets">
        <div v-for="p in petStore.comparePets" :key="p.id" class="compare-pet">
          <img :src="p.image_url" :alt="p.name" />
          <van-icon name="cross" size="14" @click="petStore.removeFromCompare(p.id)" />
        </div>
      </div>
      <van-button
        type="primary"
        size="small"
        :disabled="petStore.comparePets.length < 2"
        @click="$router.push('/pet/compare')"
      >
        对比 ({{ petStore.comparePets.length }}/2)
      </van-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { getPetList, searchPets } from '@/api/pet'
import { usePetStore } from '@/stores/pet'
import type { Pet } from '@/api/types'

const router = useRouter()
const petStore = usePetStore()

// 状态
const keyword = ref('')
const activeCategory = ref('')
const categories = ['火系', '水系', '草系', '电系', '冰系', '翼系', '土系', '石系', '虫系', '龙系', '暗系', '萌系']
const petList = ref<Pet[]>([])
const loading = ref(false)
const finished = ref(false)
const page = ref(1)
const pageSize = 20

// 方法
const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.src = '/images/default-pet.png'
}

const loadPetList = async (reset = false) => {
  if (reset) {
    page.value = 1
    finished.value = false
  }
  
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize,
      category: activeCategory.value || undefined,
      keyword: keyword.value || undefined
    }
    const res: any = await getPetList(params)
    const list = res.data?.list || []
    
    if (reset) {
      petList.value = list
    } else {
      petList.value.push(...list)
    }
    
    if (list.length < pageSize) {
      finished.value = true
    } else {
      page.value++
    }
  } catch (error) {
    console.error('加载宠物列表失败:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  if (!loading.value && !finished.value) {
    loadPetList()
  }
}

const onSearch = () => {
  loadPetList(true)
}

const goDetail = (id: number) => {
  router.push(`/pet/${id}`)
}

const addToCompare = (pet: Pet) => {
  if (petStore.comparePets.length >= 2) {
    showToast('对比栏已满，请先移除一个宠物')
    return
  }
  petStore.addToCompare(pet)
  showToast(`已添加${pet.name}到对比栏`)
}

// 监听分类变化
watch(activeCategory, () => {
  loadPetList(true)
})

onMounted(() => {
  loadPetList()
})
</script>

<style scoped>
.pet-list-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-bottom: 70px;
}

.search-bar {
  background: #fff;
}

.pet-list {
  padding: 12px;
}

.pet-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.pet-item {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.pet-image-wrapper {
  position: relative;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f9f9f9;
}

.pet-image {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
}

.pet-info {
  padding: 8px;
  text-align: center;
}

.pet-name {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: #333;
  margin-bottom: 2px;
}

.pet-category {
  font-size: 11px;
  color: #999;
}

.pet-actions {
  position: absolute;
  top: 4px;
  right: 4px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.compare-bar {
  position: fixed;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  padding: 8px 12px;
  border-radius: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 100;
}

.compare-pets {
  display: flex;
  gap: 8px;
}

.compare-pet {
  position: relative;
  width: 40px;
  height: 40px;
}

.compare-pet img {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  object-fit: cover;
}

.compare-pet .van-icon {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #fff;
  border-radius: 50%;
  color: #999;
}
</style>
