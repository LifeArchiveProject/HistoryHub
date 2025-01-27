<!-- 登录弹窗 -->
<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center">
    <!-- 遮罩层 -->
    <div class="absolute inset-0 bg-black/50" @click="handleClose"></div>
    
    <!-- 弹窗内容 -->
    <div class="relative bg-white rounded-lg shadow-xl w-[360px] max-h-[90vh] overflow-y-auto">
      <!-- 关闭按钮 -->
      <button 
        @click="handleClose"
        class="absolute right-4 top-4 text-gray-400 hover:text-gray-500"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- 标题 -->
      <div class="p-6 pb-0">
        <h3 class="text-lg font-medium text-gray-900">账号登录</h3>
        <p class="mt-2 text-sm text-gray-500">扫描二维码登录B站账号</p>
      </div>

      <!-- 登录内容 -->
      <div class="p-6 flex flex-col items-center space-y-4">
        <!-- 二维码区域 -->
        <div v-if="qrcodeKey" class="relative">
          <img :src="qrcodeImageUrl" alt="登录二维码" class="w-48 h-48 rounded-lg shadow-sm">
          <!-- 二维码失效遮罩 -->
          <div v-if="qrcodeExpired" class="absolute inset-0 bg-black/50 rounded-lg flex items-center justify-center">
            <button
              @click="refreshQRCode"
              class="px-4 py-2 bg-white text-gray-900 rounded-md text-sm hover:bg-gray-50"
            >
              点击刷新
            </button>
          </div>
        </div>
        
        <!-- 状态提示 -->
        <div class="text-sm" :class="statusClass">
          {{ loginStatusText }}
        </div>
        
        <!-- 刷新按钮 -->
        <button
          v-if="!qrcodeKey || qrcodeExpired"
          @click="refreshQRCode"
          class="px-4 py-2 text-sm text-[#fb7299] hover:bg-[#fb7299]/5 rounded-md transition-colors duration-200"
        >
          {{ qrcodeKey ? '重新获取二维码' : '获取登录二维码' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { showNotify } from 'vant'
import { 
  generateLoginQRCode,
  getQRCodeImageURL,
  pollQRCodeStatus
} from '../../api/api'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:show', 'login-success'])

// 登录相关状态
const qrcodeKey = ref('')
const qrcodeImageUrl = ref('')
const qrcodeExpired = ref(false)
const loginStatus = ref(86101) // 初始状态：未扫码
const pollingInterval = ref(null)
const pollingErrors = ref(0)

// 登录状态文本
const loginStatusText = computed(() => {
  switch (loginStatus.value) {
    case 0:
      return '登录成功'
    case 86038:
      return '二维码已失效'
    case 86090:
      return '已扫码，请在手机上确认'
    case 86101:
      return '请使用B站APP扫描二维码登录'
    default:
      return '获取二维码中...'
  }
})

// 状态样式
const statusClass = computed(() => {
  switch (loginStatus.value) {
    case 0:
      return 'text-green-500'
    case 86038:
      return 'text-red-500'
    case 86090:
      return 'text-[#fb7299]'
    default:
      return 'text-gray-500'
  }
})

// 开始轮询
const startPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
  
  let attempts = 0
  const maxAttempts = 90 // 180秒内尝试90次
  pollingErrors.value = 0 // 重置错误计数
  
  pollingInterval.value = setInterval(async () => {
    try {
      if (!qrcodeKey.value) {
        console.error('缺少qrcode_key参数')
        clearInterval(pollingInterval.value)
        showNotify({
          type: 'danger',
          message: '登录参数错误,请刷新页面重试'
        })
        return
      }

      const response = await pollQRCodeStatus(qrcodeKey.value)
      
      if (!response?.data) {
        throw new Error('服务器响应格式错误')
      }

      if (response.data.status === 'success' && response.data.data) {
        const code = response.data.data.code
        if (typeof code === 'undefined') {
          throw new Error('响应中缺少状态码')
        }

        loginStatus.value = code
        pollingErrors.value = 0
        
        if (loginStatus.value === 0) {
          // 登录成功
          clearInterval(pollingInterval.value)
          showNotify({
            type: 'success',
            message: '登录成功'
          })
          // 发送登录成功事件
          emit('login-success')
          // 关闭弹窗
          setTimeout(() => {
            handleClose()
          }, 1000)
        } else if (loginStatus.value === 86038) {
          // 二维码失效
          clearInterval(pollingInterval.value)
          qrcodeExpired.value = true
          showNotify({
            type: 'warning',
            message: '二维码已失效,请点击刷新'
          })
        } else if (loginStatus.value === 86090) {
          // 已扫码待确认
          showNotify({
            type: 'primary',
            message: '已扫码,请在手机上确认'
          })
        }
      } else {
        const errorMsg = response.data.detail || response.data.message || '获取状态失败'
        throw new Error(errorMsg)
      }
      
      attempts++
      if (attempts >= maxAttempts) {
        clearInterval(pollingInterval.value)
        qrcodeExpired.value = true
        loginStatus.value = 86038
        showNotify({
          type: 'warning',
          message: '登录超时,请重新获取二维码'
        })
      }
    } catch (error) {
      console.error('轮询出错:', error)
      pollingErrors.value++
      
      if (error.response?.status === 500) {
        clearInterval(pollingInterval.value)
        qrcodeExpired.value = true
        showNotify({
          type: 'danger',
          message: '服务器错误,请稍后重试'
        })
        return
      }
      
      if (pollingErrors.value >= 3) {
        clearInterval(pollingInterval.value)
        qrcodeExpired.value = true
        showNotify({
          type: 'danger',
          message: '网络异常,请检查网络后重试'
        })
      }
    }
  }, 2000)
}

// 获取二维码
const getQRCode = async () => {
  try {
    const response = await generateLoginQRCode()
    
    if (!response?.data) {
      throw new Error('服务器响应格式错误')
    }

    if (response.data.status === 'success' && response.data.data?.qrcode_key) {
      qrcodeKey.value = response.data.data.qrcode_key
      qrcodeImageUrl.value = getQRCodeImageURL()
      qrcodeExpired.value = false
      loginStatus.value = 86101
      pollingErrors.value = 0
      startPolling()
    } else {
      const errorMsg = response.data.detail || response.data.message || '获取二维码失败'
      throw new Error(errorMsg)
    }
  } catch (error) {
    console.error('获取二维码失败:', error)
    showNotify({
      type: 'danger',
      message: error.response?.status === 500 ? 
        '服务器错误,请稍后重试' : 
        `获取二维码失败: ${error.message}`
    })
    qrcodeExpired.value = true
  }
}

// 刷新二维码
const refreshQRCode = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
  getQRCode()
}

// 关闭弹窗
const handleClose = () => {
  emit('update:show', false)
  // 清理轮询
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
  // 重置状态
  qrcodeKey.value = ''
  qrcodeImageUrl.value = ''
  qrcodeExpired.value = false
  loginStatus.value = 86101
  pollingErrors.value = 0
}

// 监听show变化
watch(() => props.show, (newVal) => {
  if (newVal) {
    getQRCode()
  } else {
    handleClose()
  }
})

// 组件卸载时清理
onUnmounted(() => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
})
</script> 