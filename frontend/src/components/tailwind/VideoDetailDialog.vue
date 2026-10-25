<template>
  <van-dialog
    :show="dialogVisible"
    @update:show="updateVisible"
    :title="video?.title || '视频详情'"
    class="video-detail-dialog"
    close-on-click-overlay
    :show-confirm-button="false"
    :style="{ width: '1000px', maxWidth: '90%', position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', borderRadius: '0.5rem', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)' }"
  >
    <div v-if="video" class="p-4 overflow-y-auto bg-transparent" style="height: 600px">
      <!-- 视频基础信息 -->
      <div class="flex flex-col md:flex-row gap-3">
        <!-- 左侧：视频封面 -->
        <div class="md:w-[30%] flex-shrink-0">
          <div class="relative w-full h-28 md:h-32 rounded-lg overflow-hidden">
            <img
              :src="normalizeImageUrl(video.cover || video.covers?.[0])"
              class="w-full h-full object-cover"
              :class="{ 'blur-md': isPrivacyMode }"
              alt="视频封面"
            />
            <!-- 视频时长 -->
            <div class="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
              {{ formatDuration(video.duration) }}
            </div>

            <!-- 进度条 -->
            <div v-if="video.business !== 'article-list' && video.business !== 'article' && video.business !== 'live'"
                 class="absolute bottom-0 left-0 w-full h-1 bg-gray-700/50">
              <div
                class="h-full bg-[#FF6699]"
                :style="{ width: getProgressWidth(video.progress, video.duration) }">
              </div>
            </div>
          </div>

          

          <!-- 视频下载信息 -->
          <div v-if="isVideoDownloaded && downloadedFiles.length > 0" class="mt-3">
            <div class="text-xs text-gray-500 dark:text-gray-400 p-2 bg-pink-50 dark:bg-pink-900/20 rounded-lg">
              <div class="flex items-center mb-1">
                <svg class="w-3 h-3 text-[#fb7299] mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="font-medium text-[#fb7299]">视频已下载</span>
              </div>
              <div v-for="(file, index) in downloadedFiles" :key="index" class="ml-4 truncate" :title="file.file_path">
                {{ file.file_name }} ({{ file.size_mb.toFixed(1) }} MB)
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：视频详情 -->
        <div class="md:w-[70%]">

          <!-- 视频信息 -->
          <div class="space-y-2 text-xs flex flex-col h-28 md:h-32 min-h-0">
            <!-- UP主信息 + 检测信息并排显示 -->
            <div v-if="video.business !== 'cheese' && video.business !== 'pgc'"
                 class="flex items-center space-x-2"
                 @click.stop>
              <div class="flex-shrink-0">
                <img
                  :src="normalizeImageUrl(video.author_face)"
                  alt="author"
                  class="h-7 w-7 cursor-pointer rounded-full transition-all duration-300 hover:scale-110"
                  :class="{ 'blur-md': isPrivacyMode }"
                  @click="openAuthorPage"
                  :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${video.author_name} 的个人空间`"
                />
              </div>
              <div class="flex-1 min-w-0">
                <p
                  class="cursor-pointer text-gray-800 dark:text-gray-200 transition-colors hover:text-[#FF6699]"
                  @click="openAuthorPage"
                  :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${video.author_name} 的个人空间`"
                  v-html="isPrivacyMode ? '******' : video.author_name"
                ></p>
                <p class="text-xs text-gray-500 dark:text-gray-400">UP主</p>
              </div>
              
            </div>

            <!-- 视频分区/观看时间/设备 行已按需求去除 -->

            <!-- 备注 -->
            <div class="mt-2 flex-1 flex flex-col min-h-0">
              <textarea
                v-model="remarkContent"
                @blur="handleRemarkBlur"
                :disabled="isPrivacyMode"
                placeholder="添加备注..."
                rows="2"
                class="w-full flex-1 resize-none px-2 py-1.5 text-xs text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-700 rounded border border-gray-200 dark:border-gray-600 focus:border-[#fb7299] focus:ring-[#fb7299] transition-colors duration-200"
                :class="{ 'blur-sm': isPrivacyMode }"
              ></textarea>
              <div v-if="remarkTime" class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                上次编辑: {{ formatRemarkTime(remarkTime) }}
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
    <!-- 加载中 -->
    <div v-else class="p-6 flex justify-center">
      <div class="animate-spin h-8 w-8 border-4 border-[#fb7299] border-t-transparent rounded-full"></div>
    </div>

  </van-dialog>

</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { showNotify } from 'vant'
import { usePrivacyStore } from '../../store/privacy'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'
import {
  updateVideoRemark,
  checkVideoDownload,
} from '../../api/api'
import { openInBrowser } from '@/utils/openUrl.js'
import { normalizeImageUrl } from '@/utils/imageUrl.js'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  video: {
    type: Object,
    default: null,
  },
  remarkData: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:modelValue', 'remark-updated'])


// 使用计算属性处理dialog可见性
const dialogVisible = computed(() => props.modelValue)
const updateVisible = (value) => {
  emit('update:modelValue', value)
}

const { isPrivacyMode } = usePrivacyStore()

// 备注相关
const remarkContent = ref('')
const originalRemark = ref('')
const remarkTime = ref(null)

// 格式化时间戳
const formatTimestamp = (timestamp) => {
  if (!timestamp) return '时间未知'

  try {
    const date = new Date(timestamp * 1000)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch (error) {
    console.error('格式化时间戳失败:', error)
    return '时间未知'
  }
}

// 格式化备注时间
const formatRemarkTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 格式化时长
const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完'
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0')
  const secs = String(seconds % 60).padStart(2, '0')
  return `${minutes}:${secs}`
}

// 计算进度条宽度百分比
const getProgressWidth = (progress, duration) => {
  if (!duration || duration <= 0 || !progress || progress < 0) return '0%'
  const percentage = Math.min(100, (progress / duration) * 100)
  return `${percentage}%`
}

// 获取设备类型
const getDeviceType = (dt) => {
  if (dt === 1 || dt === 3 || dt === 5 || dt === 7) return '手机'
  if (dt === 2 || dt === 33) return '电脑'
  if (dt === 4 || dt === 6) return '平板'
  return '未知设备'
}

// 获取业务类型
const getBusinessType = (business) => {
  const businessTypes = {
    archive: '稿件',
    cheese: '课堂',
    pgc: '电影',
    live: '直播',
    'article-list': '专栏',
    article: '专栏',
  }
  return businessTypes[business] || '其他类型'
}

// 初始化备注内容
const initRemark = () => {
  if (!props.video) return

  const key = `${props.video.bvid}_${props.video.view_at}`
  const data = props.remarkData[key]

  if (data) {
    remarkContent.value = data.remark || ''
    remarkTime.value = data.remark_time || null
    originalRemark.value = remarkContent.value // 保存原始值
  } else {
    remarkContent.value = ''
    remarkTime.value = null
    originalRemark.value = ''
  }
}

// 处理备注失去焦点
const handleRemarkBlur = async () => {
  // 如果内容没有变化，不发送请求
  if (remarkContent.value === originalRemark.value || !props.video) {
    return
  }

  try {
    const response = await updateVideoRemark(
      props.video.bvid,
      props.video.view_at,
      remarkContent.value,
    )

    if (response.data.success || response.data.status === 'success') {
      if (remarkContent.value) { // 只在有内容时显示提示
        showNotify({
          type: 'success',
          message: '备注已保存',
        })
      }

      originalRemark.value = remarkContent.value // 更新原始值
      remarkTime.value = response.data.data.remark_time // 更新备注时间

      // 通知父组件备注已更新
      emit('remark-updated', {
        bvid: props.video.bvid,
        view_at: props.video.view_at,
        remark: remarkContent.value,
        remark_time: response.data.data.remark_time,
      })
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `保存备注失败：${error.message}`,
    })
    remarkContent.value = originalRemark.value // 恢复原始值
  }
}

