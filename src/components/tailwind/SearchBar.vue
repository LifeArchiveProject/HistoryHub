<template>
  <div class="relative mx-auto max-w-4xl">
    <!-- 搜索区域容器 -->
    <div class="relative">
      <!-- 搜索框容器 -->
      <div class="flex w-full h-8 sm:h-10 items-center rounded-md border border-gray-300 bg-white focus-within:border-[#FF6699] transition-colors duration-200">
        <!-- 搜索图标 -->
        <div class="pl-2 sm:pl-3 text-gray-400">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        
        <!-- 搜索类型选择器 -->
        <select
          v-model="searchType"
          class="h-full appearance-none border-none bg-transparent pl-1 sm:pl-2 text-[#FF6699] focus:outline-none focus:ring-0 text-xs sm:text-sm leading-none flex items-center"
        >
          <option value="all">全部</option>
          <option value="title">标题</option>
          <option value="author">UP主</option>
          <option value="tag">分区</option>
          <option value="remark">备注</option>
        </select>

        <!-- 分隔线 -->
        <div class="h-4 sm:h-5 w-px bg-gray-200 mx-1"></div>

        <!-- 输入框 -->
        <input
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          type="search"
          :placeholder="getPlaceholder"
          class="h-full w-full border-none bg-transparent px-1 sm:px-2 pr-2 sm:pr-3 text-gray-700 focus:outline-none focus:ring-0 text-xs sm:text-sm leading-none"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getAvailableYears } from '../../api/api.js'

const props = defineProps({
  initialYear: {
    type: Number,
    default: () => new Date().getFullYear()
  },
  initialKeyword: {
    type: String,
    default: ''
  },
  initialSearchType: {
    type: String,
    default: 'all'
  }
})

const emit = defineEmits(['year-change', 'search'])
const router = useRouter()
const route = useRoute()

// 搜索相关
const searchQuery = ref(props.initialKeyword)
const searchType = ref(props.initialSearchType)

// 年份相关
const selectedYear = ref(props.initialYear)
const availableYears = ref([props.initialYear])

// 根据搜索类型获取占位符文本
const getPlaceholder = computed(() => {
  switch (searchType.value) {
    case 'title':
      return '视频标题/oid'
    case 'author':
      return 'UP主名称'
    case 'tag':
      return '分区名称'
    case 'remark':
      return '备注内容'
    default:
      return '输入关键词搜索'
  }
})

// 获取可用年份列表
const fetchAvailableYears = async () => {
  try {
    const response = await getAvailableYears()
    if (response.data.status === 'success') {
      availableYears.value = response.data.data
      // 如果当前选中的年份不在可用年份列表中，设置为最新的年份
      if (!availableYears.value.includes(selectedYear.value)) {
        selectedYear.value = availableYears.value[0]
        emit('year-change', selectedYear.value)
      }
    }
  } catch (error) {
    console.error('获取可用年份失败:', error)
  }
}

// 处理年份变化
const handleYearChange = () => {
  emit('year-change', selectedYear.value)
}

// 监听搜索类型变化
watch(searchType, (newType) => {
  console.log('SearchBar - 搜索类型变化:', newType)
  // 如果在搜索页面且有搜索关键词，触发搜索
  if (route.name === 'Search' && searchQuery.value.trim()) {
    handleSearch()
  }
})

// 处理搜索
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    console.log('SearchBar - 执行搜索:', {
      keyword: searchQuery.value.trim(),
      type: searchType.value
    })
    if (route.name === 'Search') {
      // 如果在搜索页面，发出搜索事件
      emit('search', {
        keyword: searchQuery.value.trim(),
        type: searchType.value
      })
    } else {
      // 修改为在当前窗口打开搜索结果页面
      router.push({
        name: 'Search',
        params: { keyword: searchQuery.value.trim() },
        query: { 
          type: searchType.value
        }
      })
      searchQuery.value = ''
    }
  } else {
    alert('请输入有效的搜索关键词')
  }
}

// 监听props变化
watch(() => props.initialKeyword, (newKeyword) => {
  searchQuery.value = newKeyword
})

watch(() => props.initialYear, (newYear) => {
  if (newYear !== selectedYear.value) {
    selectedYear.value = newYear
  }
})

watch(() => props.initialSearchType, (newType) => {
  if (newType !== searchType.value) {
    searchType.value = newType
  }
})

onMounted(async () => {
  await fetchAvailableYears()
})
</script>

<style>
/* 移除搜索框的默认样式 */
input[type="search"]::-webkit-search-decoration,
input[type="search"]::-webkit-search-cancel-button,
input[type="search"]::-webkit-search-results-button,
input[type="search"]::-webkit-search-results-decoration {
  display: none;
}

/* 移除选择器的默认箭头和focus样式 */
select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23FF6699' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.25rem center;
  background-size: 1em;
  padding-right: 1.5rem !important;
}

select:focus {
  box-shadow: none !important;
  outline: none !important;
  -webkit-appearance: none !important;
}

select:focus-visible {
  outline: none !important;
  box-shadow: none !important;
}

/* 移除输入框的默认focus样式 */
input:focus {
  box-shadow: none !important;
  outline: none !important;
}
</style>
