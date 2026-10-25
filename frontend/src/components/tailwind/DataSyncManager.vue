<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50" v-if="showModal">
    <div class="bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-100 p-6 rounded-lg shadow-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto border border-gray-200 dark:border-gray-700">
      <!-- 头部标题 -->
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100">{{ currentTab === 'sync' ? '数据同步' : '数据完整性检查' }}</h2>
        <button @click="closeModal" class="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>

      <!-- 导航标签 -->
      <div class="flex border-b mb-4">
        <button
          @click="currentTab = 'sync'"
          class="py-2 px-4 font-medium text-sm transition-colors duration-200"
          :class="currentTab === 'sync' ? 'text-pink-500 border-b-2 border-pink-500' : 'text-gray-600 hover:text-pink-400'"
        >
          数据同步
        </button>
        <button
          @click="currentTab = 'integrity'"
          class="py-2 px-4 font-medium text-sm transition-colors duration-200"
          :class="currentTab === 'integrity' ? 'text-pink-500 border-b-2 border-pink-500' : 'text-gray-600 hover:text-pink-400'"
        >
          数据完整性检查
        </button>
      </div>

      <!-- 数据同步面板 -->
      <div v-if="currentTab === 'sync'">
        <div class="mb-4">
          <p class="text-sm text-gray-600 mb-2">同步数据库和JSON文件之间的历史记录数据。</p>

          <div class="flex flex-col sm:flex-row gap-4 mb-4">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">数据库路径</label>
              <input
                v-model="dbPath"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-pink-500 focus:border-pink-500 text-sm dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">JSON文件路径</label>
              <input
                v-model="jsonPath"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-pink-500 focus:border-pink-500 text-sm dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
          </div>

          <button
            @click="startSync"
            class="w-full bg-pink-600 hover:bg-pink-700 text-white font-medium py-2 px-4 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isSyncing"
          >
            <span v-if="isSyncing" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              数据同步中...
            </span>
            <span v-else>开始同步</span>
          </button>
        </div>

        <!-- 同步结果显示 -->
        <div v-if="syncResult" class="mt-6 border-t pt-4">
          <h3 class="font-medium text-gray-900 mb-2">最近同步结果</h3>
          <div class="bg-gray-50 dark:bg-gray-900 p-3 rounded-md border border-gray-200 dark:border-gray-700">
            <div class="grid grid-cols-2 gap-2 mb-3">
              <div class="text-sm">
                <span class="text-gray-500">同步时间：</span>
                <span class="text-gray-900 dark:text-gray-100">{{ formatDateTime(syncResult.timestamp) }}</span>
              </div>
              <div class="text-sm">
                <span class="text-gray-500">总同步记录：</span>
                <span class="text-gray-900 dark:text-gray-100 font-medium">{{ syncResult.total_synced }}</span>
              </div>
              <div class="text-sm">
                <span class="text-gray-500">JSON导入数据库：</span>
                <span class="text-gray-900">{{ syncResult.json_to_db_count }}</span>
              </div>
              <div class="text-sm">
                <span class="text-gray-500">数据库导出JSON：</span>
                <span class="text-gray-900 dark:text-gray-100">{{ syncResult.db_to_json_count }}</span>
              </div>
            </div>

            <div v-if="syncResult.synced_days && syncResult.synced_days.length > 0">
              <h4 class="text-sm font-medium text-gray-700 mb-2">同步的日期</h4>
              <div class="max-h-48 overflow-y-auto bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700">
                <div v-for="(day, index) in syncResult.synced_days" :key="index" class="p-2 text-sm border-b last:border-b-0">
                  <div class="flex justify-between items-center mb-1">
                    <div>
                      <span class="font-medium">{{ day.date }}</span>
                      <span class="ml-2 text-gray-500">({{ day.imported_count }}条记录)</span>
                    </div>
                    <span class="text-xs px-2 py-1 rounded" :class="day.source === 'json_to_db' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'">
                      {{ day.source === 'json_to_db' ? 'JSON→数据库' : '数据库→JSON' }}
                    </span>
                  </div>
                  <div v-if="day.titles && day.titles.length" class="pl-2 border-l-2 border-gray-200">
                    <div v-for="(title, titleIndex) in day.titles.slice(0, 3)" :key="titleIndex" class="text-gray-600 truncate">
                      {{ title }}
                    </div>
                    <div v-if="day.titles.length > 3" class="text-gray-400 text-xs">
                      还有{{ day.titles.length - 3 }}条记录...
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 数据完整性检查面板 -->
      <div v-if="currentTab === 'integrity'">
        <!-- 直接显示完整性报告 -->
        <div v-if="reportHtml" class="mb-6 prose prose-sm max-w-none bg-white dark:bg-gray-800 p-4 rounded-md border border-gray-200 dark:border-gray-700 dark:text-gray-100">
          <div v-html="reportHtml"></div>
        </div>

        <div class="mb-4">
          <p class="text-sm text-gray-600 mb-2">检查数据库和JSON文件之间的数据完整性。</p>

          <div class="flex flex-col sm:flex-row gap-4 mb-4">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">数据库路径</label>
              <input
                v-model="dbPath"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-pink-500 focus:border-pink-500 text-sm dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1">JSON文件路径</label>
              <input
                v-model="jsonPath"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-pink-500 focus:border-pink-500 text-sm dark:bg-gray-700 dark:text-gray-100"
              />
            </div>
          </div>

          <button
            @click="startCheck"
            class="w-full bg-pink-600 hover:bg-pink-700 text-white font-medium py-2 px-4 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isChecking"
          >
            <span v-if="isChecking" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              检查数据中...
            </span>
            <span v-else>开始检查</span>
          </button>
        </div>

        <!-- 检查结果显示 -->
        <div v-if="checkResult" class="mt-6 border-t pt-4">
          <h3 class="font-medium text-gray-900 mb-2">数据完整性检查结果</h3>
          <div class="bg-gray-50 dark:bg-gray-900 p-3 rounded-md border border-gray-200 dark:border-gray-700">
            <div class="grid grid-cols-2 gap-3 mb-3">
              <div class="text-sm">
                <span class="text-gray-500">检查时间：</span>
                <span class="text-gray-900">{{ formatDateTime(checkResult.timestamp) }}</span>
              </div>
              <div class="text-sm">
                <span class="text-gray-500">JSON文件总数：</span>
                <span class="text-gray-900">{{ checkResult.total_json_files }}</span>
              </div>
              <div class="text-sm">
                <span class="text-gray-500">JSON记录总数：</span>
                <span class="text-gray-900">{{ checkResult.total_json_records }}</span>
              </div>
              <div class="text-sm">
                <span class="text-gray-500">数据库记录总数：</span>
                <span class="text-gray-900">{{ checkResult.total_db_records }}</span>
              </div>
            </div>

            <div class="text-sm p-2 mb-3 rounded-md" :class="[checkResult.difference === 0 ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300']">
              <span class="font-medium">数据差异：</span>
              <span v-if="checkResult.difference === 0">数据一致</span>
              <span v-else-if="checkResult.difference > 0">数据库缺少 {{ checkResult.difference }} 条记录</span>
              <span v-else>数据库多出 {{ -checkResult.difference }} 条记录</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { syncData, getSyncResult, checkDataIntegrity, getIntegrityReport } from '../../api/api'
