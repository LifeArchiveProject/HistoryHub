<template>
  <div class="min-h-screen bg-gray-50/30">
    <div class="py-6">
      <div class="max-w-5xl mx-auto px-4">
        <div class="flex items-center space-x-3 text-gray-900">
          <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <h1 class="text-2xl font-medium">设置</h1>
        </div>
        
        <div class="mt-6 space-y-6">
          <!-- 数据导出卡片 -->
          <div class="bg-white border border-gray-200 rounded-lg">
            <div class="p-6">
              <div class="flex items-center space-x-3 text-gray-900">
                <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h2 class="text-lg font-medium">数据导出</h2>
              </div>
              <p class="mt-2 text-sm text-gray-500">导出历史记录数据到Excel文件，支持按年份导出</p>
              
              <div class="mt-6 flex items-center space-x-4">
                <select
                  v-model="selectedYear"
                  class="block w-32 rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                >
                  <option v-for="year in availableYears" :key="year" :value="year">
                    {{ year }}年
                  </option>
                </select>
                
                <button
                  @click="exportAndDownloadExcel"
                  :disabled="isExporting"
                  class="inline-flex items-center px-4 py-2 text-sm font-medium text-[#fb7299] bg-[#fb7299]/5 rounded-lg hover:bg-[#fb7299]/10 focus:outline-none focus:ring-2 focus:ring-[#fb7299]/20 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <svg
                    v-if="isExporting"
                    class="animate-spin -ml-1 mr-2 h-4 w-4"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      class="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      stroke-width="4"
                    ></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isExporting ? '导出中...' : '导出Excel' }}
                </button>
              </div>
            </div>
          </div>

          <!-- 数据库下载卡片 -->
          <div class="bg-white border border-gray-200 rounded-lg">
            <div class="p-6">
              <div class="flex items-center space-x-3 text-gray-900">
                <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                </svg>
                <h2 class="text-lg font-medium">数据库下载</h2>
              </div>
              <p class="mt-2 text-sm text-gray-500">下载完整的SQLite数据库文件，包含所有历史记录数据</p>
              
              <div class="mt-6">
                <button
                  @click="downloadSqlite"
                  class="inline-flex items-center px-4 py-2 text-sm font-medium text-[#fb7299] bg-[#fb7299]/5 rounded-lg hover:bg-[#fb7299]/10 focus:outline-none focus:ring-2 focus:ring-[#fb7299]/20"
                >
                  <svg class="mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  下载SQLite数据库
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showNotify } from 'vant'
import { 
  exportHistory, 
  downloadExcelFile, 
  downloadDatabase,
  getAvailableYears
} from '../../api/api'

const selectedYear = ref(new Date().getFullYear())
const availableYears = ref([])
const isExporting = ref(false)

// 获取可用年份
onMounted(async () => {
  try {
    const response = await getAvailableYears()
    if (response.data.status === 'success') {
      availableYears.value = response.data.data.sort((a, b) => b - a) // 降序排列
      // 如果有可用年份，将选中年份设置为最新的年份
      if (availableYears.value.length > 0) {
        selectedYear.value = availableYears.value[0]
      }
    } else {
      throw new Error(response.data.message || '获取年份列表失败')
    }
  } catch (error) {
    console.error('获取可用年份失败:', error)
    showNotify({
      type: 'danger',
      message: '获取年份列表失败'
    })
    // 设置默认年份范围
    availableYears.value = [new Date().getFullYear()]
  }
})

// 导出并下载Excel
const exportAndDownloadExcel = async () => {
  if (isExporting.value) return
  
  try {
    isExporting.value = true
    showNotify({
      type: 'primary',
      message: '正在导出数据...'
    })
    
    const response = await exportHistory(selectedYear.value)
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: '导出成功，准备下载...'
      })
      
      await downloadExcelFile(selectedYear.value)
      showNotify({
        type: 'success',
        message: '下载完成'
      })
    } else {
      throw new Error(response.data.message)
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `操作失败：${error.message}`
    })
  } finally {
    isExporting.value = false
  }
}

// 下载SQLite数据库
const downloadSqlite = async () => {
  try {
    await downloadDatabase()
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `下载失败：${error.message}`
    })
  }
}
</script> 