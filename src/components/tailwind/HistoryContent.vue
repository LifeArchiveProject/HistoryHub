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
      <!-- 网格布局（仅PC端） -->
      <div v-if="layout === 'grid'" class="hidden sm:grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 px-4">
        <template v-for="(record, index) in records" :key="`grid-${record.id}-${record.view_at}`">
          <!-- 日期分割线和视频数量 -->
          <div v-if="shouldShowDivider(index)" class="col-span-full relative py-1">
            <div class="px-2">
              <div class="relative">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                  <div class="w-full border-t border-gray-300" />
                </div>
                <div class="relative flex items-center justify-between">
                  <div class="bg-white dark:bg-gray-800 pr-3 flex items-center space-x-2">
                    <!-- 添加当天记录的勾选框 -->
                    <div v-if="isBatchMode"
                         class="flex items-center justify-center cursor-pointer"
                         @click.stop="toggleDaySelection(record.view_at)">
                      <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                           :class="isDaySelected(record.view_at) ? 'bg-[#fb7299] border-[#fb7299]' : 'border-gray-300 bg-white'">
                        <svg v-if="isDaySelected(record.view_at)" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    </div>
                    <span class="lm:text-xs">
                      {{ formatDividerDate(record.view_at) }}
                    </span>
                  </div>
                  <div class="bg-white dark:bg-gray-800 pl-3">
                    <span class="lm:text-xs text-[#FF6699]">
                      {{ getDailyStatsForDate(record.view_at) }}条数据
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 网格布局的视频卡片 -->
          <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-lg overflow-hidden border border-gray-200/50 hover:border-[#FF6699] hover:shadow-md transition-all duration-200 relative group"
               :class="{ 'ring-2 ring-[#fb7299]': selectedRecords.has(`${record.bvid}_${record.view_at}`) }">
            <!-- 多选框 -->
            <div v-if="isBatchMode"
                 class="absolute top-2 left-2 z-10"
                 @click.stop="toggleRecordSelection(record)">
              <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                   :class="selectedRecords.has(`${record.bvid}_${record.view_at}`) ? 'bg-[#fb7299] border-[#fb7299]' : 'border-white bg-black/20'">
                <svg v-if="selectedRecords.has(`${record.bvid}_${record.view_at}`)" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>

            <!-- 封面图片 -->
            <div class="relative aspect-video cursor-pointer" @click="handleVideoClick(record)">
              <!-- 删除按钮 -->
              <div v-if="!isBatchMode"
                   class="absolute right-2 top-2 z-20 hidden group-hover:flex items-center justify-center w-8 h-8 bg-black/50 hover:bg-[#fb7299] rounded-full cursor-pointer transition-all duration-200"
                   @click.stop="handleDelete(record)">
                <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <!-- 详情按钮 -->
              <div v-if="!isBatchMode"
                   class="absolute right-12 top-2 z-20 hidden group-hover:flex items-center justify-center w-8 h-8 bg-black/50 hover:bg-[#fb7299] rounded-full cursor-pointer transition-all duration-200"
                   @click.stop="openVideoDetail(record)">
                <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <img
                :src="record.cover || record.covers?.[0]"
                class="w-full h-full object-cover transition-all duration-300"
                :class="{ 'blur-md': isPrivacyMode }"
                alt=""
              />
              <!-- 视频进度条 -->
              <div v-if="record.business !== 'article-list' && record.business !== 'article' && record.business !== 'live'"
                   class="absolute bottom-0 left-0 w-full">
                <div class="absolute bottom-1 right-1 rounded bg-black/50 px-1 py-1 text-[10px] font-semibold text-white">
                  <span>{{ formatDuration(record.progress) }}</span>
                  <span>/</span>
                  <span>{{ formatDuration(record.duration) }}</span>
                </div>
                <div class="absolute bottom-0 left-0 h-0.5 w-full bg-black">
                  <div class="h-full bg-[#FF6699]"
                       :style="{ width: getProgressWidth(record.progress, record.duration) }">
                  </div>
                </div>
              </div>
              <!-- 右上角的类型角标 -->
              <div
                v-if="record.badge"
                class="absolute right-1 top-1 rounded bg-[#FF6699] px-1 py-0.5 text-[10px] text-white"
              >
                {{ record.badge }}
              </div>
            </div>
            <!-- 视频信息 -->
            <div class="p-3 flex flex-col space-y-1">
              <!-- 标题 - 单行显示 -->
              <div class="line-clamp-1 text-sm text-gray-900 cursor-pointer"
                   v-html="isPrivacyMode ? '******' : highlightText(record.title)"
                   :class="{ 'blur-sm': isPrivacyMode }"
                   @click="handleVideoClick(record)">
              </div>
              <!-- 分区标签 - 单行显示 -->
              <div class="text-xs text-gray-500 truncate flex items-center space-x-1">
                <span class="inline-flex items-center rounded-md bg-[#f1f2f3] px-2 py-1 text-xs text-[#71767d]">
                  {{ record.business === 'archive' ? record.tag_name : getBusinessType(record.business) }}
                </span>
                <span v-if="record.business === 'archive'" class="text-gray-400">·</span>
                <span v-if="record.business === 'archive' && record.name" class="text-[#71767d]">{{ record.name }}</span>
              </div>
              <!-- UP主和时间信息 - 单行显示 -->
              <div class="flex items-center justify-between text-xs text-gray-600">
                <div class="flex items-center space-x-2 min-w-0 flex-1">
                  <img v-if="record.business !== 'cheese' && record.business !== 'pgc'"
                       :src="record.author_face"
                       :class="{ 'blur-md': isPrivacyMode }"
                       class="w-4 h-4 rounded-full flex-shrink-0 cursor-pointer"
                       @click="handleAuthorClick(record)"
                       :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
                  />
                  <span v-html="isPrivacyMode ? '******' : highlightText(record.author_name)"
                        :class="{ 'blur-sm': isPrivacyMode }"
                        class="cursor-pointer hover:text-[#fb7299] transition-colors duration-200 truncate"
                        @click="handleAuthorClick(record)">
                  </span>
                </div>
                <div class="flex items-center space-x-2 flex-shrink-0">
                  <img v-if="record.dt === 1 || record.dt === 3 || record.dt === 5 || record.dt === 7"
                       src="/Mobile.svg"
                       alt="Mobile"
                       class="h-4 w-4"
                  />
                  <img v-else-if="record.dt === 2 || record.dt === 33"
                       src="/PC.svg"
                       alt="PC"
                       class="h-4 w-4"
                  />
                  <img v-else-if="record.dt === 4 || record.dt === 6"
                       src="/Pad.svg"
                       alt="Pad"
                       class="h-4 w-4"
                  />
                  <span>{{ formatTimestamp(record.view_at) }}</span>
                </div>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- 列表布局（移动端始终显示，PC端在list模式下显示） -->
      <div :class="{'sm:hidden': layout === 'grid'}">
        <template v-for="(record, index) in records" :key="`list-${record.id}-${record.view_at}`">
          <!-- 日期分割线和视频数量 -->
          <div v-if="shouldShowDivider(index)" class="relative py-1 max-w-4xl mx-auto">
            <div class="px-2">
              <div class="relative">
                <div class="absolute inset-0 flex items-center" aria-hidden="true">
                  <div class="w-full border-t border-gray-300" />
                </div>
                <div class="relative flex items-center justify-between">
                  <div class="bg-white dark:bg-gray-800 pr-3 flex items-center space-x-2">
                    <!-- 添加当天记录的勾选框 -->
                    <div v-if="isBatchMode"
                         class="flex items-center justify-center cursor-pointer"
                         @click.stop="toggleDaySelection(record.view_at)">
                      <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                           :class="isDaySelected(record.view_at) ? 'bg-[#fb7299] border-[#fb7299]' : 'border-gray-300 bg-white'">
                        <svg v-if="isDaySelected(record.view_at)" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    </div>
                    <span class="lm:text-xs">
                      {{ formatDividerDate(record.view_at) }}
                    </span>
                  </div>
                  <div class="bg-white dark:bg-gray-800 pl-3">
                    <span class="lm:text-xs text-[#FF6699]">
                      {{ getDailyStatsForDate(record.view_at) }}条数据
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <VideoRecord
            :record="record"
            :is-batch-mode="isBatchMode"
            :is-selected="selectedRecords.has(`${record.bvid}_${record.view_at}`)"
            :remark-data="remarkData"
            @toggle-selection="toggleRecordSelection"
            @refresh-data="fetchHistoryByDateRange"
            @remark-updated="handleRemarkUpdate"
          />
        </template>
      </div>
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

    <!-- 批量删除按钮 -->
    <div v-if="isBatchMode && selectedRecords.size > 0"
         class="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50">
      <button
        @click="handleBatchDelete"
        class="px-4 py-2 bg-[#fb7299] text-white rounded-full shadow-lg hover:bg-[#fb7299]/90 transition-colors duration-200 flex items-center space-x-2"
      >
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
        <span>删除选中的 {{ selectedRecords.size }} 条记录</span>
      </button>
    </div>
  </div>
  
  <!-- 视频详情对话框 -->
  <Teleport to="body">
    <VideoDetailDialog
      :modelValue="showDetailDialog"
      @update:modelValue="showDetailDialog = $event"
      :video="selectedRecord"
      :remarkData="remarkData"
      @remark-updated="handleRemarkUpdate"
    />
  </Teleport>
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
import {
  getBiliHistory2024,
  getMainCategories,
  getDailyStats,
  batchDeleteHistory,
  batchGetRemarks
} from '../../api/api.js'
import { showNotify, showDialog } from 'vant'
import 'vant/es/dialog/style'
import VideoRecord from './VideoRecord.vue'
import VideoCategories from './VideoCategories.vue'
import { usePrivacyStore } from '../../store/privacy'
import VideoDetailDialog from './VideoDetailDialog.vue'

const { isPrivacyMode } = usePrivacyStore()

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
  layout: {
    type: String,
    default: 'list'
  },
  searchKeyword: {
    type: String,
    default: ''
  },
  date: {
    type: String,
    default: ''
  },
  category: {
    type: String,
    default: ''
  },
  isBatchMode: {
    type: Boolean,
    default: false
  }
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
const remarkData = ref({}) // 存储备注数据

const date = ref('')
const dateRange = ref('')

const tagName = ref('')
const mainCategory = ref('')
const mainCategories = ref([])

// 每日统计数据
const dailyStats = ref({})

// 批量删除相关
const selectedRecords = ref(new Set())

// 在data区域添加
const selectedRecord = ref(null)
const showDetailDialog = ref(false)

// 选择/取消选择记录
const toggleRecordSelection = (record) => {
  const key = `${record.bvid}_${record.view_at}`
  if (selectedRecords.value.has(key)) {
    selectedRecords.value.delete(key)
  } else {
    selectedRecords.value.add(key)
  }
}

// 批量删除选中的记录
const handleBatchDelete = async () => {
  if (selectedRecords.value.size === 0) {
    showNotify({
      type: 'warning',
      message: '请先选择要删除的记录'
    })
    return
  }

  try {
    await showDialog({
      title: '确认删除',
      message: `确定要删除选中的 ${selectedRecords.value.size} 条记录吗？此操作不可恢复。`,
      showCancelButton: true,
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      confirmButtonColor: '#fb7299'
    })

    // 从记录中找到对应的完整信息
    const items = Array.from(selectedRecords.value).map(key => {
      const [bvid, view_at] = key.split('_')
      return {
        bvid,
        view_at: parseInt(view_at)
      }
    })

    const response = await batchDeleteHistory(items)
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message
      })
      selectedRecords.value.clear()
      await fetchHistoryByDateRange()
    } else {
      throw new Error(response.data.message || '删除失败')
    }
  } catch (error) {
    if (error.toString().includes('cancel')) return

    showNotify({
      type: 'danger',
      message: error.response?.data?.detail || error.message || '删除失败'
    })
  }
}

