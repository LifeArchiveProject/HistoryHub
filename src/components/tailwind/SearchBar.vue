<template>
  <div class="relative mx-auto max-w-4xl">
    <!-- 搜索区域容器 -->
    <div class="relative">
      <!-- 搜索框容器 -->
      <div class="flex w-full h-8 sm:h-10 items-center rounded-md border border-gray-300 dark:border-gray-600 bg-transparent focus-within:border-[#fb7299] transition-colors duration-200">
        <!-- 搜索图标 -->
        <div class="pl-2 sm:pl-3 text-gray-400 dark:text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 sm:h-4 sm:w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        
        <!-- 搜索类型选择器 - 替换为CustomDropdown组件 -->
        <div class="h-full pl-1 sm:pl-2 flex items-center">
          <CustomDropdown
            v-model="searchType"
            :options="searchTypeOptions"
            :selected-text="searchType"
            @change="onSearchTypeChange"
            custom-class="h-full border-none !shadow-none !p-0 !m-0 !rounded-none !pr-1"
            :min-width="180"
            :use-fixed-width="false"
          >
            <template #trigger-content>
              <span class="text-[#fb7299] text-xs sm:text-sm flex items-center whitespace-nowrap">{{ getTypeLabel(searchType) }}</span>
            </template>
          </CustomDropdown>
        </div>

        <!-- 分隔线 -->
        <div class="h-4 sm:h-5 w-px bg-gray-200 dark:bg-gray-600 mx-1"></div>

        <!-- 输入框 -->
        <input
          v-model="searchQuery"
          @keyup.enter="handleSearch"
          type="search"
          :placeholder="getPlaceholder"
          class="h-full w-full border-none bg-transparent px-1 sm:px-2 pr-2 sm:pr-3 text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-0 text-xs sm:text-sm leading-none"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getAvailableYears } from '../../api/api.js'
import CustomDropdown from './CustomDropdown.vue'

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

// 搜索类型选项
const searchTypeOptions = [
  { value: 'all', label: '全部' },
  { value: 'title', label: '标题' },
  { value: 'author', label: 'UP主' },
  { value: 'tag', label: '分区' },
  { value: 'remark', label: '备注' }
]

// 根据选项值获取显示文本
const getTypeLabel = (value) => {
  const option = searchTypeOptions.find(opt => opt.value === value)
  return option ? option.label : '全部'
}

// 处理搜索类型变更
const onSearchTypeChange = (value) => {
  searchType.value = value
  // 如果在搜索页面且有搜索关键词，触发搜索
  if (route.name === 'Search' && searchQuery.value.trim()) {
    handleSearch()
  }
}

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

<style scoped>
/* 移除搜索框的默认样式 */
input[type="search"]::-webkit-search-decoration,
input[type="search"]::-webkit-search-cancel-button,
input[type="search"]::-webkit-search-results-button,
input[type="search"]::-webkit-search-results-decoration {
  display: none;
}

/* 移除输入框的默认focus样式 */
input:focus {
  box-shadow: none !important;
  outline: none !important;
}

:deep(.custom-dropdown-trigger) {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
}

/* 确保下拉菜单按钮文本不会折行 */
:deep(.custom-dropdown-trigger span) {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
