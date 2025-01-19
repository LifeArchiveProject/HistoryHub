<template>
  <div>
    <nav class="fixed left-0 right-0 top-0 z-50 bg-white dark:bg-gray-800">
      <!-- 顶部导航栏 -->
      <div class="mx-auto max-w-7xl">
        <div class="flex h-10 justify-between items-center">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="flex items-center space-x-2">
              <svg class="h-8 w-8 text-gray-900 dark:text-white hidden sm:block" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
                <path fill="currentColor" d="M306.005333 117.632L444.330667 256h135.296l138.368-138.325333a42.666667 42.666667 0 0 1 60.373333 60.373333L700.330667 256H789.333333A149.333333 149.333333 0 0 1 938.666667 405.333333v341.333334a149.333333 149.333333 0 0 1-149.333334 149.333333h-554.666666A149.333333 149.333333 0 0 1 85.333333 746.666667v-341.333334A149.333333 149.333333 0 0 1 234.666667 256h88.96L245.632 177.962667a42.666667 42.666667 0 0 1 60.373333-60.373334zM789.333333 341.333333h-554.666666a64 64 0 0 0-63.701334 57.856L170.666667 405.333333v341.333334a64 64 0 0 0 57.856 63.701333L234.666667 810.666667h554.666666a64 64 0 0 0 63.701334-57.856L853.333333 746.666667v-341.333334A64 64 0 0 0 789.333333 341.333333zM341.333333 469.333333a42.666667 42.666667 0 0 1 42.666667 42.666667v85.333333a42.666667 42.666667 0 0 1-85.333333 0v-85.333333a42.666667 42.666667 0 0 1 42.666666-42.666667z m341.333334 0a42.666667 42.666667 0 0 1 42.666666 42.666667v85.333333a42.666667 42.666667 0 0 1-85.333333 0v-85.333333a42.666667 42.666667 0 0 1 42.666667-42.666667z"></path>
              </svg>
              <span class="text-lg font-semibold text-gray-900 dark:text-white hidden sm:block">B站历史记录</span>
            </router-link>
          </div>

          <!-- 搜索框 -->
          <div class="flex-1 max-w-2xl smd:mx-4 mx-2">
            <SearchBar />
          </div>

          <!-- 实时更新按钮 -->
          <div class="flex-shrink-0 smd:mr-4 ml-4">
            <button
              @click="handleUpdate"
              :disabled="isUpdating"
              class="inline-flex h-8 sm:h-10 items-center text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-300 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg
                :class="{'animate-spin': isUpdating}"
                class="w-4 h-4 sm:w-5 sm:h-5 mr-1"
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
              <span class="hidden sm:inline">{{ isUpdating ? '更新中' : '实时更新' }}</span>
            </button>
          </div>

          <!-- 年度总结入口（桌面端） -->
          <div class="flex-shrink-0 hidden sm:block">
            <router-link
              to="/analytics"
              class="inline-flex h-8 sm:h-10 items-center rounded-lg border border-transparent px-2 sm:px-3 text-sm text-white bg-gradient-to-r from-[#FF6699] to-[#FF9966] hover:from-[#FF5588] hover:to-[#FF8855] transition-all duration-300"
            >
              <svg class="w-4 h-4 sm:w-5 sm:h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              <span>年度总结</span>
            </router-link>
          </div>
        </div>
      </div>

      <!-- 筛选栏位 -->
      <div class="bg-white dark:bg-gray-800">
        <div class="mx-auto max-w-4xl px-2">
          <div class="py-2 flex justify-between text-lg text-gray-700 dark:text-gray-300 lm:text-sm">
            <div class="space-x-1" @click="$emit('click-date')">
              <span>日期区间:</span>
              <span class="text-xs text-[#FF6699]">{{ date }}</span>
            </div>

            <!-- 总计视频数量显示 -->
            <div class="space-x-1">
              <span>总视频数:</span>
              <span class="text-xs text-[#FF6699]">{{ total }}</span>
            </div>

            <div class="space-x-1" @click="$emit('click-category')">
              <span>视频分区:</span>
              <span class="text-xs text-[#FF6699]">{{ category || '全部分区' }}</span>
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
import 'vant/es/notify/style'

const props = defineProps({
  date: {
    type: String,
    default: ''
  },
  total: {
    type: [Number, String],
    default: 0
  },
  category: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['refresh-data', 'click-date', 'click-category'])
const isUpdating = ref(false)

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
</script>

<style scoped>
/* 如果需要添加特定样式可以在这里添加 */
</style>
