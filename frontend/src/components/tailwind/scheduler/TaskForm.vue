<template>
  <van-dialog
    :show="show"
    @update:show="$emit('update:show', $event)"
    :title="getDialogTitle"
    width="60%"
    :show-confirm-button="false"
    class="task-form-dialog"
  >
    <div class="p-2">
      <form @submit.prevent="submitForm" class="space-y-2">
        <!-- 表单标题和说明 -->
        <div class="flex items-center mb-2 pb-1 border-b border-gray-100 dark:border-gray-700">
          <div class="p-1 bg-[#fb7299]/10 rounded-lg mr-2">
            <svg class="w-3.5 h-3.5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </div>
          <div>
            <h3 class="text-sm font-medium text-gray-800 dark:text-gray-200">{{ getFormTitle }}</h3>
            <p class="text-xs text-gray-500 dark:text-gray-400">{{ getFormDescription }}</p>
          </div>
        </div>

        <!-- 基本信息 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-1.5 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            基本信息
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label for="taskId" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">任务ID</label>
              <input
                id="taskId"
                v-model="form.task_id"
                type="text"
                :disabled="props.isEditing"
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1 dark:bg-gray-700 dark:text-gray-100"
                placeholder="请输入任务ID（选择API端点后会自动填充，可修改）"
                required
              />
            </div>

            <div>
              <label for="name" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">任务名称 *</label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1 dark:bg-gray-700 dark:text-gray-100"
                required
                placeholder="例如：获取B站历史记录"
              />
            </div>
          </div>
        </div>

        <!-- API设置 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-1.5 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
            API设置
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label for="endpoint" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">API端点 *</label>
              <div class="relative">
                <button
                  type="button"
                  @click="showApiSelector = true"
                  class="block w-full text-left rounded-md border border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1.5 px-2 bg-white dark:bg-gray-700 dark:text-gray-100"
                >
                  {{ form.endpoint || '请选择API端点' }}
                </button>
              </div>
            </div>

            <div>
              <label for="method" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">请求方法</label>
              <input
                id="method"
                v-model="form.method"
                type="text"
                disabled
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1 dark:text-gray-100"
              />
            </div>
          </div>
        </div>

        <!-- 热门视频清理设置（仅清理接口显示） -->
        <div v-if="isPopularCleanupEndpoint" class="bg-white dark:bg-gray-800 rounded-lg p-1.5 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4-1.79-4-4-4zm0 10c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z" />
            </svg>
            热门视频清理
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div class="md:col-span-2">
              <label for="popularCleanupYear" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">清理年份（可选）</label>
              <select
                id="popularCleanupYear"
                v-model="popularCleanupYear"
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed dark:bg-gray-700 dark:text-gray-100 disabled:dark:bg-gray-800 disabled:dark:text-gray-500"
                :disabled="popularCleanupYearsLoading"
              >
                <option :value="null">全部年份（不传 year）</option>
                <option
                  v-for="year in popularCleanupYearOptions"
                  :key="year"
                  :value="year"
                >
                  {{ year }}
                </option>
              </select>
              <div v-if="popularCleanupYearsLoading" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                正在获取可用年份...
              </div>
              <div v-else-if="popularCleanupYearsMessage" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                {{ popularCleanupYearsMessage }}
              </div>
              <div v-else-if="popularCleanupDefaultYear" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                建议默认年份：{{ popularCleanupDefaultYear }}
              </div>
            </div>
          </div>
        </div>

        <!-- 调度设置 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-1.5 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            调度设置
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            <div>
              <label for="scheduleType" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">调度类型 *</label>
              <select
                id="scheduleType"
                v-model="form.schedule_type"
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed dark:bg-gray-700 dark:text-gray-100 disabled:dark:bg-gray-800 disabled:dark:text-gray-500"
                required
                :disabled="props.parentTaskId || props.isEditing"
              >
                <option v-if="!props.parentTaskId" value="daily">每日</option>
                <option v-if="!props.parentTaskId" value="interval">间隔执行</option>
                <option value="chain">链式</option>
              </select>
            </div>

            <div v-if="form.schedule_type === 'daily' && !props.parentTaskId">
              <label for="scheduleTime" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">执行时间 *</label>
              <input
                id="scheduleTime"
                v-model="form.schedule_time"
                type="time"
                class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1 dark:bg-gray-700 dark:text-gray-100"
                required
              />
            </div>

            <div v-if="form.schedule_type === 'interval' && !props.parentTaskId" class="col-span-2 grid grid-cols-2 gap-2">
              <div>
                <label for="intervalValue" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">间隔时间 *</label>
                <input
                  id="intervalValue"
                  v-model.number="form.interval"
                  type="number"
                  min="1"
                  class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed dark:bg-gray-700 dark:text-gray-100 disabled:dark:bg-gray-800 disabled:dark:text-gray-500"
                  required
                  :disabled="props.isEditing"
                />
                <span v-if="props.isEditing" class="text-xs text-gray-500 mt-0.5 block">间隔任务的时间不可修改</span>
              </div>
              <div>
                <label for="intervalUnit" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">时间单位 *</label>
                <select
                  id="intervalUnit"
                  v-model="form.unit"
                  class="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1 disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed dark:bg-gray-700 dark:text-gray-100 disabled:dark:bg-gray-800 disabled:dark:text-gray-500"
                  required
                  :disabled="props.isEditing"
                >
                  <option value="minutes">分钟</option>
                  <option value="hours">小时</option>
                  <option value="days">天</option>
                  <option value="months">月</option>
                  <option value="years">年</option>
                </select>
                <span v-if="props.isEditing" class="text-xs text-gray-500 mt-0.5 block">间隔任务的单位不可修改</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 依赖任务 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg p-1.5 border border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-600 uppercase tracking-wider mb-1 flex items-center">
            <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />
            </svg>
            依赖任务
          </h4>
          <div>
            <label for="requires" class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-0.5">依赖任务 (可选)</label>
            <div class="relative">
              <button
                type="button"
                @click="showDependencySelector = true"
                :disabled="props.parentTaskId || props.isEditing"
                class="block w-full text-left rounded-md border border-gray-300 dark:border-gray-600 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] text-xs py-1.5 px-2 min-h-[2rem] disabled:bg-gray-100 disabled:text-gray-500 disabled:cursor-not-allowed bg-white dark:bg-gray-700 dark:text-gray-100 disabled:dark:bg-gray-800 disabled:dark:text-gray-500"
              >
                <div v-if="form.depends_on.length === 0" class="text-gray-500 dark:text-gray-400">
                  {{ props.parentTaskId ? '子任务依赖关系由系统自动设置' : (props.isEditing ? '编辑时不可修改依赖任务' : '选择依赖任务') }}
                </div>
                <div v-else class="flex flex-wrap gap-1">
                  <div
                    v-for="taskId in form.depends_on"
                    :key="taskId"
                    class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-[#fb7299]/10 text-[#fb7299]"
                  >
                    <span>{{ getTaskName(taskId) }}</span>
                    <button
                      type="button"
                      @click.stop="removeTask(taskId)"
                      class="ml-1 hover:text-[#fb7299]/70"
                      v-if="!props.parentTaskId && !props.isEditing"
                    >
                      <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- 底部按钮 -->
        <div class="flex justify-end space-x-2 pt-1.5 border-t border-gray-100 dark:border-gray-700">
          <button
            type="button"
            @click="cancel"
            class="inline-flex items-center px-2 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-xs font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-1 focus:ring-offset-1 focus:ring-[#fb7299]"
          >
            取消
          </button>
          <button
            type="submit"
            class="inline-flex items-center px-2 py-1 border border-transparent rounded-md text-xs font-medium text-white bg-[#fb7299] hover:bg-[#fb7299]/90 focus:outline-none focus:ring-1 focus:ring-offset-1 focus:ring-[#fb7299]"
          >
            {{ getSubmitButtonText }}
          </button>
        </div>
      </form>
    </div>

    <!-- API选择弹窗 -->
    <select-dialog
      v-model:show="showApiSelector"
      title="选择API端点"
      :items="availableEndpoints"
      v-model:selected="selectedEndpoint"
      :show-method-filter="true"
      search-placeholder="搜索API端点..."
      group-by="tags"
      id-field="id"
      name-field="name"
      description-field="description"
      @select="handleApiSelect"
    />

    <!-- 依赖任务选择弹窗 -->
    <select-dialog
      v-model:show="showDependencySelector"
      title="选择依赖任务"
      :items="availableEndpoints"
      v-model:selected="form.depends_on"
      :multiple="false"
      :show-method-filter="true"
      search-placeholder="搜索任务..."
      group-by="tags"
      id-field="operationId"
      name-field="summary"
      description-field="path"
    />
  </van-dialog>
</template>

<script setup>
import { ref, computed, reactive, watch, nextTick } from 'vue'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import SelectDialog from './SelectDialog.vue'
import {
  createSchedulerTask,
  updateSchedulerTask,
  getSchedulerTaskDetail,
  getAvailableEndpoints,
  addSubTask,
  getPopularCleanupYears
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
  parentTaskId: {
    type: String,
    default: ''
  },
  tasks: {
    type: Array,
    default: () => []
  },
  currentTask: {
    type: Object,
    default: () => null
  }
})

