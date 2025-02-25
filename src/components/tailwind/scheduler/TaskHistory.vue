<template>
  <van-dialog
    :show="show"
    @update:show="$emit('update:show', $event)"
    title="任务执行历史"
    width="80%"
    :show-confirm-button="false"
    class="task-history-dialog"
  >
    <template #title>
      <div class="flex items-center justify-between">
        <span>任务执行历史</span>
        <button 
          @click="$emit('update:show', false)"
          class="p-1 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <svg class="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </template>
    <div class="p-3">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center">
          <div class="p-1.5 bg-[#fb7299]/10 rounded-lg mr-2">
            <svg class="w-4 h-4 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h3 class="text-base font-medium text-gray-800">{{ taskName }}</h3>
            <p class="text-xs text-gray-500">ID: {{ taskId }}</p>
          </div>
        </div>
        <div>
          <button 
            @click="refreshHistory" 
            class="inline-flex items-center px-2 py-1 border border-transparent rounded-md shadow-sm text-xs font-medium text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none"
          >
            <svg class="w-3.5 h-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            刷新
          </button>
        </div>
      </div>
      
      <div v-if="loading" class="flex justify-center items-center py-8">
        <van-loading type="spinner" color="#fb7299" />
      </div>
      
      <div v-else-if="history.length === 0" class="text-center py-8 text-gray-500">
        <svg class="w-12 h-12 mx-auto text-gray-300 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p>暂无执行历史记录</p>
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                执行时间
              </th>
              <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                状态
              </th>
              <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                耗时
              </th>
              <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                触发方式
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="record in history" :key="record.id" class="hover:bg-gray-50">
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-900">
                {{ record.start_time }}
              </td>
              <td class="px-3 py-2 whitespace-nowrap">
                <span 
                  :class="{
                    'bg-green-50 text-green-700 border-green-200': record.status === 'success',
                    'bg-yellow-50 text-yellow-700 border-yellow-200': record.status === 'running',
                    'bg-red-50 text-red-700 border-red-200': record.status === 'error'
                  }" 
                  class="px-1.5 py-0.5 text-xs font-medium rounded-md border"
                >
                  {{ statusLabel(record.status) }}
                </span>
                <span v-if="record.error_message" class="ml-1 text-xs text-red-600 cursor-pointer hover:text-red-800" @click="viewError(record)">
                  查看错误
                </span>
              </td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-500">
                {{ record.duration ? `${record.duration.toFixed(2)}秒` : '-' }}
              </td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-500">
                {{ record.triggered_by || '-' }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- 错误详情弹窗 -->
    <van-dialog
      v-model:show="showErrorDialog"
      title="错误详情"
      width="70%"
      :show-confirm-button="false"
      class="result-dialog"
    >
      <template #title>
        <div class="flex items-center justify-between">
          <span>错误详情</span>
          <button 
            @click="showErrorDialog = false"
            class="p-1 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </template>
      <div v-if="selectedRecord" class="p-3">
        <div class="bg-red-50 p-2 rounded-md">
          <pre class="text-xs font-mono text-red-800 whitespace-pre-wrap overflow-x-auto">{{ selectedRecord.error_message }}</pre>
        </div>
      </div>
    </van-dialog>
  </van-dialog>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { showNotify } from 'vant'
import 'vant/es/dialog/style'
import 'vant/es/notify/style'
import 'vant/es/loading/style'
import { 
  getTaskExecutionHistory 
} from '../../../api/api'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  taskId: {
    type: String,
    default: ''
  },
  taskName: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:show'])

const loading = ref(false)
const history = ref([])
const showErrorDialog = ref(false)
const selectedRecord = ref(null)

// 获取任务历史记录
const fetchHistory = async () => {
  if (!props.taskId) return
  
  loading.value = true
  try {
    const response = await getTaskExecutionHistory(props.taskId)
    if (response.data && response.data.status === 'success') {
      history.value = response.data.history || []
    } else {
      showNotify({ type: 'danger', message: '获取历史记录失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('获取历史记录出错:', error)
    showNotify({ type: 'danger', message: '获取历史记录出错: ' + (error.message || '未知错误') })
  } finally {
    loading.value = false
  }
}

// 刷新历史记录
const refreshHistory = () => {
  fetchHistory()
}

// 查看错误详情
const viewError = (record) => {
  selectedRecord.value = record
  showErrorDialog.value = true
}

// 状态标签
const statusLabel = (status) => {
  switch (status) {
    case 'success':
      return '成功'
    case 'error':
      return '失败'
    case 'running':
      return '执行中'
    default:
      return status
  }
}

// 监听任务ID变化，自动获取历史记录
onMounted(() => {
  if (props.show && props.taskId) {
    fetchHistory()
  }
})

// 监听show变化，自动获取历史记录
watch(() => props.show, (newVal) => {
  if (newVal && props.taskId) {
    fetchHistory()
  }
})
</script>

<script>
export default {
  name: 'TaskHistory'
}
</script>

<style scoped>
.task-history-dialog :deep(.van-dialog) {
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  margin-top: -10vh !important;
}

.task-history-dialog :deep(.van-dialog__header) {
  flex-shrink: 0;
  padding: 12px 16px;
  font-size: 14px;
}

.result-dialog :deep(.van-dialog) {
  max-height: 75vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  margin-top: -5vh !important;
}

.result-dialog :deep(.van-dialog__header) {
  flex-shrink: 0;
  padding: 10px 14px;
  font-size: 13px;
}
</style> 