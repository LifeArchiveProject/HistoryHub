<template>
  <div class="min-h-screen bg-gray-50/30">
    <div class="py-4">
      <div class="max-w-7xl mx-auto px-3">
        <!-- 页面标题 -->
        <div class="flex items-center space-x-2 text-gray-900 mb-4">
          <div class="p-1.5 bg-[#fb7299]/5 rounded-lg">
            <svg class="w-6 h-6 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h1 class="text-2xl font-medium bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">计划任务管理</h1>
        </div>

        <!-- 操作按钮 -->
        <div class="mb-4 flex justify-between items-center">
          <div class="flex space-x-2">
            <button 
              @click="refreshTasks" 
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#fb7299]"
            >
              <svg class="mr-2 -ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              刷新
            </button>
            
            <button 
              @click="toggleViewMode" 
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#fb7299]"
            >
              <svg class="mr-2 -ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path v-if="viewMode === 'table'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
              {{ viewMode === 'table' ? '树状视图' : '表格视图' }}
            </button>
          </div>
          <button 
            @click="openCreateTaskModal" 
            class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#fb7299]"
          >
            <svg class="mr-2 -ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            新建任务
          </button>
        </div>

        <!-- 任务列表 -->
        <div v-if="loading" class="flex justify-center items-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#fb7299]"></div>
        </div>

        <div v-else-if="tasks.length === 0" class="bg-white border border-gray-200 rounded-lg shadow-sm p-6 text-center">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900">暂无计划任务</h3>
          <p class="mt-1 text-sm text-gray-500">点击"新建任务"按钮创建您的第一个计划任务</p>
          <div class="mt-6">
            <button
              @click="openCreateTaskModal"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#fb7299]"
            >
              <svg class="-ml-1 mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              新建任务
            </button>
          </div>
        </div>

        <!-- 表格视图 -->
        <div v-else-if="viewMode === 'table'" class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">任务ID</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">名称</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">调度类型</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">调度时间</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">成功率</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">最后执行</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                  <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="task in tasks" :key="task.task_id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ task.task_id }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ task.name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span 
                      :class="{
                        'bg-blue-100 text-blue-800': task.schedule_type === 'daily',
                        'bg-purple-100 text-purple-800': task.schedule_type === 'chain',
                        'bg-green-100 text-green-800': task.schedule_type === 'once'
                      }" 
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    >
                      {{ 
                        task.schedule_type === 'daily' ? '每日' : 
                        task.schedule_type === 'chain' ? '链式' : 
                        task.schedule_type === 'once' ? '一次性' : task.schedule_type 
                      }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ task.schedule_time || '-' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span v-if="task.success_rate !== undefined" class="inline-flex items-center">
                      {{ task.success_rate }}%
                      <div class="ml-2 h-1.5 w-16 bg-gray-200 rounded-full overflow-hidden">
                        <div 
                          class="h-full rounded-full" 
                          :class="{
                            'bg-green-500': task.success_rate >= 90,
                            'bg-yellow-500': task.success_rate >= 60 && task.success_rate < 90,
                            'bg-red-500': task.success_rate < 60
                          }"
                          :style="{width: `${task.success_rate}%`}"
                        ></div>
                      </div>
                    </span>
                    <span v-else>-</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ task.last_run || '未记录' }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span 
                      :class="{
                        'bg-green-100 text-green-800': task.status === '配置完成' || task.status === 'success',
                        'bg-yellow-100 text-yellow-800': task.status === '执行中',
                        'bg-red-100 text-red-800': task.status === '失败' || task.status === 'error'
                      }" 
                      class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                    >
                      {{ task.status }}
                      </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                      <button 
                        @click="openTaskDetailModal(task.task_id)" 
                        class="text-indigo-600 hover:text-indigo-900"
                      >
                        详情
                      </button>
                      <button 
                        @click="openEditTaskModal(task.task_id)" 
                        class="text-blue-600 hover:text-blue-900"
                      >
                        编辑
                      </button>
                      <button 
                        @click="executeTask(task.task_id)" 
                        class="text-green-600 hover:text-green-900"
                      >
                        执行
                      </button>
                      <button 
                        v-if="task.enabled !== undefined"
                        @click="toggleTaskEnabled(task.task_id, !task.enabled)" 
                        :class="task.enabled ? 'text-orange-600 hover:text-orange-900' : 'text-teal-600 hover:text-teal-900'"
                      >
                        {{ task.enabled ? '禁用' : '启用' }}
                      </button>
                      <button 
                        @click="confirmDeleteTask(task.task_id)" 
                        class="text-red-600 hover:text-red-900"
                      >
                        删除
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 树状视图 -->
        <div v-else class="bg-white border border-gray-200 rounded-lg shadow-sm p-4">
          <div class="mb-4">
            <h3 class="text-sm font-medium text-gray-500">任务依赖关系树</h3>
            <p class="text-xs text-gray-400">提示：链式任务将在其依赖任务之后执行</p>
          </div>
          
          <!-- 独立任务（无依赖）和根任务（被其他任务依赖但自身无依赖） -->
          <div class="space-y-4">
            <div v-for="task in rootTasks" :key="task.task_id">
              <task-tree-item 
                :task="task" 
                :tasks="tasks" 
                @view-detail="openTaskDetailModal"
                @edit-task="openEditTaskModal"
                @execute-task="executeTask"
                @delete-task="confirmDeleteTask"
                @toggle-enabled="toggleTaskEnabled"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务详情弹窗 -->
    <TaskDetail
      v-model:show="showTaskDetailModal"
      :task="currentTask"
      @view-history="fetchTaskHistory"
      @edit-task="openEditTaskModal"
      @execute-task="executeTask"
      @toggle-enabled="toggleTaskEnabled"
      @delete-task="confirmDeleteTask"
      @refresh="fetchTasks"
    />

    <!-- 任务历史弹窗 -->
    <TaskHistory
      v-model:show="showTaskHistoryModal"
      :task-id="currentTask?.task_id"
      :task-name="currentTask?.name"
    />

    <!-- 创建/编辑任务弹窗 -->
    <TaskForm
      v-model:show="showTaskFormModal"
      :is-editing="isEditing"
      :task-id="currentTask?.task_id"
      :tasks="tasks"
      @task-saved="fetchTasks"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { showNotify, showDialog } from 'vant'
