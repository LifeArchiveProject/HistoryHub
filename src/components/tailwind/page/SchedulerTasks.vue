<template>
  <div class="min-h-screen bg-gray-50/30 dark:bg-gray-900">
    <div class="py-4">
      <div class="max-w-7xl mx-auto px-3">
        <!-- 任务列表包装层 - 添加相对定位以便放置新建按钮 -->
        <div class="relative mb-6">
          <!-- 任务列表 -->
          <div v-if="loading" class="flex justify-center items-center py-20">
            <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#fb7299]"></div>
          </div>

          <div v-else-if="tasks.length === 0" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 text-center">
            <!-- 在空状态页面添加标题和新建按钮 -->
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-base font-medium text-gray-900 dark:text-gray-100">计划任务</h3>
              <button 
                @click="openCreateTaskModal" 
                class="text-[#fb7299] hover:text-[#fb7299]/80 transition-colors text-sm font-medium"
              >
                新建任务
              </button>
            </div>
            
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-gray-100">暂无计划任务</h3>
            <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">点击"新建任务"按钮创建您的第一个计划任务</p>
          </div>

          <div v-else class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
            <!-- 添加表格标题 -->
            <div class="px-4 py-3 flex justify-between items-center border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-base font-medium text-gray-900 dark:text-gray-100">计划任务</h3>
              <button 
                @click="openCreateTaskModal" 
                class="text-[#fb7299] hover:text-[#fb7299]/80 transition-colors text-sm font-medium"
              >
                新建任务
              </button>
            </div>
            
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead class="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">任务ID</th>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">名称</th>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">调度类型</th>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">调度时间</th>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">成功率</th>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">最后执行</th>
                    <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">状态</th>
                    <th scope="col" class="px-4 py-2 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      <!-- 移除这里的新建任务按钮，因为已经添加到标题中 -->
                      操作
                    </th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  <template v-for="task in tasks" :key="task.task_id">
                    <!-- 主任务行 -->
                    <tr class="hover:bg-gray-50 dark:hover:bg-gray-700 border-t-2 border-gray-100 dark:border-gray-700">
                      <td class="px-4 py-3 whitespace-nowrap text-xs font-medium text-gray-900 dark:text-gray-100">
                        <div class="flex items-center space-x-1">
                          <button 
                            v-if="task.sub_tasks && task.sub_tasks.length > 0"
                            @click="task.isExpanded = !task.isExpanded"
                            class="p-0.5 rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                          >
                            <svg 
                              class="w-3.5 h-3.5 text-gray-500 transform transition-transform"
                              :class="{'rotate-90': task.isExpanded}"
                              fill="none" 
                              viewBox="0 0 24 24" 
                              stroke="currentColor"
                            >
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                            </svg>
                          </button>
                          {{ task.task_id }}
                        </div>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                        <div class="flex items-center">
                          {{ task.config?.name || task.task_id }}
                          <span v-if="task.sub_tasks && task.sub_tasks.length > 0" 
                                class="ml-2 px-1.5 py-0.5 text-xs rounded-full bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300">
                            {{ task.sub_tasks.length }}个子任务
                          </span>
                        </div>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                        <span 
                          :class="{
                            'bg-blue-100 text-blue-800': task.config?.schedule_type === 'daily',
                            'bg-purple-100 text-purple-800': task.config?.schedule_type === 'chain',
                            'bg-green-100 text-green-800': task.config?.schedule_type === 'once',
                            'bg-yellow-100 text-yellow-800': task.config?.schedule_type === 'interval'
                          }" 
                          class="px-1.5 inline-flex text-xs leading-5 font-semibold rounded-full"
                        >
                          {{ 
                            task.config?.schedule_type === 'daily' ? '每日' : 
                            task.config?.schedule_type === 'chain' ? '链式' : 
                            task.config?.schedule_type === 'once' ? '一次性' : 
                            task.config?.schedule_type === 'interval' ? '间隔' : 
                            task.config?.schedule_type 
                          }}
                        </span>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                        {{ 
                          task.config?.schedule_type === 'chain' ? '依赖主任务' : 
                          task.config?.schedule_type === 'interval' ? 
                            (task.config?.interval_value || '-') + ' ' + 
                            (task.config?.interval_unit === 'minutes' ? '分钟' : 
                             task.config?.interval_unit === 'hours' ? '小时' : 
                             task.config?.interval_unit === 'days' ? '天' : 
                             task.config?.interval_unit === 'months' ? '月' : 
                             task.config?.interval_unit === 'years' ? '年' : 
                             task.config?.interval_unit || '') : 
                          task.config?.schedule_time || '-' 
                        }}
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                        <span v-if="task.execution?.success_rate !== undefined" class="inline-flex items-center">
                          {{ Math.round(task.execution.success_rate) }}%
                          <div class="ml-1.5 h-1 w-12 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                            <div 
                              class="h-full rounded-full" 
                              :class="{
                                'bg-green-500': task.execution.success_rate >= 90,
                                'bg-yellow-500': task.execution.success_rate >= 60 && task.execution.success_rate < 90,
                                'bg-red-500': task.execution.success_rate < 60
                              }"
                              :style="{width: `${task.execution.success_rate}%`}"
                            ></div>
                          </div>
                        </span>
                        <span v-else>-</span>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                        {{ task.execution?.last_run || '未记录' }}
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                        <span 
                          :class="{
                            'bg-green-100 text-green-800': task.config?.enabled === true,
                            'bg-red-100 text-red-800': task.config?.enabled === false
                          }" 
                          class="px-1.5 inline-flex text-xs leading-5 font-semibold rounded-full"
                        >
                          {{ task.config?.enabled ? '已启用' : '已禁用' }}
                        </span>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-right text-xs font-medium">
                        <div class="flex justify-end space-x-1.5">
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
                            @click="openCreateSubTaskModal(task.task_id)" 
                            class="text-purple-600 hover:text-purple-900"
                          >
                            添加子任务
                          </button>
                          <button 
                            @click="executeTask(task.task_id)" 
                            class="text-green-600 hover:text-green-900"
                          >
                            执行
                          </button>
                          <button 
                            v-if="task.config?.enabled !== undefined"
                            @click="toggleTaskEnabled(task.task_id, !task.config.enabled)" 
                            :class="task.config.enabled ? 'text-orange-600 hover:text-orange-900' : 'text-teal-600 hover:text-teal-900'"
                          >
                            {{ task.config.enabled ? '禁用' : '启用' }}
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
                    <!-- 子任务行 -->
                    <template v-if="task.sub_tasks && task.sub_tasks.length > 0 && task.isExpanded">
                      <tr v-for="subTask in task.sub_tasks" 
                          :key="subTask.task_id" 
                          class="bg-[#fff8fa] dark:bg-pink-900/10 hover:bg-[#fff2f6] dark:hover:bg-pink-900/20 border-l-4 border-[#fb7299]/30">
                        <td class="pl-12 pr-4 py-2.5 whitespace-nowrap text-xs font-medium text-gray-900 dark:text-gray-100">
                          <div class="flex items-center">
                            <svg class="w-3.5 h-3.5 text-gray-400 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                            </svg>
                            {{ subTask.task_id }}
                          </div>
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                          {{ subTask.config?.name || subTask.task_id }}
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                          <span class="px-1.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
                            链式
                          </span>
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                          依赖主任务
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                          <span v-if="subTask.execution?.success_rate !== undefined" class="inline-flex items-center">
                            {{ Math.round(subTask.execution.success_rate) }}%
                            <div class="ml-1.5 h-1 w-12 bg-gray-200 rounded-full overflow-hidden">
                              <div 
                                class="h-full rounded-full" 
                                :class="{
                                  'bg-green-500': subTask.execution.success_rate >= 90,
                                  'bg-yellow-500': subTask.execution.success_rate >= 60 && subTask.execution.success_rate < 90,
                                  'bg-red-500': subTask.execution.success_rate < 60
                                }"
                                :style="{width: `${subTask.execution.success_rate}%`}"
                              ></div>
                            </div>
                          </span>
                          <span v-else>-</span>
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                          {{ subTask.execution?.last_run || '未记录' }}
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500 dark:text-gray-400">
                          <span 
                            :class="{
                              'bg-green-100 text-green-800': subTask.config?.enabled === true,
                              'bg-red-100 text-red-800': subTask.config?.enabled === false
                            }" 
                            class="px-1.5 inline-flex text-xs leading-5 font-semibold rounded-full"
                          >
                            {{ subTask.config?.enabled ? '已启用' : '已禁用' }}
                          </span>
                        </td>
                        <td class="px-4 py-3 whitespace-nowrap text-right text-xs font-medium">
                          <div class="flex justify-end space-x-1.5">
                            <button 
                              @click="openTaskDetailModal(subTask.task_id)" 
                              class="text-indigo-600 hover:text-indigo-900"
                            >
                              详情
                            </button>
                            <button 
                              @click="openEditTaskModal(subTask.task_id)" 
                              class="text-blue-600 hover:text-blue-900"
                            >
                              编辑
                            </button>
                            <button 
                              v-if="subTask.config?.enabled !== undefined"
                              @click="toggleTaskEnabled(subTask.task_id, !subTask.config.enabled)" 
                              :class="subTask.config.enabled ? 'text-orange-600 hover:text-orange-900' : 'text-teal-600 hover:text-teal-900'"
                            >
                              {{ subTask.config.enabled ? '禁用' : '启用' }}
                            </button>
                            <button 
                              @click="confirmDeleteTask(subTask.task_id, task.task_id)" 
                              class="text-red-600 hover:text-red-900"
                            >
                              删除
                            </button>
                          </div>
                        </td>
                      </tr>
                    </template>
                  </template>
                </tbody>
              </table>
            </div>
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
    :task-name="currentTask?.config?.name || currentTask?.task_id"
  />

  <!-- 创建/编辑任务弹窗 -->
  <TaskForm
    v-model:show="showTaskFormModal"
    :is-editing="isEditing"
    :task-id="currentTask?.task_id"
    :parent-task-id="parentTaskId"
    :tasks="tasks"
    @task-saved="fetchTasks"
  />
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { showNotify, showDialog } from 'vant'
import 'vant/es/dialog/style'
import 'vant/es/notify/style'
import 'vant/es/loading/style'
import { 
  getAllSchedulerTasks, 
  getSchedulerTaskDetail, 
  createSchedulerTask, 
  updateSchedulerTask, 
  deleteSchedulerTask, 
  executeSchedulerTask,
  getTaskHistory,
  setTaskEnabled,
  deleteSubTask
} from '../../../api/api'
import TaskForm from '../scheduler/TaskForm.vue'
import TaskDetail from '../scheduler/TaskDetail.vue'
import TaskHistory from '../scheduler/TaskHistory.vue'

