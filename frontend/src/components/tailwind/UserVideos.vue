<template>
  <div class="transition-all duration-300 ease-in-out">
    <!-- 加载状态 -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-16 bg-white dark:bg-gray-900 rounded-lg">
      <div class="w-16 h-16 border-4 border-[#fb7299] border-t-transparent rounded-full animate-spin mb-4"></div>
      <h3 class="text-xl font-medium text-gray-600 dark:text-gray-300 mb-2">加载中</h3>
      <p class="text-gray-500 dark:text-gray-400">正在获取视频列表...</p>
    </div>

    <!-- 视频列表为空状态 -->
    <div v-else-if="videos.length === 0" class="flex flex-col items-center justify-center py-16 bg-white dark:bg-gray-900 rounded-lg">
      <svg class="w-24 h-24 text-gray-300 dark:text-gray-600 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-medium text-gray-600 dark:text-gray-300 mb-2">暂无视频</h3>
      <p class="text-gray-500 dark:text-gray-400">该用户还没有发布任何视频</p>
    </div>

    <!-- 视频列表 -->
    <div v-else class="overflow-hidden">
      <div
        class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 px-4 mx-auto transition-all duration-300 ease-in-out transform-gpu"
        style="max-width: 1152px;">
        <div v-for="video in videos" :key="video.aid"
             class="bg-white/50 dark:bg-gray-800/60 backdrop-blur-sm rounded-lg overflow-hidden border border-gray-200/50 dark:border-gray-700 hover:border-[#FF6699] hover:shadow-md transition-all duration-200 relative group">
          <!-- 封面图片 -->
          <div class="relative aspect-video cursor-pointer" @click="handleVideoClick(video)">
            <img
              :src="video.pic"
              class="w-full h-full object-cover transition-all duration-300"
              alt=""
            />
            <!-- 视频时长 -->
            <div class="absolute bottom-1 right-1 rounded bg-black/50 px-1 py-1 text-[10px] font-semibold text-white">
              {{ video.length }}
            </div>
          </div>
          <!-- 视频信息 -->
          <div class="p-3 flex flex-col space-y-1">
            <!-- 标题 -->
            <div class="line-clamp-1 text-sm text-gray-900 dark:text-gray-100 cursor-pointer" @click="handleVideoClick(video)">
              {{ video.title }}
            </div>
            <!-- 播放量和评论数 -->
            <div class="text-xs text-gray-500 dark:text-gray-400 flex items-center space-x-2">
 <span class="flex items-center">
 <svg class="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
       d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
 </svg>
 {{ formatNumber(video.play) }}
 </span>
              <span class="flex items-center">
 <svg class="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
 <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
       d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
 </svg>
 {{ formatNumber(video.comment) }}
 </span>
            </div>
            <!-- 发布时间 -->
            <div class="text-xs text-gray-500 dark:text-gray-400">
              {{ formatTimestamp(video.created) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="mt-4 flex justify-center">
        <Pagination
          :current-page="currentPage"
          :total-pages="totalPages"
          @page-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { getUserVideos } from '@/api/api'
import Pagination from './Pagination.vue'
import { openInBrowser } from '@/utils/openUrl.js'

export default {
  name: 'UserVideos',
  components: {
    Pagination,
  },
  props: {
    mid: {
      type: [String, Number],
      required: true,
    },
  },
  setup(props) {
    const videos = ref([])
    const isLoading = ref(false)
    const currentPage = ref(1)
    const totalPages = ref(1)
    const pageSize = 30

    const fetchVideos = async () => {
      isLoading.value = true
      try {
        const response = await getUserVideos({
          mid: props.mid,
          pn: currentPage.value,
          ps: pageSize,
        })
        if (response.data.status === 'success') {
          videos.value = response.data.data.list.vlist
          totalPages.value = Math.ceil(response.data.data.page.count / pageSize)
        }
      } catch (error) {
        console.error('获取用户视频列表失败:', error)
      } finally {
        isLoading.value = false
      }
    }

    const handlePageChange = (page) => {
      currentPage.value = page
      fetchVideos()
    }

    const handleVideoClick = async (video) => {
      await openInBrowser(`https://www.bilibili.com/video/${video.bvid}`)
    }

    const formatNumber = (num) => {
      if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万'
      }
      return num.toString()
    }

    const formatTimestamp = (timestamp) => {
      const date = new Date(timestamp * 1000)
      return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      })
    }

    watch(() => props.mid, () => {
      currentPage.value = 1
      fetchVideos()
    })

    onMounted(() => {
      fetchVideos()
    })

    return {
      videos,
      isLoading,
      currentPage,
      totalPages,
      handlePageChange,
      handleVideoClick,
      formatNumber,
      formatTimestamp,
    }
  },
}
</script>
