<template>
  <div>
    <!-- 年度总结横幅 -->
    <div class="mt-1 mb-3 sm:hidden">
      <router-link
        to="/analytics"
        class="flex h-10 items-center justify-between px-2 bg-gradient-to-r from-[#FF6699] to-[#FF9966] text-white"
      >
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span class="text-sm">点击查看年度总结</span>
        </div>
        <svg class="w-4 h-4 animate-bounce-x" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </router-link>
    </div>

    <!-- 视频记录列表 -->
    <div>
      <template v-for="(record, index) in records" :key="record.id">
        <!-- 日期分割线和视频数量 -->
        <div v-if="shouldShowDivider(index)" class="relative py-1 max-w-4xl mx-auto">
          <div class="px-2">
            <div class="relative">
              <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-gray-300" />
              </div>
              <div class="relative flex items-center justify-between">
                <div class="bg-white dark:bg-gray-800 pr-3">
                <span class="lm:text-xs">
                  {{ formatDividerDate(record.view_at) }}
                </span>
                </div>
                <div class="bg-white dark:bg-gray-800 pl-3">
                <span class="lm:text-xs text-[#FF6699]">
                  {{ getDailyStatsForDate(record.view_at) }}个视频
                </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <VideoRecord :record="record" />
      </template>
    </div>

    <!-- 日期选择日历 -->
    <van-calendar
      :show-confirm="false"
      title="选择日期区间"
      switch-mode="year-month"
      :show="show"
      :style="{ height: '65%' }"
      type="range"
      @confirm="onConfirm"
      @update:show="(val) => emit('update:show', val)"
    />

    <!-- 分类选择 -->
    <VideoCategories
      :showBottom="showBottom"
      @update:showBottom="(val) => emit('update:showBottom', val)"
      @selectSubCategory="onSubCategorySelected"
    />
  </div>
</template>

<style scoped>
@keyframes bounce-x {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(25%);
  }
}

.animate-bounce-x {
  animation: bounce-x 1s infinite;
}
</style>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getBiliHistory2024, getMainCategories, getDailyStats } from '../../api/api.js'
import VideoRecord from './VideoRecord.vue'
import VideoCategories from './VideoCategories.vue'