const emit = defineEmits(['update:show', 'task-saved'])

// 表单数据
const form = reactive({
  task_id: '',
  name: '',
  endpoint: '',
  method: '',
  params: {},
  schedule_type: 'daily',
  schedule_time: '00:00',
  interval: 1,
  unit: 'hours',
  depends_on: [],
  enabled: true,
  sub_tasks: []
})

// 参数JSON文本和错误信息
const paramsJson = ref('{}')
const paramsError = ref('')

const POPULAR_CLEANUP_ENDPOINT_PATH = '/bilibili/popular/cleanup'

const parseEndpointUrlParts = (endpoint) => {
  const raw = (endpoint || '').trim()
  if (!raw) return { path: '', searchParams: new URLSearchParams() }

  try {
    const url = new URL(raw, 'http://placeholder')
    return { path: url.pathname || '', searchParams: url.searchParams || new URLSearchParams() }
  } catch {
    const [pathPart, queryPart] = raw.split('?')
    return { path: (pathPart || raw).trim(), searchParams: new URLSearchParams(queryPart || '') }
  }
}

const normalizeEndpointPath = (path) => {
  let normalized = (path || '').trim()
  if (!normalized) return ''
  if (!normalized.startsWith('/')) normalized = `/${normalized}`
  normalized = normalized.replace(/\/+$/, '')
  return normalized || '/'
}

