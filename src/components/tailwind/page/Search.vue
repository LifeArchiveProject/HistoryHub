<template>
  <div class="mx-auto mt-2 max-w-7xl sm:px-2 lg:px-8">
    <!-- 搜索框和总数显示容器 -->
    <div class="fixed left-0 right-0 top-0 z-50 bg-white px-1.5 pb-1.5">
      <!-- 使用SearchBar组件 -->
      <SearchBar
        :initial-year="selectedYear"
        :initial-keyword="keyword"
        :initial-search-type="searchType"
        @year-change="handleYearChange"
        @search="handleSearch"
      />

      <!-- 显示总条数，和输入框左端对齐 -->
      <div class="mx-auto max-w-4xl">
        <p class="p-1.5 text-lg text-gray-700 lm:text-sm">
          共 <span class="text-[#FF6699]">{{ totalResults }}</span> 条数据和
          <span class="text-[#FF6699]">{{ keyword }}</span> 相关
        </p>
      </div>
    </div>

    <!-- 使用 key 来强制组件重新渲染 -->
    <div :key="page" class="pt-20 lm:pt-16">
      <!-- 增加顶部填充，确保内容不被固定元素遮挡 -->
      <VideoRecord 
        v-for="record in records" 
        :key="record.id" 
        :record="record"
        :search-keyword="keyword"
        :search-type="searchType"
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
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchBiliHistory2024, searchBiliHistoryAuthor } from '../../../api/api.js'
import SearchBar from '../SearchBar.vue'
import VideoRecord from '../VideoRecord.vue'
import Pagination from '../Pagination.vue'

// 获取路由参数
const route = useRoute()
const router = useRouter()
const keyword = ref('')  // 初始化为空字符串
const searchType = ref('title')  // 默认为标题搜索

// 状态变量
const records = ref([])
const page = ref(1)
const size = ref(30)
const sortOrder = ref(0)
const totalPages = ref(0)
const totalResults = ref(0)

// 年份相关
const currentYear = new Date().getFullYear()
const selectedYear = ref(currentYear)

// 处理年份变化
const handleYearChange = (year) => {
  selectedYear.value = year
  router.replace({
    name: route.name,
    params: route.params,
    query: { ...route.query, year }
  })
  page.value = 1
  fetchSearchResults()
}

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
        year: selectedYear.value,
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
      await router.push(`/search/${keyword.value}`)
    } else {
      await router.push(`/search/${keyword.value}/page/${newPage}`)
    }
    await fetchSearchResults()
  }
}

// 获取搜索数据的函数
const fetchSearchResults = async () => {
  console.log('Search - 开始获取搜索结果:', {
    keyword: keyword.value,
    type: searchType.value,
    page: page.value,
    year: selectedYear.value
  })
  
  try {
    // 清空当前记录
    records.value = []
    // 确保传递的是字符串类型
    const searchKeyword = Array.isArray(keyword.value) ? keyword.value[0] : String(keyword.value)

    let response
    if (searchType.value === 'author') {
      console.log('Search - 使用作者搜索 API')
      response = await searchBiliHistoryAuthor(
        page.value,
        size.value,
        searchKeyword,
        sortOrder.value,
        selectedYear.value
      )
    } else {
      console.log('Search - 使用标题搜索 API')
      response = await searchBiliHistory2024(
        page.value,
        size.value,
        searchKeyword,
        sortOrder.value,
        selectedYear.value
      )
    }

    if (response.data && response.data.data) {
      records.value = response.data.data.records
      totalResults.value = response.data.data.total
      totalPages.value = Math.ceil(response.data.data.total / size.value)
      console.log('Search - 搜索结果:', {
        total: totalResults.value,
        records: records.value.length
      })
    }
  } catch (error) {
    console.error('搜索数据获取失败: ', error)
    records.value = []
    totalResults.value = 0
    totalPages.value = 0
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
          year: selectedYear.value,
          type: newType
        }
      })
      fetchSearchResults()
    }
  }
)

// 组件挂载时获取数据
onMounted(async () => {
  // 从URL查询参数获取年份和搜索类型
  const yearFromQuery = Number(route.query.year || 0)
  if (yearFromQuery) {
    selectedYear.value = yearFromQuery
  }

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
