<!-- 视频详情管理组件 -->
<template>
  <div class="bg-white rounded-lg border border-gray-200 p-6">
    <!-- 操作按钮 -->
    <div class="mb-6 flex flex-col space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
      <div class="flex space-x-4">
        <button
          @click="startFetchingDetails"
          :disabled="stats.pendingVideosCount === 0 || isFetching"
          class="px-4 py-2 bg-[#fb7299] text-white rounded-md hover:bg-[#fb7299]/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 border border-[#fb7299]/20"
        >
          <div class="flex items-center space-x-2">
            <svg v-if="isFetching" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>{{ isFetching ? '获取中...' : (stats.pendingVideosCount === 0 ? '无需获取' : '获取视频详情') }}</span>
          </div>
        </button>

        <!-- 停止按钮 -->
        <button
          v-if="isFetching && progress.isProcessing && !progress.isComplete"
          @click="stopFetching"
          class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-all duration-200 border border-red-600/20"
        >
          <div class="flex items-center space-x-2">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 10h6v4H9z" />
            </svg>
            <span>停止获取</span>
          </div>
        </button>
      </div>

      <!-- 下载选项 -->
      <div class="flex items-center space-x-2 bg-white/50 backdrop-blur-sm rounded-md px-4 py-2 border border-gray-200">
        <input
          type="checkbox"
          id="useSessdata"
          v-model="useSessdata"
          class="w-4 h-4 text-[#fb7299] bg-gray-100 border-gray-300 rounded focus:ring-[#fb7299]"
          :disabled="stats.pendingVideosCount === 0 || isFetching"
        >
        <label for="useSessdata" class="text-sm text-gray-700">
          使用SESSDATA获取详情（对于公开视频可以不使用SESSDATA）
        </label>
      </div>
    </div>

    <!-- 加载中状态 -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-16 w-16 border-b-2 border-[#fb7299]"></div>
    </div>

    <!-- 统计数据卡片 -->
    <div v-if="!isLoading" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white rounded-lg border border-gray-200 p-4 flex flex-col">
        <span class="text-sm text-gray-500">历史记录视频总数</span>
        <span class="text-2xl font-bold text-gray-800">{{ stats.totalHistoryVideos }}</span>
      </div>

      <div class="bg-white rounded-lg border border-gray-200 p-4 flex flex-col">
        <span class="text-sm text-gray-500">已获取详情</span>
        <span class="text-2xl font-bold text-green-600">{{ stats.existingVideosCount }}</span>
      </div>

      <div class="bg-white rounded-lg border border-gray-200 p-4 flex flex-col">
        <span class="text-sm text-gray-500">已知失效视频</span>
        <span class="text-2xl font-bold text-orange-500">{{ stats.invalidVideosCount }}</span>
      </div>

      <div class="bg-white rounded-lg border border-gray-200 p-4 flex flex-col">
        <span class="text-sm text-gray-500">待获取视频</span>
        <span class="text-2xl font-bold" :class="stats.pendingVideosCount > 0 ? 'text-blue-600' : 'text-gray-400'">
          {{ stats.pendingVideosCount }}
        </span>
      </div>
    </div>

    <!-- 进度状态卡片 - 仅在获取时显示 -->
    <div v-if="isFetching && !isLoading" class="space-y-6">
      <!-- 总体进度 -->
      <div class="bg-white rounded-lg border border-gray-200 p-4">
        <div class="mb-4">
          <div class="flex justify-between items-center mb-1 text-sm">
            <span class="font-medium">处理进度: {{ progress.processedVideos || 0 }}/{{ progress.totalVideos || 0 }}</span>
            <span>{{ progress.progressPercentage ? `${progress.progressPercentage.toFixed(1)}%` : '0%' }}</span>
          </div>
          <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
            <div
              class="h-full bg-[#fb7299] transition-all duration-300"
              :style="{width: `${progress.progressPercentage || 0}%`}"
            ></div>
          </div>
        </div>
      </div>

      <!-- 状态卡片组 -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- 成功卡片 -->
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <div>
            <p class="text-sm font-medium text-gray-500">成功获取</p>
            <p class="text-2xl font-bold text-green-600">{{ progress.successCount || 0 }}</p>
          </div>
        </div>

        <!-- 失败卡片 -->
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <div>
            <p class="text-sm font-medium text-gray-500">获取失败</p>
            <p class="text-2xl font-bold text-red-600">{{ progress.failedCount || 0 }}</p>
          </div>
        </div>

        <!-- 跳过卡片 -->
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <div>
            <p class="text-sm font-medium text-gray-500">跳过失效</p>
            <p class="text-2xl font-bold text-yellow-600">{{ progress.skippedInvalidCount || 0 }}</p>
          </div>
        </div>

        <!-- 时间卡片 -->
        <div class="bg-white rounded-lg border border-gray-200 p-4">
          <div>
            <p class="text-sm font-medium text-gray-500">已用时间</p>
            <p class="text-2xl font-bold text-blue-600">{{ progress.elapsedTime || '0秒' }}</p>
          </div>
        </div>
      </div>

      <!-- 失败视频列表 -->
      <div v-if="progress.errorVideos && progress.errorVideos.length > 0" class="bg-white rounded-lg border border-gray-200 p-4">
        <div class="font-medium text-sm mb-2 text-red-600 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          获取失败的视频:
        </div>
        <div class="max-h-[120px] overflow-y-auto text-xs bg-gray-50 p-2 rounded border border-gray-200">
          <div v-for="(bvid, index) in progress.errorVideos" :key="index" class="mb-1">
            {{ bvid }}
          </div>
        </div>
      </div>

      <!-- 完成按钮 -->
      <div v-if="progress.isComplete" class="flex justify-end">
        <button
          @click="completeFetching"
          class="inline-flex items-center px-4 py-2 rounded-md text-white bg-green-600 hover:bg-green-700 font-medium"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          完成
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getVideoDetailsStats, fetchVideoDetails, createVideoDetailsProgressSSE, stopVideoDetailsFetch } from '../../../api/api'
import { showNotify } from 'vant'
import 'vant/es/notify/style'