const isPopularCleanupEndpointPath = (path) => {
  const normalized = normalizeEndpointPath(path)
  return normalized === POPULAR_CLEANUP_ENDPOINT_PATH || normalized.endsWith(POPULAR_CLEANUP_ENDPOINT_PATH)
}

// 可用的API端点
const availableEndpoints = ref([])

// 在 script setup 部分添加
const showApiSelector = ref(false)
const showDependencySelector = ref(false)
const apiSearchQuery = ref('')
const expandedTags = reactive({})
const methodFilter = ref('ALL')
const selectedEndpoint = ref('')

const popularCleanupYears = ref([])
const popularCleanupDefaultYear = ref(null)
const popularCleanupYearsMessage = ref('')
const popularCleanupYearsLoading = ref(false)
const popularCleanupYearTouched = ref(false)
const cachedPopularCleanupYear = ref(undefined)

const popularCleanupEndpointParts = computed(() => parseEndpointUrlParts(form.endpoint))

const isPopularCleanupEndpoint = computed(() => {
  return isPopularCleanupEndpointPath(popularCleanupEndpointParts.value.path)
})

const popularCleanupYearFromEndpointQuery = computed(() => {
  const year = popularCleanupEndpointParts.value.searchParams.get('year')
  if (!year) return null
  const normalized = Number.parseInt(year, 10)
  return Number.isFinite(normalized) ? normalized : null
})