import 'vant/es/dialog/style'
import 'vant/es/notify/style'
import 'vant/es/loading/style'
import TaskTreeItem from '../../tailwind/TaskTreeItem.vue'
import { 
  getAllSchedulerTasks, 
  getSchedulerTaskDetail, 
  createSchedulerTask, 
  updateSchedulerTask, 
  deleteSchedulerTask, 
  executeSchedulerTask,
  getTaskExecutionHistory,
  getRecentTaskHistory,
  getTaskChainHistory,
  setTaskEnabled,
  setTaskPriority
} from '../../../api/api'
import TaskForm from '../scheduler/TaskForm.vue'
import TaskDetail from '../scheduler/TaskDetail.vue'
import TaskHistory from '../scheduler/TaskHistory.vue'

// 视图模式：表格或树状
const viewMode = ref('table')

// 加载状态
const loading = ref(true)

// 任务列表
const tasks = ref([])

// 当前任务
const currentTask = ref(null)

// 弹窗控制
const showTaskFormModal = ref(false)
const showTaskDetailModal = ref(false)
const showTaskHistoryModal = ref(false)

// 是否为编辑模式
const isEditing = ref(false)

// 搜索关键词
const searchKeyword = ref('')

// 标签输入
const newTagInput = ref('')

// 执行任务
const executeTask = async (taskId) => {
  try {
    const response = await executeSchedulerTask(taskId)
    if (response.data && response.data.status === 'success') {
      showNotify({ type: 'success', message: '任务执行请求已发送' })
      // 延迟刷新任务列表，以便看到状态变化
      setTimeout(() => {
        fetchTasks()
      }, 1000)
    } else {
      showNotify({ type: 'danger', message: '任务执行请求失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('执行任务出错:', error)
    showNotify({ type: 'danger', message: '执行任务出错: ' + (error.message || '未知错误') })
  }
}

// 计算属性：过滤后的任务列表
const rootTasks = computed(() => {
  // 找出所有被依赖的任务ID
  const dependedTaskIds = new Set()
  tasks.value.forEach(task => {
    // 检查depends_on或requires字段
    const dependencies = task.depends_on || task.requires || []
    if (dependencies.length > 0) {
      dependencies.forEach(reqId => dependedTaskIds.add(reqId))
    }
  })
  
  // 找出所有无依赖的任务
  return tasks.value.filter(task => {
    // 检查depends_on或requires字段
    const dependencies = task.depends_on || task.requires || []
    return dependencies.length === 0 || 
      // 如果一个任务被依赖但自身无依赖，也作为根节点
      (dependedTaskIds.has(task.task_id) && dependencies.length === 0)
  })
})

// 获取依赖指定任务的所有任务
const getDependentTasks = (taskId) => {
  return tasks.value.filter(task => {
    // 检查depends_on或requires字段
    const dependencies = task.depends_on || task.requires || []
    return dependencies.includes(taskId)
  })
}

// 切换视图模式
const toggleViewMode = () => {
  viewMode.value = viewMode.value === 'table' ? 'tree' : 'table'
}

// 获取所有计划任务
const fetchTasks = async () => {
  loading.value = true
  try {
    const response = await getAllSchedulerTasks()
    if (response.data && response.data.status === 'success' && response.data.tasks) {
      tasks.value = response.data.tasks.map(task => {
        // 添加展开状态属性
        const processedTask = { ...task, _expanded: true }
        // 如果有requires字段但没有depends_on字段，将requires复制到depends_on
        if (task.requires && !task.depends_on) {
          processedTask.depends_on = task.requires
        }
        return processedTask
      })
    } else {
      showNotify({ type: 'danger', message: '获取任务列表失败' })
    }
  } catch (error) {
    console.error('获取任务列表出错:', error)
    showNotify({ type: 'danger', message: '获取任务列表出错: ' + (error.message || '未知错误') })
  } finally {
    loading.value = false
  }
}

// 刷新任务列表
const refreshTasks = () => {
  fetchTasks()
}

// 打开任务详情弹窗
const openTaskDetailModal = async (taskId) => {
  try {
    const response = await getSchedulerTaskDetail(taskId)
    if (response.data && response.data.status === 'success' && response.data.task) {
      const task = response.data.task
      // 如果有requires字段但没有depends_on字段，将requires复制到depends_on
      if (task.requires && !task.depends_on) {
        task.depends_on = task.requires
      }
      currentTask.value = task
      showTaskDetailModal.value = true
    } else {
      showNotify({ type: 'danger', message: '获取任务详情失败' })
    }
  } catch (error) {
    console.error('获取任务详情出错:', error)
    showNotify({ type: 'danger', message: '获取任务详情出错: ' + (error.message || '未知错误') })
  }
}

// 获取任务执行历史
const fetchTaskHistory = async (taskId) => {
  try {
    const response = await getTaskExecutionHistory(taskId)
    if (response.data && response.data.status === 'success') {
      showTaskHistoryModal.value = true
    } else {
      showNotify({ type: 'danger', message: '获取任务历史记录失败' })
    }
  } catch (error) {
    console.error('获取任务历史记录出错:', error)
    showNotify({ type: 'danger', message: '获取任务历史记录出错: ' + (error.message || '未知错误') })
  }
}

// 计算历史记录的成功率
const getSuccessRate = (historyList) => {
  if (!historyList || historyList.length === 0) return 0
  
  const successCount = historyList.filter(h => h.status === 'success').length
  return Math.round((successCount / historyList.length) * 100)
}

// 启用或禁用任务
const toggleTaskEnabled = async (taskId, enabled) => {
  try {
    const response = await setTaskEnabled(taskId, enabled)
    if (response.data && response.data.status === 'success') {
      showNotify({ type: 'success', message: enabled ? '任务已启用' : '任务已禁用' })
      fetchTasks()
    } else {
      showNotify({ type: 'danger', message: '更新任务状态失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('更新任务状态出错:', error)
    showNotify({ type: 'danger', message: '更新任务状态出错: ' + (error.message || '未知错误') })
  }
}

// 打开创建任务弹窗
const openCreateTaskModal = () => {
  showNotify({ 
    type: 'warning',
    message: '新建任务功能将在下次更新开放，敬请期待！'
  })
}

// 打开编辑任务弹窗
const openEditTaskModal = async (taskId) => {
  try {
    const response = await getSchedulerTaskDetail(taskId)
    if (response.data && response.data.status === 'success' && response.data.task) {
      currentTask.value = response.data.task
      isEditing.value = true
      showTaskFormModal.value = true
    } else {
      showNotify({ type: 'danger', message: '获取任务详情失败' })
    }
  } catch (error) {
    console.error('获取任务详情出错:', error)
    showNotify({ type: 'danger', message: '获取任务详情出错: ' + (error.message || '未知错误') })
  }
}

// 确认删除任务
const confirmDeleteTask = (taskId) => {
  showDialog({
    title: '确认删除',
    message: '确定要删除此任务吗？此操作不可撤销。',
    showCancelButton: true,
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    confirmButtonColor: '#fb7299',
  }).then(() => {
    deleteTask(taskId)
  }).catch(() => {
    // 取消删除
  })
}

// 删除任务
const deleteTask = async (taskId) => {
  try {
    const response = await deleteSchedulerTask(taskId)
    if (response.data && response.data.status === 'success') {
      showNotify({ type: 'success', message: '任务删除成功' })
      // 关闭所有相关的弹窗
      showTaskDetailModal.value = false
      showTaskHistoryModal.value = false
      // 重新获取任务列表
      fetchTasks()
    } else {
      showNotify({ type: 'danger', message: '删除任务失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('删除任务出错:', error)
    showNotify({ type: 'danger', message: '删除任务出错: ' + (error.message || '未知错误') })
  }
}

// 初始化
onMounted(() => {
  fetchTasks()
})
</script>

<style scoped>
.task-detail-dialog :deep(.van-dialog__content) {
  max-height: 70vh;
  overflow-y: auto;
}

.task-form-dialog :deep(.van-dialog__content) {
  max-height: 70vh;
  overflow-y: auto;
}

.task-form-dialog :deep(.van-dialog) {
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.task-form-dialog :deep(.van-dialog__header) {
  flex-shrink: 0;
  padding: 10px 14px;
  font-size: 13px;
}

.task-history-dialog :deep(.van-dialog__content) {
  max-height: 70vh;
  overflow-y: auto;
}

/* 优化滚动条样式 */
:deep(.van-dialog__content)::-webkit-scrollbar,
pre::-webkit-scrollbar,
.max-h-32::-webkit-scrollbar,
.max-h-28::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

:deep(.van-dialog__content)::-webkit-scrollbar-thumb,
pre::-webkit-scrollbar-thumb,
.max-h-32::-webkit-scrollbar-thumb,
.max-h-28::-webkit-scrollbar-thumb {
  background: #ddd;
  border-radius: 2px;
}

:deep(.van-dialog__content)::-webkit-scrollbar-thumb:hover,
pre::-webkit-scrollbar-thumb:hover,
.max-h-32::-webkit-scrollbar-thumb:hover,
.max-h-28::-webkit-scrollbar-thumb:hover {
  background: #fb7299;
}

/* 弹窗标题样式 */
:deep(.van-dialog__header) {
  padding: 12px 16px;
  font-weight: 600;
  color: #333;
  border-bottom: 1px solid #f0f0f0;
  font-size: 14px;
}

/* 表单元素焦点样式 */
input:focus, select:focus, textarea:focus {
  border-color: #fb7299;
  box-shadow: 0 0 0 2px rgba(251, 114, 153, 0.2);
}

/* 按钮悬停效果 */
button {
  transition: all 0.2s ease;
}

/* 表格行悬停效果 */
tr.hover\:bg-gray-50:hover {
  background-color: rgba(251, 114, 153, 0.05);
}

/* 卡片阴影效果 */
.shadow-sm {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  transition: box-shadow 0.2s ease;
}

.shadow-sm:hover {
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.1);
}

/* 标签样式 */
.rounded-md {
  transition: background-color 0.2s ease;
}
</style> 