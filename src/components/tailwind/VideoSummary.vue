<template>
  <div class="w-full bg-white dark:bg-gray-800 rounded-lg shadow-sm p-4">
    <!-- 摘要内容显示区域 -->
    <div v-if="summary && !loading && !error" class="space-y-4">
      <div class="flex items-center justify-between">
        <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24"
               stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <span>AI视频摘要</span>
        </h3>

        <button
          @click="refreshSummary"
          class="text-xs text-gray-500 dark:text-gray-400 hover:text-[#fb7299] flex items-center space-x-1"
          :disabled="loading"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24"
               stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>刷新</span>
        </button>
      </div>

      <!-- 总体摘要 -->
      <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
        <p class="text-xs text-gray-700 dark:text-gray-300 whitespace-pre-line leading-relaxed">{{ summary }}</p>
      </div>

      <!-- 视频大纲 -->
      <div v-if="outline && outline.length > 0" class="mt-4">
        <h4 class="text-xs font-medium text-gray-800 dark:text-gray-200 mb-2 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1 text-[#fb7299]" fill="none"
               viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <span>视频大纲</span>
        </h4>

        <div class="space-y-3">
          <div v-for="(section, index) in outline" :key="index" class="border-l-2 border-[#fb7299]/30 pl-3 py-1">
            <!-- 章节标题 -->
            <div class="flex items-start">
              <a
                :href="`https://www.bilibili.com/video/${props.bvid}?t=${section.timestamp}`"
                target="_blank"
                class="inline-flex items-center text-xs font-medium text-[#fb7299] hover:underline"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24"
                     stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {{ formatTime(section.timestamp) }}
              </a>
              <h5 class="text-xs font-medium text-gray-800 dark:text-gray-200 ml-2">{{ section.title }}</h5>
            </div>

            <!-- 章节要点 -->
            <div v-if="section.part_outline && section.part_outline.length > 0" class="mt-1 ml-4 space-y-1">
              <div v-for="(point, pIndex) in section.part_outline" :key="`${index}-${pIndex}`" class="flex items-start">
                <a
                  :href="`https://www.bilibili.com/video/${props.bvid}?t=${point.timestamp}`"
                  target="_blank"
                  class="inline-flex items-center text-[10px] text-gray-500 hover:text-[#fb7299] hover:underline mt-0.5"
                >
                  {{ formatTime(point.timestamp) }}
                </a>
                <p class="text-[11px] text-gray-600 dark:text-gray-400 ml-2">{{ point.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="fromCache" class="text-xs text-gray-400 dark:text-gray-500 flex items-center mt-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24"
             stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>摘要来自缓存</span>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="py-6 space-y-3">
      <div class="flex items-center">
        <svg class="animate-spin h-4 w-4 text-[#fb7299] mr-2" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100">AI正在生成视频摘要...</h3>
      </div>
      <div class="animate-pulse flex space-x-4">
        <div class="flex-1 space-y-3">
          <div class="h-2 bg-gray-200 rounded"></div>
          <div class="h-2 bg-gray-200 rounded"></div>
          <div class="h-2 bg-gray-200 rounded"></div>
          <div class="h-2 bg-gray-200 rounded w-5/6"></div>
        </div>
      </div>
      <p class="text-xs text-gray-400 dark:text-gray-500">首次生成可能需要一些时间，请耐心等待</p>
    </div>

    <!-- 错误状态 -->
    <div v-if="error && !loading" class="py-8 flex flex-col items-center justify-center">
      <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100 flex items-center">
        <svg v-if="errorIsWarning" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-500 mr-1" fill="none"
             viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <svg v-else-if="isGenerating" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-500 mr-1" fill="none"
             viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-500 mr-1" fill="none" viewBox="0 0 24 24"
             stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>{{ errorTitle }}</span>
      </h3>
      <p class="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">{{ error }}</p>
      <div class="mt-4 flex items-center space-x-3">
        <button
          v-if="shouldShowRetryButton"
          @click="() => fetchSummary(false)"
          class="text-xs bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 rounded px-3 py-1.5"
        >
          重试
        </button>
        <button
          v-if="isGenerating"
          @click="() => fetchSummary(false)"
          class="text-xs bg-[#fb7299] hover:bg-[#fc8bad] text-white rounded px-3 py-1.5"
        >
          查看进度
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { getVideoSummary } from '../../api/api'
import { showNotify } from 'vant'
import 'vant/es/notify/style'

const props = defineProps({
  bvid: {
    type: String,
    required: true,
  },
  cid: {
    type: [String, Number],
    required: true,
  },
  upMid: {
    type: [String, Number],
    required: true,
  },
})

const summary = ref('')
const outline = ref(null)
const loading = ref(false)
const error = ref(null)
const fromCache = ref(false)
const stid = ref('')

// 当props变化时，清除旧数据并重新获取摘要
watch(
  () => [props.bvid, props.cid, props.upMid],
  (newValues, oldValues) => {
    // 如果是组件首次加载，不需要处理
    if (!oldValues[0]) return

    // 如果有任一值变化，说明是新的视频，清除旧数据并重新获取
    if (
      newValues[0] !== oldValues[0] ||
      newValues[1] !== oldValues[1] ||
      newValues[2] !== oldValues[2]
    ) {
      // 清除旧数据
      clearSummaryData()
      // 获取新数据
      fetchSummary()
    }
  },
)

// 清除摘要数据
const clearSummaryData = () => {
  summary.value = ''
  outline.value = null
  error.value = null
  fromCache.value = false
  stid.value = ''
}

// 将秒数格式化为时分秒
const formatTime = (seconds) => {
  if (!seconds && seconds !== 0) return '00:00'

  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hours > 0) {
    return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  } else {
    return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  }
}

// 获取视频摘要
const fetchSummary = async (forceRefresh = false) => {
  if (!props.bvid || !props.cid || !props.upMid) {
    error.value = '缺少必要参数，无法获取视频摘要'
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await getVideoSummary(
      props.bvid,
      props.cid,
      props.upMid,
      forceRefresh,
    )

    // 处理API返回的数据
    const data = response.data

    // 保存stid
    stid.value = data.stid || ''

    // 根据has_summary和result_type判断状态
    if (data.has_summary) {
      // 有摘要内容
      summary.value = data.summary || ''
      outline.value = data.outline || null
      fromCache.value = data.from_cache !== undefined ? data.from_cache : false
    } else {
      // 根据result_type判断状态
      switch (data.result_type) {
        case -1:
          error.value = '该视频不支持AI摘要（可能包含敏感内容）'
          break
        case 0:
          error.value = data.status_message || '该视频没有摘要'
          break
        case 1:
          // 仅存在摘要总结
          summary.value = data.summary || ''
          outline.value = null
          fromCache.value = data.from_cache !== undefined ? data.from_cache : false
          break
        case 2:
          // 存在摘要以及提纲
          summary.value = data.summary || ''
          outline.value = data.outline || null
          fromCache.value = data.from_cache !== undefined ? data.from_cache : false
          break
        default:
          error.value = data.status_message || '获取摘要失败'
      }
    }
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || '网络错误，请稍后重试'
    console.error('获取视频摘要失败:', err)
  } finally {
    loading.value = false
  }
}

// 强制刷新摘要
const refreshSummary = async (event) => {
  // 忽略事件对象，传递true作为force_refresh参数
  await fetchSummary(true)
  showNotify({
    type: 'success',
    message: '摘要已更新',
  })
}

// 组件挂载时获取摘要
onMounted(() => {
  if (props.bvid && props.cid && props.upMid) {
    // 先清除数据以显示加载状态
    clearSummaryData()
    loading.value = true
    // 延迟一下再获取，确保加载状态能够显示
    setTimeout(() => {
      fetchSummary()
    }, 100)
  }
})

// 计算是否显示重试按钮
const shouldShowRetryButton = computed(() => {
  // 网络错误或处理错误时显示重试按钮
  if (!error.value) return false

  // 这些情况下不显示重试按钮，因为重试没有意义
  const noRetryMessages = [
    '未识别到视频语音，无法生成摘要',
    '该视频不支持AI摘要',
    '缺少必要参数',
  ]

  return !noRetryMessages.some(msg => error.value.includes(msg))
})

// 判断错误是否为警告类型（黄色图标）
const errorIsWarning = computed(() => {
  if (!error.value) return false

  const warningMessages = [
    '未识别到视频语音',
    '此视频暂无摘要',
    '该视频不支持AI摘要',
  ]

  return warningMessages.some(msg => error.value.includes(msg))
})

// 根据错误类型返回适当的标题
const errorTitle = computed(() => {
  if (!error.value) return '获取摘要失败'

  if (isGenerating.value) {
    return '摘要生成中'
  } else if (errorIsWarning.value) {
    return '无法生成摘要'
  } else {
    return '获取摘要失败'
  }
})

// 判断是否为"生成中"状态
const isGenerating = computed(() => {
  if (!error.value) return false
  return error.value.includes('正在生成')
})
</script>

<style scoped>
/* 平滑滚动 */
html {
  scroll-behavior: smooth;
}
</style>