const popularCleanupYear = computed({
  get: () => (Object.prototype.hasOwnProperty.call(form.params, 'year') ? form.params.year : null),
  set: (year) => {
    popularCleanupYearTouched.value = true
    if (year === null || year === undefined || year === '') {
      if (Object.prototype.hasOwnProperty.call(form.params, 'year')) {
        delete form.params.year
      }
      return
    }
    form.params.year = year
  }
})

const popularCleanupYearOptions = computed(() => {
  const years = Array.isArray(popularCleanupYears.value) ? [...popularCleanupYears.value] : []
  const currentYear = form.params?.year
  const normalizedCurrentYear = typeof currentYear === 'string' ? Number.parseInt(currentYear, 10) : currentYear

  if (Number.isFinite(normalizedCurrentYear) && !years.includes(normalizedCurrentYear)) {
    years.push(normalizedCurrentYear)
  }

  return years
    .filter((y) => Number.isFinite(y))
    .sort((a, b) => b - a)
})

const applyPopularCleanupYearFromEndpointQuery = () => {
  if (!isPopularCleanupEndpoint.value) return
  const yearFromQuery = popularCleanupYearFromEndpointQuery.value
  if (yearFromQuery === null || yearFromQuery === undefined) return
  if (!Object.prototype.hasOwnProperty.call(form.params, 'year')) {
    form.params.year = yearFromQuery
  }
}

const normalizePopularCleanupYearParam = () => {
  if (!form.params || typeof form.params !== 'object') return
  if (!Object.prototype.hasOwnProperty.call(form.params, 'year')) return

  const year = form.params.year
  if (year === null || year === undefined || year === '') {
    delete form.params.year
    return
  }

  if (typeof year === 'string') {
    const normalized = Number.parseInt(year, 10)
    if (Number.isFinite(normalized)) {
      form.params.year = normalized
    } else {
      delete form.params.year
    }
  }
}

const fetchPopularCleanupYears = async () => {
  if (popularCleanupYearsLoading.value) return

  popularCleanupYearsLoading.value = true
  popularCleanupYearsMessage.value = ''
  popularCleanupDefaultYear.value = null

  try {
    const response = await getPopularCleanupYears()
    if (response.data && response.data.status === 'success') {
      popularCleanupYears.value = Array.isArray(response.data.data) ? response.data.data : []
      popularCleanupDefaultYear.value = response.data.default_year ?? null
      popularCleanupYearsMessage.value = response.data.message || ''

      // 新建任务：当用户尚未手动选择且未设置 year 时，自动使用后端建议默认年份
      if (
        isPopularCleanupEndpoint.value &&
        !props.isEditing &&
        !popularCleanupYearTouched.value &&
        !Object.prototype.hasOwnProperty.call(form.params, 'year') &&
        popularCleanupDefaultYear.value !== null &&
        popularCleanupDefaultYear.value !== undefined
      ) {
        form.params.year = popularCleanupDefaultYear.value
      }
    } else {
      popularCleanupYears.value = []
      popularCleanupYearsMessage.value = response.data?.message || '获取年份列表失败'
      popularCleanupDefaultYear.value = null
    }
  } catch (error) {
    popularCleanupYears.value = []
    popularCleanupYearsMessage.value = '获取年份列表出错: ' + (error.message || '未知错误')
    popularCleanupDefaultYear.value = null
  } finally {
    popularCleanupYearsLoading.value = false
  }
}

// 按tag对API进行分组
const groupedEndpoints = computed(() => {
  const groups = {}
  availableEndpoints.value.forEach(endpoint => {
    const tags = endpoint.tags && endpoint.tags.length > 0 ? endpoint.tags : ['未分类']
    tags.forEach(tag => {
      if (!groups[tag]) {
        groups[tag] = []
      }
      groups[tag].push(endpoint)
    })
  })
  return groups
})

// 过滤后的分组结果
const filteredGroupedEndpoints = computed(() => {
  const query = apiSearchQuery.value.toLowerCase()
  const filtered = {}

  Object.entries(groupedEndpoints.value).forEach(([tag, apis]) => {
    const filteredApis = apis.filter(endpoint => {
      const matchesSearch = !query ||
        endpoint.path.toLowerCase().includes(query) ||
        endpoint.summary?.toLowerCase().includes(query)

      const matchesMethod = methodFilter.value === 'ALL' ||
        endpoint.method === methodFilter.value

      return matchesSearch && matchesMethod
    })

    if (filteredApis.length > 0) {
      filtered[tag] = filteredApis
    }
  })

  return filtered
})

