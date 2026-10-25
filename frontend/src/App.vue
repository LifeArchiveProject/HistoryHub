<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { ConfigProvider } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'
import 'vant/es/config-provider/style'
import privacyManager from './utils/privacyManager'
import { useDarkMode } from './store/darkMode'

const { isDarkMode, initDarkMode } = useDarkMode()



// 处理隐私模式变化
const handlePrivacyModeChange = (isEnabled) => {
  console.log('隐私模式状态变化:', isEnabled)

  if (isEnabled) {
    // 隐私模式启用，无像素化相关处理
  }
}


onMounted(() => {
  // 初始化深色模式
  initDarkMode()

  // 清理localStorage中的API密钥（API密钥验证已移除）
  if (localStorage.getItem('apiKey')) {
    localStorage.removeItem('apiKey')
    console.log('已清理localStorage中的API密钥')
  }



  // 添加隐私模式变化监听器
  privacyManager.addListener(handlePrivacyModeChange)

  // 首先检查隐私模式
  const privacyModeEnabled = privacyManager.isEnabled()

    // 同步隐私模式状态
    if (privacyModeEnabled) {
      handlePrivacyModeChange(true)
    }


})

</script>

<template>
  <!-- 使用ConfigProvider根据深色模式动态切换主题 -->
  <ConfigProvider :theme="isDarkMode ? 'dark' : 'light'">
    <div class="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300">
      <!-- 主应用内容 -->
      <router-view></router-view>
    </div>
  </ConfigProvider>
</template>

<style scoped>
/* 已移除服务器连接相关样式 */
</style>
