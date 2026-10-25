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
          <div v-if="danmakuFile" class="text-green-400 text-xs mt-1 flex items-center">
            <svg class="w-3.5 h-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>已加载弹幕</span>
          </div>
        </div>

        <!-- 视频播放器 -->
        <div class="w-full h-full aspect-video max-h-[80vh] relative">
          <!-- ArtPlayer播放器 -->
          <div v-show="activeVideo" class="w-full h-full">
            <ArtPlayerWithDanmaku
              v-if="activeVideo"
              ref="artPlayerRef"
              :videoSrc="videoSrc"
              :cid="currentCid"
              :danmakuFilePath="danmakuFile"
              :title="getFileName(videoPath)"
              :autoplay="true"
              :width="'100%'"
              :height="'100%'"
            />
          </div>
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
import { getVideoStream, getDanmakuFile } from '../../api/api'
import ArtPlayerWithDanmaku from './ArtPlayerWithDanmaku.vue'

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

// 播放器引用
const artPlayerRef = ref(null)
const isLoading = ref(false)
const activeVideo = ref(false)
const videoSrc = ref('')
const danmakuFile = ref('')
const currentCid = ref('')

// 错误状态
const error = ref(false)
const errorMessage = ref('')

// 获取文件名
const getFileName = (path) => {
  if (!path) return '未知文件'
  return path.split('\\').pop().split('/').pop() || '未知文件'
}

// 从视频路径中提取CID
const extractCid = (path) => {
  if (!path) return ''
  
  // 尝试从文件名中提取CID
  const fileName = getFileName(path)
  const cidMatch = fileName.match(/_(\d+)\.mp4$/) || fileName.match(/_(\d+)\.flv$/) || fileName.match(/_(\d+)\.m4a$/)
  
  if (cidMatch && cidMatch[1]) {
    return cidMatch[1]
  }
  
  // 如果文件名中没有CID，尝试从目录路径中提取
  const dirMatch = path.match(/(\d{8,})/)
  return dirMatch ? dirMatch[1] : ''
}

// 获取弹幕文件路径
const findDanmakuFile = (videoPath) => {
  if (!videoPath) return ''
  
  // 根据视频文件路径推断弹幕文件路径
  const fileNameWithoutExt = videoPath.replace(/\.(mp4|flv|m4a)$/i, '')
  return `${fileNameWithoutExt}.ass`
}

// 处理播放错误
const handlePlayError = (error) => {
  console.error('视频播放错误:', error)
  isLoading.value = false
  error.value = true
  errorMessage.value = `无法播放视频，错误信息: ${error?.message || '未知错误'}`
}

// 销毁播放器
const destroyPlayer = () => {
  if (artPlayerRef.value && artPlayerRef.value.player) {
    artPlayerRef.value.player.destroy()
  }
  
  // 重置变量
  videoSrc.value = ''
  danmakuFile.value = ''
  currentCid.value = ''
  activeVideo.value = false
}

// 关闭对话框
const handleClose = () => {
  // 销毁播放器
  destroyPlayer()
  
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
  
  // 确保之前的播放器已被销毁
  destroyPlayer()
  
  // 提取CID
  currentCid.value = extractCid(props.videoPath)
  
  // 查找弹幕文件
  danmakuFile.value = findDanmakuFile(props.videoPath)
  
  // 使用api生成视频流URL
  videoSrc.value = getVideoStream(props.videoPath)
  
  // 激活视频元素
  nextTick(() => {
    activeVideo.value = true
  })
}

// 监听show变化
watch(() => props.show, (newVal) => {
  if (newVal) {
    // 对话框打开时加载视频
    loadVideo()
  } else {
    // 对话框关闭时销毁播放器
    destroyPlayer()
  }
})

// 监听videoPath变化
watch(() => props.videoPath, (newVal) => {
  if (props.show && newVal) {
    // 如果对话框已打开并且视频路径变化，重新加载视频
    loadVideo()
  }
})

// 组件挂载时初始化
onMounted(() => {
  if (props.show && props.videoPath) {
    loadVideo()
  }
})

// 组件卸载时清理资源
onUnmounted(() => {
  destroyPlayer()
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