// 切换tag展开状态
const toggleTagExpand = (tag) => {
  expandedTags[tag] = !expandedTags[tag]
}

// 重置搜索和展开状态
const resetSearch = () => {
  apiSearchQuery.value = ''
  methodFilter.value = 'ALL'
  Object.keys(groupedEndpoints.value).forEach(tag => {
    expandedTags[tag] = true
  })
}

// 监听搜索框变化
watch(apiSearchQuery, (newVal) => {
  if (!newVal) {
    // 当搜索框清空时，重置所有展开状态
    resetSearch()
  }
})

// 初始化所有tag为展开状态
watch(() => showApiSelector.value, (newVal) => {
  if (newVal) {
    resetSearch()
  }
})

// 监听选中的API端点变化
watch(selectedEndpoint, (newVal) => {
  if (newVal) {
    const endpoint = availableEndpoints.value.find(e => e.id === newVal || e.operationId === newVal || e.path === newVal)
    if (endpoint) {
      form.endpoint = endpoint.description || endpoint.path
      form.method = endpoint.method || 'GET'
      if (!form.task_id) {
        form.task_id = endpoint.id || endpoint.operationId || endpoint.path
      }
      if (!form.name && (endpoint.name || endpoint.summary)) {
        form.name = endpoint.name || endpoint.summary
      }
    }
  }
})

// 获取任务名称
const getTaskName = (taskId) => {
  const endpoint = availableEndpoints.value.find(e => e.operationId === taskId || e.path === taskId)
  return endpoint ? `${endpoint.summary || endpoint.path} (${taskId})` : taskId
}

// 移除依赖任务
const removeTask = (taskId) => {
  form.depends_on = form.depends_on.filter(id => id !== taskId)
}

// 计算属性：检查表单是否有效
const isFormValid = computed(() => {
  // 检查基本字段
  if (!form.task_id.trim() || !form.name.trim() || !form.endpoint || !form.method) {
    return false
  }

  // 检查调度相关字段
  if (form.schedule_type === 'daily' && !form.schedule_time) {
    return false
  }

  if (form.schedule_type === 'interval' && (!form.interval || form.interval < 1 || !form.unit)) {
    return false
  }

  // 检查参数JSON格式
  return paramsError.value === ''
})

// 重置表单
const resetForm = () => {
  // 根据当前的props状态设置初始值
  const initialState = {
    task_id: '',
    name: '',
    endpoint: '',
    method: '',
    params: {},
    schedule_type: props.parentTaskId ? 'chain' : 'daily',
    schedule_time: '00:00',
    interval: 1,
    unit: 'hours',
    depends_on: props.currentTask?.depends_on ? [props.currentTask.depends_on.task_id] : [],
    enabled: true,
    sub_tasks: []
  }

  // 使用Object.keys确保所有属性都被重置
  Object.keys(form).forEach(key => {
    if (key === 'depends_on' && props.parentTaskId && props.currentTask) {
      return
    }
    form[key] = initialState[key]
  })

  // 重置其他相关状态
  selectedEndpoint.value = ''
  paramsJson.value = '{}'
  paramsError.value = ''
  popularCleanupYearTouched.value = false
  cachedPopularCleanupYear.value = undefined
  showApiSelector.value = false
  showDependencySelector.value = false
  apiSearchQuery.value = ''
  methodFilter.value = 'ALL'
  Object.keys(expandedTags).forEach(key => {
    expandedTags[key] = false
  })
}

