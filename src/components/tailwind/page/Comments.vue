<template>
  <div class="min-h-screen bg-gray-50/30">
    <div class="py-4">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 页面标题 -->
        <div class="bg-white rounded-lg shadow-sm p-5 mb-4">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between">
            <div class="flex items-center mb-4 md:mb-0">
              <div class="p-2 bg-[#fb7299]/10 rounded-lg mr-3">
                <svg class="w-6 h-6 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <div>
                <h1 class="text-2xl font-medium text-gray-800">我的评论</h1>
                <p class="text-sm text-gray-500 mt-0.5">查看和管理您在B站的所有评论记录</p>
              </div>
            </div>
            
            <!-- API致谢 -->
            <div class="bg-blue-50 border border-blue-100 px-4 py-3 rounded-lg">
              <div class="flex items-center">
                <div class="bg-white p-1 rounded-full mr-2">
                  <img src="https://www.aicu.cc/favicon.ico" alt="AICU" class="w-5 h-5" />
                </div>
                <div>
                  <div class="text-sm text-gray-700 font-medium">
                    感谢 <a href="https://www.aicu.cc/" target="_blank" class="text-blue-600 hover:underline">AICU.cc</a> 网站开放API
                  </div>
                  <div class="text-xs text-gray-500 mt-0.5 flex items-center">
                    <svg class="w-3.5 h-3.5 text-amber-500 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <span>非官方API，数据可能不是实时</span>
                    <a href="https://www.aicu.cc/help.html?id=11" target="_blank" class="text-blue-600 ml-1 hover:underline">
                      了解更多
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 筛选和搜索区域 -->
        <div class="mb-4 bg-white rounded-lg shadow-sm p-5">
          <!-- 标题 -->
          <h2 class="text-sm font-medium text-gray-700 mb-3 flex items-center">
            <svg class="w-4 h-4 mr-1.5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            筛选与搜索
          </h2>
          
          <div class="space-y-4 md:space-y-0 md:flex md:items-end md:space-x-4">
            <!-- 搜索框 -->
            <div class="flex-1">
              <label for="search-comment" class="block text-xs font-medium text-gray-600 mb-1.5">关键词</label>
              <div class="relative rounded-md shadow-sm">
                <input
                  id="search-comment"
                  v-model="keyword"
                  type="text"
                  placeholder="搜索评论内容..."
                  class="w-full pl-10 pr-4 py-2.5 rounded-md border border-gray-300 focus:border-[#fb7299] focus:ring focus:ring-[#fb7299]/30 focus:ring-opacity-50 text-sm transition-all"
                  @keyup.enter="handleSearch"
                />
                <svg class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>

            <!-- 评论类型 -->
            <div class="w-full md:w-48">
              <label for="comment-type" class="block text-xs font-medium text-gray-600 mb-1.5">评论类型</label>
              <div class="relative">
                <select
                  id="comment-type"
                  v-model="commentType"
                  class="w-full bg-white rounded-md border border-gray-300 focus:border-[#fb7299] focus:ring focus:ring-[#fb7299]/30 focus:ring-opacity-50 py-2.5 px-3 text-sm shadow-sm transition-all"
                  @change="handleSearch"
                >
                  <option value="all">全部评论</option>
                  <option value="root">一级评论</option>
                  <option value="reply">二级评论</option>
                </select>
              </div>
            </div>

            <!-- 内容类型 -->
            <div class="w-full md:w-48">
              <label for="content-type" class="block text-xs font-medium text-gray-600 mb-1.5">内容类型</label>
              <div class="relative">
                <select
                  id="content-type"
                  v-model="typeFilter"
                  class="w-full bg-white rounded-md border border-gray-300 focus:border-[#fb7299] focus:ring focus:ring-[#fb7299]/30 focus:ring-opacity-50 py-2.5 px-3 text-sm shadow-sm transition-all"
                  @change="handleSearch"
                >
                  <option value="0">全部</option>
                  <option value="1">视频</option>
                  <option value="17">动态</option>
                  <option value="11">动态(旧版)</option>
                </select>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="w-full md:w-auto">
              <button
                @click="handleSearch"
                class="w-full bg-[#fb7299] hover:bg-[#fc8bad] text-white rounded-md px-4 py-2.5 text-sm font-medium transition-colors duration-200 shadow-sm flex items-center justify-center"
              >
                <svg class="w-4 h-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                搜索
              </button>
            </div>
          </div>
        </div>
        
        <!-- 评论列表 -->
        <div class="space-y-4">
          <!-- 筛选状态指示器 -->
          <div v-if="hasActiveFilters" class="bg-gray-50 border border-gray-200/70 rounded-lg p-3 flex items-center justify-between">
            <div class="flex items-center">
              <svg class="w-4 h-4 text-[#fb7299] mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              <div class="text-sm text-gray-600">
                <span class="font-medium">筛选条件：</span>
                <span v-if="keyword" class="ml-1 bg-[#fb7299]/10 text-[#fb7299] px-2 py-0.5 rounded-full text-xs font-medium">
                  关键词：{{ keyword }}
                </span>
                <span v-if="commentType !== 'all'" class="ml-1 bg-[#fb7299]/10 text-[#fb7299] px-2 py-0.5 rounded-full text-xs font-medium">
                  {{ getCommentTypeText(commentType) }}
                </span>
                <span v-if="typeFilter !== '0'" class="ml-1 bg-[#fb7299]/10 text-[#fb7299] px-2 py-0.5 rounded-full text-xs font-medium">
                  {{ getContentTypeText(typeFilter) }}
                </span>
              </div>
            </div>
            <button
              @click="clearFilters"
              class="text-xs text-gray-500 hover:text-[#fb7299] flex items-center space-x-1 hover:underline"
            >
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span>清除所有筛选</span>
            </button>
          </div>

          <div v-for="comment in comments" :key="comment.rpid" class="bg-white p-4 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-300 border border-gray-100">
            <div class="flex justify-between items-start">
              <div class="flex-1">
                <div class="flex items-center mb-2">
                  <span class="text-xs px-1.5 py-0.5 rounded-full mr-2" 
                        :class="comment.type === 1 ? 'bg-blue-100 text-blue-700' : 'bg-green-100 text-green-700'">
                    {{ getCommentType(comment.type) }}
                  </span>
                  <span class="text-gray-500 text-xs">{{ comment.time_str }}</span>
                </div>
                <p class="text-gray-900 mb-3 text-sm whitespace-pre-wrap leading-relaxed">{{ comment.message }}</p>
                <div class="flex items-center text-xs">
                  <a
                    :href="getCommentLink(comment)"
                    target="_blank"
                    class="text-[#fb7299] hover:underline flex items-center"
                  >
                    <svg class="w-3.5 h-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                    查看原文
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- 加载状态 -->
          <div v-if="loading" class="bg-white p-8 rounded-lg shadow-sm flex flex-col items-center justify-center">
            <div class="animate-spin h-8 w-8 border-3 border-[#fb7299] border-t-transparent rounded-full mb-3"></div>
            <p class="text-gray-500 text-sm">加载评论中...</p>
          </div>

          <!-- 空状态 -->
          <div v-if="!loading && comments.length === 0" class="bg-white p-8 rounded-lg shadow-sm flex flex-col items-center justify-center">
            <div class="bg-gray-50 rounded-full p-3 mb-3">
              <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <p class="text-gray-600 font-medium">暂无评论数据</p>
            <p v-if="hasActiveFilters" class="text-gray-500 text-sm mt-1">
              没有找到符合筛选条件的评论
            </p>
            <button
              v-if="hasActiveFilters"
              @click="clearFilters"
              class="mt-3 bg-[#fb7299]/10 hover:bg-[#fb7299]/20 text-[#fb7299] px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 flex items-center"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              清除筛选条件
            </button>
          </div>
        </div>

        <!-- 分页 -->
        <div v-if="totalPages > 0" class="mt-6 flex justify-center">
          <Pagination
            :current-page="currentPage"
            :total-pages="totalPages"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { getComments, getLoginStatus } from '../../../api/api'