import { showNotify } from 'vant'
import 'vant/es/notify/style'

// 定义Props
const props = defineProps({
  showModal: {
    type: Boolean,
    default: false
  },
  initialTab: {
    type: String,
    default: 'integrity'
  }
})

// 定义事件
const emit = defineEmits(['update:showModal', 'sync-complete', 'check-complete'])

// 状态变量
const currentTab = ref(props.initialTab)
const dbPath = ref('output/bilibili_history.db')
const jsonPath = ref('output/history_by_date')
const isSyncing = ref(false)
const isChecking = ref(false)
const syncResult = ref(null)
const checkResult = ref(null)
const reportHtml = ref('')

// 格式化日期时间
const formatDateTime = (dateTimeString) => {
  if (!dateTimeString) return ''
  const date = new Date(dateTimeString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// 关闭模态框
const closeModal = () => {
  emit('update:showModal', false)
}

// 获取上次同步结果
const fetchSyncResult = async () => {
  try {
    const response = await getSyncResult()
    if (response.data && response.data.success) {
      syncResult.value = response.data
    }
  } catch (error) {
    console.error('获取同步结果失败:', error)
    showNotify({ type: 'danger', message: '获取同步结果失败' })
  }
}

// 开始同步数据
const startSync = async () => {
  isSyncing.value = true
  try {
    const response = await syncData(dbPath.value, jsonPath.value, false) // 禁用异步模式

    if (response.data.success) {
      syncResult.value = response.data
      showNotify({ type: 'success', message: `同步完成，共同步${response.data.total_synced}条记录` })
      emit('sync-complete', response.data)
    } else {
      showNotify({ type: 'danger', message: response.data.message || '同步失败' })
    }
  } catch (error) {
    console.error('同步数据失败:', error)
    showNotify({ type: 'danger', message: error.response?.data?.detail || '同步数据失败' })
  } finally {
    isSyncing.value = false
  }
}

// 开始数据完整性检查
const startCheck = async () => {
  isChecking.value = true
  try {
    // 强制执行检查，忽略配置设置
    const response = await checkDataIntegrity(dbPath.value, jsonPath.value, false, true)

    if (response.data.success) {
      checkResult.value = response.data

      // 检查是否有消息提示（可能是配置禁用了检查）
      if (response.data.message && response.data.message.includes('数据完整性校验已在配置中禁用')) {
        showNotify({
          type: 'warning',
          message: '数据完整性校验已在配置中禁用，但已强制执行检查'
        })
      } else {
        showNotify({ type: 'success', message: '数据完整性检查完成' })
      }

      emit('check-complete', response.data)

      // 检查完成后自动获取报告内容
      await fetchIntegrityReport()
    } else {
      showNotify({ type: 'danger', message: response.data.message || '检查失败' })
    }
  } catch (error) {
    console.error('数据完整性检查失败:', error)
    showNotify({ type: 'danger', message: error.response?.data?.detail || '数据完整性检查失败' })
  } finally {
    isChecking.value = false
  }
}

// 获取完整性报告内容
const fetchIntegrityReport = async () => {
  try {
    const response = await getIntegrityReport()

    // 检查是否有报告内容
    if (response.data && response.data.content) {
      // 更完善的Markdown到HTML转换
      let content = response.data.content
        // 预处理 - 先移除单独的#行和不带空格的#开头
        .replace(/^#\s*$/gm, '') // 移除单独的#行
        .replace(/^\s*#\s*$/gm, '') // 移除仅有空格和#的行
        .replace(/^#(?!\s)/gm, '') // 移除不带空格的#开头

      // 整理标题格式
      content = content.replace(/### ([^\n]+)/g, '<h3 class="text-base font-medium my-2">$1</h3>')
        .replace(/## ([^\n]+)/g, '<h2 class="text-lg font-semibold my-3">$1</h2>')
        .replace(/# ([^\n]+)/g, '<h1 class="text-xl font-bold my-4">$1</h1>')

      // 处理列表项
      content = content.replace(/^\* (.*?)$/gm, '<li class="ml-4">$1</li>')

      // 将列表项包装在ul标签中
      content = content.replace(/<li class="ml-4">(.*?)<\/li>(\s*)<li/g, '<li class="ml-4">$1</li></ul><ul><li')
        .replace(/<li class="ml-4">(.*?)<\/li>(?!\s*<li|\s*<\/ul>)/g, '<li class="ml-4">$1</li></ul>')
        .replace(/<li/g, '<ul><li')

      // 修复可能的重复ul标签
      content = content.replace(/<\/ul>\s*<ul>/g, '')

      // 段落处理
      content = content.replace(/\n\n/g, '</p><p class="my-2">')

      // 处理一些特殊格式
      content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')

      // 确保所有内容都有封装标签
      if (!content.startsWith('<')) {
        content = '<p class="my-2">' + content + '</p>'
      }

      reportHtml.value = content
      return true
    } else if (response.data && response.data.message && response.data.message.includes('数据完整性校验已在配置中禁用')) {
      // 如果报告为空是因为配置禁用了校验
      reportHtml.value = `<div class="p-4 bg-yellow-50 text-yellow-800 rounded-md">
        <h3 class="font-medium">数据完整性校验已在配置中禁用</h3>
        <p class="mt-2">您已在设置中禁用启动时数据完整性校验。如需查看报告，请点击"开始检查"按钮强制执行检查。</p>
      </div>`
      return true
    } else {
      // 其他原因导致报告为空
      showNotify({ type: 'warning', message: '报告内容为空' })
      reportHtml.value = `<div class="p-4 bg-gray-50 text-gray-600 rounded-md">
        <p>暂无报告内容。请点击"开始检查"按钮执行数据完整性检查。</p>
      </div>`
      return false
    }
  } catch (error) {
    console.error('获取报告失败:', error)
    reportHtml.value = `<div class="p-4 bg-red-50 text-red-600 rounded-md">
      <h3 class="font-medium">获取报告失败</h3>
      <p class="mt-2">错误信息: ${error.message || '未知错误'}</p>
      <p class="mt-1">请点击"开始检查"按钮重新执行数据完整性检查。</p>
    </div>`
    return false
  }
}

// 监听模态框状态变化
watch(() => props.showModal, async (newVal) => {
  if (newVal) {
    // 模态框打开时，获取最新数据
    await fetchIntegrityReport() // 先获取报告
    await fetchSyncResult() // 再获取同步结果
  }
})

// 监听initialTab变化
watch(() => props.initialTab, (newVal) => {
  currentTab.value = newVal
})

// 组件挂载时
onMounted(async () => {
  if (props.showModal) {
    await fetchIntegrityReport() // 默认加载报告
    await fetchSyncResult()
  }
})
</script>