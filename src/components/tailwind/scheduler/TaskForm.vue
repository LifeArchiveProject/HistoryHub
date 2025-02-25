<template>
  <van-dialog
    :show="show"
    @update:show="$emit('update:show', $event)"
    :title="isEditing ? '编辑任务' : '创建任务'"
    width="60%"
    :show-confirm-button="false"
    class="task-form-dialog"
  >
    <div class="p-2">
      <form @submit.prevent="submitForm" class="space-y-2">
        <!-- 表单标题和说明 -->
        <div class="flex items-center mb-2 pb-1 border-b border-gray-100">
          <div class="p-1 bg-[#fb7299]/10 rounded-lg mr-2">
            <svg class="w-3.5 h-3.5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-800">{{ isEditing ? '编辑任务信息' : '创建新任务' }}</h3>
            <p class="text-xs text-gray-500">{{ isEditing ? '修改任务配置信息' : '填写以下信息创建新的计划任务' }}</p>
          </div>
        </div>

        <!-- 基本信息 -->
        <div class="bg-white rounded-lg p-1.5 border border-gray-100 shadow-sm">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            基本信息
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label for="taskId" class="block text-xs font-medium text-gray-700 mb-0.5">任务ID *</label>
              <input 
                id="taskId" 
                v-model="form.task_id" 
                type="text" 
                :disabled="isEditing"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1" 
                required
                placeholder="例如：fetch_history"
              />
            </div>
            
            <div>
              <label for="name" class="block text-xs font-medium text-gray-700 mb-0.5">任务名称 *</label>
              <input 
                id="name" 
                v-model="form.name" 
                type="text" 
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1" 
                required
                placeholder="例如：获取B站历史记录"
              />
            </div>
          </div>
        </div>
        
        <!-- API设置 -->
        <div class="bg-white rounded-lg p-1.5 border border-gray-100 shadow-sm">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            API设置
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label for="endpoint" class="block text-xs font-medium text-gray-700 mb-0.5">API端点 *</label>
              <input 
                id="endpoint" 
                v-model="form.endpoint" 
                type="text" 
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1" 
                required
                placeholder="例如：/fetch/bili-history"
              />
            </div>
            
            <div>
              <label for="method" class="block text-xs font-medium text-gray-700 mb-0.5">请求方法 *</label>
              <select 
                id="method" 
                v-model="form.method" 
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1"
                required
              >
                <option value="GET">GET</option>
                <option value="POST">POST</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- 调度设置 -->
        <div class="bg-white rounded-lg p-1.5 border border-gray-100 shadow-sm">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            调度设置
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label for="scheduleType" class="block text-xs font-medium text-gray-700 mb-0.5">调度类型 *</label>
              <select 
                id="scheduleType" 
                v-model="form.schedule.type" 
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1"
                required
              >
                <option value="daily">每日</option>
                <option value="chain">链式</option>
                <option value="once">一次性</option>
              </select>
            </div>
            
            <div v-if="form.schedule.type === 'daily'">
              <label for="scheduleTime" class="block text-xs font-medium text-gray-700 mb-0.5">执行时间 *</label>
              <input 
                id="scheduleTime" 
                v-model="form.schedule.time" 
                type="time" 
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1" 
                required
              />
            </div>
            
            <div v-if="form.schedule.type === 'once'">
              <label for="scheduleDelay" class="block text-xs font-medium text-gray-700 mb-0.5">延迟时间(秒) *</label>
              <input 
                id="scheduleDelay" 
                v-model.number="form.schedule.delay" 
                type="number" 
                min="0"
                class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1" 
                required
              />
            </div>
          </div>
        </div>
        
        <!-- 依赖任务 -->
        <div class="bg-white rounded-lg p-1.5 border border-gray-100 shadow-sm">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
            </svg>
            依赖任务
          </h4>
          <div>
            <label for="requires" class="block text-xs font-medium text-gray-700 mb-0.5">依赖任务 (可选)</label>
            <select 
              id="requires" 
              v-model="form.depends_on" 
              multiple
              class="block w-full rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1"
              size="4"
            >
              <option v-for="task in tasks.filter(t => t.task_id !== form.task_id)" :key="task.task_id" :value="task.task_id">
                {{ task.name }} ({{ task.task_id }})
              </option>
            </select>
            <p class="mt-0.5 text-xs text-gray-500">按住Ctrl键可多选</p>
          </div>
        </div>
        
        <!-- 底部按钮 -->
        <div class="flex justify-end space-x-2 pt-1.5 border-t border-gray-100">
          <button 
            type="button"
            @click="cancel" 
            class="inline-flex items-center px-2 py-1 border border-gray-300 rounded-md shadow-sm text-xs font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-1 focus:ring-offset-1 focus:ring-[#fb7299]"
          >
            取消
          </button>
          <button 
            type="submit" 
            class="inline-flex items-center px-2 py-1 border border-transparent rounded-md shadow-sm text-xs font-medium text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none focus:ring-1 focus:ring-offset-1 focus:ring-[#fb7299]"
          >
            {{ isEditing ? '保存' : '创建' }}
          </button>
        </div>
      </form>
    </div>
  </van-dialog>
