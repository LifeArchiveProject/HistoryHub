<template>
  <div class="privacy-control">
    <div class="privacy-status" :class="{ 'privacy-enabled': isPrivacyEnabled }">
      隐私模式: {{ isPrivacyEnabled ? '已开启' : '已关闭' }}
    </div>
    <button @click="togglePrivacy" class="privacy-toggle">
      {{ isPrivacyEnabled ? '关闭隐私模式' : '开启隐私模式' }}
    </button>
    <div class="privacy-info">
      {{ isPrivacyEnabled ? '隐私模式开启时将隐藏敏感信息' : '隐私模式关闭时将显示完整信息' }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import privacyManager from '../utils/privacyManager'

const isPrivacyEnabled = ref(false)
let checkInterval = null

// 切换隐私模式
const togglePrivacy = () => {
  const newState = privacyManager.toggle()
  isPrivacyEnabled.value = newState
}

// 隐私模式变化处理
const handlePrivacyChange = (enabled) => {
  isPrivacyEnabled.value = enabled
}

onMounted(() => {
  // 初始化状态
  isPrivacyEnabled.value = privacyManager.isEnabled()
  
  // 添加隐私模式变化监听
  privacyManager.addListener(handlePrivacyChange)
  
  // 定时检查，确保UI状态与实际存储状态一致
  checkInterval = setInterval(() => {
    const currentState = privacyManager.isEnabled()
    if (isPrivacyEnabled.value !== currentState) {
      isPrivacyEnabled.value = currentState
    }
  }, 1000)
})

onUnmounted(() => {
  if (checkInterval) {
    clearInterval(checkInterval)
  }
})
</script>

<style scoped>
.privacy-control {
  margin: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  text-align: center;
}

.privacy-status {
  font-weight: bold;
  margin-bottom: 10px;
}

.privacy-enabled {
  color: #e74c3c;
}

.privacy-toggle {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.privacy-toggle:hover {
  background-color: #2980b9;
}

.privacy-info {
  margin-top: 10px;
  font-size: 0.9em;
  color: #666;
}
</style> 