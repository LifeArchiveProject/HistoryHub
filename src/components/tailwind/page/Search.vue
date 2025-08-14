<template>
  <div>
    <!-- 搜索框和总数显示容器 -->
    <div class="sticky top-0 bg-white lg:pt-4 z-50">
      <div class="bg-white">
        <div class="mx-auto max-w-4xl">
          <!-- 使用SearchBar组件 -->
          <SearchBar
            :initial-keyword="keyword"
            :initial-search-type="searchType"
            @search="handleSearch"
          />

          <!-- 显示总条数，和输入框左端对齐 -->
          <p class="p-1.5 text-lg text-gray-700 lm:text-sm">
            共 <span class="text-[#fb7299]">{{ totalResults }}</span> 条数据和
            <span class="text-[#fb7299]">{{ keyword }}</span> 相关
          </p>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="mx-auto max-w-7xl sm:px-2 lg:px-8">
      <!-- 使用 key 来强制组件重新渲染 -->
      <div :key="page">
        <!-- 视频记录列表 -->
        <VideoRecord
          v-for="record in records"
          :key="record.id"
          :record="record"
          :search-keyword="keyword"
          :search-type="searchType"
          :remark-data="remarkData"
          @remark-updated="handleRemarkUpdate"
        />
      </div>

      <!-- 分页功能 -->
      <div class="mb-5 mt-8">
        <Pagination
          v-model:current-page="page"
          :total-pages="totalPages"
          :use-routing="true"
          @update:current-page="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchBiliHistory2024, batchGetRemarks } from '../../../api/api.js'
import SearchBar from '../SearchBar.vue'
import VideoRecord from '../VideoRecord.vue'
import Pagination from '../Pagination.vue'
import { normalizeImageUrl } from '@/utils/imageUrl.js'

// 获取路由参数
const route = useRoute()
const router = useRouter()

// 状态变量
const records = ref([])
const page = ref(1)
const size = ref(30)
const totalPages = ref(0)
const totalResults = ref(0)
const remarkData = ref({}) // 存储备注数据

// 搜索相关变量
const keyword = ref('')  // 初始化为空字符串
const searchType = ref('all')  // 默认为全部搜索

// 处理搜索
const handleSearch = ({ keyword: searchKeyword, type }) => {
  console.log('Search - 收到搜索事件:', { searchKeyword, type })
  if (searchKeyword.trim()) {
    keyword.value = searchKeyword.trim()
    searchType.value = type
    page.value = 1
    router.push({
      name: 'Search',
      params: { keyword: searchKeyword.trim() },
      query: {
        type: type
      }
    })
    fetchSearchResults()
  }
}

// 处理页码变化
const handlePageChange = async (newPage) => {
  if (newPage !== page.value) {
    page.value = newPage
    // 清空当前记录，避免显示旧数据
    records.value = []
    // 更新路由
    if (newPage === 1) {
      await router.push({
        name: 'Search',
        params: { keyword: keyword.value },
        query: {
          type: searchType.value
        }
      })
    } else {
      await router.push({
        name: 'Search',
        params: { keyword: keyword.value, pageNumber: newPage },
        query: {
          type: searchType.value
        }
      })
    }
    await fetchSearchResults()
  }
}

// 获取搜索结果
const fetchSearchResults = async () => {
  try {
    // 从localStorage获取是否使用本地图片源的设置
    const useLocalImages = localStorage.getItem('useLocalImages') === 'true'

    const response = await searchBiliHistory2024(
      keyword.value,           // search
      searchType.value,        // searchType
      page.value,             // page
      size.value,             // size
      useLocalImages          // 使用本地图片源
    )

    if (response.data.status === 'success') {
      records.value = response.data.data.records
      totalPages.value = Math.ceil(response.data.data.total / size.value)
      totalResults.value = response.data.data.total

      // 批量获取备注
      if (records.value.length > 0) {
        const batchRecords = records.value.map(record => ({
          bvid: record.bvid,
          view_at: record.view_at
        }))
        const remarksResponse = await batchGetRemarks(batchRecords)
        if (remarksResponse.data.status === 'success') {
          remarkData.value = remarksResponse.data.data
        }
      }
    }
  } catch (error) {
    console.error('搜索失败:', error)
  }
}

// 处理备注更新
const handleRemarkUpdate = (data) => {
  const key = `${data.bvid}_${data.view_at}`
  remarkData.value[key] = {
    bvid: data.bvid,
    view_at: data.view_at,
    remark: data.remark,
    remark_time: data.remark_time
  }
}

// 监听 keyword 变化
watch(
  () => route.params.keyword,
  (newKeyword) => {
    if (newKeyword !== keyword.value) {
      // 确保 keyword 是字符串类型
      keyword.value = Array.isArray(newKeyword) ? newKeyword[0] : String(newKeyword)
      page.value = 1
      records.value = [] // 清空当前记录
      fetchSearchResults()
    }
  }
)

// 监听页码变化
watch(
  () => route.params.pageNumber,
  async (newPage) => {
    const pageNum = Number(newPage) || 1
    if (pageNum !== page.value) {
      page.value = pageNum
      records.value = [] // 清空当前记录
      await fetchSearchResults()
    }
  }
)

// 监听搜索类型变化
watch(
  searchType,
  (newType) => {
    console.log('Search - 搜索类型变化:', newType)
    if (keyword.value) {  // 只有在有搜索关键词时才重新搜索
      records.value = [] // 清空当前记录
      router.push({
        name: 'Search',
        params: { keyword: keyword.value },
        query: {
          type: newType
        }
      })
      fetchSearchResults()
    }
  }
)

// 组件挂载时获取数据
onMounted(async () => {
  const typeFromQuery = String(route.query.type || '')
  if (typeFromQuery) {
    searchType.value = typeFromQuery
  }

  // 设置初始关键词
  const initialKeyword = Array.isArray(route.params.keyword)
    ? route.params.keyword[0]
    : String(route.params.keyword || '')
  keyword.value = initialKeyword

  // 从路由参数获取页码
  page.value = Number(route.params.pageNumber || 1)

  await fetchSearchResults()
})
</script>

<style scoped>
/* 移除之前的sticky样式 */
</style>
