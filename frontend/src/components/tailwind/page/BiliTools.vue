<template>
  <div class="min-h-screen bg-gray-50/30 dark:bg-gray-900">
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 主内容卡片 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
          <!-- 标签导航 -->
          <div class="border-b border-gray-200 dark:border-gray-700">
            <nav class="-mb-px flex px-6 overflow-x-auto" aria-label="B站工具选项卡">
              <button
                @click="activeTab = 'video-download'"
                class="py-4 px-3 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'video-download'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                <span>视频下载</span>
              </button>

              <button
                @click="activeTab = 'comment-query'"
                class="ml-8 py-4 px-3 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'comment-query'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <span>评论查询</span>
              </button>
            </nav>
          </div>

          <!-- 内容区域 -->
          <div class="transition-all duration-300">
            <!-- 视频下载 -->
            <div v-if="activeTab === 'video-download'" class="animate-fadeIn">
              <VideoDownloader />
            </div>

            <!-- 评论查询 -->
            <div v-if="activeTab === 'comment-query'" class="animate-fadeIn">
              <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <!-- 用户ID输入区域 -->
                <div class="mb-6 bg-transparent">
                  <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-3">B站评论查询</h2>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    输入B站用户UID，查询该用户的全部评论记录。
                  </p>

                  <div class="flex space-x-3">
                    <div class="flex-1">
                      <div class="relative">
                        <input
                          v-model="queryUserId"
                          type="text"
                          placeholder="输入用户UID，例如：12345678"
                          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-transparent text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#fb7299] focus:border-transparent pr-10"
                          @keyup.enter="fetchUserComments()"
                        />
                        <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                          <svg v-if="commentLoading" class="animate-spin h-5 w-5 text-[#fb7299]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <button
                            v-else
                            @click="fetchUserComments()"
                            class="text-[#fb7299] hover:text-[#fb7299]/80 transition-colors"
                          >
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 筛选区域 -->
                <div v-if="comments.length > 0 || commentLoading" class="mb-6 bg-transparent">
                  <div class="mb-4">
                    <!-- 总评论数显示 -->
                    <div class="mb-3 flex items-center text-sm text-gray-600">
                      <span>共</span>
                      <span class="mx-1 text-[#fb7299] font-medium">{{ commentTotal }}</span>
                      <span>条评论</span>
                    </div>

                    <div class="flex flex-nowrap items-center space-x-2">
                      <!-- 关键词搜索 -->
                      <div class="flex-1 min-w-0">
                        <div class="relative">
                          <div class="flex h-9 items-center rounded-md border border-gray-300 dark:border-gray-600 bg-transparent focus-within:border-[#fb7299] transition-colors duration-200">
                            <!-- 搜索图标 -->
                            <div class="pl-3 text-gray-400">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                              </svg>
                            </div>

                            <!-- 输入框 -->
                            <input
                              v-model="commentKeyword"
                              type="search"
                              placeholder="搜索评论内容..."
                              class="h-full w-full border-none bg-transparent px-2 pr-3 text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-0 text-xs leading-none"
                              @keyup.enter="handleCommentSearch"
                            />
                          </div>
                        </div>
                      </div>

                      <!-- 评论类型筛选 -->
                      <div class="w-24 flex-shrink-0">
                        <div class="relative">
                          <button
                            @click="toggleCommentTypeDropdown"
                            type="button"
                            class="w-full py-1.5 px-2 border border-gray-300 dark:border-gray-600 rounded-md text-xs text-gray-800 dark:text-gray-200 bg-transparent focus:border-[#fb7299] focus:outline-none focus:ring focus:ring-[#fb7299]/20 flex items-center justify-between transition-colors duration-200 h-9 whitespace-nowrap overflow-hidden"
                          >
                            <span class="truncate mr-1">{{ getCommentTypeText(commentType) }}</span>
                            <svg class="w-3 h-3 text-[#fb7299] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                          </button>

                          <!-- 评论类型下拉菜单 -->
                          <div
                            v-if="showCommentTypeDropdown"
                            class="absolute z-10 mt-1 w-full rounded-md bg-white dark:bg-gray-800 shadow-lg ring-1 ring-black ring-opacity-5 dark:ring-white/10 focus:outline-none"
                          >
                            <div class="py-1">
                              <button
                                v-for="option in commentTypeOptions"
                                :key="option.value"
                                @click="selectCommentType(option.value)"
                                class="w-full px-2 py-1 text-xs text-left hover:bg-[#fb7299]/5 hover:text-[#fb7299] transition-colors flex items-center whitespace-nowrap"
                                :class="{'text-[#fb7299] bg-[#fb7299]/5 font-medium': commentType === option.value}"
                              >
                                {{ option.label }}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- 内容类型筛选 -->
                      <div class="w-24 flex-shrink-0">
                        <div class="relative">
                          <button
                            @click="toggleContentTypeDropdown"
                            type="button"
                            class="w-full py-1.5 px-2 border border-gray-300 dark:border-gray-600 rounded-md text-xs text-gray-800 dark:text-gray-200 bg-transparent focus:border-[#fb7299] focus:outline-none focus:ring focus:ring-[#fb7299]/20 flex items-center justify-between transition-colors duration-200 h-9 whitespace-nowrap overflow-hidden"
                          >
                            <span class="truncate mr-1">{{ getContentTypeText(contentTypeFilter) }}</span>
                            <svg class="w-3 h-3 text-[#fb7299] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                          </button>

                          <!-- 内容类型下拉菜单 -->
                          <div
                            v-if="showContentTypeDropdown"
                            class="absolute z-10 mt-1 w-full rounded-md bg-white dark:bg-gray-800 shadow-lg ring-1 ring-black ring-opacity-5 dark:ring-white/10 focus:outline-none"
                          >
                            <div class="py-1">
                              <button
                                v-for="option in contentTypeOptions"
                                :key="option.value"
                                @click="selectContentType(option.value)"
                                class="w-full px-2 py-1 text-xs text-left hover:bg-[#fb7299]/5 hover:text-[#fb7299] transition-colors flex items-center whitespace-nowrap"
                                :class="{'text-[#fb7299] bg-[#fb7299]/5 font-medium': contentTypeFilter === option.value}"
                              >
                                {{ option.label }}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 评论列表 -->
                <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
                  <!-- 评论项 -->
                  <div v-if="!commentLoading && comments.length > 0" class="divide-y divide-gray-100">
                    <div v-for="comment in comments" :key="comment.rpid" class="p-4 md:p-6">
                      <div class="space-y-2">
                        <!-- 评论内容 -->
                        <p class="text-gray-800 text-sm md:text-base whitespace-pre-wrap leading-relaxed">{{ comment.message }}</p>

                        <!-- 评论元数据 -->
                        <div class="flex items-center justify-between text-xs text-gray-500">
                          <div class="flex items-center space-x-3">
                            <span :class="comment.type === 1 ? 'text-[#fb7299]' : 'text-[#fb7299]'">
                              {{ getCommentTypeDisplay(comment.type) }}
                            </span>
                            <span>{{ comment.time_str }}</span>
                          </div>

                          <a
                            :href="getCommentLink(comment)"
                            target="_blank"
                            class="text-[#fb7299] hover:text-[#fb7299]/80 transition-colors"
                          >
                            查看原文 →
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 加载状态 -->
                  <div v-if="commentLoading" class="flex justify-center items-center py-16">
                    <div class="flex flex-col items-center">
                      <div class="animate-spin h-8 w-8 border-3 border-[#fb7299] border-t-transparent rounded-full"></div>
                      <p class="text-gray-500 text-sm mt-4">加载评论中...</p>
                    </div>
                  </div>

                  <!-- 空状态 -->
                  <div v-if="!commentLoading && comments.length === 0" class="flex justify-center items-center py-16">
                    <div class="flex flex-col items-center">
                      <div class="bg-[#fb7299]/5 rounded-full p-3 mb-3">
                        <svg class="w-8 h-8 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                        </svg>
                      </div>
                      <p class="text-gray-600 dark:text-gray-300 font-medium">暂无评论数据</p>
                      <p v-if="hasActiveCommentFilters" class="text-gray-500 dark:text-gray-400 text-sm mt-1 text-center max-w-sm">
                        尝试调整搜索条件
                      </p>
                      <button
                        v-if="hasActiveCommentFilters"
                        @click="clearCommentFilters"
                        class="mt-4 px-4 py-2 text-white bg-[#fb7299] hover:bg-[#fb7299]/90 rounded-md text-sm transition-colors"
                      >
                        清除筛选
                      </button>
                    </div>
                  </div>
                </div>

                <!-- 分页控件 -->
                <div v-if="commentTotalPages > 0" class="mt-6 flex justify-center">
                  <div class="mx-auto mb-5 mt-8 max-w-4xl lm:text-xs">
                    <div class="flex justify-between items-center space-x-4 lm:mx-5">
                      <button
                        @click="handleCommentPageChange(commentCurrentPage - 1)"
                        :disabled="commentCurrentPage === 1"
                        class="flex items-center text-gray-500 hover:text-[#fb7299] disabled:opacity-40 disabled:cursor-not-allowed transition-colors px-3 py-2"
                      >
                        <svg class="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                        </svg>
                        <span class="hidden sm:inline">上一页</span>
                      </button>

                      <div class="flex items-center text-gray-700 lm:text-xs">
                        <div class="relative mx-1 inline-block">
                          <input
                            type="number"
                            v-model="commentPageInput"
                            @keyup.enter="handleCommentJumpPage"
                            @blur="handleCommentJumpPage"
                            @focus="$event.target.select()"
                            min="1"
                            :max="commentTotalPages"
                            class="h-8 w-12 rounded border border-gray-200 dark:border-gray-600 px-2 text-center text-gray-700 dark:text-gray-200 bg-transparent transition-colors [appearance:textfield] hover:border-[#fb7299] focus:border-[#fb7299] focus:outline-none focus:ring-1 focus:ring-[#fb7299]/30 lm:h-6 lm:w-10 lm:text-xs [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                          />
                        </div>
                        <span class="text-gray-500 mx-1">/ {{ commentTotalPages }}</span>
                      </div>

                      <button
                        @click="handleCommentPageChange(commentCurrentPage + 1)"
                        :disabled="commentCurrentPage === commentTotalPages"
                        class="flex items-center text-gray-500 hover:text-[#fb7299] disabled:opacity-40 disabled:cursor-not-allowed transition-colors px-3 py-2"
                      >
                        <span class="hidden sm:inline">下一页</span>
                        <svg class="w-5 h-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import VideoDownloader from './VideoDownloader.vue'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import { getComments } from '../../../api/api'

