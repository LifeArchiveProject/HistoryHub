<!-- 图片管理页面 -->
<template>
  <div class="container mx-auto max-w-full">
    <!-- 操作按钮 -->
    <div class="mb-6 flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
      <div class="flex space-x-4">
        <button
          @click="handleDownloadClick"
          :disabled="isLoading || isStoppingDownload"
          class="px-4 py-2 bg-[#fb7299] text-white rounded-md hover:bg-[#fb7299]/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 border border-[#fb7299]/20"
        >
          <div class="flex items-center space-x-2">
            <svg v-if="isDownloading" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>{{ isDownloading ? (isStoppingDownload ? '正在停止...' : '停止下载') : '下载图片' }}</span>
          </div>
        </button>

        <button
          @click="handleClear"
          :disabled="isDownloading || isLoading || isStoppingDownload"
          class="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 border border-red-400/20"
        >
          <div class="flex items-center space-x-2">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            <span>清空图片</span>
          </div>
        </button>
      </div>

      <!-- 下载选项 -->
      <div class="flex items-center space-x-2 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-md px-4 py-2 border border-gray-200 dark:border-gray-700">
        <input
          type="checkbox"
          id="useSessdata"
          v-model="useSessdata"
          class="w-4 h-4 text-[#fb7299] bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 rounded focus:ring-[#fb7299]"
        >
        <label for="useSessdata" class="text-sm text-gray-700 dark:text-gray-300">
          使用SESSDATA下载图片（对于公开内容如视频封面和头像，可以不使用SESSDATA）
        </label>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="space-y-8">
      <div v-for="i in 2" :key="i" class="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-200 dark:border-gray-700 animate-pulse">
        <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-32 mb-4"></div>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
          <div v-for="j in 4" :key="j" class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-16 mb-2"></div>
            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-20"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 下载状态 -->
    <div v-else class="space-y-8">
      <!-- 封面图片状态 -->
      <div class="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-[#fb7299]">封面图片</h2>
          <span class="text-sm text-gray-500 dark:text-gray-400">最后更新: {{ formatTime(status?.last_update) }}</span>
        </div>

        <!-- 进度条 -->
        <div v-if="isDownloading" class="mb-6">
          <div class="flex justify-between mb-1">
            <span class="text-sm text-gray-600 dark:text-gray-400">下载进度</span>
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ getProgressPercentage(status?.covers, 'covers') }}%</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div class="bg-[#fb7299] h-2.5 rounded-full transition-all duration-500 animate-pulse"
                 :style="{ width: getProgressPercentage(status?.covers, 'covers') + '%' }"></div>
          </div>
        </div>

        <!-- 状态卡片网格 -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="text-2xl font-bold text-[#fb7299]">{{ status?.covers?.total || 0 }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">计划下载</div>
          </div>
          <div class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="text-2xl font-bold text-[#fb7299]">{{ status?.covers?.downloaded || 0 }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">已下载</div>
          </div>
          <div class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="text-2xl font-bold text-red-500">{{ status?.covers?.failed || 0 }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">失败数</div>
          </div>
          <div class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="text-2xl font-bold text-blue-500">{{ status?.covers?.total_planned || 0 }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">待下载</div>
          </div>
        </div>

        <!-- 失败列表 -->
        <div v-if="status?.covers?.failed_urls?.length" class="mt-4">
          <div class="flex items-center space-x-2 mb-2">
            <svg class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="text-lg font-medium text-red-500">失败列表</h3>
          </div>
          <div class="max-h-40 overflow-y-auto space-y-2">
            <div v-for="(item, index) in status.covers.failed_urls" :key="index"
                 class="text-sm text-gray-600 dark:text-gray-300 p-2 bg-red-50 dark:bg-red-900/20 rounded border border-red-100 dark:border-red-900/30">
              <div class="flex justify-between">
                <span class="font-medium">错误: {{ item.error }}</span>
                <span class="text-gray-500 dark:text-gray-400">{{ formatTime(item.timestamp) }}</span>
              </div>
              <div class="mt-1 text-gray-500 dark:text-gray-400 break-all">URL: {{ item.url }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 头像图片状态 -->
      <div class="bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-[#fb7299]">头像图片</h2>
        </div>

        <!-- 进度条 -->
        <div v-if="isDownloading" class="mb-6">
          <div class="flex justify-between mb-1">
            <span class="text-sm text-gray-600 dark:text-gray-400">下载进度</span>
            <span class="text-sm text-gray-600 dark:text-gray-400">{{ getProgressPercentage(status?.avatars, 'avatars') }}%</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div class="bg-[#fb7299] h-2.5 rounded-full transition-all duration-500 animate-pulse"
                 :style="{ width: getProgressPercentage(status?.avatars, 'avatars') + '%' }"></div>
          </div>
        </div>

        <!-- 状态卡片网格 -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="text-2xl font-bold text-[#fb7299]">{{ status?.avatars?.total || 0 }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">计划下载</div>
          </div>
          <div class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="text-2xl font-bold text-[#fb7299]">{{ status?.avatars?.downloaded || 0 }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">已下载</div>
          </div>
          <div class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="text-2xl font-bold text-red-500">{{ status?.avatars?.failed || 0 }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">失败数</div>
          </div>
          <div class="bg-white/50 dark:bg-gray-800/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700">
            <div class="text-2xl font-bold text-blue-500">{{ status?.avatars?.total_planned || 0 }}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400">待下载</div>
          </div>
        </div>

        <!-- 失败列表 -->
        <div v-if="status?.avatars?.failed_urls?.length" class="mt-4">
          <div class="flex items-center space-x-2 mb-2">
            <svg class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="text-lg font-medium text-red-500">失败列表</h3>
          </div>
          <div class="max-h-40 overflow-y-auto space-y-2">
            <div v-for="(item, index) in status.avatars.failed_urls" :key="index"
                 class="text-sm text-gray-600 p-2 bg-red-50 rounded border border-red-100">
              <div class="flex justify-between">
                <span class="font-medium">错误: {{ item.error }}</span>
                <span class="text-gray-500">{{ formatTime(item.timestamp) }}</span>
              </div>
              <div class="mt-1 text-gray-500 break-all">URL: {{ item.url }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getImagesStatus, startImagesDownload, stopImagesDownload, clearImages } from '../../../api/api'
import { showNotify, showDialog } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'

const status = ref(null)
const isDownloading = ref(false)
const isLoading = ref(true)
const isStoppingDownload = ref(false)  // 新增：是否正在停止下载
const useSessdata = ref(true)  // 新增：是否使用SESSDATA
let statusInterval = null

// 格式化时间戳
const formatTime = (timestamp) => {
  if (!timestamp) return '无'
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 计算进度百分比
const getProgressPercentage = (data, type) => {
  if (!data) return 0
  return Math.round((data.downloaded / (data.total || 1)) * 100)
}

// 获取状态
const fetchStatus = async () => {
  try {
    const response = await getImagesStatus()
    if (response.data.status === 'success') {
      status.value = response.data.data
      isDownloading.value = status.value.is_downloading
      isLoading.value = false  // 数据加载完成，关闭加载状态

      // 如果下载完成，停止轮询
      if (!status.value.is_downloading && statusInterval) {
        clearInterval(statusInterval)
        statusInterval = null
        showNotify({
          type: 'success',
          message: '下载已完成'
        })
        // 1秒后刷新页面
        setTimeout(() => {
          window.location.reload()
        }, 1000)
      }
    }
  } catch (error) {
    console.error('获取状态失败:', error)
    isLoading.value = false  // 发生错误时也关闭加载状态
    if (statusInterval) {
      clearInterval(statusInterval)
      statusInterval = null
    }
  }
}

// 处理下载按钮点击
const handleDownloadClick = async () => {
  if (isDownloading.value) {
    // 如果已经在停止过程中，直接返回
    if (isStoppingDownload.value) return

    // 显示确认对话框
    try {
      await showDialog({
        title: '确认停止',
        message: '确定要停止当前下载任务吗？',
        showCancelButton: true,
        confirmButtonText: '确认停止',
        cancelButtonText: '取消',
        confirmButtonColor: '#ef4444'
      })

      // 设置停止状态，防止重复点击
      isStoppingDownload.value = true

      // 停止下载
      const response = await stopImagesDownload()
      if (response.data.status === 'success') {
        showNotify({
          type: 'success',
          message: '已停止下载'
        })
        // 重置状态
        isDownloading.value = false
        isStoppingDownload.value = false

        // 清除定时器
        if (statusInterval) {
          clearInterval(statusInterval)
          statusInterval = null
        }

        // 刷新状态
        await fetchStatus()
      }
    } catch (error) {
      // 如果是用户取消，直接返回
      if (error.toString().includes('cancel')) return

      showNotify({
        type: 'danger',
        message: `停止下载失败: ${error.message}`
      })
    } finally {
      // 如果停止失败，也需要重置停止状态
      isStoppingDownload.value = false
    }
  } else {
    // 如果未在下载，则开始下载
    try {
      const response = await startImagesDownload(null, useSessdata.value)
      if (response.data.status === 'success') {
        showNotify({
          type: 'success',
          message: response.data.message
        })
        isDownloading.value = true

        // 立即获取一次状态
        await fetchStatus()

        // 开始定时获取状态
        if (!statusInterval) {
          statusInterval = setInterval(fetchStatus, 1000)
        }
      }
    } catch (error) {
      showNotify({
        type: 'danger',
        message: `开始下载失败: ${error.message}`
      })
    }
  }
}

// 处理清空图片
const handleClear = async () => {
  try {
    await showDialog({
      title: '确认清空',
      message: '确定要清空所有图片和下载状态吗？此操作不可恢复。',
      showCancelButton: true,
      confirmButtonText: '确认清空',
      cancelButtonText: '取消',
      confirmButtonColor: '#ef4444'
    })

    const response = await clearImages()
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message
      })
      // 立即刷新状态
      await fetchStatus()
    } else {
      throw new Error(response.data.message || '清空失败')
    }
  } catch (error) {
    if (error.toString().includes('cancel')) return

    showNotify({
      type: 'danger',
      message: error.response?.status === 500 ?
        '服务器错误,请稍后重试' :
        `清空失败: ${error.message}`
    })
  }
}

// 组件挂载时获取一次状态
onMounted(() => {
  fetchStatus()
})

// 组件卸载时清除定时器
onUnmounted(() => {
  if (statusInterval) {
    clearInterval(statusInterval)
  }
})
</script>

<style scoped>
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .7;
  }
}
</style>
