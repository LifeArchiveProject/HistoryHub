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
      <div class="flex items-center justify-between px-3">
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
            class="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </template>
    <div v-if="task" class="p-3">
      <!-- 任务标题和状态栏 -->
      <div class="flex items-center justify-between mb-3 pb-2 border-b border-gray-100 dark:border-gray-700">
        <div class="flex items-center">
          <div class="p-1.5 bg-[#fb7299]/10 rounded-lg mr-2">
            <svg class="w-4 h-4 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <div class="flex items-center space-x-1">
              <h3 class="text-base font-medium text-gray-800 dark:text-gray-100 truncate" :title="task.config?.name">{{ task.config?.name }}</h3>
            </div>
            <p class="text-xs text-gray-500 dark:text-gray-400">ID: {{ task.task_id }}</p>
          </div>
        </div>
        <div class="flex flex-col items-end">
          <div class="flex items-center space-x-1 mb-1">
            <span
              v-if="task.execution?.status"
              :class="{
                'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 border-green-200 dark:border-green-900/30': task.execution.status === 'success',
                'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-900/30': task.execution.status === 'running',
                'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border-red-200 dark:border-red-900/30': task.execution.status === 'error'
              }"
              class="px-1.5 py-0.5 text-xs font-medium rounded-md border"
            >
              {{ statusLabel }}
            </span>
            <span 
              v-if="task.config?.enabled !== undefined"
              :class="{'bg-green-50 text-green-700 border-green-200': task.config.enabled, 'bg-red-50 text-red-700 border-red-200': !task.config.enabled}" 
              class="px-1.5 py-0.5 text-xs font-medium rounded-md border"
            >
              {{ task.config.enabled ? '已启用' : '已禁用' }}
            </span>
          </div>
        </div>
      </div>

      <!-- 任务详情内容 -->
      <div class="space-y-3">
        <!-- 基本信息 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-2 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            基本信息
          </h4>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">API端点</p>
              <p class="text-sm text-gray-800 dark:text-gray-100 font-mono">{{ task.config?.endpoint }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">请求方法</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">{{ task.config?.method }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">优先级</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">{{ task.config?.priority || 0 }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">最后修改</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">{{ task.last_modified?.replace('T', ' ') }}</p>
            </div>
          </div>
        </div>

        <!-- 调度信息 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-2 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            调度信息
          </h4>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">调度类型</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">{{ scheduleTypeLabel }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">执行时间</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">
                <template v-if="task.task_type === 'main'">
                  <template v-if="task.config?.schedule_type === 'interval'">
                    {{ task.config?.interval_value || '-' }} 
                    {{ 
                      task.config?.interval_unit === 'minutes' ? '分钟' : 
                      task.config?.interval_unit === 'hours' ? '小时' : 
                      task.config?.interval_unit === 'days' ? '天' : 
                      task.config?.interval_unit === 'months' ? '月' : 
                      task.config?.interval_unit === 'years' ? '年' : 
                      task.config?.interval_unit || ''
                    }}
                  </template>
                  <template v-else>
                    {{ task.config?.schedule_time || '未设置' }}
                  </template>
                </template>
                <template v-else>
                  依赖于主任务
                </template>
              </p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">上次执行</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">{{ task.execution?.last_run?.replace('T', ' ') || '从未执行' }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">下次执行</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">
                <template v-if="task.task_type === 'main'">
                  {{ task.execution?.next_run || '未排定' }}
                </template>
                <template v-else>
                  依赖于主任务
                </template>
              </p>
            </div>
          </div>
        </div>

        <!-- 执行统计 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-2 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            执行统计
          </h4>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="text-xs text-gray-500 dark:text-gray-400">成功率</span>
                <span class="text-xs text-gray-800 dark:text-gray-100">
                  {{ Math.round(executionInfo.successRate) }}%
                </span>
              </div>
              <div class="h-1.5 w-full bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                <div class="h-full rounded-full" 
                  :class="{
                    'bg-green-500': executionInfo.successRate >= 90,
                    'bg-yellow-500': executionInfo.successRate >= 60 && executionInfo.successRate < 90,
                    'bg-red-500': executionInfo.successRate < 60
                  }" 
                  :style="{width: `${executionInfo.successRate}%`}">
                </div>
              </div>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">平均耗时</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">
                {{ executionInfo.avgDuration.toFixed(2) }}秒
              </p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">总执行次数</p>
              <p class="text-sm text-gray-800 dark:text-gray-100">
                {{ executionInfo.totalRuns }}
              </p>
            </div>
            <div>
              <p class="text-xs text-gray-500 dark:text-gray-400">成功/失败</p>
              <p class="text-sm">
                <span class="text-green-600">{{ executionInfo.successRuns }}</span>
                <span class="text-gray-400 mx-1">/</span>
                <span class="text-red-600">{{ executionInfo.failRuns }}</span>
              </p>
            </div>
          </div>
        </div>

        <!-- 依赖任务 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-2 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 dark:text-gray-300 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
            </svg>
            依赖任务
          </h4>
          <div v-if="task.depends_on" class="flex flex-wrap gap-0.5">
            <span
              class="inline-flex items-center px-1.5 py-0.5 rounded-md text-xs font-medium bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-900/30"
              :title="task.depends_on.name"
            >
              {{ task.depends_on.name }} ({{ task.depends_on.task_id }})
            </span>
          </div>
          <p v-else class="text-xs text-gray-500 dark:text-gray-400">无依赖</p>
        </div>

        <!-- 最近错误 -->
        <div v-if="task.execution?.last_error" class="bg-white dark:bg-gray-800 rounded-lg p-2 border border-red-100 dark:border-red-900/30 shadow-sm">
          <h4 class="text-xs font-semibold text-red-600 uppercase tracking-wider mb-1.5 flex items-center">
            <svg class="w-3 h-3 mr-1 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            最近错误
          </h4>
          <p class="text-xs text-red-600 whitespace-pre-wrap">{{ task.execution.last_error }}</p>
        </div>
      </div>
    </div>
  </van-dialog>
</template>

<script setup>
import { computed, watch } from 'vue'
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

// 添加 watch 来监控 task 属性的变化
watch(() => props.task, (newTask) => {
  if (!newTask) {
    return
  }
}, { deep: true, immediate: true })

// 添加计算属性来处理执行信息
const executionInfo = computed(() => {
  const execution = props.task?.execution || {}
  
  // 确保所有数值类型的字段都有默认值
  const info = {
    lastRun: execution.last_run ?? null,
    nextRun: execution.next_run ?? null,
    status: execution.status ?? 'pending',
    successRate: typeof execution.success_rate === 'number' ? execution.success_rate : 0,
    avgDuration: typeof execution.avg_duration === 'number' ? execution.avg_duration : 0,
    totalRuns: typeof execution.total_runs === 'number' ? execution.total_runs : 0,
    successRuns: typeof execution.success_runs === 'number' ? execution.success_runs : 0,
    failRuns: typeof execution.fail_runs === 'number' ? execution.fail_runs : 0
  }
  
  return info
})

// 计算调度类型标签
const scheduleTypeLabel = computed(() => {
  const type = props.task?.config?.schedule_type
  return type === 'daily' ? '每日' : 
         type === 'chain' ? '链式任务' : 
         type === 'once' ? '一次性' : 
         type === 'interval' ? '间隔执行' : type
})

// 计算状态标签
const statusLabel = computed(() => {
  const status = props.task?.execution?.status
  return status === 'success' ? '成功' :
         status === 'running' ? '执行中' :
         status === 'error' ? '失败' :
         status === 'pending' ? '等待中' : status
})

// 确认删除
const confirmDelete = () => {
  showDialog({
    title: '确认删除',
    message: `确定要删除任务 "${props.task.config?.name}" 吗？此操作不可撤销。`,
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

<style>
/* 确保弹窗在X轴和Y轴都居中 */
.task-detail-dialog .van-dialog {
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  margin: 0 !important;
  max-height: 80vh !important;
  overflow-y: auto !important;
}

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