const route = useRoute()

// 当前激活的标签
const activeTab = ref('video-download')

// 监听路由变化以更新激活的标签
watch(
  () => route.query.tab,
  (tab) => {
    if (tab && ['video-download', 'comment-query'].includes(tab)) {
      activeTab.value = tab
    }
  },
  { immediate: true }
)

// 组件挂载时根据URL初始化标签
onMounted(() => {
  const { tab } = route.query
  if (tab && ['video-download', 'comment-query'].includes(tab)) {
    activeTab.value = tab
  }
})

// 评论查询数据
const queryUserId = ref('')
const comments = ref([])
const commentLoading = ref(false)
const commentCurrentPage = ref(1)
const commentPageSize = ref(20)
const commentTotal = ref(0)
const commentTotalPages = ref(0)
const commentKeyword = ref('')
const commentType = ref('all')
const contentTypeFilter = ref('0')
const commentPageInput = ref('1')

// 下拉菜单状态
const showCommentTypeDropdown = ref(false)
const showContentTypeDropdown = ref(false)

// 下拉菜单选项数据
const commentTypeOptions = [
  { value: 'all', label: '全部' },
  { value: 'root', label: '一级' },
  { value: 'reply', label: '二级' }
]

const contentTypeOptions = [
  { value: '0', label: '全部' },
  { value: '1', label: '视频' },
  { value: '17', label: '动态' },
  { value: '11', label: '旧动态' }
]

