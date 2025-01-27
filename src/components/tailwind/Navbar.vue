<template>
  <div class="sticky top-0 z-50">
    <nav class="bg-white lg:pt-4">
      <div class="mx-auto max-w-4xl">
        <div class="flex h-10 items-center gap-2 sm:gap-6 px-2">
          <!-- 搜索框 -->
          <div class="flex-1 max-w-[85%]">
            <SearchBar />
          </div>

          <!-- 实时更新按钮 -->
          <button
            @click="handleUpdate"
            :disabled="isUpdating"
            class="flex items-center px-2 sm:px-3 py-2 text-gray-700 hover:text-[#fb7299] transition-colors duration-200 whitespace-nowrap"
          >
            <svg
              :class="{'animate-spin': isUpdating}"
              class="w-5 h-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                v-if="isUpdating"
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                v-if="isUpdating"
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
              <path
                v-if="!isUpdating"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              ></path>
            </svg>
            <span class="ml-2 hidden sm:inline">{{ isUpdating ? '更新中' : '实时更新' }}</span>
          </button>

          <!-- 隐私模式按钮 -->
          <button
            @click="togglePrivacyMode"
            class="sm:hidden flex items-center px-3 py-2 text-gray-700 hover:text-[#fb7299] transition-colors duration-200 whitespace-nowrap"
          >
            <svg 
              class="w-5 h-5" 
              fill="none" 
              viewBox="0 0 256 256"
              :stroke="isPrivacyMode ? '#fb7299' : 'currentColor'"
            >
              <path 
                d="M128,56C48,56,8,128,8,128s40,72,120,72s120-72,120-72S208,56,128,56Z" 
                :class="isPrivacyMode ? 'hidden' : 'block'"
                fill="none" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="16"
              />
              <circle 
                cx="128" 
                cy="128" 
                r="32"
                :class="isPrivacyMode ? 'hidden' : 'block'"
                fill="none" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="16"
              />
              <path 
                d="M48,40L208,216"
                :class="isPrivacyMode ? 'block' : 'hidden'"
                fill="none" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="16"
              />
              <path 
                d="M154.9,157.6A32,32,0,0,1,97.6,100.3"
                :class="isPrivacyMode ? 'block' : 'hidden'"
                fill="none" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="16"
              />
              <path 
                d="M183.9,186.1C165.9,197.5,147.2,204,128,204,48,204,8,132,8,132s15.3-27.4,41.9-48.5"
                :class="isPrivacyMode ? 'block' : 'hidden'"
                fill="none" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="16"
              />
              <path 
                d="M90.1,97.5a38.5,38.5,0,0,0-1.1,4.5"
                :class="isPrivacyMode ? 'block' : 'hidden'"
                fill="none" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="16"
              />
              <path 
                d="M165.8,166.2a37.2,37.2,0,0,0,4.2-1.2"
                :class="isPrivacyMode ? 'block' : 'hidden'"
                fill="none" 
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="16"
              />
            </svg>
          </button>

          <!-- 布局切换按钮 -->
          <div class="hidden sm:flex items-center border border-gray-200/50 rounded-lg">
            <button
              @click="$emit('change-layout', 'list')"
              class="px-2 py-2 transition-colors duration-200"
              :class="layout === 'list' ? 'text-[#fb7299]' : 'text-gray-600 hover:text-[#fb7299]'"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <button
              @click="$emit('change-layout', 'grid')"
              class="px-2 py-2 transition-colors duration-200"
              :class="layout === 'grid' ? 'text-[#fb7299]' : 'text-gray-600 hover:text-[#fb7299]'"
            >
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 筛选栏位 -->
      <div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-md dark:border-gray-700">
        <div class="mx-auto max-w-4xl">
          <div class="p-2 grid grid-cols-3 gap-4 text-lg text-gray-700 dark:text-gray-300 lm:text-sm">
            <!-- 日期区间 -->
            <div class="flex items-center justify-start space-x-1 cursor-pointer hover:text-[#fb7299] transition-colors duration-200" @click="$emit('click-date')">
              <span>日期区间:</span>
              <span class="text-xs text-[#FF6699]">{{ date || '全部' }}</span>
              <button
                v-if="date"
                @click.stop="clearDate"
                class="text-gray-400 hover:text-[#fb7299] transition-colors duration-200"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- 视频分区 -->
            <div class="flex items-center justify-center space-x-1 cursor-pointer hover:text-[#fb7299] transition-colors duration-200" @click="$emit('click-category')">
              <span>视频分区:</span>
              <span class="text-xs text-[#FF6699]">{{ category || '全部' }}</span>
              <button
                v-if="category"
                @click.stop="clearCategory"
                class="text-gray-400 hover:text-[#fb7299] transition-colors duration-200"
              >
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <!-- 总计视频数量显示 -->
            <div class="flex items-center justify-end space-x-1 text-lg text-gray-700 dark:text-gray-300 lm:text-sm">
              <span>总视频数:</span>
              <span class="text-xs text-[#FF6699]">{{ total }}</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import SearchBar from './SearchBar.vue'
import { ref } from 'vue'
import { updateBiliHistoryRealtime } from '../../api/api'
import { showNotify } from 'vant'
import { usePrivacyStore } from '../../store/privacy'
import 'vant/es/notify/style'

const props = defineProps({
  date: {
    type: String,
    default: ''
  },
  total: {
    type: Number,
    default: 0
  },
  category: {
    type: String,
    default: ''
  },
  isUpdating: {
    type: Boolean,
    default: false
  },
  layout: {
    type: String,
    default: 'list'
  }
})

const emit = defineEmits([
  'click-date', 
  'click-category', 
  'change-layout',
  'update:date',
  'update:category',
  'refresh-data'
])

const isUpdating = ref(false)

// 隐私模式状态
const { isPrivacyMode, togglePrivacyMode } = usePrivacyStore()

const handleUpdate = async () => {
  if (isUpdating.value) return

  isUpdating.value = true
  try {
    console.log('开始请求实时更新')
    const response = await updateBiliHistoryRealtime()
    console.log('实时更新响应:', response)

    if (response?.data) {
      if (response.data.status === 'success') {
        const message = response.data.message
        const importMatch = message.match(/成功导入\s*(\d+)\s*条记录到SQLite数据库/)
        const importCount = importMatch ? importMatch[1] : '0'

        showNotify({
          type: 'success',
          message: '成功导入 ' + importCount + ' 条记录到SQLite数据库',
          duration: 3500,
        })
        console.log('触发 refresh-data 事件')
        emit('refresh-data')
      } else {
        showNotify({
          type: 'warning',
          message: response.data.message || '更新未完成',
          duration: 3500,
        })
      }
    } else {
      throw new Error('响应格式错误')
    }
  } catch (error) {
    console.error('更新失败详细信息:', error)

    let errorMessage = '更新失败，请稍后重试'
    if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.message) {
      errorMessage = error.message
    }

    showNotify({
      type: 'danger',
      message: errorMessage,
      duration: 3500,
    })
  } finally {
    console.log('更新流程结束')
    isUpdating.value = false
  }
}

// 添加单独的清除方法
const clearDate = () => {
  console.log('清除日期')
  emit('update:date', '')
  emit('refresh-data')
}

const clearCategory = () => {
  console.log('清除分区')
  emit('update:category', '')
  emit('refresh-data')
}
</script>

<style scoped>
/* 如果需要添加特定样式可以在这里添加 */
</style>