// 监听批量模式变化
watch(() => props.isBatchMode, (newVal) => {
  if (!newVal) {
    selectedRecords.value.clear()
  }
})

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
  console.log('HistoryContent - fetchHistoryByDateRange 被调用')
  console.log('参数:', {
    page: props.page,
    size: size.value,
    sortOrder: sortOrder.value,
    tagName: tagName.value,
    mainCategory: mainCategory.value,
    dateRange: dateRange.value,
    useLocalImages: localStorage.getItem('useLocalImages') === 'true'
  })

  try {
    records.value = []
    const response = await getBiliHistory2024(
      props.page,
      size.value,
      sortOrder.value,
      tagName.value,
      mainCategory.value,
      dateRange.value || '',
      localStorage.getItem('useLocalImages') === 'true'
    )

    console.log('API 响应:', response.data)

    if (response.data && response.data.data) {
      total.value = response.data.data.total
      records.value = response.data.data.records
      emit('update:total-pages', Math.ceil(response.data.data.total / size.value))
      emit('update:total', response.data.data.total)

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
    console.log('HistoryContent - 年份或页码变化')
    fetchHistoryByDateRange()
  },
)

// 监听父组件的 date 变化
watch(
  () => props.date,
  (newDate) => {
    console.log('HistoryContent - date prop 变化:', newDate)
    if (!newDate) {
      dateRange.value = ''
      fetchHistoryByDateRange()
    }
  }
)

