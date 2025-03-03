<template>
  <van-dialog
    :show="dialogVisible"
    @update:show="updateVisible"
    :title="video?.title || '视频详情'"
    class="video-detail-dialog"
    close-on-click-overlay
    :show-confirm-button="false"
    :style="{ width: '90%', maxWidth: '900px' }"
  >
    <div v-if="video" class="p-4 overflow-y-auto max-h-[70vh]">
      <!-- 视频基础信息 -->
      <div class="flex flex-col md:flex-row gap-4">
        <!-- 左侧：视频封面 -->
        <div class="md:w-1/3 flex-shrink-0">
          <div class="relative aspect-video rounded-lg overflow-hidden">
            <img
              :src="video.cover || video.covers?.[0]"
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
          
          <!-- 操作按钮 -->
          <div class="mt-4 flex space-x-2">
            <button
              @click="openInBilibili"
              class="w-full px-4 py-2 bg-[#fb7299] hover:bg-[#fc8bad] text-white text-sm rounded-lg flex items-center justify-center space-x-1"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              <span>在B站打开</span>
            </button>
          </div>
        </div>
        
        <!-- 右侧：视频详情 -->
        <div class="md:w-2/3">
          <!-- 视频标题 -->
          <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-3"
              :class="{ 'blur-sm': isPrivacyMode }"
              v-html="isPrivacyMode ? '******' : video.title">
          </h3>
          
          <!-- 视频信息 -->
          <div class="space-y-3 text-sm">
            <!-- UP主信息 -->
            <div v-if="video.business !== 'cheese' && video.business !== 'pgc'"
                 class="flex items-center space-x-2"
                 @click.stop>
              <div class="flex-shrink-0">
                <img
                  :src="video.author_face"
                  alt="author"
                  class="h-8 w-8 cursor-pointer rounded-full transition-all duration-300 hover:scale-110"
                  :class="{ 'blur-md': isPrivacyMode }"
                  @click="openAuthorPage"
                  :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${video.author_name} 的个人空间`"
                />
              </div>
              <div class="flex-1">
                <p
                  class="cursor-pointer text-gray-800 dark:text-gray-200 transition-colors hover:text-[#FF6699]"
                  @click="openAuthorPage"
                  :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${video.author_name} 的个人空间`"
                  v-html="isPrivacyMode ? '******' : video.author_name"
                ></p>
                <p class="text-xs text-gray-500 dark:text-gray-400">UP主</p>
              </div>
            </div>
            
            <!-- 视频分区和时间 -->
            <div class="flex flex-wrap gap-2">
              <div class="rounded-md bg-[#f1f2f3] dark:bg-gray-700 px-2 py-1 text-xs text-gray-700 dark:text-gray-300">
                {{ video.business === 'archive' ? video.tag_name : getBusinessType(video.business) }}
              </div>
              <div class="rounded-md bg-[#f1f2f3] dark:bg-gray-700 px-2 py-1 text-xs text-gray-700 dark:text-gray-300">
                观看于: {{ formatTimestamp(video.view_at) }}
              </div>
              <div class="rounded-md bg-[#f1f2f3] dark:bg-gray-700 px-2 py-1 text-xs text-gray-700 dark:text-gray-300"
                   v-if="video.dt">
                设备: {{ getDeviceType(video.dt) }}
              </div>
              <div class="rounded-md bg-[#f1f2f3] dark:bg-gray-700 px-2 py-1 text-xs text-gray-700 dark:text-gray-300"
                   v-if="video.badge">
                {{ video.badge }}
              </div>
            </div>
            
            <!-- 备注 -->
            <div class="mt-3">
              <label class="text-sm text-gray-700 dark:text-gray-300 mb-1 block">备注</label>
              <textarea
                v-model="remarkContent"
                @blur="handleRemarkBlur"
                :disabled="isPrivacyMode"
                placeholder="添加备注..."
                rows="2"
                class="w-full px-3 py-2 text-sm text-gray-800 dark:text-white bg-gray-50 dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700 focus:border-[#fb7299] focus:ring-[#fb7299] transition-colors duration-200"
                :class="{ 'blur-sm': isPrivacyMode }"
              ></textarea>
              <div v-if="remarkTime" class="text-xs text-gray-400 mt-1">
                上次编辑: {{ formatRemarkTime(remarkTime) }}
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 视频摘要 -->
      <div v-if="video.business === 'archive'" class="mt-6">
        <VideoSummary 
          :bvid="video.bvid" 
          :cid="String(video.cid)" 
          :upMid="String(video.author_mid)"
        />
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
import { updateVideoRemark } from '../../api/api'
import { showNotify } from 'vant'
import { usePrivacyStore } from '../../store/privacy'
import VideoSummary from './VideoSummary.vue'
import 'vant/es/dialog/style'
import 'vant/es/notify/style'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  video: {
    type: Object,
    default: null
  },
  remarkData: {
    type: Object,
    default: () => ({})
  }
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
      minute: '2-digit'
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
    minute: '2-digit'
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
      remarkContent.value
    )
    
    if (response.data.status === 'success') {
      if (remarkContent.value) { // 只在有内容时显示提示
        showNotify({
          type: 'success',
          message: '备注已保存'
        })
      }
      
      originalRemark.value = remarkContent.value // 更新原始值
      remarkTime.value = response.data.data.remark_time // 更新备注时间
      
      // 通知父组件备注已更新
      emit('remark-updated', {
        bvid: props.video.bvid,
        view_at: props.video.view_at,
        remark: remarkContent.value,
        remark_time: response.data.data.remark_time
      })
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `保存备注失败：${error.message}`
    })
    remarkContent.value = originalRemark.value // 恢复原始值
  }
}

// 在B站打开视频
const openInBilibili = () => {
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
    window.open(url, '_blank')
  }
}

// 打开UP主页面
const openAuthorPage = () => {
  if (!props.video || !props.video.author_mid) return
  const url = `https://space.bilibili.com/${props.video.author_mid}`
  window.open(url, '_blank')
}

// 监听video变化，初始化备注
watch(() => props.video, () => {
  if (props.video) {
    initRemark()
  }
}, { deep: true, immediate: true })
</script>

<style>
.video-detail-dialog .van-dialog__content {
  max-height: 85vh;
  overflow-y: auto;
}
</style> 