const props = defineProps({
  selectedYear: {
    type: Number,
    required: true,
  },
  page: {
    type: Number,
    required: true,
  },
  show: {
    type: Boolean,
    required: true,
  },
  showBottom: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits([
  'update:total-pages',
  'update:total',
  'update:date',
  'update:category',
  'update:show',
  'update:showBottom',
])

// 状态变量
const records = ref([])
const total = ref(0)
const sortOrder = ref(0)
const size = ref(30)

const date = ref('')
const dateRange = ref('')

const tagName = ref('')
const mainCategory = ref('')
const mainCategories = ref([])

// 每日统计数据
const dailyStats = ref({})

// 计算属性用于显示当前选中的分类
computed(() => {
  return mainCategory.value || tagName.value || '全部分区'
})
// 获取主分区列表
const fetchMainCategories = async () => {
  try {
    const response = await getMainCategories()
    if (response.data.status === 'success') {
      mainCategories.value = response.data.data.map((cat) => cat.name)
    }
  } catch (error) {
    console.error('Error fetching main categories:', error)
  }
}

// 接收子组件传递的子分区并立即获取数据
const onSubCategorySelected = ({ name, type }) => {
  const isMainName = mainCategories.value.includes(name)
  emit('update:showBottom', false)

  let categoryText = ''
  if (type === 'main' || (type === 'sub' && isMainName)) {
    if (mainCategory.value === name) {
      mainCategory.value = ''
    } else {
      mainCategory.value = name
      categoryText = name
    }
    tagName.value = ''
  } else if (type === 'sub') {
    if (tagName.value === name) {
      tagName.value = ''
    } else {
      tagName.value = name
      categoryText = name
    }
    mainCategory.value = ''
  }

  emit('update:category', categoryText)
  fetchHistoryByDateRange()
}

// 辅助函数：格式化日期
const formatDate = (date) => `${date.getMonth() + 1}/${date.getDate()}`
const formatDateWithYear = (date) => `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
const formatDateForAPI = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}${month}${day}`
}

// 处理日期区间确认
const onConfirm = (values) => {
  const [start, end] = values
  emit('update:show', false)

  const startYear = start.getFullYear()
  const endYear = end.getFullYear()

  let dateText
  if (startYear === props.selectedYear && endYear === props.selectedYear) {
    dateText = `${formatDate(start)} - ${formatDate(end)}`
  } else {
    dateText = `${formatDateWithYear(start)} - ${formatDateWithYear(end)}`
  }

  emit('update:date', dateText)
  dateRange.value = `${formatDateForAPI(start)}-${formatDateForAPI(end)}`
  fetchHistoryByDateRange()
}

// 数据获取函数
const fetchHistoryByDateRange = async () => {
  try {
    records.value = []
    const response = await getBiliHistory2024(
      props.page,
      size.value,
      sortOrder.value,
      tagName.value,
      mainCategory.value,
      dateRange.value,
    )

    if (response.data && response.data.data) {
      total.value = response.data.data.total
      records.value = response.data.data.records
      emit('update:total-pages', Math.ceil(response.data.data.total / size.value))
      emit('update:total', response.data.data.total)
    }
  } catch (error) {
    console.error('数据获取失败:', error)
    records.value = []
    total.value = 0
    emit('update:total-pages', 0)
    emit('update:total', 0)
  }
}

// 监听年份和页码变化
watch(
  () => [props.selectedYear, props.page],
  () => {
    if (dateRange.value) {
      fetchHistoryByDateRange()
    }
  },
)

// 获取每日统计数据
const fetchDailyStats = async (timestamp) => {
  if (!timestamp) return

  try {
    const date = new Date(timestamp * 1000)
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const dateStr = `${month}${day}`

    // 如果已经有这个日期的数据，就不重复获取
    const dateKey = `${date.getFullYear()}-${month}-${day}`
    if (dailyStats.value[dateKey]) return

    const response = await getDailyStats(dateStr, props.selectedYear)
    if (response.data.status === 'success') {
      dailyStats.value[dateKey] = response.data.data
    }
  } catch (error) {
    console.error('获取每日统计数据失败:', error)
  }
}

// 监听记录变化，获取所有不同日期的统计数据
watch(() => records.value, (newRecords) => {
  if (newRecords && newRecords.length > 0) {
    // 获取所有不同日期的时间戳
    const uniqueDates = new Set()
    newRecords.forEach(record => {
      const date = new Date(record.view_at * 1000)
      const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
      if (!uniqueDates.has(dateKey)) {
        uniqueDates.add(dateKey)
        fetchDailyStats(record.view_at)
      }
    })
  } else {
    dailyStats.value = {}
  }
}, { deep: true })

// 获取指定日期的统计数据
const getDailyStatsForDate = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const dateKey = `${date.getFullYear()}-${month}-${day}`
  return dailyStats.value[dateKey]?.total_videos || 0
}

onMounted(async () => {
  await fetchMainCategories()
  const today = new Date()
  const startOfYear = new Date(props.selectedYear, 0, 1)
  onConfirm([startOfYear, today])
})

// 暴露方法给父组件
defineExpose({
  fetchHistoryByDateRange,
})

// 格式化分割线日期
const formatDividerDate = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${month}月${day}日`
}

// 判断是否需要显示分割线
const shouldShowDivider = (index) => {
  if (index === 0) return true

  const currentDate = new Date(records.value[index].view_at * 1000)
  const prevDate = new Date(records.value[index - 1].view_at * 1000)

  return currentDate.getDate() !== prevDate.getDate() ||
    currentDate.getMonth() !== prevDate.getMonth() ||
    currentDate.getFullYear() !== prevDate.getFullYear()
}
</script>
