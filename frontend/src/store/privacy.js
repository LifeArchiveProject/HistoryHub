import { ref } from 'vue'

// 从 localStorage 读取初始状态
const isPrivacyMode = ref(localStorage.getItem('privacyMode') === 'true')

export const usePrivacyStore = () => {
  const togglePrivacyMode = () => {
    isPrivacyMode.value = !isPrivacyMode.value
    // 保存到 localStorage
    localStorage.setItem('privacyMode', isPrivacyMode.value.toString())
  }
  
  const setPrivacyMode = (value) => {
    isPrivacyMode.value = value
    // 保存到 localStorage
    localStorage.setItem('privacyMode', value.toString())
  }

  return {
    isPrivacyMode,
    togglePrivacyMode,
    setPrivacyMode
  }
} 