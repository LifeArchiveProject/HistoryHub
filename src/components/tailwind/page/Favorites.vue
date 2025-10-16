<!-- 收藏夹页面 -->
<template>
  <div class="min-h-screen bg-gray-50/30 dark:bg-gray-900">
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 主内容卡片 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
          <!-- 标签导航 -->
          <div class="border-b border-gray-200 dark:border-gray-700" v-if="!showFolderContents">
            <nav class="-mb-px flex space-x-6 px-4 overflow-x-auto" aria-label="收藏夹选项卡">
              <button
                @click="activeTab = 'created'"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'created'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 13h6m-3-3v6m-9 1V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
                </svg>
                <span>我创建的收藏夹</span>
              </button>

              <button
                @click="activeTab = 'collected'"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'collected'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
                <span>我收藏的收藏夹</span>
              </button>

              <button
                @click="activeTab = 'local'"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'local'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
                </svg>
                <span>本地收藏夹</span>
              </button>
            </nav>
          </div>

          <!-- 文件夹内容标题栏 -->
          <div class="border-b border-gray-200 dark:border-gray-700" v-if="showFolderContents">
            <div class="flex items-center justify-between px-4 py-3">
              <div class="flex items-center space-x-4">
                <button
                  @click="backToFolderList"
                  class="p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <svg class="w-5 h-5 text-gray-600 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                  </svg>
                </button>
                <h2 class="text-lg font-medium truncate">{{ currentFolder?.title || '收藏夹内容' }}</h2>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  v-if="activeTab !== 'local'"
                  @click="fetchAllContents"
                  class="flex items-center px-3 py-1.5 text-xs text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-md transition-colors"
                  :disabled="fetchingAll"
                >
                  <svg class="w-3.5 h-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  <span>同步到本地</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 内容区域 -->
          <div class="transition-all duration-300 p-5">
            <!-- 全局提示信息 -->
            <div class="mb-4 p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700 rounded-md text-amber-700 dark:text-amber-300 text-sm">
              <div class="flex items-start">
                <svg class="w-5 h-5 text-amber-500 mt-0.5 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <div>
                  <p class="mt-1">用户收藏夹往往非常庞大，解析时很容易触发反爬机制。如遇该问题请稍等片刻后重试。（emmm，如果视频太多的话还是建议逐个收藏夹下载……）</p>
                </div>
              </div>
            </div>

            <!-- 收藏夹列表 -->
            <div class="animate-fadeIn" v-if="!showFolderContents">
              <!-- 收藏夹列表显示区域 -->
              <div v-if="loading" class="flex justify-center py-20">
                <div class="inline-flex items-center px-4 py-2 bg-white dark:bg-gray-800 rounded-md shadow text-gray-900 dark:text-gray-100">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>加载中...</span>
                </div>
              </div>

              <div v-else-if="favorites.length === 0" class="text-center py-20">
                <svg class="w-16 h-16 mx-auto text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
                <p class="mt-4 text-gray-500 dark:text-gray-400">暂无收藏夹</p>
                <!-- 在线收藏夹（需要登录） -->
                <template v-if="(activeTab === 'created' || activeTab === 'collected') && !isLoggedIn">
                  <p class="mt-2 text-sm text-gray-400">您需要登录B站账号才能查看收藏夹</p>
                  <button
                    @click="openLoginDialog"
                    class="mt-4 px-4 py-2 bg-[#fb7299] text-white rounded-md hover:bg-[#fb7299]/90 transition-colors"
                  >
                    登录账号
                  </button>
                </template>
                <!-- 已登录但没有收藏夹 -->
                <template v-else-if="(activeTab === 'created' || activeTab === 'collected') && isLoggedIn">
                  <p class="mt-2 text-sm text-gray-400">
                    {{ activeTab === 'created' ? '您还没有创建过收藏夹' : '您还没有收藏任何收藏夹' }}
                  </p>
                </template>
                <!-- 本地收藏夹为空 -->
                <template v-else-if="activeTab === 'local'">
                  <p class="mt-2 text-sm text-gray-400">您的本地数据库中没有保存的收藏夹</p>
                </template>
              </div>

              <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                <!-- 收藏夹卡片 -->
                <div
                  v-for="folder in favorites"
                  :key="folder.id || folder.media_id"
                  class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow border border-gray-200 dark:border-gray-700 flex flex-col"
                >
                  <!-- 封面图 -->
                  <div class="relative aspect-video bg-gray-100 dark:bg-gray-700 overflow-hidden">
                     <img
                      :src="normalizeImageUrl(folder.cover)"
                      :alt="folder.title"
                      class="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
                      @click="viewFolderContents(folder)"
                    />
                    <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-2">
                      <p class="text-white text-sm font-medium truncate">{{ folder.title }}</p>
                      <div class="flex items-center mt-1">
                        <span class="text-white/80 text-xs">{{ folder.media_count }}个内容</span>
                      </div>
                    </div>
                  </div>

                  <!-- 收藏夹信息 -->
                  <div class="p-3 flex-1 flex flex-col">
                    <div class="flex items-start justify-between">
                      <div class="flex-1">
                        <h3
                          class="font-medium text-gray-900 dark:text-gray-100 hover:text-[#fb7299] transition-colors cursor-pointer"
                          @click="viewFolderContents(folder)"
                        >
                          {{ folder.title }}
                        </h3>
                        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400 line-clamp-2">{{ folder.intro || '无简介' }}</p>
                      </div>
                    </div>

                    <div class="mt-3 pt-2 border-t border-gray-100 dark:border-gray-700 flex items-center justify-between">
                      <div class="flex items-center">
                        <img
                          :src="normalizeImageUrl(folder.upper?.face || folder.creator_face)"
                          :alt="folder.upper?.name || folder.creator_name"
                          class="w-5 h-5 rounded-full"
                        />
                        <span class="ml-1.5 text-xs text-gray-600 dark:text-gray-400">{{ folder.upper?.name || folder.creator_name }}</span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <button
                          v-if="activeTab !== 'local'"
                          @click="startDownloadFolder(folder)"
                          class="text-xs text-blue-500 hover:bg-blue-50 px-2 py-1 rounded transition-colors"
                          title="下载收藏夹中的视频"
                        >
                          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                          </svg>
                        </button>
                        <button
                          @click="viewFolderContents(folder)"
                          class="text-xs text-[#fb7299] hover:bg-[#fb7299]/10 px-2 py-1 rounded transition-colors"
                        >
                          查看详情
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 分页控件 -->
              <div v-if="favorites.length > 0 && totalPages > 1" class="mt-6 flex justify-center">
                <Pagination
                  :current-page="currentPage"
                  :total-pages="totalPages"
                  @page-change="handlePageChange"
                />
              </div>
            </div>

            <!-- 收藏夹内容 -->
            <div v-if="showFolderContents" class="animate-fadeIn">
              <div v-if="loadingContents" class="flex justify-center py-20">
                <div class="inline-flex items-center px-4 py-2 bg-white dark:bg-gray-800 rounded-md shadow text-gray-900 dark:text-gray-100">
                  <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>加载中...</span>
                </div>
              </div>

              <div v-else-if="folderContents.length === 0" class="py-10 text-center">
                <p class="text-gray-500 dark:text-gray-400">该收藏夹暂无内容</p>
              </div>

              <div v-else>
                <!-- 收藏夹操作栏 -->
                <div class="mb-4 flex flex-wrap justify-between items-center bg-white/70 dark:bg-gray-800/70 p-3 rounded-lg shadow-sm">
                  <div class="flex items-center space-x-3">
                    <div class="text-sm text-gray-700 dark:text-gray-300">共 {{ contentsTotalItems }} 个内容</div>
                    <div v-if="invalidVideosCount > 0" class="text-sm text-red-500">
                      ({{ invalidVideosCount }} 个失效)
                    </div>
                  </div>

                  <div class="flex items-center space-x-3 mt-2 sm:mt-0">
                    <button
                      v-if="activeTab !== 'local'"
                      @click="startDownloadFolder(currentFolder)"
                      class="flex items-center px-3 py-1.5 text-xs text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-md transition-colors"
                    >
                      <svg class="w-3.5 h-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                      <span>下载收藏夹</span>
                    </button>


                  </div>
                </div>

                <!-- 内容列表 - 网格布局 -->
                <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-3">
                  <div
                    v-for="item in folderContents"
                    :key="item.id || item.bvid"
                    class="bg-white/50 dark:bg-gray-800/50 rounded-md overflow-hidden border border-gray-200/50 dark:border-gray-700/50 hover:border-[#fb7299] hover:shadow-sm transition-all duration-200 relative group"
                  >
                    <!-- 视频封面 -->
                    <div class="relative pb-[56.25%] overflow-hidden cursor-pointer group" @click="openVideo(item)">


                       <img
                         :src="normalizeImageUrl(getVideoImage(item))"
                        :alt="getVideoTitle(item)"
                        class="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        loading="lazy"
                        onerror="this.src='https://i0.hdslb.com/bfs/archive/c9e72655b7c9c9c68a30d3275313c501e68427d1.jpg'"
                      />

                      <!-- 视频时长标签 -->
                      <div class="absolute bottom-1 right-1 bg-black/60 px-1 py-0.5 rounded text-white text-[10px]">
                        {{ formatDuration(item.duration) }}
                      </div>


                    </div>

                    <!-- 视频信息 -->
                    <div class="p-2 flex flex-col space-y-1">
                      <!-- 标题 -->
                      <div class="line-clamp-2 text-xs text-gray-900 dark:text-gray-100 font-medium cursor-pointer" @click="openVideo(item)">
                        {{ getVideoTitle(item) }}
                      </div>

                      <!-- 作者信息 -->
                      <div class="flex items-center space-x-1">
                        <img
                          :src="normalizeImageUrl(getAuthorFace(item))"
                          :alt="getAuthorName(item)"
                          class="w-3.5 h-3.5 rounded-full object-cover cursor-pointer"
                          loading="lazy"
                          onerror="this.src='https://i1.hdslb.com/bfs/face/1b6f746be0d0c8324e01e618c5e85e113a8b38be.jpg'"
                          @click.stop="openAuthorPage(item)"
                        />
                        <span class="text-[10px] text-gray-600 dark:text-gray-400 truncate hover:text-[#fb7299] cursor-pointer" @click.stop="openAuthorPage(item)">
                          {{ getAuthorName(item) }}
                        </span>
                      </div>

                      <!-- 收藏时间 -->
                      <div class="flex justify-between items-center text-[10px] text-gray-500">
                        <div class="flex items-center space-x-1">
                          <svg class="w-2.5 h-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          <span>收藏于: {{ formatTime(item.fav_time) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 内容分页 -->
                <div v-if="contentsTotalPages > 1" class="flex justify-center mt-6">
                  <Pagination
                    :current-page="contentsPage"
                    :total-pages="contentsTotalPages"
                    @page-change="handleContentsPageChange"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 登录弹窗 -->
    <LoginDialog
      v-model:show="showLoginDialog"
      @login-success="onLoginSuccess"
    />

    <!-- 全屏加载遮罩 -->
    <div v-if="fetchingAll" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 p-6 rounded-lg max-w-xs w-full shadow-xl text-center">
        <svg class="animate-spin h-10 w-10 text-[#fb7299] mx-auto mb-4" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">正在获取全部收藏内容</h3>
        <p class="text-gray-600 dark:text-gray-400 mb-3">请耐心等待，这可能需要一些时间</p>
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 mb-3">
          <div class="bg-[#fb7299] h-2.5 rounded-full" :style="{ width: `${fetchProgress}%` }"></div>
        </div>
        <p class="text-sm text-gray-700 dark:text-gray-300">已获取 {{ currentFetchPage }} / {{ totalFetchPages }} 页</p>
      </div>
    </div>

    <!-- 使用DownloadDialog组件 -->
    <DownloadDialog
      v-model:show="showDownloadDialog"
      :video-info="favoriteDownloadInfo"
      @download-complete="handleDownloadComplete"
    />


  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'