// 监听show变化
watch(() => props.show, async (newVal) => {
  if (newVal) {
    await fetchAvailableEndpoints()

    if (props.isEditing && props.taskId) {
      await loadTaskDetail(props.taskId)
    } else if (!props.isEditing && props.parentTaskId) {
      resetForm()
      form.schedule_type = 'chain'

      // 查找父任务及其子任务
      const parentTask = props.tasks.find(task => task.task_id === props.parentTaskId)

      if (parentTask?.sub_tasks?.length > 0) {
        // 如果父任务有子任务，依赖最后一个子任务
        const lastSubTask = parentTask.sub_tasks[parentTask.sub_tasks.length - 1]
        form.depends_on = [lastSubTask.task_id]

        // 确保依赖任务在availableEndpoints中
        if (!availableEndpoints.value.find(e => e.operationId === lastSubTask.task_id)) {
          availableEndpoints.value.push({
            operationId: lastSubTask.task_id,
            summary: lastSubTask.config?.name || lastSubTask.task_id,
            path: lastSubTask.task_id
          })
        }
      } else {
        // 如果父任务没有子任务，依赖父任务
        form.depends_on = [props.parentTaskId]

        // 确保父任务在availableEndpoints中
        if (!availableEndpoints.value.find(e => e.operationId === props.parentTaskId)) {
          availableEndpoints.value.push({
            operationId: props.parentTaskId,
            summary: parentTask?.config?.name || props.parentTaskId,
            path: props.parentTaskId
          })
        }
      }
    } else {
      resetForm()
    }
  } else {
    resetForm()
    emit('task-saved')
  }
}, { immediate: true })

// 监听currentTask变化
watch(() => props.currentTask, async (newVal) => {
  if (props.show && !props.isEditing && props.parentTaskId && newVal) {
    await nextTick()
    setDependencyFromCurrentTask(newVal)
  }
})

// 设置依赖关系的辅助函数
const setDependencyFromCurrentTask = (task) => {
  if (!task) {
    form.depends_on = [props.parentTaskId]
    return
  }

  if (task.sub_tasks?.length > 0) {
    // 如果主任务有子任务，依赖最后一个子任务
    const lastSubTask = task.sub_tasks[task.sub_tasks.length - 1]
    form.depends_on = [lastSubTask.task_id]

    // 确保依赖任务在availableEndpoints中
    if (!availableEndpoints.value.find(e => e.operationId === lastSubTask.task_id)) {
      availableEndpoints.value.push({
        operationId: lastSubTask.task_id,
        summary: lastSubTask.config?.name || lastSubTask.task_id,
        path: lastSubTask.task_id
      })
    }
  } else {
    // 如果主任务没有子任务，依赖主任务
    form.depends_on = [props.parentTaskId]

    // 确保父任务在availableEndpoints中
    if (!availableEndpoints.value.find(e => e.operationId === props.parentTaskId)) {
      availableEndpoints.value.push({
        operationId: props.parentTaskId,
        summary: props.parentTaskId,
        path: props.parentTaskId
      })
    }
  }
}