import { showNotify } from 'vant'
import { useRouter } from 'vue-router'
import Pagination from '../Pagination.vue'
import 'vant/es/notify/style'

const router = useRouter()
const comments = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const totalPages = ref(0)
const userInfo = ref(null)
const keyword = ref('')
const commentType = ref('all')
const typeFilter = ref('0')

// 获取用户信息
const getUserInfo = async () => {
  try {
    const response = await getLoginStatus()
    if (response.data.status === 'success' && response.data.data.is_logged_in) {
      userInfo.value = response.data.data.user_info
      return true
    } else {
      showNotify({
        type: 'warning',
        message: '请先登录后查看评论'
      })
      router.push('/')
      return false
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
    showNotify({
      type: 'danger',
      message: '获取用户信息失败'
    })
    return false
  }
}

// 处理页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage
}

// 获取评论列表
const fetchComments = async () => {
  if (!userInfo.value?.uid) {
    const hasUser = await getUserInfo()
    if (!hasUser) return
  }

  loading.value = true
  try {
    const response = await getComments(
      userInfo.value.uid,
      currentPage.value,
      pageSize.value,
      commentType.value,
      keyword.value,
      typeFilter.value
    )
    
    if (response.data) {
      comments.value = response.data.comments
      total.value = response.data.total
      totalPages.value = response.data.total_pages
    }
  } catch (error) {
    console.error('获取评论列表失败:', error)
    showNotify({
      type: 'danger',
      message: '获取评论列表失败'
    })
  } finally {
    loading.value = false
  }
}

// 获取评论类型显示文本
const getCommentType = (type) => {
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

// 监听分页变化
watch(currentPage, () => {
  fetchComments()
})

// 监听筛选条件变化
watch([commentType, typeFilter], () => {
  currentPage.value = 1
  fetchComments()
})

onMounted(async () => {
  const hasUser = await getUserInfo()
  if (hasUser) {
    fetchComments()
  }
})

// 处理搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchComments()
}

// 获取评论类型文本
const getCommentTypeText = (type) => {
  switch (type) {
    case 'root':
      return '一级评论'
    case 'reply':
      return '二级评论'
    default:
      return '全部评论'
  }
}

// 获取内容类型文本
const getContentTypeText = (type) => {
  switch (type) {
    case '1':
      return '视频'
    case '17':
      return '动态'
    case '11':
      return '动态(旧版)'
    case '0':
    default:
      return '全部'
  }
}

// 清除筛选条件
const clearFilters = () => {
  keyword.value = ''
  commentType.value = 'all'
  typeFilter.value = '0'
  currentPage.value = 1
  fetchComments()
}

// 判断是否有活动筛选条件
const hasActiveFilters = computed(() => {
  return keyword.value || commentType.value !== 'all' || typeFilter.value !== '0'
})
</script> 