<template>
  <!-- 每条记录的容器 -->
  <div
    class="mx-auto max-w-2xl cursor-pointer border-b border-gray-200 transition-all duration-200 ease-in-out hover:scale-[1.01] hover:border-[#FF6699] hover:bg-[#f5f5f5] hover:shadow-md sm:px-4 lg:max-w-4xl lg:px-0 relative group"
    @click="handleClick"
  >
    <!-- 内层容器 -->
    <div class="p-2">
      <!-- 当类型为文章或文集时，图片铺满整行，标题在上方 -->
      <div v-if="record.business === 'article-list' || record.business === 'article'">
        <!-- 标题在封面图片上方 -->
        <div class="mb-2">
          <div
            class="line-clamp-2 text-gray-900 lm:text-sm lg:font-semibold"
            v-html="isPrivacyMode ? '******' : highlightedTitle"
            :class="{ 'blur-sm': isPrivacyMode }"
          ></div>
        </div>
        <!-- 封面图片，铺满整行 -->
        <div class="relative h-28 w-full overflow-hidden rounded-lg">
          <!-- 删除按钮 -->
          <div v-if="!isBatchMode"
               class="absolute right-2 top-2 z-20 hidden group-hover:flex items-center space-x-2">
            <!-- 删除按钮 -->
            <div class="flex items-center justify-center w-8 h-8 bg-black/50 hover:bg-[#fb7299] rounded-full cursor-pointer transition-all duration-200"
                 @click.stop="handleDelete">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </div>
          </div>
          <!-- 多选框 -->
          <div v-if="isBatchMode"
               class="absolute left-2 top-2 z-10"
               @click.stop="$emit('toggle-selection', record)">
            <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                 :class="isSelected ? 'bg-[#fb7299] border-[#fb7299]' : 'border-white bg-black/20'">
              <svg v-if="isSelected" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
          <img
            :src="record.cover || record.covers[0]"
            class="h-full w-full object-cover transition-all duration-300"
            :class="{ 'blur-md': isPrivacyMode }"
            alt=""
          />
          <!-- 右上角的类型角标，仅当不是稿件时显示 -->
          <div
            v-if="record.business !== 'archive'"
            class="absolute right-1 top-1 rounded bg-[#FF6699] px-1 py-0.5 text-[10px] text-white"
          >
            {{ getBusinessType(record.business) }}
          </div>
        </div>
        <!-- 文章类型：作者信息、观看设备、时间放在封面图片下方 -->
        <div class="mt-2 flex items-center justify-between text-sm text-[#99a2aa] lm:text-xs">
          <!-- 左侧：仅当类型不是剧集或课程时，显示作者头像和名字 -->
          <div
            v-if="record.business !== 'cheese' && record.business !== 'pgc'"
            class="flex items-center space-x-2"
            @click.stop
          >
            <img
              :src="record.author_face"
              alt="author"
              class="h-4 w-4 cursor-pointer rounded-full transition-all duration-300 hover:scale-110 lg:h-8 lg:w-8"
              :class="{ 'blur-md': isPrivacyMode }"
              @click="handleAuthorClick"
              :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
            />
            <p
              class="cursor-pointer transition-colors hover:text-[#FF6699]"
              @click="handleAuthorClick"
              :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
              v-html="isPrivacyMode ? '******' : highlightedAuthorName"
            ></p>
          </div>
          <!-- 右侧：设备和时间信息 -->
          <div class="flex items-center space-x-2">
            <img
              v-if="record.dt === 1 || record.dt === 3 || record.dt === 5 || record.dt === 7"
              src="/Mobile.svg"
              alt="Mobile"
              class="h-4 w-4 lg:h-8 lg:w-8"
            />
            <img
              v-else-if="record.dt === 2 || record.dt === 33"
              src="/PC.svg"
              alt="PC"
              class="h-4 w-4 lg:h-8 lg:w-8"
            />
            <img
              v-else-if="record.dt === 4 || record.dt === 6"
              src="/Pad.svg"
              alt="Pad"
              class="h-4 w-4 lg:h-8 lg:w-8"
            />
            <p v-else>未知设备</p>
            <!-- 显示时间 -->
            <span>{{ formatTimestamp(record.view_at) }}</span>
          </div>
        </div>
      </div>

      <!-- 其他类型的展示方式 -->
      <div v-else class="flex space-x-2">
        <!-- 封面图片区域 -->
        <div class="relative h-20 w-32 overflow-hidden rounded-lg sm:h-28 sm:w-40">
          <!-- 多选框 -->
          <div v-if="isBatchMode"
               class="absolute left-2 top-2 z-10"
               @click.stop="$emit('toggle-selection', record)">
            <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                 :class="isSelected ? 'bg-[#fb7299] border-[#fb7299]' : 'border-white bg-black/20'">
              <svg v-if="isSelected" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
          <img
            v-if="record.cover"
            :src="record.cover"
            class="h-full w-full object-cover transition-all duration-300"
            :class="{ 'blur-md': isPrivacyMode }"
            alt=""
          />
          <div v-else>
            <div v-for="(cover, index) in record.covers" :key="index" class="mb-1">
              <img
                :src="cover"
                class="h-full w-full object-cover transition-all duration-300"
                :class="{ 'blur-md': isPrivacyMode }"
                alt=""
              />
            </div>
          </div>
          <!-- 右上的类型角标，稿件显示角标 -->
          <div
            v-if="record.business !== 'archive'"
            class="absolute right-1 top-1 rounded bg-[#FF6699] px-1 py-0.5 text-[10px] font-semibold text-white"
          >
            {{ getBusinessType(record.business) }}
          </div>
          <!-- 右下角的时间进度角标和进度条，仅当不是文章时显示 -->
          <div
            v-if="
              record.business !== 'article-list' &&
              record.business !== 'article' &&
              record.business !== 'live'
            "
          >
            <div
              class="absolute bottom-1 right-1 rounded bg-black/50 px-1 py-1 text-[10px] font-semibold text-white"
            >
              <span>{{ formatDuration(record.progress) }}</span>
              <span>/</span>
              <span>{{ formatDuration(record.duration) }}</span>
            </div>
            <div class="absolute bottom-0 left-0 h-0.5 w-full bg-black">
              <div
                class="h-full bg-[#FF6699]"
                :style="{ width: getProgressWidth(record.progress, record.duration) }"
              ></div>
            </div>
          </div>
        </div>

        <!-- 右侧内容区域 -->
        <div class="ml-2 flex flex-1 flex-col justify-between lm:text-sm lg:font-semibold relative">
          <!-- 删除按钮 -->
          <div v-if="!isBatchMode"
               class="absolute right-2 top-2 z-20 hidden group-hover:flex items-center space-x-2">
            <!-- 删除按钮 -->
            <div class="flex items-center justify-center w-8 h-8 bg-black/50 hover:bg-[#fb7299] rounded-full cursor-pointer transition-all duration-200"
                 @click.stop="handleDelete">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </div>
          </div>
          <div class="items-center justify-between lg:flex">
            <div
              class="line-clamp-2 text-gray-900 lm:text-sm lg:font-semibold"
              v-html="isPrivacyMode ? '******' : highlightedTitle"
              :class="{ 'blur-sm': isPrivacyMode }"
            ></div>
          </div>
          <div class="flex items-center space-x-2">
            <span
              class="inline-flex items-center rounded-md bg-[#f1f2f3] px-2 py-1 text-xs text-[#71767d]"
            >
              {{ record.tag_name }}
            </span>
            <!-- 备注输入框 -->
            <div class="flex-1 relative group" @click.stop>
              <div class="flex items-center space-x-1">
                <span class="text-xs text-[#fb7299]">备注:</span>
                <input
                  type="text"
                  v-model="remarkContent"
                  @focus="handleRemarkFocus"
                  @blur="handleRemarkBlur"
                  placeholder="添加备注..."
                  :disabled="isPrivacyMode"
                  :value="isPrivacyMode ? '******' : remarkContent"
                  class="flex-1 px-2 py-1 text-xs text-[#fb7299] bg-[#f8f8f8] rounded border-0 border-b border-transparent hover:border-gray-200 focus:border-[#fb7299] focus:ring-0 transition-colors duration-200 placeholder-[#fb7299]/50"
                  :class="{ 'blur-sm': isPrivacyMode }"
                />
              </div>
              <div v-if="!remarkContent && !isPrivacyMode" class="absolute right-2 top-1/2 -translate-y-1/2 hidden group-hover:block">
                <svg class="w-3 h-3 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="flex items-end justify-between text-sm text-[#99a2aa] lm:text-xs">
            <div class="flex items-center space-x-2" @click.stop>
              <img
                v-if="record.business !== 'cheese' && record.business !== 'pgc'"
                :src="record.author_face"
                alt="author"
                class="h-5 w-5 cursor-pointer rounded-full transition-all duration-300 hover:scale-110 lg:h-8 lg:w-8"
                :class="{ 'blur-md': isPrivacyMode }"
                @click="handleAuthorClick"
                :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
              />
              <p
                class="cursor-pointer transition-colors hover:text-[#FF6699]"
                @click="handleAuthorClick"
                :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
                v-html="isPrivacyMode ? '******' : highlightedAuthorName"
              ></p>
            </div>

            <div class="flex items-center space-x-2">
              <img
                v-if="record.dt === 1 || record.dt === 3 || record.dt === 5 || record.dt === 7"
                src="/Mobile.svg"
                alt="Mobile"
                class="h-4 w-4 lg:h-8 lg:w-8"
              />
              <img
                v-else-if="record.dt === 2 || record.dt === 33"
                src="/PC.svg"
                alt="PC"
                class="h-4 w-4 lg:h-8 lg:w-8"
              />
              <img
                v-else-if="record.dt === 4 || record.dt === 6"
                src="/Pad.svg"
                alt="Pad"
                class="h-4 w-4 lg:h-8 lg:w-8"
              />
              <p v-else>未知设备</p>

              <!-- 显示时间 -->
              <span>{{ formatTimestamp(record.view_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { usePrivacyStore } from '../../store/privacy'
import { showDialog, showNotify } from 'vant'
import { batchDeleteHistory, updateVideoRemark, getVideoRemark } from '../../api/api'
import 'vant/es/dialog/style'
import 'vant/es/popup/style'
import 'vant/es/field/style'

const { isPrivacyMode } = usePrivacyStore()

const props = defineProps({
  record: {
    type: Object,
    required: true
  },
  searchKeyword: {
    type: String,
    default: ''
  },
  searchType: {
    type: String,
    default: 'title'
  },
  isBatchMode: {
    type: Boolean,
    default: false
  },
  isSelected: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['toggle-selection', 'refresh-data'])

const remarkContent = ref('')
const originalRemark = ref('') // 用于存储原始备注内容

// 高亮显示匹配的文本
const highlightText = (text) => {
  if (!props.searchKeyword || !text) return text

  const regex = new RegExp(props.searchKeyword, 'gi')
  return text.replace(regex, match => `<span class="text-[#FF6699]">${match}</span>`)
}

// 获取高亮后的标题
const highlightedTitle = computed(() => {
  if (props.searchType !== 'title' || !props.searchKeyword) return props.record.title
  return highlightText(props.record.title)
})

// 获取高亮后的作者名称
const highlightedAuthorName = computed(() => {
  if (props.searchType !== 'author' || !props.searchKeyword) return props.record.author_name
  return highlightText(props.record.author_name)
})

// 处理点击事件
const handleClick = () => {
  if (props.isBatchMode) {
    emit('toggle-selection', props.record)
  } else {
    handleContentClick()
  }
}

// 处理内容点击事件
const handleContentClick = () => {
  let url = ''

  switch (props.record.business) {
    case 'archive':
      url = `https://www.bilibili.com/video/${props.record.bvid}`
      break
    case 'article':
      url = `https://www.bilibili.com/read/cv${props.record.oid}`
      break
    case 'article-list':
      url = `https://www.bilibili.com/read/readlist/rl${props.record.oid}`
      break
    case 'live':
      url = `https://live.bilibili.com/${props.record.oid}`
      break
    case 'pgc':
      url = props.record.uri || `https://www.bilibili.com/bangumi/play/ep${props.record.epid}`
      break
    case 'cheese':
      url = props.record.uri || `https://www.bilibili.com/cheese/play/ep${props.record.epid}`
      break
    default:
      console.warn('未知的业务类型:', props.record.business)
      return
  }

  if (url) {
    window.open(url, '_blank')
  }
}

// 处理UP主点击事件
const handleAuthorClick = () => {
  const url = `https://space.bilibili.com/${props.record.author_mid}`
  window.open(url, '_blank')
}

// 修改时间戳显示相关的代码
const formatTimestamp = (timestamp) => {
  // 检查 timestamp 是否有效
  if (!timestamp) {
    console.warn('Invalid timestamp:', timestamp)
    return '时间未知'
  }

  try {
    // 将秒级时间戳转换为毫秒级
    const date = new Date(timestamp * 1000)
    const now = new Date()

    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      console.warn('Invalid date from timestamp:', timestamp)
      return '时间未知'
    }

    const isToday = now.toDateString() === date.toDateString()
    const isYesterday =
      new Date(now.setDate(now.getDate() - 1)).toDateString() === date.toDateString()
    const timeString = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })

    if (isToday) {
      return timeString
    } else if (isYesterday) {
      return `昨天 ${timeString}`
    } else if (now.getFullYear() === date.getFullYear()) {
      return `${date.getMonth() + 1}-${date.getDate()} ${timeString}`
    } else {
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${timeString}`
    }
  } catch (error) {
    console.error('Error formatting timestamp:', error)
    return '时间未知'
  }
}

const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完'
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0')
  const secs = String(seconds % 60).padStart(2, '0')
  return `${minutes}:${secs}`
}

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

const getProgressWidth = (progress, duration) => {
  if (progress === -1) return '100%'
  if (duration === 0) return '0%'
  return `${(progress / duration) * 100}%`
}

// 处理删除事件
const handleDelete = async () => {
  try {
    await showDialog({
      title: '确认删除',
      message: '确定要删除这条记录吗？此操作不可恢复。',
      showCancelButton: true,
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      confirmButtonColor: '#fb7299'
    })

    const response = await batchDeleteHistory([{
      bvid: props.record.bvid,
      view_at: props.record.view_at
    }])
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message
      })
      emit('refresh-data')
    } else {
      throw new Error(response.data.message || '删除失败')
    }
  } catch (error) {
    if (error.toString().includes('cancel')) return

    showNotify({
      type: 'danger',
      message: error.response?.data?.detail || error.message || '删除失败'
    })
  }
}

// 初始化备注内容
const initRemark = async () => {
  try {
    const response = await getVideoRemark(props.record.bvid, props.record.view_at)
    remarkContent.value = response.data.data.remark || ''
    originalRemark.value = remarkContent.value // 保存原始值
  } catch (error) {
    console.error('获取备注失败:', error)
  }
}

// 处理备注获取焦点
const handleRemarkFocus = async () => {
  if (remarkContent.value === '') {
    await initRemark()
  }
}

// 处理备注失去焦点
const handleRemarkBlur = async () => {
  // 如果内容没有变化，不发送请求
  if (remarkContent.value === originalRemark.value) {
    return
  }

  try {
    const response = await updateVideoRemark(
      props.record.bvid,
      props.record.view_at,
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
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `保存备注失败：${error.message}`
    })
    remarkContent.value = originalRemark.value // 恢复原始值
  }
}

// 组件挂载时初始化备注
onMounted(async () => {
  await initRemark()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 可以添加一些额外的悬停效果样式 */
.hover\:scale-110:hover {
  transform: scale(1.1);
}

.hover\:text-\[\#FF6699\]:hover {
  color: #ff6699;
}

/* 添加 group-hover 相关样式 */
.group:hover .group-hover\:flex {
  display: flex;
}
</style>
