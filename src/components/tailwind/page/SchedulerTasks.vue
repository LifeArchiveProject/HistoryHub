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
          </div>
          <button 
            @click="openCreateTaskModal" 
            class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#fb7299]"
          >
            <svg class="mr-2 -ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
            新建主任务
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

        <div v-else class="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">任务ID</th>
                  <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">名称</th>
                  <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">调度类型</th>
                  <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">调度时间</th>
                  <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">成功率</th>
                  <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">最后执行</th>
                  <th scope="col" class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
                  <th scope="col" class="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <template v-for="task in tasks" :key="task.task_id">
                  <!-- 主任务行 -->
                  <tr class="hover:bg-gray-50 border-t-2 border-gray-100">
                    <td class="px-4 py-3 whitespace-nowrap text-xs font-medium text-gray-900">
                      <div class="flex items-center space-x-1">
                        <button 
                          v-if="task.sub_tasks && task.sub_tasks.length > 0"
                          @click="task.isExpanded = !task.isExpanded"
                          class="p-0.5 rounded hover:bg-gray-200 transition-colors"
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
                    <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                      <div class="flex items-center">
                        {{ task.config?.name || task.task_id }}
                        <span v-if="task.sub_tasks && task.sub_tasks.length > 0" 
                              class="ml-2 px-1.5 py-0.5 text-xs rounded-full bg-gray-100 text-gray-600">
                          {{ task.sub_tasks.length }}个子任务
                        </span>
                      </div>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                      <span 
                        :class="{
                          'bg-blue-100 text-blue-800': task.config?.schedule_type === 'daily',
                          'bg-purple-100 text-purple-800': task.config?.schedule_type === 'chain',
                          'bg-green-100 text-green-800': task.config?.schedule_type === 'once'
                        }" 
                        class="px-1.5 inline-flex text-xs leading-5 font-semibold rounded-full"
                      >
                        {{ 
                          task.config?.schedule_type === 'daily' ? '每日' : 
                          task.config?.schedule_type === 'chain' ? '链式' : 
                          task.config?.schedule_type === 'once' ? '一次性' : task.config?.schedule_type 
                        }}
                      </span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                      {{ task.config?.schedule_type === 'chain' ? '依赖主任务' : task.config?.schedule_time || '-' }}
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                      <span v-if="task.execution?.success_rate !== undefined" class="inline-flex items-center">
                        {{ Math.round(task.execution.success_rate) }}%
                        <div class="ml-1.5 h-1 w-12 bg-gray-200 rounded-full overflow-hidden">
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
                    <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                      {{ task.execution?.last_run || '未记录' }}
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
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
                        class="bg-[#fff8fa] hover:bg-[#fff2f6] border-l-4 border-[#fb7299]/30">
                      <td class="pl-12 pr-4 py-2.5 whitespace-nowrap text-xs font-medium text-gray-900">
                        <div class="flex items-center">
                          <svg class="w-3.5 h-3.5 text-gray-400 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                          </svg>
                          {{ subTask.task_id }}
                        </div>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                        {{ subTask.config?.name || subTask.task_id }}
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                        <span class="px-1.5 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
                          链式
                        </span>
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                        依赖主任务
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
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
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
                        {{ subTask.execution?.last_run || '未记录' }}
                      </td>
                      <td class="px-4 py-3 whitespace-nowrap text-xs text-gray-500">
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
                            @click="confirmDeleteTask(subTask.task_id)" 
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
  setTaskEnabled
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
      showNotify({ type: 'danger', message: '执行任务失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    console.error('执行任务出错:', error)
    showNotify({ type: 'danger', message: '执行任务出错: ' + (error.message || '未知错误') })
  }
}

// 获取所有计划任务
const fetchTasks = debounce(async () => {
  console.log('开始获取任务列表')
  if (loading.value) return // 如果正在加载，则不重复获取
  
  loading.value = true
  try {
    const response = await getAllSchedulerTasks({
      include_subtasks: true,
      detail_level: 'full'
    })
    console.log('获取任务列表响应:', response)
    if (response.data && response.data.status === 'success') {
      // 为每个任务添加展开/收起状态
      tasks.value = (response.data.tasks || []).map(task => {
        console.log('处理任务:', task)
        return {
          ...task,
          isExpanded: true // 默认展开
        }
      })
      console.log('更新后的任务列表:', tasks.value)
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
        console.log('主任务有子任务，新子任务将依赖于最后一个子任务:', lastSubTask.task_id)
        currentTask.value = {
          ...mainTask,
          depends_on: {
            task_id: lastSubTask.task_id,
            name: lastSubTask.config?.name || lastSubTask.task_id
          }
        }
      } else {
        console.log('主任务没有子任务，新子任务将依赖于主任务:', taskId)
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