// 监听父组件的 category 变化
watch(
  () => props.category,
  (newCategory) => {
    console.log('HistoryContent - category prop 变化:', newCategory)
    if (!newCategory) {
      tagName.value = ''
      mainCategory.value = ''
      fetchHistoryByDateRange()
    }
  }
)

// 获取每日统计数据
const fetchDailyStats = async (timestamp) => {
  if (!timestamp) return

  try {
    const date = new Date(timestamp * 1000)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const dateStr = `${month}${day}`

    // 如果已经有这个日期的数据，就不重复获取
    const dateKey = `${year}-${month}-${day}`
    if (dailyStats.value[dateKey]) return

    const response = await getDailyStats(dateStr, year)
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
  return dailyStats.value[dateKey]?.total_count || 0
}

onMounted(async () => {
  await fetchMainCategories()
  fetchHistoryByDateRange()
})

// 暴露方法给父组件
defineExpose({
  fetchHistoryByDateRange,
})

// 格式化分割线日期
const formatDividerDate = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const currentYear = new Date().getFullYear()
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()

  if (year === currentYear) {
    return `${month}月${day}日`
  } else {
    return `${year}年${month}月${day}日`
  }
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

// 处理视频点击
const handleVideoClick = (record) => {
  let url = ''

  switch (record.business) {
    case 'archive':
      url = `https://www.bilibili.com/video/${record.bvid}`
      break
    case 'article':
      url = `https://www.bilibili.com/read/cv${record.oid}`
      break
    case 'article-list':
      url = `https://www.bilibili.com/read/readlist/rl${record.oid}`
      break
    case 'live':
      url = `https://live.bilibili.com/${record.oid}`
      break
    case 'pgc':
      url = record.uri || `https://www.bilibili.com/bangumi/play/ep${record.epid}`
      break
    case 'cheese':
      url = record.uri || `https://www.bilibili.com/cheese/play/ep${record.epid}`
      break
    default:
      console.warn('未知的业务类型:', record.business)
      return
  }

  if (url) {
    window.open(url, '_blank')
  }
}

// 处理UP主点击
const handleAuthorClick = (record) => {
  const url = `https://space.bilibili.com/${record.author_mid}`
  window.open(url, '_blank')
}

// 格式化时长
const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完'
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0')
  const secs = String(seconds % 60).padStart(2, '0')
  return `${minutes}:${secs}`
}

