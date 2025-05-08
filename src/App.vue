<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'
import { globalPixelate } from './utils/globalPixelate'
import privacyManager from './utils/privacyManager'
import { showDialog } from 'vant'
import { useRouter } from 'vue-router'
import { checkApiKey, updateApiKey } from './api/api'
import ApiKeyDialog from './components/ApiKeyDialog.vue'

let privacyCheckInterval = null
const router = useRouter()
const DEFAULT_API_KEY = 'your-secret-api-key-change-this'

// API密钥校验状态
const isApiKeyChecking = ref(false)
const isApiKeyValid = ref(false)
const isShowingApiKeyDialog = ref(false)

// 自定义API密钥输入弹窗控制
const showApiKeyInputDialog = ref(false) // 用于默认密钥情况
const showApiKeyConfigDialog = ref(false) // 用于未配置密钥情况
const showApiKeyMismatchDialog = ref(false) // 用于密钥不匹配情况

// 处理API密钥输入确认 - 用于默认密钥情况
const handleApiKeyConfirm = async (userApiKey) => {
  // 更新后端API密钥
  const updated = await updateBackendApiKey(userApiKey)

  // 重置对话框状态
  isShowingApiKeyDialog.value = false

  if (updated) {
    isApiKeyValid.value = true
    showDialog({
      title: '成功',
      message: 'API密钥已成功更新。',
      confirmButtonText: '确定',
      confirmButtonColor: '#fb7299'
    })
  } else {
    // 如果更新失败，跳转到设置页面
    router.push('/settings?tab=security')
  }
}

// 处理API密钥配置 - 用于未配置密钥情况
const handleApiKeyConfig = async (userApiKey) => {
  // 保存API密钥到本地存储
  localStorage.setItem('apiKey', userApiKey)

  // 重置对话框状态
  isShowingApiKeyDialog.value = false

  // 重新检查API密钥状态
  setTimeout(() => {
    checkApiKeyStatus()
  }, 500)
}

// 处理API密钥不匹配 - 用于密钥不匹配情况
const handleApiKeyMismatch = async (userApiKey) => {
  // 保存API密钥到本地存储
  localStorage.setItem('apiKey', userApiKey)

  // 重置对话框状态
  isShowingApiKeyDialog.value = false

  // 重新检查API密钥状态
  setTimeout(() => {
    checkApiKeyStatus()
  }, 500)
}

// 确保像素化设置的初始值
const ensurePixelSettings = () => {
  // 如果用户之前没有设置过像素化质量值，设置默认值为20
  if (localStorage.getItem('pixelQuality') === null) {
    localStorage.setItem('pixelQuality', '20')
  }
}

// 更新API密钥
const updateBackendApiKey = async (newApiKey) => {
  try {
    const response = await updateApiKey(newApiKey)
    if (response.data && response.data.success) {
      localStorage.setItem('apiKey', newApiKey)
      return true
    }
    return false
  } catch (error) {
    console.error('更新API密钥失败:', error)
    return false
  }
}

// 显示API密钥验证失败对话框
const showApiKeyFailureDialog = () => {
  if (isShowingApiKeyDialog.value) return

  isShowingApiKeyDialog.value = true

  // 显示自定义API密钥不匹配弹窗
  showApiKeyMismatchDialog.value = true
}

