<template>
  <div id="app">
    <router-view v-slot="{ Component }">
      <keep-alive>
        <component :is="Component" />
      </keep-alive>
    </router-view>
    
    <!-- 悬浮窗入口 -->
    <FloatingBubble />
  </div>
</template>

<script setup lang="ts">
import FloatingBubble from '@/components/FloatingBubble.vue'
</script>

<style>
#app {
  width: 100%;
  height: 100%;
  background-color: var(--van-background);
}
</style>