import Pagination from '../Pagination.vue'
import LoginDialog from '../LoginDialog.vue'
import DownloadDialog from '../DownloadDialog.vue'
import {
  getCreatedFavoriteFolders,
  getCollectedFavoriteFolders,
  getLocalFavoriteFolders,
  getFavoriteContents,
  getLocalFavoriteContents,
  getLoginStatus
} from '@/api/api.js'
import { openInBrowser } from '@/utils/openUrl.js'
import { normalizeImageUrl } from '@/utils/imageUrl.js'

const router = useRouter()

// 状态变量
const loading = ref(false)
const favorites = ref([])
const activeTab = ref('created')
const currentPage = ref(1)
const pageSize = ref(40)
const totalItems = ref(0)
const searchKeyword = ref('')

// 收藏夹内容状态
const showFolderContents = ref(false)
const currentFolder = ref(null)
const folderContents = ref([])
const loadingContents = ref(false)
const contentsPage = ref(1)
const contentsPageSize = ref(40)
const contentsTotalItems = ref(0)

// 登录弹窗状态
const showLoginDialog = ref(false)

// 已移除修复功能相关弹窗

// 登录状态
const isLoggedIn = ref(false)
const checkingLoginStatus = ref(false)

// 获取全部收藏夹内容相关状态
const fetchingAll = ref(false)
const currentFetchPage = ref(0)
const totalFetchPages = ref(0)
const fetchProgress = ref(0)
const allFetchedContents = ref([])