// 在B站打开视频
const openInBilibili = async () => {
  if (!props.video) return

  let url = ''

  switch (props.video.business) {
    case 'archive':
      url = `https://www.bilibili.com/video/${props.video.bvid}`
      break
    case 'article':
      url = `https://www.bilibili.com/read/cv${props.video.oid}`
      break
    case 'article-list':
      url = `https://www.bilibili.com/read/readlist/rl${props.video.oid}`
      break
    case 'live':
      url = `https://live.bilibili.com/${props.video.oid}`
      break
    case 'pgc':
      url = props.video.uri || `https://www.bilibili.com/bangumi/play/ep${props.video.epid}`
      break
    case 'cheese':
      url = props.video.uri || `https://www.bilibili.com/cheese/play/ep${props.video.epid}`
      break
    default:
      console.warn('未知的业务类型:', props.video.business)
      return
  }

  if (url) {
    await openInBrowser(url)
  }
}

// 打开UP主页面
const openAuthorPage = async () => {
  if (!props.video || !props.video.author_mid) return
  const url = `https://space.bilibili.com/${props.video.author_mid}`
  await openInBrowser(url)
}

// 监听video变化，初始化备注
watch(() => props.video, () => {
  if (props.video) {
    initRemark()
  }
}, { deep: true, immediate: true })

// 下载相关
const isVideoDownloaded = ref(false)
const downloadedFiles = ref([])

// 检查视频是否已下载
const checkIsVideoDownloaded = async () => {
  try {
    // 如果没有CID，则无法检查
    if (!props.video?.cid) return

    const response = await checkVideoDownload(props.video.cid)
    if (response.data && response.data.status === 'success') {
      isVideoDownloaded.value = response.data.downloaded

      if (isVideoDownloaded.value && response.data.files) {
        downloadedFiles.value = response.data.files
      } else {
        downloadedFiles.value = []
      }
    }
  } catch (error) {
    console.error('检查视频下载状态出错:', error)
    isVideoDownloaded.value = false
    downloadedFiles.value = []
  }
}

// 监听视频变化，检查下载状态
watch(() => props.video?.cid, (newCid) => {
  if (newCid) {
    checkIsVideoDownloaded()
  } else {
    isVideoDownloaded.value = false
    downloadedFiles.value = []
  }
})
</script>

<style>
.video-detail-dialog :deep(.van-dialog) {
  border-radius: 0.5rem;
  overflow: hidden;
}

/* 对话框正文背景与页面正文一致 */
.video-detail-dialog :deep(.van-dialog__content) {
  background-color: #ffffff; /* light */
}
.dark .video-detail-dialog :deep(.van-dialog__content) {
  background-color: #1f2937; /* gray-800 */
}

.video-detail-dialog :deep(.van-dialog__header) {
  padding: 12px 16px;
  background-color: #ffffff; /* light: white 与正文一致 */
  border-bottom: 1px solid #e5e7eb; /* gray-200 */
  color: #111827; /* gray-900 */
}
.dark .video-detail-dialog :deep(.van-dialog__header) {
  background-color: #1f2937; /* dark: gray-800 与正文一致 */
  border-bottom: 1px solid #374151; /* gray-700 */
  color: #e5e7eb; /* gray-200 */
}
</style>
