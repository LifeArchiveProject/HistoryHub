<template>
  <div class="min-h-screen overflow-y-auto">
    <!-- 页面标题 -->
    <div class="bg-white/5 backdrop-blur-sm px-6 py-4 border-b border-gray-200/50">
      <div class="flex items-center justify-between">
        <h1 class="text-xl font-semibold text-gray-900">我的下载</h1>
        <div class="space-x-2">
          <div class="relative">
            <input
              type="text"
              v-model="searchTerm"
              @keyup.enter="loadDownloadedVideos"
              placeholder="搜索已下载的视频..."
              class="w-64 pr-10 pl-3 py-2 text-sm rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-[#fb7299] focus:border-transparent"
            />
            <button
              @click="loadDownloadedVideos"
              class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500 hover:text-[#fb7299]"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
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
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="(video, index) in downloads.videos" :key="index" class="bg-white rounded-lg shadow-sm border border-gray-200/50 overflow-hidden hover:shadow-md transition-shadow relative group">
            <!-- 视频信息 -->
            <div class="p-4">
              <h3 class="text-lg font-medium text-gray-900 line-clamp-2 mb-2">{{ video.title }}</h3>
              
              <div class="flex items-start space-x-2 mb-3">
                <svg class="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="text-sm text-gray-500">下载时间: {{ video.download_date }}</span>
              </div>
              
              <div class="flex items-start space-x-2 mb-3">
                <svg class="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                </svg>
                <span class="text-sm text-gray-500">CID: {{ video.cid }}</span>
              </div>
              
              <!-- 目录信息 -->
              <div v-if="video.directory" class="flex items-start space-x-2 mb-3">
                <svg class="w-5 h-5 text-gray-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                <span class="text-sm text-gray-500 truncate" :title="video.directory">目录: {{ getShortDirectory(video.directory) }}</span>
              </div>
              
              <!-- 文件列表 -->
              <div class="space-y-2 mb-4">
                <div v-for="(file, fileIndex) in video.files" :key="fileIndex" class="flex items-center justify-between text-sm">
                  <div class="flex items-center space-x-2 truncate">
                    <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path 
                        v-if="file.is_audio_only" 
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" 
                      />
                      <path 
                        v-else 
                        stroke-linecap="round" 
                        stroke-linejoin="round" 
                        stroke-width="2" 
                        d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" 
                      />
                    </svg>
                    <span class="truncate">{{ file.file_name }}</span>
                  </div>
                  <span class="text-gray-500 ml-2 flex-shrink-0">{{ file.size_mb.toFixed(1) }} MB</span>
                </div>
              </div>
              
              <!-- 删除按钮 -->
              <div class="absolute top-3 right-3 hidden group-hover:block">
                <button 
                  @click.stop="handleDeleteVideo(video)"
                  class="flex items-center justify-center p-1.5 rounded-full bg-red-100 hover:bg-red-200 text-red-600 transition-colors"
                  title="删除视频"
                >
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
              
              <!-- 操作按钮 -->
              <div class="flex space-x-2 mt-2">
                <button 
                  @click="playVideo(file.file_path)"
                  v-for="file in video.files" 
                  :key="file.file_path"
                  class="flex-1 flex items-center justify-center px-3 py-2 text-sm font-medium rounded-md text-white bg-[#fb7299] hover:bg-[#fb7299]/90 transition-colors"
                >
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ file.is_audio_only ? '播放音频' : '播放视频' }}
                </button>
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
        <div class="relative bg-white rounded-lg shadow-xl w-[450px] z-10 p-6">
          <h3 class="text-lg font-medium text-gray-900 mb-4">确认删除视频</h3>
          
          <p class="text-gray-600 mb-4">
            确定要删除以下视频吗？此操作不可恢复。
          </p>
          
          <p class="font-medium text-gray-800 mb-2">{{ currentVideo?.title }}</p>
          
          <!-- 显示CID和目录信息 -->
          <div class="mb-3 text-sm text-gray-500">
            <p>CID: {{ currentVideo?.cid }}</p>
            <p v-if="currentVideoDirectory" class="truncate mt-1">
              <span class="text-gray-600">目录: </span>
              <span :title="currentVideoDirectory">{{ getShortDirectory(currentVideoDirectory) }}</span>
            </p>
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
              :disabled="isDeleting"
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
import { showNotify } from 'vant'
import 'vant/es/notify/style'

// 定义组件选项
defineOptions({
  name: 'Downloads'
})

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

// 删除视频相关
const showDeleteConfirm = ref(false)
const currentVideo = ref(null)
const deleteDirectory = ref(true)
const isDeleting = ref(false)

// 获取当前选中视频的目录
const currentVideoDirectory = computed(() => {
  if (!currentVideo.value) return null;
  return getVideoDirectory(currentVideo.value);
})

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
  deleteDirectory.value = true // 默认勾选删除整个目录
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

// 确认删除视频
const confirmDeleteVideo = async () => {
  if (!currentVideo.value || !currentVideo.value.cid) return
  
  try {
    isDeleting.value = true
    // 获取视频目录路径
    const directory = getVideoDirectory(currentVideo.value);
    const response = await deleteDownloadedVideo(currentVideo.value.cid, deleteDirectory.value, directory)
    
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