// 已移除修复状态与结果

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(totalItems.value / pageSize.value)
})

// 计算内容总页数
const contentsTotalPages = computed(() => {
  return Math.ceil(contentsTotalItems.value / contentsPageSize.value)
})

// 监听活动标签变化
watch(activeTab, () => {
  currentPage.value = 1
  fetchFavorites()
})

// 组件挂载时加载数据
onMounted(() => {
  checkLoginStatus()
  fetchFavorites()

  // 添加全局登录状态变化的监听
  window.addEventListener('login-status-changed', handleLoginStatusChange)
})

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('login-status-changed', handleLoginStatusChange)
})

// 处理登录状态变化事件
function handleLoginStatusChange(event) {
  console.log('收藏页面收到登录状态变化事件:', event.detail)
  if (event.detail && typeof event.detail.isLoggedIn !== 'undefined') {
    isLoggedIn.value = event.detail.isLoggedIn
    if (isLoggedIn.value) {
      // 如果登录状态变为已登录，重新获取收藏夹
      fetchFavorites()
    }
  } else {
    // 如果事件没有包含登录状态信息，则重新检查
    checkLoginStatus()
  }
}

// 检查登录状态
async function checkLoginStatus() {
  checkingLoginStatus.value = true
  try {
    const response = await getLoginStatus()
    console.log('获取登录状态响应:', response.data)
    if (response.data && response.data.code === 0) {
      isLoggedIn.value = response.data.data.isLogin
      console.log('登录状态:', isLoggedIn.value)
    } else {
      console.warn('登录状态响应异常:', response.data)
      isLoggedIn.value = false
    }
  } catch (error) {
    console.error('获取登录状态失败:', error)
    isLoggedIn.value = false
  } finally {
    checkingLoginStatus.value = false
  }
}

