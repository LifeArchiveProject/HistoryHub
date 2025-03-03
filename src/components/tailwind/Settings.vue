<template>
  <div class="min-h-screen bg-gray-50/30">
    <div class="py-4">
      <div class="max-w-7xl mx-auto px-3">
        <!-- 页面标题 -->
        <div class="flex items-center space-x-2 text-gray-900 mb-4">
          <div class="p-1.5 bg-[#fb7299]/5 rounded-lg">
            <svg class="w-6 h-6 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <h1 class="text-2xl font-medium bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">设置</h1>
        </div>

        <!-- 基础设置分类 -->
        <div class="mb-6">
          <h2 class="text-lg font-medium text-gray-900 mb-3 flex items-center space-x-2">
            <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
            </svg>
            <span>基础设置</span>
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- 服务器配置卡片 -->
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all duration-300">
              <div class="p-4">
                <div class="flex items-center space-x-2 text-gray-900 mb-2">
                  <div class="p-1.5 bg-[#fb7299]/5 rounded-lg">
                    <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
                    </svg>
                  </div>
                  <h2 class="text-lg font-medium">服务器配置</h2>
                </div>
                <p class="text-sm text-gray-500 mb-3">配置API服务器地址，修改后将自动刷新页面</p>

                <div class="space-y-2">
                  <div class="flex flex-col space-y-2">
                    <label for="serverUrl" class="text-sm font-medium text-gray-700">服务器地址</label>
                    <div class="flex space-x-2">
                      <input
                        id="serverUrl"
                        v-model="serverUrl"
                        type="text"
                        class="flex-1 block rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
                        placeholder="例如：http://localhost:8899"
                      />
                      <button
                        @click="resetServerUrl"
                        class="inline-flex items-center px-3 py-2 text-sm font-medium text-[#fb7299] bg-[#fb7299]/5 rounded-lg hover:bg-[#fb7299]/10 focus:outline-none focus:ring-2 focus:ring-[#fb7299]/20"
                        title="重置为默认地址"
                      >
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                      </button>
                      <button
                        @click="saveServerUrl"
                        class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90 focus:outline-none focus:ring-2 focus:ring-[#fb7299]/20"
                      >
                        保存
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 图片源设置卡片 -->
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all duration-300">
              <div class="p-4">
                <div class="flex items-center space-x-2 text-gray-900 mb-2">
                  <div class="p-1.5 bg-[#fb7299]/5 rounded-lg">
                    <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <h2 class="text-lg font-medium">图片源设置</h2>
                </div>
                <p class="text-sm text-gray-500 mb-3">选择使用本地图片源或在线图片源，本地图片源适合离线访问</p>

                <div class="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                  <span class="text-sm font-medium text-gray-700">使用本地图片源</span>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="useLocalImages" class="sr-only peer" @change="handleImageSourceChange">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#fb7299]"></div>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AI摘要配置 -->
        <div class="mb-6">
          <h2 class="text-lg font-medium text-gray-900 mb-3 flex items-center space-x-2">
            <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>AI摘要配置</span>
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all duration-300">
              <SummaryConfig />
            </div>
          </div>
        </div>

        <!-- 数据管理分类 -->
        <div class="mb-6">
          <h2 class="text-lg font-medium text-gray-900 mb-3 flex items-center space-x-2">
            <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
            </svg>
            <span>数据管理</span>
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- 数据导出卡片 -->
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all duration-300">
              <div class="p-4">
                <div class="flex items-center space-x-2 text-gray-900 mb-2">
                  <div class="p-1.5 bg-[#fb7299]/5 rounded-lg">
                    <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <h2 class="text-lg font-medium">数据导出</h2>
                </div>
                <p class="text-sm text-gray-500 mb-3">导出历史记录数据到Excel文件，支持按年份导出</p>

                <div class="flex items-center space-x-4 bg-gray-50 p-3 rounded-lg">
                  <select
                    v-model="selectedYear"
                    class="block w-32 rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm bg-white"
                  >
                    <option v-for="year in availableYears" :key="year" :value="year">
                      {{ year }}年
                    </option>
                  </select>

                  <button
                    @click="exportAndDownloadExcel"
                    :disabled="isExporting"
                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90 focus:outline-none focus:ring-2 focus:ring-[#fb7299]/20 disabled:opacity-50 disabled:cursor-not-allowed"
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
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all duration-300">
              <div class="p-4">
                <div class="flex items-center space-x-2 text-gray-900 mb-2">
                  <div class="p-1.5 bg-[#fb7299]/5 rounded-lg">
                    <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                    </svg>
                  </div>
                  <h2 class="text-lg font-medium">数据库下载</h2>
                </div>
                <p class="text-sm text-gray-500 mb-3">下载完整的SQLite数据库文件，包含所有历史记录数据</p>

                <div class="bg-gray-50 p-3 rounded-lg">
                  <button
                    @click="downloadSqlite"
                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-lg hover:bg-[#fb7299]/90 focus:outline-none focus:ring-2 focus:ring-[#fb7299]/20 w-full justify-center"
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

        <!-- 危险操作分类 -->
        <div>
          <h2 class="text-lg font-medium text-gray-900 mb-3 flex items-center space-x-2">
            <svg class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <span>危险操作</span>
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- 数据库重置卡片 -->
            <div class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-all duration-300">
              <div class="p-4">
                <div class="flex items-center space-x-2 text-gray-900 mb-2">
                  <div class="p-1.5 bg-red-50 rounded-lg">
                    <svg class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </div>
                  <h2 class="text-lg font-medium">数据库重置</h2>
                </div>
                <p class="text-sm text-gray-500 mb-3">由于本地存储的有原始的历史记录数据文件，所以删除现有数据库并重新导入数据并不会丢失数据，目的是用于解决数据异常问题（此操作不可逆）</p>

                <div class="bg-red-50 p-3 rounded-lg">
                  <button
                    @click="handleResetDatabase"
                    class="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-red-500 rounded-lg hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500/20 w-full justify-center"
                  >
                    <svg class="mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    重置数据库
                  </button>
                </div>
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
import { showDialog, showNotify } from 'vant'
import { getCurrentBaseUrl, setBaseUrl, resetDatabase, getAvailableYears, importSqliteData, exportHistory, downloadExcelFile, downloadDatabase } from '../../api/api'
import 'vant/es/dialog/style'
import 'vant/es/notify/style'
import SummaryConfig from './SummaryConfig.vue'

const selectedYear = ref(new Date().getFullYear())
const availableYears = ref([])
const isExporting = ref(false)
const serverUrl = ref('')
const useLocalImages = ref(localStorage.getItem('useLocalImages') === 'true')

// 初始化服务器地址
onMounted(async () => {
  serverUrl.value = getCurrentBaseUrl()
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

// 保存服务器地址
const saveServerUrl = () => {
  try {
    // 简单的URL格式验证
    const url = new URL(serverUrl.value)
    setBaseUrl(serverUrl.value)
    showNotify({
      type: 'success',
      message: '服务器地址已更新，页面即将刷新'
    })
  } catch (error) {
    showNotify({
      type: 'danger',
      message: '请输入有效的URL地址'
    })
  }
}

// 在script setup部分添加重置功能
const DEFAULT_SERVER_URL = 'http://localhost:8899'

// 重置服务器地址
const resetServerUrl = () => {
  showDialog({
    title: '重置服务器地址',
    message: '确定要将服务器地址重置为默认值吗？',
    showCancelButton: true,
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    confirmButtonColor: '#fb7299'
  }).then((result) => {
    if (result === 'confirm') {
      serverUrl.value = DEFAULT_SERVER_URL
      setBaseUrl(DEFAULT_SERVER_URL)
      showNotify({
        type: 'success',
        message: '服务器地址已重置，页面即将刷新'
      })
    }
  })
}

// 处理数据库重置
const handleResetDatabase = () => {
  showDialog({
    title: '危险操作确认',
    message: '此操作将删除现有数据库并重新导入数据。此操作不可逆，确定要继续吗？',
    showCancelButton: true,
    confirmButtonText: '确定重置',
    cancelButtonText: '取消',
    confirmButtonColor: '#dc2626'
  }).then(async (result) => {
    if (result === 'confirm') {
      try {
        showNotify({
          type: 'warning',
          message: '正在重置数据库...'
        })

        // 重置数据库
        const resetResponse = await resetDatabase()
        if (resetResponse.data.status === 'success') {
          showNotify({
            type: 'success',
            message: '数据库已重置，正在重新导入数据...'
          })

          // 重新导入数据
          try {
            const importResponse = await importSqliteData()
            if (importResponse.data.status === 'success') {
              showNotify({
                type: 'success',
                message: '数据导入完成，页面即将刷新'
              })
              // 等待1秒后刷新页面，确保用户看到成功提示
              setTimeout(() => {
                window.location.reload()
              }, 1000)
            } else {
              throw new Error(importResponse.data.message || '数据导入失败')
            }
          } catch (importError) {
            showNotify({
              type: 'danger',
              message: `数据导入失败：${importError.message}`
            })
          }
        }
      } catch (error) {
        showNotify({
          type: 'danger',
          message: `重置失败：${error.message}`
        })
      }
    }
  })
}

// 处理图片源变更
const handleImageSourceChange = () => {
  localStorage.setItem('useLocalImages', useLocalImages.value.toString())
  showNotify({
    type: 'success',
    message: `已${useLocalImages.value ? '启用' : '禁用'}本地图片源`
  })
  // 刷新页面以应用新设置
  window.location.reload()
}
</script>
