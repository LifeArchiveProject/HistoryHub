import { ref, watch } from 'vue'

// 深色模式状态管理
const isDarkMode = ref(false)

// 从localStorage读取深色模式设置
const initDarkMode = () => {
  const savedMode = localStorage.getItem('darkMode')
  if (savedMode !== null) {
    isDarkMode.value = savedMode === 'true'
  } else {
    // 默认检测系统偏好
    isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  applyDarkMode()
}

// 应用深色模式
const applyDarkMode = () => {
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// 切换深色模式
const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('darkMode', isDarkMode.value.toString())
  applyDarkMode()
}

// 监听深色模式变化
watch(isDarkMode, () => {
  applyDarkMode()
})

export const useDarkMode = () => {
  return {
    isDarkMode,
    toggleDarkMode,
    initDarkMode
  }
}