// 获取收藏夹列表
async function fetchFavorites() {
  loading.value = true
  favorites.value = []

  try {
    let response

    if (activeTab.value === 'created') {
      response = await getCreatedFavoriteFolders({
        keyword: searchKeyword.value || undefined
      })
    } else if (activeTab.value === 'collected') {
      response = await getCollectedFavoriteFolders({
        pn: currentPage.value,
        ps: pageSize.value,
        keyword: searchKeyword.value || undefined
      })
    } else if (activeTab.value === 'local') {
      response = await getLocalFavoriteFolders({
        page: currentPage.value,
        size: pageSize.value
      })
    }

    if (response.data.status === 'success') {
      if (activeTab.value === 'created') {
        favorites.value = response.data.data.list || []
        totalItems.value = response.data.data.count || 0
      } else if (activeTab.value === 'collected') {
        favorites.value = response.data.data.list || []
        totalItems.value = response.data.data.count || 0
      } else if (activeTab.value === 'local') {
        favorites.value = response.data.data.list || []
        totalItems.value = response.data.data.total || 0
      }

      // 如果收藏夹没有封面，使用第一个视频的封面
      for (const folder of favorites.value) {
        if (!folder.cover || folder.cover.includes('nocover')) {
          // 预加载第一个视频的封面
          preloadFirstVideoCover(folder)
        }
      }
    } else {
      showNotify({ type: 'danger', message: response.data.message || '获取收藏夹失败' })
    }
  } catch (error) {
    console.error('获取收藏夹出错:', error)
    showNotify({ type: 'danger', message: '获取收藏夹出错: ' + (error.message || '未知错误') })
  } finally {
    loading.value = false
  }
}