// 防抖函数
const debounce = (fn, delay) => {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

// 加载状态
const loading = ref(false)

// 任务列表
const tasks = ref([])

// 当前任务
const currentTask = ref(null)

// 弹窗控制
const showTaskFormModal = ref(false)
const showTaskDetailModal = ref(false)
const showTaskHistoryModal = ref(false)
const selectedTaskHistory = ref([])

// 是否为编辑模式
const isEditing = ref(false)

// 搜索关键词
const searchKeyword = ref('')

// 标签输入
const newTagInput = ref('')

// 父任务ID
const parentTaskId = ref(null)

// 执行任务
const executeTask = async (taskId) => {
  try {
    const response = await executeSchedulerTask(taskId, {
      wait_for_completion: false
    })
    
    if (response.data && response.data.status === 'success') {
      showNotify({ type: 'success', message: '任务执行已启动' })
      // 刷新任务列表
      fetchTasks()
    } else {
      const errorMessage = '执行任务失败: ' + (response.data?.message || '未知错误')
      showNotify({ type: 'danger', message: errorMessage })
    }
  } catch (error) {
    console.error('执行任务出错:', error)
    showNotify({ type: 'danger', message: '执行任务出错: ' + (error.message || '未知错误') })
  }
}

// 获取所有计划任务
const fetchTasks = debounce(async () => {
  if (loading.value) return // 如果正在加载，则不重复获取
  
  loading.value = true
  try {
    const response = await getAllSchedulerTasks({
      include_subtasks: true,
      detail_level: 'full'
    })
    if (response.data && response.data.status === 'success') {
      // 为每个任务添加展开/收起状态
      tasks.value = (response.data.tasks || []).map(task => {
        return {
          ...task,
          isExpanded: true // 默认展开
        }
      })
    } else {
      showNotify({ type: 'danger', message: '获取任务列表失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('获取任务列表出错:', error)
    showNotify({ type: 'danger', message: '获取任务列表出错: ' + (error.message || '未知错误') })
  } finally {
    loading.value = false
  }
}, 300) // 300ms 的防抖延迟

// 刷新任务列表
const refreshTasks = () => {
  fetchTasks()
}

// 打开任务详情弹窗
const openTaskDetailModal = async (taskId) => {
  if (!taskId) {
    return;
  }

  const response = await getSchedulerTaskDetail(taskId);
  
  if (response.data?.status === 'success' && Array.isArray(response.data.tasks) && response.data.tasks.length > 0) {
    const task = response.data.tasks[0];
    
    if (!task.execution) {
      task.execution = {
        status: 'pending',
        success_rate: 0,
        avg_duration: 0,
        total_runs: 0,
        success_runs: 0,
        fail_runs: 0
      };
    }
    
    currentTask.value = task;
    showTaskDetailModal.value = true;
  } else {
    showNotify({ type: 'danger', message: '获取任务详情失败：' + (response.data?.message || '未知错误') });
  }
}

// 获取任务历史记录
const fetchTaskHistory = async (taskId) => {
  try {
    const response = await getTaskHistory({
      task_id: taskId,
      include_subtasks: true,
      page: 1,
      page_size: 20
    })
    if (response.data && response.data.status === 'success') {
      showTaskHistoryModal.value = true
      selectedTaskHistory.value = response.data.history || []
    } else {
      showNotify({ type: 'danger', message: '获取任务历史失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('获取任务历史出错:', error)
    showNotify({ type: 'danger', message: '获取任务历史出错: ' + (error.message || '未知错误') })
  }
}

// 计算历史记录的成功率
const getSuccessRate = (historyList) => {
  if (!historyList || historyList.length === 0) return 0
  
  const successCount = historyList.filter(h => h.status === 'success').length
  return Math.round((successCount / historyList.length) * 100)
}

// 启用/禁用任务
const toggleTaskEnabled = async (taskId, enabled) => {
  try {
    const response = await setTaskEnabled(taskId, enabled)
    if (response.data && response.data.status === 'success') {
      showNotify({ type: 'success', message: enabled ? '任务已启用' : '任务已禁用' })
      // 刷新任务列表
      fetchTasks()
    } else {
      showNotify({ type: 'danger', message: (enabled ? '启用' : '禁用') + '任务失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    showNotify({ type: 'danger', message: '切换任务状态出错: ' + (error.message || '未知错误') })
  }
}

// 打开编辑任务弹窗
const openEditTaskModal = async (taskId) => {
  try {
    // 重置状态
    isEditing.value = true
    parentTaskId.value = null  // 确保编辑时parentTaskId为null
    currentTask.value = null
    
    const response = await getSchedulerTaskDetail(taskId)
    if (response.data?.status === 'success' && Array.isArray(response.data.tasks) && response.data.tasks.length > 0) {
      currentTask.value = response.data.tasks[0]
      showTaskFormModal.value = true
    } else {
      showNotify({ type: 'danger', message: '获取任务详情失败：' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('获取任务详情出错:', error)
    showNotify({ type: 'danger', message: '获取任务详情出错: ' + (error.message || '未知错误') })
  }
}

// 打开创建子任务弹窗
const openCreateSubTaskModal = async (taskId) => {
  try {
    // 重置状态
    isEditing.value = false
    currentTask.value = null
    
    // 先获取主任务详情
    const response = await getSchedulerTaskDetail(taskId)
    if (response.data?.status === 'success' && Array.isArray(response.data.tasks) && response.data.tasks.length > 0) {
      const mainTask = response.data.tasks[0]
      currentTask.value = mainTask
      parentTaskId.value = taskId

      // 检查主任务是否有子任务
      if (mainTask.sub_tasks && mainTask.sub_tasks.length > 0) {
        // 如果有子任务，新子任务应该依赖于最后一个子任务
        const lastSubTask = mainTask.sub_tasks[mainTask.sub_tasks.length - 1]
        currentTask.value = {
          ...mainTask,
          depends_on: {
            task_id: lastSubTask.task_id,
            name: lastSubTask.config?.name || lastSubTask.task_id
          }
        }
      } else {
      }
      
      showTaskFormModal.value = true
    } else {
      showNotify({ type: 'danger', message: '获取主任务详情失败：' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('获取主任务详情出错:', error)
    showNotify({ type: 'danger', message: '获取主任务详情出错: ' + (error.message || '未知错误') })
  }
}

// 打开创建任务弹窗
const openCreateTaskModal = () => {
  // 重置所有状态
  isEditing.value = false
  parentTaskId.value = null
  currentTask.value = null
  showTaskFormModal.value = true
}

// 确认删除任务
const confirmDeleteTask = (taskId, parentTaskId = null) => {
  const isSubTask = !!parentTaskId;
  showDialog({
    title: '确认删除',
    message: isSubTask ? '确定要删除此子任务吗？此操作不可撤销。' : '确定要删除此任务吗？此操作不可撤销。',
    showCancelButton: true,
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    confirmButtonColor: '#fb7299',
  }).then(() => {
    deleteTask(taskId, parentTaskId)
  }).catch(() => {
    // 取消删除
  })
}

// 删除任务
const deleteTask = async (taskId, parentTaskId = null) => {
  try {
    console.log('开始删除任务:', taskId, parentTaskId ? `(父任务: ${parentTaskId})` : '');
    let response;
    
    if (parentTaskId) {
      // 删除子任务
      response = await deleteSubTask(parentTaskId, taskId)
    } else {
      // 删除主任务
      response = await deleteSchedulerTask(taskId)
    }
    
    if (response.data && response.data.status === 'success') {
      showNotify({ type: 'success', message: parentTaskId ? '子任务删除成功' : '任务删除成功' })
      // 关闭所有相关的弹窗
      showTaskDetailModal.value = false
      showTaskHistoryModal.value = false
      // 重新获取任务列表
      fetchTasks()
    } else {
      showNotify({ type: 'danger', message: (parentTaskId ? '删除子任务失败: ' : '删除任务失败: ') + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('删除任务出错:', error)
    showNotify({ type: 'danger', message: (parentTaskId ? '删除子任务出错: ' : '删除任务出错: ') + (error.message || '未知错误') })
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