// 检查API密钥
const checkApiKeyStatus = async () => {
  if (isApiKeyChecking.value) return
  isApiKeyChecking.value = true

  try {
    // 获取前端存储的API密钥
    const frontendApiKey = localStorage.getItem('apiKey')

    // 如果前端未配置API密钥，显示自定义对话框
    if (!frontendApiKey) {
      isApiKeyValid.value = false

      try {
        // 先检查后端API密钥是否为默认密钥
        const response = await checkApiKey()

        // 获取后端配置的API密钥状态
        const isBackendKeyDefault = response.data && response.data.message &&
                                   response.data.message.includes(DEFAULT_API_KEY)

        // 如果后端使用默认API密钥，优先显示安全警告弹窗
        if (isBackendKeyDefault) {
          // 显示自定义API密钥输入弹窗（安全警告）
          showApiKeyInputDialog.value = true
        } else {
          // 显示自定义API密钥配置弹窗
          showApiKeyConfigDialog.value = true
        }
      } catch (error) {
        console.error('检查后端API密钥状态失败:', error)
        // 出错时显示API密钥配置弹窗
        showApiKeyConfigDialog.value = true
      }

      isApiKeyChecking.value = false
      return
    }

    // 检查API密钥
    const response = await checkApiKey()

    // 如果API安全验证未启用，不需要进一步处理
    if (response.data && response.data.message === "API安全验证未启用") {
      isApiKeyValid.value = true
      isApiKeyChecking.value = false
      return
    }

    // 获取后端配置的API密钥状态
    const isBackendKeyDefault = response.data && response.data.message &&
                               response.data.message.includes(DEFAULT_API_KEY)

    // 如果后端使用默认API密钥，提示用户修改
    if (isBackendKeyDefault) {
      isApiKeyValid.value = false

      // 显示自定义API密钥输入弹窗
      showApiKeyInputDialog.value = true
    }
    // 如果前端API密钥与后端不一致
    else if (response.data && !response.data.is_valid) {
      isApiKeyValid.value = false
      showApiKeyFailureDialog()
    }
    // API密钥验证成功
    else {
      isApiKeyValid.value = true
      isShowingApiKeyDialog.value = false
    }
  } catch (error) {
    console.error('检查API密钥状态失败:', error)
    isApiKeyValid.value = false

    // 如果是401错误，说明API密钥无效
    if (error.response && error.response.status === 401) {
      showApiKeyFailureDialog()
    }
  } finally {
    isApiKeyChecking.value = false
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

  // 立即检查API密钥状态
  setTimeout(() => {
    checkApiKeyStatus()
  }, 1000) // 延迟1秒检查，确保路由已经初始化

  // 设置定期检查API密钥状态
  const apiKeyCheckInterval = setInterval(() => {
    // 只有当API密钥无效时才重新检查
    if (!isApiKeyValid.value) {
      checkApiKeyStatus()
    }
  }, 5000) // 每5秒检查一次，直到API密钥有效

  // 组件卸载时清除定时器
  onUnmounted(() => {
    clearInterval(apiKeyCheckInterval)
  })

  // 监听API密钥状态变化
  watch(isApiKeyValid, (newVal) => {
    console.log('API密钥状态变化:', newVal)

    // 如果API密钥无效，且当前没有显示对话框，则显示对话框
    if (!newVal && !isShowingApiKeyDialog.value) {
      // 延迟一点时间，避免多次显示对话框
      setTimeout(() => {
        checkApiKeyStatus()
      }, 1000)
    }
  })

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

    <!-- 自定义API密钥输入弹窗 - 用于默认密钥情况 -->
    <ApiKeyDialog
      v-model:show="showApiKeyInputDialog"
      title="安全警告"
      message="检测到服务器正在使用默认的API密钥，这可能会导致安全风险。请输入新的API密钥："
      :showCancelButton="false"
      confirmText="确认修改"
      inputPlaceholder="请输入新的API密钥"
      hintText="建议使用复杂的随机字符串。注意：为了安全，此密钥将不会在前端显示，请妥善保存。后续只能在配置文件中查看。"
      @confirm="handleApiKeyConfirm"
      @cancel="() => { showApiKeyInputDialog = false; isShowingApiKeyDialog.value = false; }"
    />

    <!-- 自定义API密钥配置弹窗 - 用于未配置密钥情况 -->
    <ApiKeyDialog
      v-model:show="showApiKeyConfigDialog"
      title="请输入API密钥"
      message="请输入服务器配置的API密钥以继续使用："
      :showCancelButton="false"
      confirmText="确认"
      inputPlaceholder="输入服务器配置的密钥"
      hintText="如果忘记密钥，请在配置文件 config/config.yaml 中查看。"
      @confirm="handleApiKeyConfig"
      @cancel="() => { showApiKeyConfigDialog = false; isShowingApiKeyDialog.value = false; }"
    />

    <!-- 自定义API密钥不匹配弹窗 - 用于密钥不匹配情况 -->
    <ApiKeyDialog
      v-model:show="showApiKeyMismatchDialog"
      title="API密钥验证失败"
      message="您的API密钥与服务器不匹配。请输入正确的API密钥以继续使用："
      :showCancelButton="false"
      confirmText="确认"
      inputPlaceholder="请输入正确的API密钥"
      hintText="如果忘记密钥，请在配置文件 config/config.yaml 中查看。"
      @confirm="handleApiKeyMismatch"
      @cancel="() => { showApiKeyMismatchDialog = false; isShowingApiKeyDialog.value = false; }"
    />
  </div>
</template>

<style scoped>
/* 已移除服务器连接相关样式 */
</style>
