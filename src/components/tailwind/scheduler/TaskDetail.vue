<template>
  <van-dialog
    :show="show"
    @update:show="$emit('update:show', $event)"
    title="任务详情"
    width="60%"
    :show-confirm-button="false"
    class="task-detail-dialog"
  >
    <template #title>
      <div class="flex items-center justify-between">
        <span>任务详情</span>
        <div class="flex items-center space-x-2">
          <button 
            @click="$emit('view-history', task.task_id)" 
            class="inline-flex items-center px-2 py-1 text-xs font-medium text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none rounded-md"
          >
            <svg class="w-3.5 h-3.5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            查看历史
          </button>
          <button 
            @click="$emit('update:show', false)"
            class="p-1 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg class="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </template>
    <div v-if="task" class="p-3">
      <!-- 任务标题和状态栏 -->
      <div class="flex items-center justify-between mb-3 pb-2 border-b border-gray-100">
        <div class="flex items-center">
          <div class="p-1.5 bg-[#fb7299]/10 rounded-lg mr-2">
            <svg class="w-4 h-4 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <div class="flex items-center space-x-1">
              <h3 class="text-base font-medium text-gray-800 truncate" :title="task.name">{{ task.name }}</h3>
            </div>
            <p class="text-xs text-gray-500">ID: {{ task.task_id }}</p>
          </div>
        </div>
        <div class="flex flex-col items-end">
          <div class="flex items-center space-x-1 mb-1">
            <span 
              v-if="task.last_status"
              :class="{
                'bg-green-50 text-green-700 border-green-200': task.last_status === 'success',
                'bg-yellow-50 text-yellow-700 border-yellow-200': task.last_status === 'running',
                'bg-red-50 text-red-700 border-red-200': task.last_status === 'error'
              }" 
              class="px-1.5 py-0.5 text-xs font-medium rounded-md border"
            >
              {{ task.last_status }}
            </span>
            <span 
              v-if="task.enabled !== undefined"
              :class="{'bg-green-50 text-green-700 border-green-200': task.enabled, 'bg-red-50 text-red-700 border-red-200': !task.enabled}" 
              class="px-1.5 py-0.5 text-xs font-medium rounded-md border"
            >
              {{ task.enabled ? '已启用' : '已禁用' }}
            </span>
          </div>
        </div>
      </div>

      <!-- 任务详情内容 -->
      <div class="space-y-3">
        <!-- 基本信息 -->
        <div class="bg-white rounded-lg p-2 border border-gray-100 shadow-sm">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            基本信息
          </h4>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <p class="text-xs text-gray-500">API端点</p>
              <p class="text-sm text-gray-800 font-mono">{{ task.endpoint }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">请求方法</p>
              <p class="text-sm text-gray-800">{{ task.method }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">优先级</p>
              <p class="text-sm text-gray-800">{{ task.priority || 0 }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">最后修改</p>
              <p class="text-sm text-gray-800">{{ task.last_modified?.replace('T', ' ') }}</p>
            </div>
          </div>
        </div>

        <!-- 调度信息 -->
        <div class="bg-white rounded-lg p-2 border border-gray-100 shadow-sm">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            调度信息
          </h4>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <p class="text-xs text-gray-500">调度类型</p>
              <p class="text-sm text-gray-800">{{ scheduleTypeLabel }}</p>
            </div>
            <div v-if="task.schedule?.type === 'daily'">
              <p class="text-xs text-gray-500">执行时间</p>
              <p class="text-sm text-gray-800">{{ task.schedule.time }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">上次执行</p>
              <p class="text-sm text-gray-800">{{ task.last_run_time || '从未执行' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">下次执行</p>
              <p class="text-sm text-gray-800">{{ task.next_run_time || '未排定' }}</p>
            </div>
          </div>
        </div>

        <!-- 执行统计 -->
        <div class="bg-white rounded-lg p-2 border border-gray-100 shadow-sm">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            执行统计
          </h4>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-xs text-gray-500">成功率</span>
                <span class="text-xs text-gray-800">{{ task.success_rate }}%</span>
              </div>
              <div class="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                <div class="h-full rounded-full" 
                  :class="{
                    'bg-green-500': task.success_rate >= 90,
                    'bg-yellow-500': task.success_rate >= 60 && task.success_rate < 90,
                    'bg-red-500': task.success_rate < 60
                  }" 
                  :style="{width: `${task.success_rate}%`}">
                </div>
              </div>
            </div>
            <div>
              <p class="text-xs text-gray-500">平均耗时</p>
              <p class="text-sm text-gray-800">{{ task.avg_duration?.toFixed(2) || 0 }}秒</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">总执行次数</p>
              <p class="text-sm text-gray-800">{{ task.total_runs || 0 }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">成功/失败</p>
              <p class="text-sm">
                <span class="text-green-600">{{ task.success_runs || 0 }}</span>
                <span class="text-gray-400 mx-1">/</span>
                <span class="text-red-600">{{ task.fail_runs || 0 }}</span>
              </p>
            </div>
          </div>
        </div>

        <!-- 依赖任务 -->
        <div class="bg-white rounded-lg p-2 border border-gray-100 shadow-sm">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
            </svg>
            依赖任务
          </h4>
          <div v-if="task.requires && task.requires.length > 0" class="flex flex-wrap gap-0.5">
            <span 
              v-for="(req, index) in task.requires" 
              :key="index"
              class="inline-flex items-center px-1.5 py-0.5 rounded-md text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200"
            >
              {{ req }}
            </span>
          </div>
          <p v-else class="text-xs text-gray-500">无依赖</p>
        </div>

        <!-- 最近错误 -->
        <div v-if="task.last_error" class="bg-white rounded-lg p-2 border border-red-100 shadow-sm">
          <h4 class="text-xs font-semibold text-red-600 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            最近错误
          </h4>
          <p class="text-xs text-red-600 whitespace-pre-wrap">{{ task.last_error }}</p>
        </div>
      </div>
    </div>
  </van-dialog>
</template>

<script setup>
import { computed } from 'vue'
import { showNotify, showDialog } from 'vant'
import 'vant/es/dialog/style'
import 'vant/es/notify/style'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  task: {
    type: Object,
    default: null
  }
})

const emit = defineEmits([
  'update:show',
  'view-history',
  'edit-task',
  'execute-task',
  'toggle-enabled',
  'delete-task'
])

// 计算调度类型标签
const scheduleTypeLabel = computed(() => {
  const type = props.task?.schedule?.type
  return type === 'daily' ? '每日' : 
         type === 'chain' ? '链式' : 
         type === 'once' ? '一次性' : type
})

// 确认删除
const confirmDelete = () => {
  showDialog({
    title: '确认删除',
    message: `确定要删除任务 "${props.task.name}" 吗？此操作不可撤销。`,
    showCancelButton: true,
    confirmButtonText: '删除',
    confirmButtonColor: '#ee0a24',
  }).then(() => {
    emit('delete-task', props.task.task_id)
  }).catch(() => {
    // 用户取消删除
  })
}
</script>

<script>
export default {
  name: 'TaskDetail'
}
</script>

<style scoped>
.task-detail-dialog :deep(.van-dialog__content) {
  max-height: 70vh;
  overflow-y: auto;
}

.task-detail-dialog :deep(.van-dialog) {
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.task-detail-dialog :deep(.van-dialog__header) {
  flex-shrink: 0;
  padding: 12px 16px;
  font-size: 14px;
}
</style> 