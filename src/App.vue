<script setup>
import { onMounted, onUnmounted } from 'vue'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'
import { globalPixelate } from './utils/globalPixelate'
import privacyManager from './utils/privacyManager'

let privacyCheckInterval = null

// 确保像素化设置的初始值
const ensurePixelSettings = () => {
  // 如果用户之前没有设置过像素化质量值，设置默认值为20
  if (localStorage.getItem('pixelQuality') === null) {
    localStorage.setItem('pixelQuality', '20')
  }
}

// 处理隐私模式变化
const handlePrivacyModeChange = (isEnabled) => {
  console.log('隐私模式状态变化:', isEnabled)

  if (isEnabled) {
    // 隐私模式开启，强制关闭像素化
    localStorage.setItem('usePixelImage', 'false')

    // 如果全局像素化已启用，则禁用它
    if (globalPixelate.enabled) {
      globalPixelate.disable()

      // 移除像素化样式
      document.documentElement.classList.remove('use-pixel-images')
    }
  }
}

// 设置定时检查隐私模式
const setupPrivacyModeChecker = () => {
  // 每秒检查一次隐私模式状态
  privacyCheckInterval = setInterval(() => {
    // 如果隐私模式开启，检查并确保像素化已关闭
    if (privacyManager.isEnabled() &&
        (globalPixelate.enabled || localStorage.getItem('usePixelImage') === 'true')) {
      handlePrivacyModeChange(true)
    }
  }, 1000)
}

onMounted(() => {
  // 确保像素化默认设置
  ensurePixelSettings()

  // 初始化像素字体设置
  const usePixelFont = localStorage.getItem('usePixelFont') === 'true'
  document.documentElement.classList.toggle('use-pixel-font', usePixelFont)

  // 预加载像素字体
  if (usePixelFont) {
    // 预加载Ark像素字体
    const preloadArkLatin = document.createElement('link')
    preloadArkLatin.href = '/fonts/ark-pixel-font-10px-monospaced-ttf-v2025.03.14/ark-pixel-10px-monospaced-latin.ttf'
    preloadArkLatin.rel = 'preload'
    preloadArkLatin.as = 'font'
    preloadArkLatin.type = 'font/ttf'
    preloadArkLatin.crossOrigin = 'anonymous'
    document.head.appendChild(preloadArkLatin)

    const preloadArkZH = document.createElement('link')
    preloadArkZH.href = '/fonts/ark-pixel-font-10px-monospaced-ttf-v2025.03.14/ark-pixel-10px-monospaced-zh_cn.ttf'
    preloadArkZH.rel = 'preload'
    preloadArkZH.as = 'font'
    preloadArkZH.type = 'font/ttf'
    preloadArkZH.crossOrigin = 'anonymous'
    document.head.appendChild(preloadArkZH)
  }

  // 监听像素字体设置变更事件
  window.addEventListener('pixel-font-changed', (event) => {
    if (event.detail && typeof event.detail.usePixelFont === 'boolean') {
      document.documentElement.classList.toggle('use-pixel-font', event.detail.usePixelFont)
    }
  })

  // 添加隐私模式变化监听器
  privacyManager.addListener(handlePrivacyModeChange)

  // 首先检查隐私模式
  const privacyModeEnabled = privacyManager.isEnabled()

  // 如果隐私模式已开启，强制关闭像素化
  if (privacyModeEnabled) {
    handlePrivacyModeChange(true)
  } else {
    // 初始化图片像素化设置（只在非隐私模式下）
    const usePixelImage = localStorage.getItem('usePixelImage') === 'true'
    const pixelQuality = parseInt(localStorage.getItem('pixelQuality') || '20') // 默认值从50改为20

    // 如果启用了像素化，初始化全局像素化处理器
    if (usePixelImage) {
      // 先添加像素渲染样式（在等待像素化处理时保持像素化效果）
      document.documentElement.classList.add('use-pixel-images')
      document.documentElement.setAttribute('data-pixel-quality', pixelQuality.toString())

      // 启用全局像素化管理器
      globalPixelate.enable({
        quality: pixelQuality
      })
    }
  }

  // 监听图片像素化设置变更事件
  window.addEventListener('pixel-image-changed', (event) => {
    if (event.detail) {
      const { usePixelImage, pixelQuality } = event.detail

      // 如果隐私模式开启，阻止开启像素化
      if (privacyManager.isEnabled() && usePixelImage) {
        console.log('隐私模式下尝试开启像素化，已阻止')
        return
      }

      // 添加或移除全局像素化样式
      document.documentElement.classList.toggle('use-pixel-images', usePixelImage)
      document.documentElement.setAttribute('data-pixel-quality', pixelQuality.toString())

      if (usePixelImage) {
        // 启用或更新全局像素化处理
        if (globalPixelate.enabled) {
          globalPixelate.updateQuality(pixelQuality)
        } else {
          globalPixelate.enable({
            quality: pixelQuality
          })
        }
      } else {
        // 禁用全局像素化处理
        globalPixelate.disable()
      }
    }
  })

  // 设置定时检查隐私模式
  setupPrivacyModeChecker()
})

onUnmounted(() => {
  // 清除定时器
  if (privacyCheckInterval) {
    clearInterval(privacyCheckInterval)
  }
})
</script>

<template>
  <div>
    <!-- 主应用内容 -->
    <router-view></router-view>
  </div>
</template>

<style scoped>
/* 已移除服务器连接相关样式 */
</style>
