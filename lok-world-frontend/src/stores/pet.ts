import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Pet } from '@/api/types'

export const usePetStore = defineStore('pet', () => {
  // State
  const selectedPets = ref<Pet[]>([])
  const comparePets = ref<Pet[]>([])
  
  // Getters
  const canCompare = computed(() => comparePets.value.length === 2)
  const selectedCount = computed(() => selectedPets.value.length)
  
  // Actions
  const selectPet = (pet: Pet) => {
    if (!selectedPets.value.find(p => p.id === pet.id)) {
      selectedPets.value.push(pet)
    }
  }
  
  const deselectPet = (petId: number) => {
    selectedPets.value = selectedPets.value.filter(p => p.id !== petId)
  }
  
  const addToCompare = (pet: Pet) => {
    if (comparePets.value.length < 2 && !comparePets.value.find(p => p.id === pet.id)) {
      comparePets.value.push(pet)
    }
  }
  
  const removeFromCompare = (petId: number) => {
    comparePets.value = comparePets.value.filter(p => p.id !== petId)
  }
  
  const clearCompare = () => {
    comparePets.value = []
  }
  
  const clearSelection = () => {
    selectedPets.value = []
  }
  
  return {
    selectedPets,
    comparePets,
    canCompare,
    selectedCount,
    selectPet,
    deselectPet,
    addToCompare,
    removeFromCompare,
    clearCompare,
    clearSelection
  }
})
