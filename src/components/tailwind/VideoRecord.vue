<template>
  <!-- 每条记录的容器，添加边框和圆角 -->
  <div
    class="mx-auto max-w-2xl cursor-pointer space-y-8 border-b border-gray-200 transition-all duration-200 ease-in-out hover:scale-[1.01] hover:border-[#FF6699] hover:bg-[#f5f5f5] hover:shadow-md sm:px-4 lg:max-w-4xl lg:px-0"
    @click="handleContentClick"
  >
    <!-- 内层容器，加入 padding 以确保内容有足够的内边距 -->
    <div class="p-2">
      <!-- 当类型为文章或文集时，图片铺满整行，标题在上方 -->
      <div v-if="record.business === 'article-list' || record.business === 'article'">
        <!-- 标题在封面图片上方 -->
        <div class="mb-2">
          <div class="line-clamp-2 text-gray-900 lm:text-sm lg:font-semibold" v-html="highlightedTitle"></div>
        </div>
        <!-- 封面图片，铺满整行 -->
        <div class="relative h-28 w-full overflow-hidden rounded-lg">
          <img :src="record.cover || record.covers[0]" class="h-full w-full object-cover" alt="" />
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
              class="h-4 w-4 cursor-pointer rounded-full transition-transform hover:scale-110 lg:h-8 lg:w-8"
              @click="handleAuthorClick"
              :title="`访问 ${record.author_name} 的个人空间`"
            />
            <p
              class="cursor-pointer transition-colors hover:text-[#FF6699]"
              @click="handleAuthorClick"
              :title="`访问 ${record.author_name} 的个人空间`"
              v-html="highlightedAuthorName"
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
              src="/public/PC.svg"
              alt="PC"
              class="h-4 w-4 lg:h-8 lg:w-8"
            />

            <img
              v-else-if="record.dt === 4 || record.dt === 6"
              src="/public/Pad.svg"
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
        <!-- 封面图片区域，设置为 relative，方便放置绝对定位的角标 -->
        <div class="relative h-20 w-32 overflow-hidden rounded-lg sm:h-28 sm:w-40">
          <img v-if="record.cover" :src="record.cover" class="h-full w-full object-cover" alt="" />
          <div v-else>
            <div v-for="(cover, index) in record.covers" :key="index" class="mb-1">
              <img :src="cover" class="h-full w-full object-cover" alt="" />
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
        <div class="ml-2 flex flex-1 flex-col justify-between lm:text-sm lg:font-semibold">
          <div class="items-center justify-between lg:flex">
            <div class="line-clamp-2 text-gray-900 lm:text-sm lg:font-semibold" v-html="highlightedTitle"></div>
          </div>
          <div>
            <span
              class="inline-flex items-center rounded-md bg-[#f1f2f3] px-2 py-1 text-xs text-[#71767d]"
            >
              {{ record.tag_name }}
            </span>
          </div>

          <div class="flex items-end justify-between text-sm text-[#99a2aa] lm:text-xs">
            <div class="flex items-center space-x-2" @click.stop>
              <img
                v-if="record.business !== 'cheese' && record.business !== 'pgc'"
                :src="record.author_face"
                alt="author"
                class="h-5 w-5 cursor-pointer rounded-full transition-transform hover:scale-110 lg:h-8 lg:w-8"
                @click="handleAuthorClick"
                :title="`访问 ${record.author_name} 的个人空间`"
              />
              <p
                class="cursor-pointer transition-colors hover:text-[#FF6699]"
                @click="handleAuthorClick"
                :title="`访问 ${record.author_name} 的个人空间`"
                v-html="highlightedAuthorName"
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
                src="/public/PC.svg"
                alt="PC"
                class="h-4 w-4 lg:h-8 lg:w-8"
              />
              <img
                v-else-if="record.dt === 4 || record.dt === 6"
                src="/public/Pad.svg"
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
import { defineProps, computed } from 'vue'

const props = defineProps({
  record: Object,
  searchKeyword: {
    type: String,
    default: ''
  },
  searchType: {
    type: String,
    default: 'title'
  }
})

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
</style>