// 预加载收藏夹的第一个视频封面
async function preloadFirstVideoCover(folder) {
  try {
    const folderId = folder.id || folder.media_id
    if (!folderId) return

    let response
    if (activeTab.value === 'local') {
      response = await getLocalFavoriteContents({
        media_id: folderId,
        page: 1,
        size: 1
      })
    } else {
      // 对于线上收藏夹，直接获取收藏夹详细信息
      response = await getFavoriteContents({
        media_id: folderId,
        pn: 1,
        ps: 1
      })

      // 从响应中获取收藏夹详细信息
      if (response.data.status === 'success' && response.data.data && response.data.data.info) {
        // 更新收藏夹信息
        const info = response.data.data.info
        folder.title = info.title || folder.title
        folder.cover = info.cover || folder.cover
        folder.intro = info.intro || folder.intro
        folder.media_count = info.media_count || folder.media_count

        // 更新UP主信息
        if (info.upper) {
          folder.upper = info.upper
        }

        // 获取到了详细信息，无需继续处理
        return
      }
    }

    // 如果没有获取到详细信息或是本地收藏夹，则使用第一个视频的封面
    if (response.data.status === 'success') {
      let contents = []
      if (activeTab.value === 'local') {
        contents = response.data.data.list || []
      } else if (response.data.data && response.data.data.medias) {
        contents = response.data.data.medias || []
      } else if (response.data.data && Array.isArray(response.data.data)) {
        contents = response.data.data
      }

      if (contents.length > 0 && contents[0].cover) {
        folder.cover = contents[0].cover
      }
    }
  } catch (error) {
    console.error('获取封面出错:', error)
  }
}

// 查看收藏夹内容
async function viewFolderContents(folder) {
  currentFolder.value = folder
  showFolderContents.value = true
  contentsPage.value = 1
  folderContents.value = []

  // 先加载内容
  const contents = await loadContents()
  console.log(`收藏夹[${folder.media_id || folder.id}]加载完成，共${contents.length}个视频`)
}

// 返回到收藏夹列表
function backToFolderList() {
  showFolderContents.value = false
  currentFolder.value = null
  folderContents.value = []
}

// 加载收藏夹内容
async function loadContents() {
  if (!currentFolder.value) return

  loadingContents.value = true
  folderContents.value = []

  try {
    let response
    // 确保使用正确的收藏夹ID
    const folderId = currentFolder.value.media_id || currentFolder.value.id

    console.log(`开始加载收藏夹[${folderId}]第${contentsPage.value}页内容`)

    if (activeTab.value === 'local') {
      response = await getLocalFavoriteContents({
        media_id: folderId,
        page: contentsPage.value,
        size: contentsPageSize.value
      })

      if (response.data.status === 'success') {
        folderContents.value = response.data.data.list || []
        contentsTotalItems.value = response.data.data.total || 0
        console.log(`加载到本地收藏夹内容 ${folderContents.value.length} 条`)
      } else {
        console.error('本地收藏夹请求失败:', response.data)
        showNotify({ type: 'danger', message: response.data.message || '获取本地收藏夹内容失败' })
      }
    } else {
      console.log('发送在线收藏夹请求:', {
        media_id: folderId,
        pn: contentsPage.value,
        ps: contentsPageSize.value
      })

      response = await getFavoriteContents({
        media_id: folderId,
        pn: contentsPage.value,
        ps: contentsPageSize.value,
        keyword: searchKeyword.value || undefined
      })

      console.log('收到在线收藏夹响应:', response.data)

      if (response.data.status === 'success') {
        // 更新收藏夹信息
        if (response.data.data && response.data.data.info) {
          const info = response.data.data.info
          // 更新当前展示的收藏夹信息
          currentFolder.value.title = info.title || currentFolder.value.title
          currentFolder.value.cover = info.cover || currentFolder.value.cover
          currentFolder.value.intro = info.intro || currentFolder.value.intro
          currentFolder.value.media_count = info.media_count || currentFolder.value.media_count

          // 更新UP主信息
          if (info.upper) {
            currentFolder.value.upper = info.upper
          }
        }

        // 确保我们能够正确处理不同的数据结构
        if (response.data.data && response.data.data.medias) {
          console.log('找到媒体数据，数量:', response.data.data.medias.length)
          folderContents.value = response.data.data.medias
          contentsTotalItems.value = currentFolder.value.media_count || 0
        } else if (response.data.data && Array.isArray(response.data.data)) {
          console.log('找到数组数据，数量:', response.data.data.length)
          folderContents.value = response.data.data
          contentsTotalItems.value = response.data.total || currentFolder.value.media_count || 0
        } else {
          console.warn('收藏夹内容数据结构异常:', response.data)
          folderContents.value = []
          showNotify({ type: 'warning', message: '收藏夹数据结构异常，无法显示内容' })
        }

        // 确保至少更新了folderContents
        if (folderContents.value.length === 0) {
          console.warn('无法从响应中提取内容数据')
          showNotify({ type: 'warning', message: '无法从响应中提取内容数据' })
        }
      } else {
        console.error('在线收藏夹请求失败:', response.data)
        showNotify({ type: 'danger', message: response.data.message || '获取收藏夹内容失败' })
      }
    }


  } catch (error) {
    console.error('获取收藏夹内容出错:', error)
    showNotify({ type: 'danger', message: '获取收藏夹内容出错: ' + (error.message || '未知错误') })
  } finally {
    loadingContents.value = false
  }

  // 返回加载的内容，便于调用者使用
  return folderContents.value
}

