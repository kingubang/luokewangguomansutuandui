import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useFloatingStore = defineStore('floating', () => {
  // State
  const isVisible = ref(false)
  const currentView = ref<'home' | 'pet' | 'forum' | 'channel'>('home')
  
  // Actions
  const show = () => {
    isVisible.value = true
  }
  
  const hide = () => {
    isVisible.value = false
  }
  
  const toggle = () => {
    isVisible.value = !isVisible.value
  }
  
  const setView = (view: 'home' | 'pet' | 'forum' | 'channel') => {
    currentView.value = view
  }
  
  return {
    isVisible,
    currentView,
    show,
    hide,
    toggle,
    setView
  }
})