// 获取业务类型
const getBusinessType = (business) => {
  const businessTypes = {
    archive: '稿件',
    cheese: '课堂',
    pgc: '电影',
    live: '直播',
    'article-list': '专栏',
    article: '专栏',
  }
  return businessTypes[business] || '其他类型'
}

// 获取进度条宽度
const getProgressWidth = (progress, duration) => {
  if (progress === -1) return '100%'
  if (duration === 0) return '0%'
  return `${(progress / duration) * 100}%`
}

// 格式化时间戳
const formatTimestamp = (timestamp) => {
  if (!timestamp) {
    console.warn('Invalid timestamp:', timestamp)
    return '时间未知'
  }

  try {
    const date = new Date(timestamp * 1000)
    const now = new Date()

    if (isNaN(date.getTime())) {
      console.warn('Invalid date from timestamp:', timestamp)
      return '时间未知'
    }

    const isToday = now.toDateString() === date.toDateString()
    const isYesterday =
      new Date(now.setDate(now.getDate() - 1)).toDateString() === date.toDateString()
    const timeString = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })

    if (isToday) {
      return timeString
    } else if (isYesterday) {
      return `昨天 ${timeString}`
    } else if (now.getFullYear() === date.getFullYear()) {
      return `${date.getMonth() + 1}-${date.getDate()} ${timeString}`
    } else {
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${timeString}`
    }
  } catch (error) {
    console.error('Error formatting timestamp:', error)
    return '时间未知'
  }
}

// 高亮显示匹配的文本
const highlightText = (text) => {
  if (!props.searchKeyword || !text) return text

  const regex = new RegExp(props.searchKeyword, 'gi')
  return text.replace(regex, match => `<span class="text-[#FF6699]">${match}</span>`)
}

// 处理删除记录
const handleDelete = async (record) => {
  try {
    await showDialog({
      title: '确认删除',
      message: '确定要删除这条记录吗？此操作不可恢复。',
      showCancelButton: true,
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      confirmButtonColor: '#fb7299'
    })

    const response = await batchDeleteHistory([{
      bvid: record.bvid,
      view_at: record.view_at
    }])
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message
      })
      fetchHistoryByDateRange()
    } else {
      throw new Error(response.data.message || '删除失败')
    }
  } catch (error) {
    if (error.toString().includes('cancel')) return

    showNotify({
      type: 'danger',
      message: error.response?.data?.detail || error.message || '删除失败'
    })
  }
}

// 判断某一天是否被全部选中
const isDaySelected = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const dayStart = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime() / 1000
  const dayEnd = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1).getTime() / 1000 - 1

  const dayRecords = records.value.filter(record =>
    record.view_at >= dayStart && record.view_at <= dayEnd
  )

  return dayRecords.every(record =>
    selectedRecords.value.has(`${record.bvid}_${record.view_at}`)
  )
}

// 切换某一天的所有记录的选中状态
const toggleDaySelection = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const dayStart = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime() / 1000
  const dayEnd = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1).getTime() / 1000 - 1

  const dayRecords = records.value.filter(record =>
    record.view_at >= dayStart && record.view_at <= dayEnd
  )

  const allSelected = isDaySelected(timestamp)

  dayRecords.forEach(record => {
    const key = `${record.bvid}_${record.view_at}`
    if (allSelected) {
      selectedRecords.value.delete(key)
    } else {
      selectedRecords.value.add(key)
    }
  })
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

// 添加打开详情对话框的方法
const openVideoDetail = (record) => {
  selectedRecord.value = record
  showDetailDialog.value = true
}

</script>