// 打开视频
async function openVideo(video) {
  // 使用BV号或视频ID打开视频，跳转到B站
  const videoId = video.bvid || video.id
  if (videoId) {
    // 在系统默认浏览器中打开B站视频链接
    await openInBrowser(`https://www.bilibili.com/video/${videoId}`)
  }
}

// 处理搜索
// 处理分页变化
function handlePageChange(page) {
  currentPage.value = page
  fetchFavorites()
}

// 处理内容分页变化
async function handleContentsPageChange(page) {
  console.log(`切换到第${page}页内容`)
  contentsPage.value = page

  try {
    // 等待内容加载完成
    await loadContents()

  } catch (error) {
    console.error('分页处理出错:', error)
    showNotify({
      type: 'danger',
      message: '分页处理出错: ' + (error.message || '未知错误')
    })
  }
}

// 打开登录对话框
function openLoginDialog() {
  showLoginDialog.value = true
}

// 登录成功回调
function onLoginSuccess() {
  isLoggedIn.value = true
  showNotify({ type: 'success', message: '登录成功，正在获取收藏夹数据' })
  fetchFavorites()
}

// 格式化时间戳为可读格式
function formatTime(timestamp) {
  if (!timestamp) return '未知'

  const date = new Date(timestamp * 1000)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 格式化视频时长
function formatDuration(seconds) {
  if (!seconds) return '00:00'

  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60

  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 获取作者头像
function getAuthorFace(item) {
  // 首先检查upper对象
  if (item.upper && item.upper.face) {
    return item.upper.face
  }
  // 然后检查creator_face属性（本地数据结构）
  else if (item.creator_face) {
    return item.creator_face
  }
  // 再检查upper_mid关联的信息（本地数据可能有的另一种形式）
  else if (item.upper_mid && typeof item.upper_mid === 'number') {
    // 如果只有mid而没有头像，返回默认头像
    return 'https://i1.hdslb.com/bfs/face/1b6f746be0d0c8324e01e618c5e85e113a8b38be.jpg'
  }
  // 最后返回默认头像
  else {
    return 'https://i1.hdslb.com/bfs/face/1b6f746be0d0c8324e01e618c5e85e113a8b38be.jpg'
  }
}

// 获取作者名称
function getAuthorName(item) {
  // 首先检查upper对象
  if (item.upper && item.upper.name) {
    return item.upper.name
  }
  // 然后检查creator_name属性（本地数据结构）
  else if (item.creator_name) {
    return item.creator_name
  }
  // 最后返回默认名称
  else {
    return '未知UP主'
  }
}

// 获取视频是否有修复信息
// 已移除修复信息获取逻辑

// 获取全部收藏夹内容的函数，每页请求间隔1秒
async function fetchAllContents() {
  if (!currentFolder.value || fetchingAll.value) return

  fetchingAll.value = true
  allFetchedContents.value = []

  try {
    // 获取收藏夹信息以确定总页数
    const folderId = currentFolder.value.media_id || currentFolder.value.id
    let firstPageResponse
    let fetchApi
    let processResponse

    console.log('开始获取全部收藏内容，收藏夹ID:', folderId, '每页大小:', contentsPageSize.value)

    if (activeTab.value === 'local') {
      fetchApi = (page) => getLocalFavoriteContents({
        media_id: folderId,
        page: page,
        size: contentsPageSize.value
      })

      processResponse = (response, page) => {
        console.log(`处理本地收藏夹第${page}页响应:`, response.data)
        if (response.data.status === 'success') {
          return {
            contents: response.data.data.list || [],
            total: response.data.data.total || 0
          }
        }
        return { contents: [], total: 0 }
      }
    } else {
      fetchApi = (page) => {
        console.log(`请求在线收藏夹第${page}页, 参数:`, {
          media_id: folderId,
          pn: page,
          ps: contentsPageSize.value
        })
        return getFavoriteContents({
          media_id: folderId,
          pn: page,
          ps: contentsPageSize.value
        })
      }

      processResponse = (response, page) => {
        console.log(`处理在线收藏夹第${page}页响应:`, response.data)
        if (response.data.status === 'success') {
          // 更新收藏夹信息
          if (response.data.data && response.data.data.info && page === 1) {
            const info = response.data.data.info
            currentFolder.value.title = info.title || currentFolder.value.title
            currentFolder.value.cover = info.cover || currentFolder.value.cover
            currentFolder.value.intro = info.intro || currentFolder.value.intro
            currentFolder.value.media_count = info.media_count || currentFolder.value.media_count

            if (info.upper) {
              currentFolder.value.upper = info.upper
            }
          }

          // 处理多种可能的数据结构
          if (response.data.data && response.data.data.medias) {
            console.log(`第${page}页: 找到媒体数据，数量:`, response.data.data.medias.length)
            return {
              contents: response.data.data.medias,
              total: currentFolder.value.media_count || 0
            }
          } else if (response.data.data && Array.isArray(response.data.data)) {
            console.log(`第${page}页: 找到数组数据，数量:`, response.data.data.length)
            return {
              contents: response.data.data,
              total: response.data.total || currentFolder.value.media_count || 0
            }
          } else {
            console.warn(`第${page}页: 数据结构异常:`, response.data)
            return { contents: [], total: currentFolder.value.media_count || 0 }
          }
        }
        console.error(`第${page}页: 请求失败:`, response.data)
        return { contents: [], total: 0 }
      }
    }

    // 第一页请求，获取总数量信息
    console.log('获取第1页数据...')
    firstPageResponse = await fetchApi(1)
    const result = processResponse(firstPageResponse, 1)
    const total = result.total

    console.log('首页数据获取完成，总数据条目:', total)

    // 计算总页数
    totalFetchPages.value = Math.ceil(total / contentsPageSize.value)
    console.log('计算出总页数:', totalFetchPages.value)

    currentFetchPage.value = 1
    fetchProgress.value = (1 / totalFetchPages.value) * 100

    // 添加第一页数据
    allFetchedContents.value = [...allFetchedContents.value, ...result.contents]

    // 如果只有一页，则完成
    if (totalFetchPages.value <= 1) {
      showNotify({ type: 'success', message: '收藏夹内容获取完成！' })
      fetchingAll.value = false
      folderContents.value = allFetchedContents.value
      return
    }

    // 依次请求后续页面
    for (let page = 2; page <= totalFetchPages.value; page++) {
      console.log(`等待1秒后获取第${page}页数据...`)
      // 等待1秒
      await new Promise(resolve => setTimeout(resolve, 1000))

      try {
        console.log(`开始获取第${page}页数据`)
        const response = await fetchApi(page)
        const pageResult = processResponse(response, page)

        // 添加本页数据
        allFetchedContents.value = [...allFetchedContents.value, ...pageResult.contents]

        // 更新进度
        currentFetchPage.value = page
        fetchProgress.value = (page / totalFetchPages.value) * 100
        console.log(`第${page}页数据获取完成，当前进度: ${fetchProgress.value.toFixed(2)}%`)
      } catch (error) {
        console.error(`获取第${page}页出错:`, error)
        showNotify({ type: 'warning', message: `获取第${page}页出错，将继续获取下一页: ${error.message}` })
      }
    }

    // 完成后更新数据并通知
    folderContents.value = allFetchedContents.value
    console.log('所有页面获取完成，总共获取到', allFetchedContents.value.length, '条内容')
    showNotify({
      type: 'success',
      message: `已获取全部${allFetchedContents.value.length}个收藏内容！`
    })
  } catch (error) {
    console.error('获取全部收藏夹内容出错:', error)
    showNotify({ type: 'danger', message: '获取收藏夹内容出错: ' + (error.message || '未知错误') })
  } finally {
    fetchingAll.value = false
  }
}

// 获取视频封面，优先使用修复后的封面
function getVideoImage(video) {
  // 检查video对象是否存在
  if (!video) return ''

  console.log('获取视频封面:', video.bvid || video.avid)



  // 返回原始封面
  return video.cover || ''
}

// 获取视频标题，优先使用修复后的标题
function getVideoTitle(video) {
  // 检查video对象是否存在
  if (!video) return '未知标题'

  console.log('获取视频标题:', video.bvid || video.avid)



  // 返回原始标题
  return video.title || '未知标题'
}

// 判断视频是否正在修复
// 已移除修复中状态判断

// 打开UP主页面
function openAuthorPage(video) {
  let upId = null;

// 已移除从修复结果提取UP主ID逻辑

  // 然后检查视频本身的数据
  if (!upId && video.upper_mid) {
    upId = video.upper_mid
  } else if (!upId && video.upper && video.upper.mid) {
    upId = video.upper.mid
  }

  // 如果找到UP主ID，跳转到B站UP主页面
  if (upId) {
    window.open(`https://space.bilibili.com/${upId}`, '_blank')
  } else {
    showNotify({ type: 'warning', message: '无法获取UP主信息' })
  }
}

// 下载相关状态
const showDownloadDialog = ref(false)
const favoriteDownloadInfo = ref({
  title: '',
  author: '',
  bvid: '',
  cover: '',
  cid: 0
})

// 计算无效视频数量
const invalidVideosCount = computed(() => 0)

// 开始下载收藏夹
async function startDownloadFolder(folder) {
  if (!folder) return;

  // 检查登录状态
  if (!isLoggedIn.value) {
    showNotify({ type: 'warning', message: '请先登录B站账号' });
    showLoginDialog.value = true;
    return;
  }

  // 获取完整的收藏夹视频总数
  try {
    // 发起一次API请求获取视频总数，仅获取第一页第一条
    const response = await getFavoriteContents({
      media_id: folder.id || folder.media_id,
      pn: 1,
      ps: 1
    });

    if (response.data && response.data.status === 'success' && response.data.data) {
      // 更新收藏夹信息
      if (response.data.data.info) {
        folder.media_count = response.data.data.info.media_count || response.data.data.total || folder.media_count;
      } else if (response.data.data.total) {
        folder.media_count = response.data.data.total;
      }

      console.log(`获取到收藏夹[${folder.title}]视频总数: ${folder.media_count}`);
    }
  } catch (error) {
    console.error('获取收藏夹信息失败:', error);
  }

  // 设置要下载的收藏夹信息
  favoriteDownloadInfo.value = {
    title: `收藏夹: ${folder.title || '未命名收藏夹'}`,
    author: folder.upper?.name || folder.creator_name || '未知创建者',
    bvid: `fid_${(folder.id || folder.media_id || '').toString()}`,  // 使用特殊格式标识这是收藏夹ID
    cover: folder.cover || '',
    cid: 0,
    // 添加额外信息供下载组件使用
    is_favorite_folder: true,
    user_id: (folder.mid || folder.creator_mid || '').toString(),
    fid: (folder.id || folder.media_id || '').toString(),
    // 添加视频总数信息，帮助下载对话框显示正确的总数
    total_videos: folder.media_count || 0
  };

  // 打开下载对话框
  showDownloadDialog.value = true;
}

// 处理下载完成
function handleDownloadComplete() {
  showNotify({ type: 'success', message: '收藏夹下载完成' });
}
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
