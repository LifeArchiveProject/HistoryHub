<template>
  <div class="relative mx-auto max-w-4xl p-1">
    <!-- 搜索区域容器 -->
    <div class="flex items-center space-x-2">
      <!-- 年份选择器 -->
      <div class="relative inline-block">
        <select
          v-model="selectedYear"
          @change="handleYearChange"
          class="appearance-none rounded-lg border border-gray-300 bg-[#edf2fa] px-2 py-2 pr-8 text-[#FF6699] hover:bg-[#e1e6ed] focus:outline-none lm:text-xs lg:text-lg"
        >
          <option v-for="year in availableYears" :key="year" :value="year">
            {{ year }}年
          </option>
        </select>
      </div>

      <!-- 输入框 -->
      <input
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        type="search"
        placeholder="视频标题/oid"
        class="w-full rounded-lg border border-gray-300 bg-[#edf2fa] p-2 text-gray-900 hover:bg-[#e1e6ed] focus:outline-none lm:text-xs lg:text-lg"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
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
  }
})

const emit = defineEmits(['year-change', 'search'])
const router = useRouter()
const route = useRoute()

// 搜索相关
const searchQuery = ref(props.initialKeyword)

// 年份相关
const selectedYear = ref(props.initialYear)
const availableYears = ref([props.initialYear])

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
    if (route.name === 'Search') {
      // 如果在搜索页面，发出搜索事件
      emit('search', searchQuery.value.trim())
    } else {
      // 如果在其他页面，打开新标签页
      const newUrl = router.resolve({
        name: 'Search',
        params: { keyword: searchQuery.value.trim() },
        query: { year: selectedYear.value }
      }).href
      window.open(newUrl, '_blank')
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

onMounted(async () => {
  await fetchAvailableYears()
})
</script>

<style>
/* 覆盖输入框和选择器的 focus 样式 */
select:focus {
  outline: none !important;
  box-shadow: none !important;
  border-color: #e5e7eb !important;
}

input:focus {
  outline: none !important;
  box-shadow: none !important;
  border-color: #FF6699 !important;
}
</style>