// 状态变量
const isLoading = ref(true)
const isFetching = ref(false)
const useSessdata = ref(true) // 默认使用SESSDATA
const stats = ref({
  totalHistoryVideos: 0,
  existingVideosCount: 0,
  invalidVideosCount: 0,
  pendingVideosCount: 0,
  completionPercentage: 0,
  errorTypeStats: {},
  pendingVideos: []
})

// 进度相关
const progressSource = ref(null)
const progress = ref({
  isProcessing: false,
  totalVideos: 0,
  processedVideos: 0,
  successCount: 0,
  failedCount: 0,
  errorVideos: [],
  skippedInvalidCount: 0,
  progressPercentage: 0,
  elapsedTime: '',
  isComplete: false
})

// 获取统计数据
const fetchStats = async () => {
  isLoading.value = true
  try {
    // 调用API获取视频详情统计数据
    const response = await getVideoDetailsStats()
    if (response.data.status === 'success') {
      // 确保数据结构完整
      const data = response.data.data || {}
      stats.value = {
        totalHistoryVideos: data.total_videos || 0,
        existingVideosCount: data.videos_with_details || 0,
        invalidVideosCount: (data.invalid_videos_count ?? 0),
        pendingVideosCount: (data.pending_videos_count ?? data.videos_without_details ?? 0),
        completionPercentage: data.completion_percentage ?? 0,
        errorTypeStats: (data.invalid_error_type_stats || {}),
        pendingVideos: data.pending_videos || []
      }
    } else {
      throw new Error(response.data.message || '获取统计数据失败')
    }
  } catch (error) {
    console.error('获取视频详情统计失败:', error)
    showNotify({
      type: 'danger',
      message: error.message || '获取统计数据失败'
    })
  } finally {
    isLoading.value = false
  }
}

// 格式化错误类型名称
const formatErrorType = (type) => {
  const errorTypes = {
    'parse_error': '解析错误',
    'not_found': '视频不存在',
    'restricted': '访问受限',
    'api_error': 'API错误',
    'timeout': '超时',
    'network_error': '网络错误',
    '404_not_found': '视频不存在',
    '62002_invisible': '视频已设为私有'
  }
  return errorTypes[type] || type
}

