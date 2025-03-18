<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-[9999] flex items-center justify-center">
      <!-- 遮罩层 -->
      <div class="fixed inset-0 bg-black/80 backdrop-blur-sm" @click="handleClose"></div>

      <!-- 视频播放器 -->
      <div class="relative bg-black rounded-lg shadow-xl w-[90%] max-w-4xl max-h-[90vh] z-10 overflow-hidden">
        <!-- 关闭按钮 -->
        <button
          @click="handleClose"
          class="absolute right-4 top-4 text-white/70 hover:text-white z-20 bg-black/40 p-2 rounded-full"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- 视频标题 -->
        <div class="absolute top-0 left-0 right-0 p-4 bg-gradient-to-b from-black/80 to-transparent z-10">
          <h3 class="text-white text-lg font-medium truncate">
            {{ getFileName(videoPath) }}
          </h3>
        </div>

        <!-- 视频播放器 -->
        <div class="w-full h-full aspect-video max-h-[80vh] relative">
          <!-- 加载指示器 -->
          <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center bg-black/60 z-10">
            <div class="text-center">
              <svg class="w-12 h-12 text-[#fb7299] mx-auto animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <p class="text-white mt-3">视频加载中...</p>
            </div>
          </div>
          
          <video 
            v-if="activeVideo"
            ref="videoElement" 
            controls 
            class="w-full h-full"
            :src="videoSrc"
            preload="auto"
            @error="handleVideoError"
            @loadstart="isLoading = true"
            @loadeddata="isLoading = false"
            @canplay="isLoading = false"
          >
            您的浏览器不支持 HTML5 视频播放
          </video>
        </div>

        <!-- 错误提示 -->
        <div v-if="error" class="absolute inset-0 flex items-center justify-center bg-black/90">
          <div class="text-center p-6">
            <svg class="w-16 h-16 text-red-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h3 class="text-xl font-medium text-white mb-2">视频播放失败</h3>
            <p class="text-white/70 mb-4">{{ errorMessage }}</p>
            <button 
              @click="handleClose"
              class="px-4 py-2 bg-[#fb7299] text-white rounded-md hover:bg-[#fb7299]/90 transition-colors"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { getCurrentBaseUrl } from '../../api/api'

defineOptions({
  name: 'VideoPlayerDialog'
})

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  videoPath: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:show'])

// 视频元素引用
const videoElement = ref(null)
const isLoading = ref(false)
const activeVideo = ref(false)
const videoSrc = ref('')

// 错误状态
const error = ref(false)
const errorMessage = ref('')

// 生成视频流URL
const getVideoUrl = (path) => {
  if (!path) return ''
  const baseUrl = getCurrentBaseUrl()
  return `${baseUrl}/download/stream_video?file_path=${encodeURIComponent(path)}&t=${Date.now()}`
}

// 获取文件名
const getFileName = (path) => {
  if (!path) return '未知文件'
  return path.split('\\').pop().split('/').pop() || '未知文件'
}

// 处理视频错误
const handleVideoError = (e) => {
  console.error('视频播放错误:', e)
  isLoading.value = false
  error.value = true
  errorMessage.value = `无法播放视频，错误信息: ${e.target.error ? e.target.error.message : '未知错误'}`
}

// 完全销毁视频元素
const destroyVideo = () => {
  if (videoElement.value) {
    // 暂停播放
    videoElement.value.pause()
    
    // 移除所有事件监听器
    videoElement.value.onloadeddata = null
    videoElement.value.onloadstart = null
    videoElement.value.oncanplay = null
    videoElement.value.onerror = null
    
    // 清空src（添加空白src并加载以释放资源）
    videoElement.value.removeAttribute('src')
    videoElement.value.load()
  }
  
  // 重置变量
  videoSrc.value = ''
  activeVideo.value = false
}

// 关闭对话框
const handleClose = () => {
  // 销毁视频元素
  destroyVideo()
  
  // 重置错误状态
  error.value = false
  errorMessage.value = ''
  isLoading.value = false
  
  // 通知父组件关闭对话框
  emit('update:show', false)
}

// 加载视频
const loadVideo = () => {
  if (!props.videoPath) return
  
  // 确保之前的视频已被销毁
  destroyVideo()
  
  // 设置加载状态
  isLoading.value = true
  
  // 生成带有时间戳的URL避免缓存问题
  videoSrc.value = getVideoUrl(props.videoPath)
  
  // 激活视频元素
  nextTick(() => {
    activeVideo.value = true
    
    // 确保视频开始播放
    setTimeout(() => {
      if (videoElement.value) {
        videoElement.value.play().catch(err => {
          console.warn('无法自动播放视频:', err)
        })
      }
    }, 100)
  })
}

// 监听show变化
watch(() => props.show, (newVal) => {
  if (newVal) {
    // 对话框打开时加载视频
    loadVideo()
  } else {
    // 对话框关闭时销毁视频
    destroyVideo()
  }
})

// 监听videoPath变化
watch(() => props.videoPath, (newVal, oldVal) => {
  if (newVal && newVal !== oldVal && props.show) {
    // 当视频路径变化且对话框已打开时重新加载视频
    loadVideo()
  }
})

// 监听键盘事件
const handleKeyDown = (e) => {
  if (e.key === 'Escape' && props.show) {
    handleClose()
  }
}

// 挂载和卸载时的事件监听
onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
  destroyVideo() // 确保在组件卸载时清理资源
})
</script>

<style scoped>
/* 当对话框显示时禁用页面滚动 */
:deep(body) {
  overflow: hidden;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 