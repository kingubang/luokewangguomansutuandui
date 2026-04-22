<template>
  <div v-if="!isInApp" class="floating-bubble" @click="openFloating">
    <van-icon name="apps-o" size="24" color="#fff" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useFloatingStore } from '@/stores/floating'

const floatingStore = useFloatingStore()

const isInApp = computed(() => {
  // 检测是否在APP内运行
  return !!(window as any).Capacitor
})

const openFloating = () => {
  floatingStore.show()
  // 调用原生悬浮窗
  if ((window as any).Capacitor?.Plugins?.FloatingWindow) {
    (window as any).Capacitor.Plugins.FloatingWindow.show()
  }
}
</script>

<style scoped>
.floating-bubble {
  position: fixed;
  right: 16px;
  bottom: 80px;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #FF6B35, #FF8C42);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
  z-index: 9999;
  cursor: pointer;
  transition: transform 0.2s;
}

.floating-bubble:active {
  transform: scale(0.95);
}
</style>
