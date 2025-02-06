<!-- 视频下载弹窗 -->
<template>
  <div v-if="show" class="fixed inset-0 z-[9999] flex items-center justify-center">
    <!-- 遮罩层 -->
    <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="handleClose"></div>

    <!-- 弹窗内容 -->
    <div class="relative bg-white rounded-lg shadow-xl w-[1000px] max-h-[90vh] z-10">
      <!-- 关闭按钮 -->
      <button
        @click="handleClose"
        class="absolute right-4 top-4 text-gray-400 hover:text-gray-500 z-20"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>

      <!-- Yutto 项目致谢 -->
      <div class="py-3 px-4 flex items-center justify-center space-x-4 bg-gray-50 border-b border-gray-100 rounded-t-lg">
        <img src="https://yutto.nyakku.moe/logo-mini.svg" alt="Yutto Logo" class="w-8 h-8">
        <div class="flex flex-col">
          <p class="text-sm text-gray-600">下载功能由 <a href="https://yutto.nyakku.moe/" target="_blank" class="text-[#fb7299] hover:text-[#fb7299]/80 font-medium">Yutto</a> 提供支持</p>
          <p class="text-xs text-gray-400">感谢 Yutto 开发团队的开源贡献</p>
        </div>
      </div>

      <!-- 标题 -->
      <div class="px-6 pt-4 pb-0">
        <h3 class="text-lg font-medium text-gray-900">下载视频</h3>
        <p v-if="downloadStarted" class="mt-1 text-sm text-gray-500">
          {{ isDownloading ? '正在下载：' : (downloadError ? '下载出错：' : '下载完成：') }} {{ videoInfo.title }}
        </p>
        <p v-else class="mt-1 text-sm text-gray-500">
          {{ videoInfo.title }}
        </p>
      </div>

      <!-- 视频信息 -->
      <div class="p-6 pt-4 flex flex-col items-center space-y-3">
        <!-- 封面图 -->
        <div class="relative w-full">
          <div class="flex space-x-6">
            <div class="w-44 h-28 flex-shrink-0">
              <img :src="videoInfo.cover" :alt="videoInfo.title" class="w-full h-full object-cover rounded-lg">
            </div>
            <div class="flex-1 min-w-0 space-y-2">
              <h4 class="text-base font-medium text-gray-900">{{ videoInfo.title }}</h4>
              <p class="text-sm text-gray-500">UP主：{{ videoInfo.author }}</p>
              <p class="text-sm text-gray-500">BV号：{{ videoInfo.bvid }}</p>
            </div>
          </div>
        </div>

        <!-- 下载日志 -->
        <div class="w-full h-[260px] bg-gray-50 rounded-lg p-4 font-mono text-sm overflow-y-auto" ref="logContainer">
          <div v-if="!downloadStarted" class="text-gray-500">
            点击下方按钮开始下载...
          </div>
          <div v-else>
            <div v-for="(log, index) in downloadLogs" :key="index" class="whitespace-pre break-all leading-6" :class="{
              'text-gray-600': !log.includes('ERROR'),
              'text-red-500': log.includes('ERROR'),
              'text-green-500': log.includes('下载完成'),
              'text-yellow-500': log.includes('WARN'),
            }">{{ log }}</div>
          </div>
        </div>

        <!-- 状态和按钮 -->
        <div class="w-full flex items-center justify-between">
          <div class="text-sm" :class="{
            'text-gray-500': !downloadStarted,
            'text-red-500': downloadError,
            'text-green-500': !isDownloading && downloadStarted && !downloadError,
            'text-[#fb7299]': isDownloading
          }">
            {{ downloadStatus }}
          </div>
          <div class="flex space-x-4">
            <button
              @click="handleClose"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
              :disabled="isDownloading"
            >
              {{ isDownloading ? '下载中...' : '关闭' }}
            </button>
            <button
              v-if="!downloadStarted || downloadError"
              @click="startDownload"
              class="px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-md hover:bg-[#fb7299]/90 disabled:opacity-50"
              :disabled="isDownloading"
            >
              {{ downloadError ? '重试' : '开始下载' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onUnmounted, nextTick } from 'vue'
import { downloadVideo } from '../../api/api'

defineOptions({
  name: 'DownloadDialog'
})

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  videoInfo: {
    type: Object,
    required: true,
    default: () => ({
      title: '',
      author: '',
      bvid: '',
      cover: ''
    })
  }
})

const emit = defineEmits(['update:show'])

// 下载相关状态
const downloadStarted = ref(false)
const isDownloading = ref(false)
const downloadError = ref(false)
const downloadLogs = ref([])

// 下载状态文本
const downloadStatus = computed(() => {
  if (!downloadStarted.value) return '准备就绪'
  if (downloadError.value) return '下载出错'
  if (isDownloading.value) return '下载中...'
  return '下载完成'
})

// 日志容器引用
const logContainer = ref(null)

// 开始下载
const startDownload = async () => {
  try {
    // 重置状态
    downloadStarted.value = true
    isDownloading.value = true
    downloadError.value = false
    downloadLogs.value = []

    // 发起下载请求并处理实时消息
    await downloadVideo(props.videoInfo.bvid, null, (content) => {
      downloadLogs.value.push(content)

      // 检查下载状态
      if (content.includes('下载完成')) {
        isDownloading.value = false
      } else if (content.includes('ERROR')) {
        downloadError.value = true
        isDownloading.value = false
      }

      // 自动滚动到底部
      nextTick(() => {
        scrollToBottom()
      })
    })
  } catch (error) {
    console.error('下载失败:', error)
    downloadError.value = true
    isDownloading.value = false
    downloadLogs.value.push(`ERROR: ${error.message}`)
  }
}

// 滚动到底部的优化实现
const scrollToBottom = () => {
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
}

// 监听日志变化
watch(() => downloadLogs.value.length, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

// 关闭弹窗
const handleClose = () => {
  if (isDownloading.value) {
    if (!confirm('下载正在进行中，确定要关闭吗？')) {
      return
    }
  }
  emit('update:show', false)
  // 重置状态
  downloadStarted.value = false
  isDownloading.value = false
  downloadError.value = false
  downloadLogs.value = []
}

// 监听show变化
watch(() => props.show, (newVal) => {
  if (!newVal) {
    handleClose()
  }
})

// 组件卸载时清理
onUnmounted(() => {
  // 重置状态
  downloadStarted.value = false
  isDownloading.value = false
  downloadError.value = false
  downloadLogs.value = []
})
</script>

<style scoped>
/* 当弹窗显示时禁用页面滚动 */
:global(body) {
  overflow: hidden;
}
</style>
