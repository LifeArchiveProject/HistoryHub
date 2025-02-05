<!-- 图片管理页面 -->
<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <h1 class="text-2xl font-bold mb-8 bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">图片管理</h1>

    <!-- 操作按钮 -->
    <div class="mb-8 flex space-x-4">
      <div class="relative">
        <button
          @click="showDownloadMenu = !showDownloadMenu"
          :disabled="isDownloading"
          class="px-4 py-2 bg-[#fb7299] text-white rounded-lg hover:bg-[#fb7299]/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
        >
          <div class="flex items-center space-x-2">
            <svg v-if="isDownloading" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>{{ isDownloading ? '下载中...' : '下载图片' }}</span>
            <svg class="h-5 w-5 transition-transform duration-200" :class="{ 'rotate-180': showDownloadMenu }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </button>
        <!-- 下拉菜单 -->
        <div v-if="showDownloadMenu && !isDownloading" 
             class="absolute z-10 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100">
          <div class="py-1">
            <button
              @click="handleDownload()"
              class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-[#fb7299]/10 hover:text-[#fb7299]"
            >
              下载全部图片
            </button>
            <button
              @click="handleDownload(new Date().getFullYear())"
              class="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-[#fb7299]/10 hover:text-[#fb7299]"
            >
              下载本年图片
            </button>
          </div>
        </div>
      </div>

      <button
        @click="handleClear"
        :disabled="isDownloading"
        class="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
      >
        <div class="flex items-center space-x-2">
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          <span>清空图片</span>
        </div>
      </button>
    </div>

    <!-- 下载状态 -->
    <div class="space-y-8">
      <!-- 封面图片状态 -->
      <div class="bg-white/50 backdrop-blur-sm rounded-lg p-6 border border-gray-200/50">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-[#fb7299]">封面图片</h2>
          <span class="text-sm text-gray-500">最后更新: {{ formatTime(status?.last_update) }}</span>
        </div>

        <!-- 进度条 -->
        <div v-if="isDownloading" class="mb-6">
          <div class="flex justify-between mb-1">
            <span class="text-sm text-gray-600">下载进度</span>
            <span class="text-sm text-gray-600">{{ getProgressPercentage(status?.covers) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div class="bg-[#fb7299] h-2.5 rounded-full transition-all duration-500 animate-pulse"
                 :style="{ width: getProgressPercentage(status?.covers) + '%' }"></div>
          </div>
        </div>

        <!-- 状态卡片网格 -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
          <div class="bg-white/50 rounded-lg p-4 border border-gray-200/50">
            <div class="text-2xl font-bold text-[#fb7299]">{{ status?.covers?.total || 0 }}</div>
            <div class="text-sm text-gray-500">总数</div>
          </div>
          <div class="bg-white/50 rounded-lg p-4 border border-gray-200/50">
            <div class="text-2xl font-bold text-green-500">{{ status?.covers?.downloaded || 0 }}</div>
            <div class="text-sm text-gray-500">已下载</div>
          </div>
          <div class="bg-white/50 rounded-lg p-4 border border-gray-200/50">
            <div class="text-2xl font-bold text-red-500">{{ status?.covers?.failed || 0 }}</div>
            <div class="text-sm text-gray-500">失败数</div>
          </div>
          <div class="bg-white/50 rounded-lg p-4 border border-gray-200/50">
            <div class="text-2xl font-bold text-blue-500">{{ status?.covers?.pending || 0 }}</div>
            <div class="text-sm text-gray-500">待下载</div>
          </div>
        </div>

        <!-- 额外信息 -->
        <div class="text-sm text-gray-600 space-y-1">
          <div class="flex justify-between">
            <span>实际文件数：{{ status?.covers?.existing_files || 0 }}</span>
            <span>孤立文件数：{{ status?.covers?.orphaned_files || 0 }}</span>
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

      <!-- 头像图片状态 -->
      <div class="bg-white/50 backdrop-blur-sm rounded-lg p-6 border border-gray-200/50">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold text-[#fb7299]">头像图片</h2>
        </div>

        <!-- 进度条 -->
        <div v-if="isDownloading" class="mb-6">
          <div class="flex justify-between mb-1">
            <span class="text-sm text-gray-600">下载进度</span>
            <span class="text-sm text-gray-600">{{ getProgressPercentage(status?.avatars) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2.5">
            <div class="bg-[#fb7299] h-2.5 rounded-full transition-all duration-500 animate-pulse"
                 :style="{ width: getProgressPercentage(status?.avatars) + '%' }"></div>
          </div>
        </div>

        <!-- 状态卡片网格 -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-4">
          <div class="bg-white/50 rounded-lg p-4 border border-gray-200/50">
            <div class="text-2xl font-bold text-[#fb7299]">{{ status?.avatars?.total || 0 }}</div>
            <div class="text-sm text-gray-500">总数</div>
          </div>
          <div class="bg-white/50 rounded-lg p-4 border border-gray-200/50">
            <div class="text-2xl font-bold text-green-500">{{ status?.avatars?.downloaded || 0 }}</div>
            <div class="text-sm text-gray-500">已下载</div>
          </div>
          <div class="bg-white/50 rounded-lg p-4 border border-gray-200/50">
            <div class="text-2xl font-bold text-red-500">{{ status?.avatars?.failed || 0 }}</div>
            <div class="text-sm text-gray-500">失败数</div>
          </div>
          <div class="bg-white/50 rounded-lg p-4 border border-gray-200/50">
            <div class="text-2xl font-bold text-blue-500">{{ status?.avatars?.pending || 0 }}</div>
            <div class="text-sm text-gray-500">待下载</div>
          </div>
        </div>

        <!-- 额外信息 -->
        <div class="text-sm text-gray-600 space-y-1">
          <div class="flex justify-between">
            <span>实际文件数：{{ status?.avatars?.existing_files || 0 }}</span>
            <span>孤立文件数：{{ status?.avatars?.orphaned_files || 0 }}</span>
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
import { ref, onMounted, onUnmounted, onBeforeUnmount } from 'vue'
import { getImagesStatus, startImagesDownload, clearImages } from '../../../api/api'
import { showNotify } from 'vant'
import { showDialog } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'

const status = ref(null)
const isDownloading = ref(false)
const showDownloadMenu = ref(false)
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
const getProgressPercentage = (data) => {
  if (!data || !data.total_to_download) return 0
  return Math.round((data.downloaded / data.total_to_download) * 100)
}

// 获取状态
const fetchStatus = async () => {
  try {
    const response = await getImagesStatus()
    if (response.data.status === 'success') {
      status.value = response.data.data
      isDownloading.value = status.value.is_downloading

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
    if (statusInterval) {
      clearInterval(statusInterval)
      statusInterval = null
    }
  }
}

// 点击外部关闭下拉菜单
const handleClickOutside = (event) => {
  const menu = document.querySelector('.relative')
  if (menu && !menu.contains(event.target)) {
    showDownloadMenu.value = false
  }
}

// 处理下载
const handleDownload = async (year = null) => {
  showDownloadMenu.value = false
  await startDownload(year)
}

// 开始下载
const startDownload = async (year = null) => {
  try {
    const response = await startImagesDownload(year)
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

// 组件挂载时获取一次状态和添加点击事件监听
onMounted(() => {
  fetchStatus()
  document.addEventListener('click', handleClickOutside)
})

// 组件卸载时移除事件监听和清除定时器
onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

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