// 开始获取视频详情
const startFetchingDetails = async () => {
  try {
    // 调用API启动获取流程，设置maxVideos=0表示获取全部
    const response = await fetchVideoDetails({
      max_videos: 0,  // 获取全部视频
      specific_videos: '',
      use_sessdata: useSessdata.value // 传递是否使用SESSDATA的选项
    })

    if (response.data.status === 'success') {
      isFetching.value = true

      // 初始化进度对象
      const data = response.data.data || {}
      progress.value = {
        isProcessing: data.is_processing || true,
        totalVideos: data.total_videos || 0,
        processedVideos: data.processed_videos || 0,
        successCount: data.success_count || 0,
        failedCount: data.failed_count || 0,
        errorVideos: data.error_videos || [],
        skippedInvalidCount: data.skipped_invalid_count || 0,
        progressPercentage: data.progress_percentage || 0,
        elapsedTime: typeof data.elapsed_time === 'number' ? `${data.elapsed_time.toFixed(2)}秒` : '0.00秒',
        isComplete: false
      }

      // 启动进度监听
      startProgressStream()

      showNotify({
        type: 'success',
        message: '已开始获取视频详情'
      })
    } else {
      throw new Error(response.data.message || '启动获取失败')
    }
  } catch (error) {
    console.error('启动视频详情获取失败:', error)
    showNotify({
      type: 'danger',
      message: error.message || '启动获取失败'
    })
  }
}

// 停止获取
const stopFetching = async () => {
  try {
    const response = await stopVideoDetailsFetch()
    if (response.data.status === 'success') {
      // 立即重置前端状态
      closeProgressStream()
      isFetching.value = false

      // 重置进度状态到初始状态
      progress.value = {
        isProcessing: false,
        totalVideos: 0,
        processedVideos: 0,
        successCount: 0,
        failedCount: 0,
        errorVideos: [],
        skippedInvalidCount: 0,
        progressPercentage: 0,
        elapsedTime: '',
        isComplete: false
      }

      showNotify({
        type: 'success',
        message: '任务已停止'
      })

      // 刷新统计数据
      fetchStats()
    } else {
      throw new Error(response.data.message || '停止失败')
    }
  } catch (error) {
    console.error('停止视频详情获取失败:', error)
    showNotify({
      type: 'danger',
      message: error.message || '停止失败'
    })
  }
}

// 完成获取
const completeFetching = () => {
  closeProgressStream()
  isFetching.value = false

  showNotify({
    type: 'success',
    message: `视频详情获取完成! 成功: ${progress.value.successCount}, 失败: ${progress.value.failedCount}`
  })

  // 刷新统计数据
  fetchStats()
}

// 开始流式获取进度
const startProgressStream = () => {
  // 关闭可能存在的连接
  closeProgressStream()

  try {
    console.log('开始获取视频详情进度流')
    // 使用接口文档中的更新间隔参数
    progressSource.value = createVideoDetailsProgressSSE({ update_interval: 0.2 })

    // 连接建立
    progressSource.value.onopen = (event) => {
      console.log('视频详情进度流连接已建立')
    }

    // 接收消息
    progressSource.value.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('收到进度更新:', data)

        // 更新进度，映射API文档中的字段
        progress.value = {
          isProcessing: data.is_processing,
          totalVideos: data.total_videos,
          processedVideos: data.processed_videos,
          successCount: data.success_count,
          failedCount: data.failed_count,
          errorVideos: data.error_videos || [],
          skippedInvalidCount: data.skipped_invalid_count || 0,
          progressPercentage: data.progress_percentage,
          elapsedTime: data.elapsed_time,
          isComplete: data.is_complete
        }

        // 处理完成
        if (data.is_complete) {
          console.log('视频详情获取完成')
          showNotify({
            type: 'success',
            message: '视频详情获取任务已完成'
          })
        }
      } catch (error) {
        console.error('解析进度数据失败:', error)
      }
    }

    // 错误处理
    progressSource.value.onerror = (event) => {
      console.error('视频详情进度流错误:', event)
      closeProgressStream()

      // 如果正在获取中，显示错误消息
      if (isFetching.value) {
        showNotify({
          type: 'warning',
          message: '进度更新连接已断开'
        })
      }
    }
  } catch (error) {
    console.error('创建进度流失败:', error)
    showNotify({
      type: 'danger',
      message: '无法获取实时进度'
    })
  }
}

// 关闭SSE连接
const closeProgressStream = () => {
  if (progressSource.value) {
    console.log('关闭视频详情进度流')
    progressSource.value.close()
    progressSource.value = null
  }
}

// 组件挂载时获取统计数据
onMounted(() => {
  fetchStats()
})

// 组件卸载时清理资源
onUnmounted(() => {
  closeProgressStream()
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
