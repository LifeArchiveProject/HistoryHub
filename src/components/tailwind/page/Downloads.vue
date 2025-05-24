<template>
  <div class="overflow-y-auto">
    <!-- 搜索框 -->
    <div class="mb-6">
      <SimpleSearchBar
        v-model="searchTerm"
        placeholder="搜索已下载的视频或目录路径..."
        @search="loadDownloadedVideos"
        class="w-full"
      />
    </div>

    <!-- 主要内容 -->
    <div>
      <!-- 下载数据加载中的占位 -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
        <svg class="animate-spin h-8 w-8 text-[#fb7299] mb-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-gray-500">加载中，请稍候...</p>
      </div>

      <!-- 没有数据时的显示 -->
      <div v-else-if="!downloads.videos || downloads.videos.length === 0" class="flex flex-col items-center justify-center py-12">
        <svg class="w-16 h-16 text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10" />
        </svg>
        <p class="text-xl font-medium text-gray-600 mb-2">暂无下载记录</p>
        <p class="text-gray-500 mb-4 text-center">
          你还没有下载任何视频，在浏览历史记录时可以点击"下载"按钮下载视频。
        </p>
      </div>

      <!-- 下载视频列表 -->
      <div v-else>
        <p class="text-sm text-gray-500 mb-4">
          共找到 {{ downloads.total }} 个下载记录，当前第 {{ downloads.page }} 页，共 {{ downloads.pages }} 页
        </p>

        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
          <div v-for="(video, index) in downloads.videos" :key="index" class="bg-white/50 backdrop-blur-sm rounded-md overflow-hidden border border-gray-200/50 hover:border-[#fb7299] hover:shadow-sm transition-all duration-200 relative group">
            <!-- 视频封面 -->
            <div class="relative pb-[56.25%] overflow-hidden cursor-pointer group" @click="handleVideoClick(video)">
              <img
                :src="video.cover || 'https://i0.hdslb.com/bfs/archive/c9e72655b7c9c9c68a30d3275313c501e68427d1.jpg'"
                :alt="video.title"
                class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                loading="lazy"
                onerror="this.src='https://i0.hdslb.com/bfs/archive/c9e72655b7c9c9c68a30d3275313c501e68427d1.jpg'"
              />

              <!-- 播放按钮覆盖 -->
              <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <button
                  v-if="video.files && video.files.length > 0 && !video.files[0].is_audio_only"
                  @click.stop="playVideo(video.files[0].file_path)"
                  class="w-8 h-8 rounded-full bg-[#fb7299]/80 text-white flex items-center justify-center backdrop-blur-sm"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </button>
              </div>

              <!-- 文件信息标签 -->
              <div class="absolute bottom-1 right-1 bg-black/60 backdrop-blur-sm px-1 py-0.5 rounded text-white text-[10px]">
                <div v-if="video.files && video.files.length > 0">
                  {{ video.files[0].size_mb.toFixed(1) }} MB
                </div>
              </div>

              <!-- 删除按钮 -->
              <div class="absolute right-1.5 top-1.5 z-20 hidden group-hover:flex items-center justify-center w-6 h-6 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop="handleDeleteVideo(video)">
                <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>

              <!-- 多文件角标 -->
              <div v-if="video.files && video.files.length > 1"
                   class="absolute left-1 top-1 rounded bg-[#fb7299] px-1 py-0.5 text-[10px] text-white">
                {{ video.files.length }}
              </div>
            </div>

            <!-- 视频信息 -->
            <div class="p-2 flex flex-col space-y-1">
              <!-- 标题 -->
              <div class="line-clamp-1 text-xs text-gray-900 font-medium cursor-pointer" @click="handleVideoClick(video)">
                {{ video.title }}
              </div>

              <!-- 作者信息 -->
              <div class="flex items-center space-x-1">
                <img
                  :src="video.author_face || 'https://i1.hdslb.com/bfs/face/1b6f746be0d0c8324e01e618c5e85e113a8b38be.jpg'"
                  :alt="video.author_name"
                  class="w-3.5 h-3.5 rounded-full object-cover cursor-pointer"
                  loading="lazy"
                  onerror="this.src='https://i1.hdslb.com/bfs/face/1b6f746be0d0c8324e01e618c5e85e113a8b38be.jpg'"
                  @click.stop="handleAuthorClick(video)"
                />
                <span class="text-[10px] text-gray-600 truncate hover:text-[#fb7299] cursor-pointer" @click.stop="handleAuthorClick(video)">
                  {{ video.author_name || '未知UP主' }}
                </span>
              </div>

              <!-- 下载时间 -->
              <div class="flex justify-between items-center text-[10px] text-gray-500">
                <div class="flex items-center space-x-1">
                  <svg class="w-2.5 h-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>{{ video.download_date }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="mt-8 flex justify-center">
          <Pagination
            :current-page="currentPage"
            :total-pages="downloads.pages"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>

    <!-- 视频播放对话框 -->
    <VideoPlayerDialog
      v-model:show="showVideoPlayer"
      :video-path="currentVideoPath"
    />

    <!-- 删除确认对话框 -->
    <Teleport to="body">
      <div v-if="showDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center">
        <!-- 遮罩层 -->
        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="showDeleteConfirm = false"></div>

        <!-- 弹窗内容 -->
        <div class="relative bg-white rounded-lg border border-gray-200 w-[500px] z-10 p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">确认删除视频</h3>

          <p class="text-gray-600 mb-4">
            确定要删除以下视频吗？此操作不可恢复。
          </p>

          <p class="font-medium text-gray-800 mb-2">{{ currentVideo?.title || '未知视频' }}</p>

          <!-- 显示CID和目录信息 -->
          <div class="mb-3 text-sm text-gray-500">
            <p v-if="currentVideo?.cid">CID: {{ currentVideo?.cid }}</p>

            <!-- 目录信息显示 -->
            <div class="mt-2">
              <p class="text-gray-600 mb-1">目录路径:</p>
              <div class="px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-gray-700 text-sm break-all">
                {{ getVideoDirectory(currentVideo) || '无法获取目录路径' }}
              </div>
            </div>
          </div>

          <!-- 删除选项 -->
          <div class="mb-4">
            <label class="flex items-center space-x-2 cursor-pointer select-none">
              <input
                type="checkbox"
                v-model="deleteDirectory"
                class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
              >
              <span>同时删除整个目录（包含所有相关文件）</span>
            </label>
          </div>

          <!-- 视频来源提示 (针对收藏夹视频) -->
          <div v-if="!currentVideo?.cid && getVideoDirectory(currentVideo)" class="mb-4 p-2 bg-amber-50 rounded-md border border-amber-200">
            <p class="text-sm text-amber-700">
              <span class="font-medium">提示：</span>
              该视频可能来自收藏夹批量下载，将使用目录路径进行删除。
            </p>
          </div>

          <!-- 按钮 -->
          <div class="flex justify-end space-x-3 mt-6">
            <button
              @click="showDeleteConfirm = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              取消
            </button>
            <button
              @click="confirmDeleteVideo"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700"
              :disabled="isDeleting || (!currentVideo?.cid && !getVideoDirectory(currentVideo))"
            >
              {{ isDeleting ? '删除中...' : '确认删除' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import Pagination from '../Pagination.vue'
import VideoPlayerDialog from '../VideoPlayerDialog.vue'
import { getDownloadedVideos, deleteDownloadedVideo } from '../../../api/api'
import axios from 'axios'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import SimpleSearchBar from '../SimpleSearchBar.vue'
import { openInBrowser } from '@/utils/openUrl.js'

// 定义组件选项
defineOptions({
  name: 'Downloads'
})

// 定义API基础URL，与api.js中保持一致
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 状态变量
const isLoading = ref(true)
const downloads = ref({
  videos: [],
  total: 0,
  page: 1,
  limit: 20,
  pages: 1
})
const searchTerm = ref('')
const currentPage = ref(1)

// 视频播放相关
const showVideoPlayer = ref(false)
const currentVideoPath = ref('')

// 删除相关
const showDeleteConfirm = ref(false)
const currentVideo = ref(null)
const deleteDirectory = ref(true)
const isDeleting = ref(false)

// 加载已下载的视频
const loadDownloadedVideos = async () => {
  try {
    isLoading.value = true
    const response = await getDownloadedVideos(searchTerm.value, currentPage.value, 20)

    if (response.data && response.data.status === 'success') {
      downloads.value = {
        videos: response.data.videos,
        total: response.data.total,
        page: response.data.page,
        limit: response.data.limit,
        pages: response.data.pages
      }
    } else {
      console.error('获取下载视频失败:', response.data?.message || '未知错误')
    }
  } catch (error) {
    console.error('请求获取下载视频列表出错:', error)
  } finally {
    isLoading.value = false
  }
}

// 处理页码变化
const handlePageChange = (page) => {
  currentPage.value = page
  loadDownloadedVideos()
}

// 播放视频
const playVideo = (filePath) => {
  // 先关闭播放器并重置路径
  showVideoPlayer.value = false
  currentVideoPath.value = ''

  // 在短暂延迟后重新设置路径并打开播放器
  setTimeout(() => {
    currentVideoPath.value = filePath
    showVideoPlayer.value = true
  }, 50)
}

// 处理删除视频
const handleDeleteVideo = (video) => {
  currentVideo.value = video
  showDeleteConfirm.value = true
  deleteDirectory.value = true
}

// 获取视频目录
const getVideoDirectory = (video) => {
  // 如果视频对象已经有目录属性，直接使用
  if (video.directory) return video.directory;

  // 否则，尝试从第一个文件路径中提取目录
  if (video.files && video.files.length > 0) {
    const filePath = video.files[0].file_path;
    if (filePath) {
      // 提取目录路径 (去掉文件名)
      const lastSlashIndex = Math.max(filePath.lastIndexOf('/'), filePath.lastIndexOf('\\'));
      if (lastSlashIndex !== -1) {
        return filePath.substring(0, lastSlashIndex);
      }
    }
  }
  return null;
}

// 提取短目录名
const getShortDirectory = (directory) => {
  if (!directory) return '';
  // 获取最后一级目录名
  const parts = directory.split(/[\/\\]/);
  const lastPart = parts[parts.length - 1];

  // 如果路径太长，截断显示
  if (directory.length > 40) {
    return '...' + directory.substring(directory.length - 40);
  }
  return directory;
}

// 确认删除视频
const confirmDeleteVideo = async () => {
  try {
    isDeleting.value = true

    // 确定目录路径
    const directory = getVideoDirectory(currentVideo.value)

    // 自动判断是否使用CID
    // 如果有CID则使用CID，否则使用目录路径
    const cid = currentVideo.value?.cid || null

    // 如果既没有CID也没有目录路径，则无法删除
    if (!cid && !directory) {
      showNotify({
        type: 'warning',
        message: '无法获取视频信息，删除失败'
      })
      isDeleting.value = false
      return
    }

    const response = await deleteDownloadedVideo(cid, deleteDirectory.value, directory)

    if (response.data && response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message
      })

      // 关闭对话框
      showDeleteConfirm.value = false

      // 重新加载列表
      await loadDownloadedVideos()
    } else {
      throw new Error(response.data?.message || '删除视频失败')
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: error.response?.data?.message || error.message || '删除视频失败'
    })
  } finally {
    isDeleting.value = false
  }
}

// 点击视频跳转到B站
const handleVideoClick = async (video) => {
  // 构建视频链接，使用bvid而不是cid
  const url = `https://www.bilibili.com/video/${video.bvid}`
  // 在系统默认浏览器中打开
  await openInBrowser(url)
}

// 点击作者头像或名称跳转到作者页面
const handleAuthorClick = async (video) => {
  if (video.author_mid) {
    const url = `https://space.bilibili.com/${video.author_mid}`
    await openInBrowser(url)
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadDownloadedVideos()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.group:hover .group-hover\:block {
  display: block;
}
</style>