// 是否有活跃的评论筛选条件
const hasActiveCommentFilters = computed(() => {
  return commentKeyword.value !== '' || commentType.value !== 'all' || contentTypeFilter.value !== '0'
})

// 获取评论类型显示文本
const getCommentTypeText = (type) => {
  const option = commentTypeOptions.find(opt => opt.value === type)
  return option ? option.label : '全部'
}

// 获取内容类型显示文本
const getContentTypeText = (type) => {
  const option = contentTypeOptions.find(opt => opt.value === type)
  return option ? option.label : '全部'
}

// 获取评论类型显示文本（单个评论）
const getCommentTypeDisplay = (type) => {
  switch (type) {
    case 1:
      return '视频评论'
    case 11:
    case 17:
      return '动态评论'
    default:
      return '其他评论'
  }
}

// 获取评论链接
const getCommentLink = (comment) => {
  const { type, oid, rpid } = comment

  switch (type) {
    case 1: // 视频评论
      return `https://www.bilibili.com/video/av${oid}#reply${rpid}`
    case 11: // 动态评论类型11
      return `https://t.bilibili.com/${oid}?type=2#reply${rpid}`
    case 17: // 动态评论类型17
      return `https://t.bilibili.com/${oid}#reply${rpid}`
    default:
      return '#'
  }
}

