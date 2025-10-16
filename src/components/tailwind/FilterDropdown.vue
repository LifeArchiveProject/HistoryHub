<template>
  <div class="relative">
    <!-- 筛选头部 - 所有元素在同一行 -->
    <div class="flex items-center justify-between flex-wrap py-2 px-3 rounded-md">
      <!-- 条目类型快速切换区域 -->
      <div class="flex flex-1 flex-wrap gap-1 sm:gap-2">
        <button
          v-for="(label, type) in businessTypeMap"
          :key="type"
          class="px-2 sm:px-3 py-1 sm:py-1.5 text-xs rounded-md border transition-colors duration-200"
          :class="business === type ? 'border-[#fb7299] bg-[#fb7299]/10 text-[#fb7299]' : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:border-[#fb7299]/50'"
          @click="selectBusiness(type)"
        >
          {{ label }}
        </button>
      </div>

      <!-- 右侧操作区 -->
      <div class="flex items-center space-x-2 sm:space-x-3 ml-1 sm:ml-2">
        <!-- 每页显示条数设置 -->
        <div class="flex items-center text-xs text-gray-500 dark:text-gray-400">
          <span class="mr-1">每页</span>
          <input
            type="number"
            :value="pageSize"
            @input="handlePageSizeChange"
            @blur="handlePageSizeBlur"
            min="10"
            max="100"
            class="w-12 h-6 rounded border border-gray-200 dark:border-gray-600 bg-transparent px-1 text-center text-gray-700 dark:text-gray-200 transition-colors [appearance:textfield] hover:border-[#fb7299] focus:border-[#fb7299] focus:outline-none focus:ring-1 focus:ring-[#fb7299]/30 [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
          />
          <span class="ml-1">条</span>
        </div>

        <!-- 总视频数显示 -->
        <div class="text-xs text-gray-500 dark:text-gray-400">
          总视频数: <span class="text-[#FF6699] font-medium">{{ total }}</span>
        </div>

        <!-- 筛选图标按钮 -->
        <button
          @click="showFilterPopup = true"
          class="p-1 sm:p-1.5 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
        >
          <svg class="w-4 h-4 sm:w-5 sm:h-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 底部弹出式筛选栏 -->
    <VanPopup
      v-model:show="showFilterPopup"
      position="bottom"
      round
      :z-index="2000"
      get-container="body"
      teleport="body"
      :style="{ height: '70%' }"
      class="overflow-hidden"
    >
      <div class="p-3 sm:p-4 h-full flex flex-col bg-white dark:bg-gray-900">

        <div class="flex-1 overflow-y-auto">
          <!-- 条目类型筛选 -->
          <div class="mb-4 sm:mb-6">
            <div class="flex items-center mb-2">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-200">条目类型</h4>
              <div class="flex items-center ml-2 flex-1">
                <span
                  class="text-xs sm:text-sm text-[#fb7299] font-medium truncate max-w-[80%]">{{ businessLabel || '全部'
                  }}</span>
                <button
                  v-if="business"
                  @click="clearBusiness"
                  class="ml-1 sm:ml-2 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-gray-500" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="grid grid-cols-3 gap-1.5 sm:gap-2">
              <div
                v-for="(label, type) in businessTypeMap"
                :key="type"
                class="flex items-center p-1.5 sm:p-2 rounded-lg cursor-pointer border transition-colors duration-200"
                :class="business === type ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 dark:border-gray-700 hover:border-[#fb7299]/50'"
                @click="selectBusinessFromPopup(type)"
              >
                <div class="flex-1">
                  <div class="text-xs font-medium truncate">{{ label }}</div>
                </div>
                <div v-if="business === type" class="text-[#fb7299]">
                  <svg class="w-3 h-3 sm:w-4 sm:h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          <!-- 日期筛选 -->
          <div class="mb-4 sm:mb-6">
            <div class="flex items-center mb-2">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-200">日期区间</h4>
              <div class="flex items-center ml-2 flex-1">
                <span class="text-xs sm:text-sm text-[#fb7299] font-medium truncate max-w-[80%]">{{ date || '全部'
                  }}</span>
                <button
                  v-if="date"
                  @click="clearDate"
                  class="ml-1 sm:ml-2 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-gray-500" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="flex items-center space-x-2">
              <div class="relative flex-1">
                <input
                  type="date"
                  v-model="startDate"
                  @change="onDateChange"
                  class="w-full p-1.5 sm:p-2 text-xs sm:text-sm border border-gray-300 dark:border-gray-600 bg-transparent text-gray-900 dark:text-gray-100 rounded-md focus:outline-none focus:ring-1 focus:ring-[#fb7299] focus:border-[#fb7299] cursor-pointer"
                  :max="endDate || undefined"
                />
                <label class="absolute -top-1.5 left-2 text-[10px] bg-transparent px-1 text-gray-500 dark:text-gray-400">开始日期</label>
              </div>
              <span class="text-gray-400">至</span>
              <div class="relative flex-1">
                <input
                  type="date"
                  v-model="endDate"
                  @change="onDateChange"
                  class="w-full p-1.5 sm:p-2 text-xs sm:text-sm border border-gray-300 dark:border-gray-600 bg-transparent text-gray-900 dark:text-gray-100 rounded-md focus:outline-none focus:ring-1 focus:ring-[#fb7299] focus:border-[#fb7299] cursor-pointer"
                  :min="startDate || undefined"
                />
                <label class="absolute -top-1.5 left-2 text-[10px] bg-transparent px-1 text-gray-500 dark:text-gray-400">结束日期</label>
              </div>
            </div>
          </div>

          <!-- 视频分区筛选 -->
          <div>
            <div class="flex items-center mb-2">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-200">视频分区</h4>
              <div class="flex items-center ml-2 flex-1">
                <span class="text-xs sm:text-sm text-[#fb7299] font-medium truncate max-w-[80%]">{{ category || '全部'
                  }}</span>
                <button
                  v-if="category"
                  @click="clearCategory"
                  class="ml-1 sm:ml-2 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"
                >
                  <svg class="w-3 h-3 sm:w-4 sm:h-4 text-gray-500" fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- 分区选择器 -->
            <div class="border border-gray-300 dark:border-gray-600 rounded-md overflow-hidden">
              <!-- 主分区选择 -->
              <div class="flex h-48 sm:h-56">
                <div class="w-1/3 border-r border-gray-300 dark:border-gray-600 overflow-y-auto bg-transparent">
                  <div
                    v-for="(category, index) in videoCategories"
                    :key="category.text"
                    class="p-1.5 sm:p-2 text-xs sm:text-sm cursor-pointer transition-colors duration-200 truncate"
                    :class="activeMainCategory === index ? 'bg-[#fb7299]/10 text-[#fb7299] font-medium' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'"
                    @click="activeMainCategory = index"
                  >
                    {{ category.text }}
                  </div>
                </div>

                <!-- 子分区选择 -->
                <div class="w-2/3 overflow-y-auto bg-transparent">
                  <div class="grid grid-cols-2 gap-1.5 sm:gap-2 p-1 sm:p-2">
                    <!-- 主分区选项 -->
                    <div
                      class="p-1 sm:p-2 text-xs sm:text-sm border rounded-md cursor-pointer transition-colors duration-200 truncate"
                      :class="category === videoCategories[activeMainCategory]?.text ? 'border-[#fb7299] bg-[#fb7299]/10 text-[#fb7299]' : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'"
                      @click="selectVideoCategory({text: videoCategories[activeMainCategory]?.text, type: 'main'})"
                    >
                      {{ videoCategories[activeMainCategory]?.text || '全部' }}
                    </div>

                    <!-- 子分区选项 -->
                    <div
                      v-for="subCategory in videoCategories[activeMainCategory]?.children"
                      :key="subCategory.id"
                      class="p-1 sm:p-2 text-xs sm:text-sm border rounded-md cursor-pointer transition-colors duration-200 truncate"
                      :class="category === subCategory.text ? 'border-[#fb7299] bg-[#fb7299]/10 text-[#fb7299]' : 'border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'"
                      @click="selectVideoCategory(subCategory)"
                    >
                      {{ subCategory.text }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </VanPopup>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { showNotify, Popup as VanPopup } from 'vant'
import 'vant/es/popup/style'
import 'vant/es/notify/style'

const props = defineProps({
  business: {
    type: String,
    default: '',
  },
  businessLabel: {
    type: String,
    default: '',
  },
  date: {
    type: String,
    default: '',
  },
  category: {
    type: String,
    default: '',
  },
  total: {
    type: Number,
    default: 0,
  },
  pageSize: {
    type: Number,
    default: 30,
  },
})

const emit = defineEmits([
  'update:business',
  'update:businessLabel',
  'update:date',
  'update:category',
  'update:pageSize',
  'refresh-data',
])

// 底部弹出筛选栏的显示状态
const showFilterPopup = ref(false)

// 日期选择相关
const startDate = ref('')
const endDate = ref('')

// 视频分区选择相关
const videoCategories = ref([])
const activeMainCategory = ref(0)

// 获取视频分类
const fetchVideoCategories = async () => {
  try {
    const { getVideoCategories } = await import('../../api/api.js')
    const response = await getVideoCategories()
    if (response.data.status === 'success') {
      videoCategories.value = response.data.data.map((category) => ({
        text: category.name,
        type: 'main',
        children: category.sub_categories.map((sub) => ({
          text: sub.name,
          id: sub.tid,
          type: 'sub',
        })),
      }))
    }
  } catch (error) {
    console.error('获取视频分类失败:', error)
  }
}

// 选择视频分区
const selectVideoCategory = (item) => {
  const isMainName = videoCategories.value.some(cat =>
    cat.text === item.text && item.type === 'main',
  )

  let categoryText = ''
  if (item.type === 'main' || (item.type === 'sub' && isMainName)) {
    categoryText = item.text
  } else if (item.type === 'sub') {
    categoryText = item.text
  }

  // 打印日志，帮助调试
  console.log('选择分区:', {
    item,
    categoryText,
    isMainName,
  })

  // 先更新分类，然后重置页码
  emit('update:category', categoryText)

  // 重置页码到第一页，而不是触发实时更新
  emit('update:page', 1)

  showNotify({
    type: 'success',
    message: `已筛选分区: ${categoryText || '全部'}`,
    duration: 1000,
  })
}

// 监听日期属性变化，解析为开始和结束日期
watch(() => props.date, (newDate) => {
  if (newDate) {
    const dates = newDate.split(' 至 ')
    if (dates.length === 2) {
      startDate.value = formatDateForInput(dates[0])
      endDate.value = formatDateForInput(dates[1])
    }
  } else {
    startDate.value = ''
    endDate.value = ''
  }
}, { immediate: true })

// 格式化日期为输入框格式 (YYYY-MM-DD)
const formatDateForInput = (dateStr) => {
  try {
    const parts = dateStr.split('/')
    if (parts.length === 3) {
      return `${parts[0]}-${parts[1].padStart(2, '0')}-${parts[2].padStart(2, '0')}`
    }
    return ''
  } catch (e) {
    return ''
  }
}

// 格式化日期为显示格式 (YYYY/MM/DD)
const formatDateForDisplay = (dateStr) => {
  try {
    const date = new Date(dateStr)
    if (isNaN(date.getTime())) return ''
    return `${date.getFullYear()}/${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`
  } catch (e) {
    console.error('日期格式化错误:', e)
    return ''
  }
}

// 业务类型映射表
const businessTypeMap = {
  '': '全部',
  'archive': '普通视频',
  'pgc': '番剧',
  'live': '直播',
  'article': '文章',
  'article-list': '文集',
}

// 选择业务类型（快速切换区域）
const selectBusiness = (type) => {
  emit('update:business', type)
  emit('update:businessLabel', businessTypeMap[type])
  // 移除实时更新触发，改为只更新当前数据
  emit('update:page', 1) // 重置页码到第一页

  showNotify({
    type: 'success',
    message: `已切换到${businessTypeMap[type]}`,
    duration: 1000,
  })
}

// 从弹出窗口选择业务类型
const selectBusinessFromPopup = (type) => {
  emit('update:business', type)
  emit('update:businessLabel', businessTypeMap[type])
  // 移除实时更新触发，改为只更新当前数据
  emit('update:page', 1) // 重置页码到第一页

  showNotify({
    type: 'success',
    message: `已切换到${businessTypeMap[type]}`,
    duration: 1000,
  })
}

// 应用日期筛选
const applyDateFilter = () => {
  if (startDate.value && endDate.value) {
    const formattedStartDate = formatDateForDisplay(startDate.value)
    const formattedEndDate = formatDateForDisplay(endDate.value)

    if (formattedStartDate && formattedEndDate) {
      const dateRange = `${formattedStartDate} 至 ${formattedEndDate}`
      console.log('设置日期区间:', dateRange)
      emit('update:date', dateRange)
      emit('update:page', 1) // 重置页码到第一页，而不是触发实时更新

      showNotify({
        type: 'success',
        message: `已筛选日期: ${dateRange}`,
        duration: 1000,
      })
    } else {
      showNotify({
        type: 'warning',
        message: '日期格式无效',
        duration: 2000,
      })

    }
  } else if (!startDate.value && !endDate.value) {
    // 如果两个日期都为空，清除筛选
    emit('update:date', '')
    emit('update:page', 1) // 重置页码到第一页，而不是触发实时更新
  } else {
    // 如果只有一个日期，显示提示
    showNotify({
      type: 'warning',
      message: '请同时设置开始和结束日期',
      duration: 2000,
    })

  }
}

// 处理日期变化
const onDateChange = () => {
  applyDateFilter()
}

// 清除分区
const clearCategory = () => {
  console.log('清除分区筛选')
  // 先更新分类，然后重置页码
  emit('update:category', '')
  emit('update:page', 1) // 重置页码到第一页，而不是触发实时更新

  showNotify({
    type: 'success',
    message: '已清除分区筛选',
    duration: 1000,
  })
}

// 清除日期
const clearDate = () => {
  console.log('清除日期筛选')
  // 先更新日期，然后重置页码
  emit('update:date', '')
  emit('update:page', 1) // 重置页码到第一页，而不是触发实时更新

  showNotify({
    type: 'success',
    message: '已清除日期筛选',
    duration: 1000,
  })
}

// 清除业务类型
const clearBusiness = () => {
  console.log('清除业务类型筛选')
  // 先更新业务类型，然后重置页码
  emit('update:business', '')
  emit('update:businessLabel', '')
  emit('update:page', 1) // 重置页码到第一页，而不是触发实时更新

  showNotify({
    type: 'success',
    message: '已清除业务类型筛选',
    duration: 1000,
  })
}

// 处理每页条数变化
const handlePageSizeChange = (event) => {
  const value = parseInt(event.target.value)
  if (!isNaN(value) && value >= 10 && value <= 100) {
    emit('update:pageSize', value)
  }
}

// 处理输入框失焦
const handlePageSizeBlur = (event) => {
  let value = parseInt(event.target.value)
  if (isNaN(value) || value < 10) {
    value = 10
  } else if (value > 100) {
    value = 100
  }
  emit('update:pageSize', value)
  // 不调用 refresh-data，因为 pageSize 的 watch 会自动触发 fetchHistoryByDateRange
}

// 组件挂载时获取视频分类
onMounted(() => {
  fetchVideoCategories()
})
</script>

<style scoped>
/* 可以添加自定义样式 */

/* 确保日期输入框在移动设备上正常工作 */
input[type="date"] {
  -webkit-appearance: none;
  appearance: none;
  position: relative;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}
</style>