</template>

<script setup>
import { ref, computed, reactive, watch } from 'vue'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import { 
  createSchedulerTask, 
  updateSchedulerTask,
  getSchedulerTaskDetail
} from '../../../api/api'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  isEditing: {
    type: Boolean,
    default: false
  },
  taskId: {
    type: String,
    default: ''
  },
  tasks: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:show', 'task-saved'])

// 表单数据
const form = reactive({
  task_id: '',
  name: '',
  endpoint: '',
  method: 'GET',
  params: {},
  schedule: {
    type: 'daily',
    time: '00:00',
    delay: 0
  },
  depends_on: []
})

// 参数JSON文本和错误信息
const paramsJson = ref('{}')
const paramsError = ref('')

// 计算属性：检查表单是否有效
const isFormValid = computed(() => {
  if (!form.task_id || !form.name || !form.endpoint || !form.method) {
    return false
  }
  
  if (form.schedule.type === 'daily' && !form.schedule.time) {
    return false
  }
  
  if (form.schedule.type === 'once' && (form.schedule.delay === null || form.schedule.delay < 0)) {
    return false
  }
  
  return paramsError.value === ''
})

// 重置表单
const resetForm = () => {
  form.task_id = ''
  form.name = ''
  form.endpoint = ''
  form.method = 'GET'
  form.params = {}
  form.schedule.type = 'daily'
  form.schedule.time = '00:00'
  form.schedule.delay = 0
  form.depends_on = []
  paramsJson.value = '{}'
  paramsError.value = ''
}

// 加载任务详情
const loadTaskDetail = async (taskId) => {
  try {
    const response = await getSchedulerTaskDetail(taskId)
    if (response.data && response.data.status === 'success' && response.data.task) {
      const task = response.data.task
      form.task_id = task.task_id
      form.name = task.name
      form.endpoint = task.endpoint
      form.method = task.method
      form.params = task.params || {}
      form.schedule.type = task.schedule?.type || 'daily'
      form.schedule.time = task.schedule?.time || '00:00'
      form.schedule.delay = task.schedule?.delay || 0
      form.depends_on = task.depends_on || task.requires || []
      paramsJson.value = JSON.stringify(task.params || {}, null, 2)
      paramsError.value = ''
    } else {
      showNotify({ type: 'danger', message: '获取任务详情失败' })
    }
  } catch (error) {
    console.error('获取任务详情出错:', error)
    showNotify({ type: 'danger', message: '获取任务详情出错: ' + (error.message || '未知错误') })
  }
}

// 监听taskId变化，加载任务详情
watch(() => props.taskId, (newVal) => {
  if (newVal && props.isEditing) {
    loadTaskDetail(newVal)
  }
})

// 监听show变化，重置表单
watch(() => props.show, (newVal) => {
  if (newVal && !props.isEditing) {
    resetForm()
  }
})

// 监听paramsJson变化，验证JSON格式
watch(paramsJson, (newVal) => {
  if (!newVal.trim()) {
    paramsJson.value = '{}'
    paramsError.value = ''
    return
  }
  
  try {
    JSON.parse(newVal)
    paramsError.value = ''
  } catch (error) {
    paramsError.value = 'JSON格式错误: ' + error.message
  }
})

// 取消按钮
const cancel = () => {
  emit('update:show', false)
}

// 提交表单
const submitForm = async () => {
  if (!isFormValid.value) {
    showNotify({ type: 'warning', message: '请填写所有必填字段并确保参数格式正确' })
    return
  }

  try {
    // 解析参数JSON
    form.params = JSON.parse(paramsJson.value)
    
    let response
    if (props.isEditing) {
      // 更新任务
      response = await updateSchedulerTask(form.task_id, form)
      if (response.data && response.data.status === 'success') {
        showNotify({ type: 'success', message: '任务更新成功' })
      } else {
        showNotify({ type: 'danger', message: '任务更新失败: ' + (response.data?.message || '未知错误') })
        return
      }
    } else {
      // 创建任务
      response = await createSchedulerTask(form)
      if (response.data && response.data.status === 'success') {
        showNotify({ type: 'success', message: '任务创建成功' })
      } else {
        showNotify({ type: 'danger', message: '任务创建失败: ' + (response.data?.message || '未知错误') })
        return
      }
    }
    
    // 关闭弹窗并通知父组件
    emit('update:show', false)
    emit('task-saved')
  } catch (error) {
    console.error('提交任务表单出错:', error)
    showNotify({ type: 'danger', message: '提交任务表单出错: ' + (error.message || '未知错误') })
  }
}
</script>

<script>
export default {
  name: 'TaskForm'
}
</script>

<style scoped>
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
</style> 