// 切换评论类型下拉菜单
const toggleCommentTypeDropdown = () => {
  showCommentTypeDropdown.value = !showCommentTypeDropdown.value
  showContentTypeDropdown.value = false
}

// 切换内容类型下拉菜单
const toggleContentTypeDropdown = () => {
  showContentTypeDropdown.value = !showContentTypeDropdown.value
  showCommentTypeDropdown.value = false
}

// 选择评论类型
const selectCommentType = (value) => {
  commentType.value = value
  showCommentTypeDropdown.value = false
  commentCurrentPage.value = 1
  fetchUserComments()
}

// 选择内容类型
const selectContentType = (value) => {
  contentTypeFilter.value = value
  showContentTypeDropdown.value = false
  commentCurrentPage.value = 1
  fetchUserComments()
}

// 获取用户评论列表
const fetchUserComments = async () => {
  if (!queryUserId.value) {
    showNotify({
      type: 'warning',
      message: '请输入用户UID'
    })
    return
  }

  commentLoading.value = true

  try {
    const response = await getComments(
      queryUserId.value,
      commentCurrentPage.value,
      commentPageSize.value,
      commentType.value,
      commentKeyword.value,
      contentTypeFilter.value
    )

    if (response.data) {
      comments.value = response.data.comments || []
      commentTotal.value = response.data.total || 0
      commentTotalPages.value = response.data.total_pages || 0
      commentPageInput.value = commentCurrentPage.value.toString()
    }
  } catch (error) {
    console.error('获取评论列表失败:', error)
    showNotify({
      type: 'danger',
      message: error.response?.data?.message || '获取评论列表失败'
    })
    comments.value = []
    commentTotal.value = 0
    commentTotalPages.value = 0
  } finally {
    commentLoading.value = false
  }
}

// 处理评论搜索
const handleCommentSearch = () => {
  commentCurrentPage.value = 1
  fetchUserComments()
}

// 处理评论页码变化
const handleCommentPageChange = (newPage) => {
  if (newPage >= 1 && newPage <= commentTotalPages.value) {
    commentCurrentPage.value = newPage
    fetchUserComments()
  }
}

// 处理评论跳转页
const handleCommentJumpPage = () => {
  const targetPage = parseInt(commentPageInput.value)
  if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= commentTotalPages.value) {
    if (targetPage !== commentCurrentPage.value) {
      commentCurrentPage.value = targetPage
      fetchUserComments()
    }
  } else {
    commentPageInput.value = commentCurrentPage.value.toString()
  }
}

// 清除评论筛选条件
const clearCommentFilters = () => {
  commentKeyword.value = ''
  commentType.value = 'all'
  contentTypeFilter.value = '0'
  commentCurrentPage.value = 1
  fetchUserComments()
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
