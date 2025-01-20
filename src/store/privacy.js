import { ref } from 'vue'

const isPrivacyMode = ref(false)

export const usePrivacyStore = () => {
  const togglePrivacyMode = () => {
    isPrivacyMode.value = !isPrivacyMode.value
  }

  return {
    isPrivacyMode,
    togglePrivacyMode
  }
} 