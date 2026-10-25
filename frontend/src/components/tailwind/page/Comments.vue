<template>
  <div>
        <!-- 致谢 -->
        <div class="mb-4">
          <div class="bg-[#fb7299]/5 dark:bg-pink-900/20 border border-[#fb7299]/20 dark:border-[#fb7299]/30 px-3 py-0 rounded-md w-full flex items-center justify-center h-9">
            <img src="https://www.aicu.cc/favicon.ico" alt="AICU" class="w-3 h-3 mr-1.5" />
            <div class="flex items-center">
              <span class="text-xs text-gray-700 dark:text-gray-300">
                感谢 <a href="https://www.aicu.cc/" target="_blank" class="text-[#fb7299] hover:text-[#fb7299]/80 font-medium">aicu.cc</a> 开放API
              </span>
              <span class="mx-1.5 text-gray-300 dark:text-gray-600">|</span>
              <div class="flex items-center text-xs text-gray-500 dark:text-gray-400">
                <svg class="w-3 h-3 text-[#fb7299] mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span>非官方API，数据不是实时更新</span>
                <a href="https://www.aicu.cc/help.html?id=11" target="_blank" class="text-[#fb7299] hover:text-[#fb7299]/80 ml-1 font-medium">
                  了解更多
                </a>
              </div>
            </div>
          </div>
        </div>

        <!-- 搜索和筛选 -->
        <div class="mb-6 bg-transparent">
      <div class="mb-4">
            <!-- 总评论数显示 -->
            <div class="mb-3 flex items-center text-sm text-gray-600">
              <span>共</span>
              <span class="mx-1 text-[#fb7299] font-medium">{{ total }}</span>
              <span>条评论</span>
            </div>

            <div class="flex flex-nowrap items-center space-x-2">
              <!-- 关键词搜索 - 改为与首页一致的样式 -->
              <div class="flex-1 min-w-0">
                <SimpleSearchBar
                  v-model="keyword"
                  placeholder="搜索评论内容..."
                  @search="handleSearch"
                  class="w-full"
                />
              </div>

              <!-- 评论类型筛选 -->
              <div class="w-24 flex-shrink-0">
                <CustomDropdown
                  v-model="commentType"
                  :options="commentTypeOptions"
                  :selected-text="getCommentTypeText(commentType)"
                  @change="selectCommentType"
                  :min-width="80"
                  :use-fixed-width="true"
                  custom-class="h-9"
                />
              </div>

              <!-- 内容类型筛选 -->
              <div class="w-24 flex-shrink-0">
                <CustomDropdown
                  v-model="typeFilter"
                  :options="contentTypeOptions"
                  :selected-text="getContentTypeText(typeFilter)"
                  @change="selectContentType"
                  :min-width="80"
                  :use-fixed-width="true"
                  custom-class="h-9"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- 评论列表 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
          <!-- 评论项 -->
          <div v-if="!loading && comments.length > 0" class="divide-y divide-gray-100 dark:divide-gray-700">
            <div v-for="comment in comments" :key="comment.rpid" class="p-4 md:p-6">
              <div class="space-y-2">
                <!-- 评论内容 -->
                <p class="text-gray-800 dark:text-gray-200 text-sm md:text-base whitespace-pre-wrap leading-relaxed">{{ comment.message }}</p>

                <!-- 评论元数据 -->
                <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                  <div class="flex items-center space-x-3">
                    <span :class="comment.type === 1 ? 'text-[#fb7299]' : 'text-[#fb7299]'">
                      {{ getCommentType(comment.type) }}
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
          <div v-if="loading" class="flex justify-center items-center py-16">
            <div class="flex flex-col items-center">
              <div class="animate-spin h-8 w-8 border-3 border-[#fb7299] border-t-transparent rounded-full"></div>
              <p class="text-gray-500 text-sm mt-4">加载评论中...</p>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-if="!loading && comments.length === 0" class="flex justify-center items-center py-16">
            <div class="flex flex-col items-center">
              <div class="bg-[#fb7299]/5 rounded-full p-3 mb-3">
                <svg class="w-8 h-8 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <p class="text-gray-600 dark:text-gray-300 font-medium">暂无评论数据</p>
              <p v-if="hasActiveFilters" class="text-gray-500 dark:text-gray-400 text-sm mt-1 text-center max-w-sm">
                尝试调整搜索条件
              </p>
              <button
                v-if="hasActiveFilters"
                @click="clearFilters"
                class="mt-4 px-4 py-2 text-white bg-[#fb7299] hover:bg-[#fb7299]/90 rounded-md text-sm transition-colors"
              >
                清除筛选
              </button>
            </div>
          </div>
        </div>

        <!-- 分页控件 -->
        <div v-if="totalPages > 0" class="mt-6 flex justify-center">
          <Pagination
            :current-page="currentPage"
            :total-pages="totalPages"
            @page-change="handlePageChange"
          />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed, onUnmounted } from 'vue'
import { getComments, getLoginStatus } from '../../../api/api'
import { showNotify } from 'vant'
import { useRouter } from 'vue-router'
import Pagination from '../Pagination.vue'
import 'vant/es/notify/style'
import SimpleSearchBar from '../SimpleSearchBar.vue'
import CustomDropdown from '../CustomDropdown.vue'

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
    // 新的API响应格式是 {code: 0, message: "0", ttl: 1, data: {...}}
    // code为0表示请求成功
    if (response.data && response.data.code === 0) {
      const userData = response.data.data
      if (userData.isLogin) {
        userInfo.value = userData
        return true
      }
    }
    
    // 如果未登录，显示提示
    showNotify({
      type: 'warning',
      message: '请先登录后查看评论'
    })
    router.push('/')
    return false
  } catch (error) {
    console.error('获取用户信息失败:', error)
    showNotify({
      type: 'danger',
      message: '获取用户信息失败'
    })
    return false
  }
}

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

// 计算下拉菜单按钮宽度 - 响应式设计
const windowWidth = ref(window.innerWidth)
computed(() => {
  // 检测是否为移动设备
  const isMobile = windowWidth.value < 768
  return isMobile ? '100%' : 100
})
// 处理窗口大小变化
const handleWindowResize = () => {
  windowWidth.value = window.innerWidth
}

// 处理页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage
}

// 获取评论列表
const fetchComments = async () => {
  if (!userInfo.value?.mid) {
    const hasUser = await getUserInfo()
    if (!hasUser) return
  }

  loading.value = true
  try {
    const response = await getComments(
      userInfo.value.mid,
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

// 在组件挂载时添加事件监听器和获取数据
onMounted(async () => {
  window.addEventListener('resize', handleWindowResize)
  const hasUser = await getUserInfo()
  if (hasUser) {
    fetchComments()
  }
})

// 在组件卸载时移除事件监听器
onUnmounted(() => {
  window.removeEventListener('resize', handleWindowResize)
})

// 处理搜索
const handleSearch = () => {
  if (keyword.value.trim() || hasActiveFilters.value) {
    currentPage.value = 1
    fetchComments()
  }
}

// 获取评论类型文本
const getCommentTypeText = (type) => {
  switch (type) {
    case 'root':
      return '一级'
    case 'reply':
      return '二级'
    default:
      return '全部'
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
      return '旧动态'
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

// 选择评论类型
const selectCommentType = (value) => {
  commentType.value = value
  handleSearch()
}

// 选择内容类型
const selectContentType = (value) => {
  typeFilter.value = value
  handleSearch()
}
</script>

<style>
/* 这里可以添加任何需要的自定义样式 */
</style>