// 加载任务详情
const loadTaskDetail = async (taskId) => {
  try {
    const response = await getSchedulerTaskDetail(taskId, { include_subtasks: true })
    if (response.data && response.data.status === 'success') {
      const taskInfo = response.data.tasks[0]
      if (taskInfo) {
        // 基本信息
        form.task_id = taskInfo.task_id
        form.name = taskInfo.config.name
        form.endpoint = taskInfo.config.endpoint
        form.method = taskInfo.config.method
        form.params = taskInfo.config.params || {}
        if (isPopularCleanupEndpointPath(taskInfo.config.endpoint)) {
          popularCleanupYearTouched.value = true
          applyPopularCleanupYearFromEndpointQuery()
          normalizePopularCleanupYearParam()
        }
        form.schedule_type = taskInfo.config.schedule_type
        form.schedule_time = taskInfo.config.schedule_time
        form.enabled = taskInfo.config.enabled

        // 间隔执行配置
        if (taskInfo.config.schedule_type === 'interval') {
          form.interval = taskInfo.config.interval || 1
          form.unit = taskInfo.config.unit || 'hours'
        }

        // 设置依赖任务
        if (taskInfo.depends_on) {
          form.depends_on = [taskInfo.depends_on.task_id]
          // 确保依赖任务在availableEndpoints中
          if (!availableEndpoints.value.find(e => e.operationId === taskInfo.depends_on.task_id)) {
            availableEndpoints.value.push({
              operationId: taskInfo.depends_on.task_id,
              summary: taskInfo.depends_on.name,
              path: taskInfo.depends_on.task_id
            })
          }
        } else {
          form.depends_on = []
        }

        // 加载子任务
        if (taskInfo.sub_tasks) {
          form.sub_tasks = taskInfo.sub_tasks
        }
      }
    } else {
      showNotify({ type: 'danger', message: '获取任务详情失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    showNotify({ type: 'danger', message: '获取任务详情出错: ' + (error.message || '未知错误') })
  }
}

watch(
  () => [props.show, isPopularCleanupEndpoint.value],
  async ([show, isCleanup]) => {
    if (!show || !isCleanup) return
    applyPopularCleanupYearFromEndpointQuery()
    normalizePopularCleanupYearParam()
    await fetchPopularCleanupYears()
  }
)

watch(isPopularCleanupEndpoint, (isCleanup, wasCleanup) => {
  if (wasCleanup && !isCleanup) {
    cachedPopularCleanupYear.value = popularCleanupYear.value
    if (Object.prototype.hasOwnProperty.call(form.params, 'year')) {
      delete form.params.year
    }
    return
  }

  if (!wasCleanup && isCleanup) {
    normalizePopularCleanupYearParam()
    if (
      cachedPopularCleanupYear.value !== undefined &&
      !Object.prototype.hasOwnProperty.call(form.params, 'year') &&
      cachedPopularCleanupYear.value !== null
    ) {
      form.params.year = cachedPopularCleanupYear.value
    }
  }
})

// 获取可用的API端点
const fetchAvailableEndpoints = async () => {
  try {
    const response = await getAvailableEndpoints()
    if (response.data && response.data.status === 'success') {
      availableEndpoints.value = response.data.endpoints || []
    } else {
      showNotify({ type: 'danger', message: '获取API端点失败: ' + (response.data?.message || '未知错误') })
    }
  } catch (error) {
    showNotify({ type: 'danger', message: '获取API端点出错: ' + (error.message || '未知错误') })
  }
}

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
  resetForm()
  emit('update:show', false)
  emit('task-saved')
}

// 提交表单
const submitForm = async () => {
  try {
    if (props.parentTaskId) {
      form.schedule_type = 'chain'
    }

    // 确保任务ID不为空
    if (!form.task_id.trim()) {
      showNotify({ type: 'danger', message: '任务ID不能为空' })
      return
    }

    console.log('开始提交任务表单:', props.isEditing ? '编辑模式' : (props.parentTaskId ? '子任务模式' : '主任务模式'))

    const taskData = {
      task_id: form.task_id.trim(),
      name: form.name,
      endpoint: form.endpoint,
      method: form.method,
      params: form.params,
      enabled: form.enabled
    }

    // 只有在创建新任务时才设置调度类型和依赖任务
    if (!props.isEditing) {
      taskData.schedule_type = form.schedule_type

      if (form.schedule_type === 'daily') {
        taskData.schedule_time = form.schedule_time
      } else if (form.schedule_type === 'interval') {
        taskData.interval = form.interval
        taskData.unit = form.unit
      }

      if (form.depends_on.length > 0) {
        taskData.depends_on = {
          task_id: form.depends_on[0],
          name: getTaskName(form.depends_on[0])
        }
      }
    } else {
      // 编辑模式下，保留原有的调度类型
      taskData.schedule_type = form.schedule_type

      // 如果是每日任务，可以修改执行时间
      if (form.schedule_type === 'daily') {
        taskData.schedule_time = form.schedule_time
      }
      // 注意：如果是间隔任务，不允许修改间隔时间和单位，所以这里不设置这些字段
    }

    console.log('准备提交的任务数据:', taskData)

    let response
    if (props.isEditing) {
      console.log('开始更新任务:', props.taskId)
      response = await updateSchedulerTask(props.taskId, taskData)
    } else if (props.parentTaskId) {
      console.log('开始添加子任务:', props.parentTaskId)
      response = await addSubTask(props.parentTaskId, {
        ...taskData,
        schedule_type: 'chain'
      })
    } else {
      console.log('开始创建主任务')
      response = await createSchedulerTask({
        task_id: form.task_id.trim(),
        task_type: 'main',
        config: {
          name: form.name,
          endpoint: form.endpoint,
          method: form.method,
          params: form.params,
          schedule_type: form.schedule_type,
          schedule_time: form.schedule_type === 'daily' ? form.schedule_time : undefined,
          interval: form.schedule_type === 'interval' ? form.interval : undefined,
          unit: form.schedule_type === 'interval' ? form.unit : undefined,
          enabled: form.enabled
        },
        depends_on: taskData.depends_on
      })
    }

    console.log('任务操作响应:', response.data)

    if (response.data && response.data.status === 'success') {
      const successMessage = props.isEditing ? '更新成功' :
                             props.parentTaskId ? '子任务创建成功' : '创建成功'
      console.log('任务操作成功:', successMessage)
      showNotify({
        type: 'success',
        message: successMessage
      })
      emit('task-saved')
      emit('update:show', false)
      resetForm()
    } else {
      const errorMessage = (props.isEditing ? '更新失败: ' :
                           props.parentTaskId ? '创建子任务失败: ' : '创建失败: ') +
                           (response.data?.message || '未知错误')
      console.error('任务操作失败:', errorMessage)
      showNotify({
        type: 'danger',
        message: errorMessage
      })
    }
  } catch (error) {
    const errorMessage = (props.isEditing ? '更新出错: ' :
                         props.parentTaskId ? '创建子任务出错: ' : '创建出错: ') +
                         (error.message || '未知错误')
    console.error('任务操作异常:', errorMessage, error)
    showNotify({
      type: 'danger',
      message: errorMessage
    })
  }
}

// 添加handleApiSelect函数
const handleApiSelect = (endpoint) => {
  selectedEndpoint.value = endpoint.id
}

// 在 script setup 中添加计算属性
const getDialogTitle = computed(() => {
  if (props.isEditing) return '编辑任务'
  if (props.parentTaskId) return '创建子任务'
  return '创建主任务'
})

const getFormTitle = computed(() => {
  if (props.isEditing) return '编辑任务信息'
  if (props.parentTaskId) return '创建新子任务'
  return '创建新主任务'
})

const getFormDescription = computed(() => {
  if (props.isEditing) return '修改任务配置信息'
  if (props.parentTaskId) return '填写以下信息创建新的子任务'
  return '填写以下信息创建新的主任务'
})

const getSubmitButtonText = computed(() => {
  if (props.isEditing) return '保存'
  if (props.parentTaskId) return '创建子任务'
  return '创建主任务'
})

// 监听props变化，确保状态同步
watch(() => props.parentTaskId, (newVal) => {
  if (props.show) {
    // 如果弹窗是打开的，根据parentTaskId的变化更新schedule_type
    form.schedule_type = newVal ? 'chain' : 'daily'
  }
})

watch(() => props.isEditing, (newVal) => {
  if (props.show && newVal && props.taskId) {
    // 如果弹窗是打开的且切换到编辑模式，加载任务详情
    loadTaskDetail(props.taskId)
  }
})
</script>

<script>
export default {
  name: 'TaskForm'
}
</script>

<style scoped>
.task-form-dialog :deep(.van-dialog) {
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.task-form-dialog :deep(.van-dialog__header) {
  flex-shrink: 0;
  padding: 12px 16px;
  font-size: 14px;
  background-color: #f9fafb; /* gray-50 */
  border-bottom: 1px solid #f3f4f6; /* gray-100 */
  color: #111827; /* gray-900 */
}
.dark .task-form-dialog :deep(.van-dialog__header) {
  background-color: #1f2937; /* gray-800 */
  border-bottom-color: #374151; /* gray-700 */
  color: #e5e7eb; /* gray-200 */
}

/* 自定义滚动条样式 */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #fb7299 #f3f4f6;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f3f4f6;
  border-radius: 2px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #fb7299;
  border-radius: 2px;
}
</style>
