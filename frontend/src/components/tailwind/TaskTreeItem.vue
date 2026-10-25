<template>
  <div class="task-tree-node">
    <div class="flex items-start">
      <div class="flex items-center">
        <div class="w-6 h-6 flex items-center justify-center">
          <button 
            v-if="childTasks.length > 0" 
            @click="toggleExpanded" 
            class="w-5 h-5 rounded hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center justify-center focus:outline-none"
          >
            <svg 
              class="w-4 h-4 text-gray-500 dark:text-gray-400 transform transition-transform duration-200"
              :class="{ 'rotate-90': expanded }" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
        <div class="flex-1 min-w-0">
          <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm p-3 hover:border-[#fb7299] transition-colors duration-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <span class="font-medium text-sm text-gray-900 dark:text-gray-100">{{ task.config?.name || task.task_id }}</span>
                <div class="flex items-center space-x-1">
                  <span 
                    v-if="task.config?.schedule_type"
                    :class="scheduleTypeClass" 
                    class="px-1.5 py-0.5 rounded-full text-xs"
                  >
                    {{ scheduleTypeLabel }}
                  </span>
                  <span 
                    v-if="task.execution?.status" 
                    :class="statusClass" 
                    class="px-1.5 py-0.5 rounded-full text-xs"
                  >
                    {{ task.execution.status }}
                  </span>
                </div>
              </div>
              <div class="flex items-center space-x-1">
                <button 
                  @click="viewDetail" 
                  class="text-blue-600 hover:text-blue-900 text-xs px-1.5 py-0.5"
                >
                  详情
                </button>
                <button 
                  @click="editTask" 
                  class="text-green-600 hover:text-green-900 text-xs px-1.5 py-0.5"
                >
                  编辑
                </button>
                <button 
                  @click="executeTask" 
                  class="text-purple-600 hover:text-purple-900 text-xs px-1.5 py-0.5"
                >
                  执行
                </button>
                <button 
                  v-if="task.config?.enabled !== undefined"
                  @click="toggleEnabled" 
                  :class="task.config.enabled ? 'text-orange-600 hover:text-orange-900' : 'text-teal-600 hover:text-teal-900'"
                  class="text-xs px-1.5 py-0.5"
                >
                  {{ task.config.enabled ? '禁用' : '启用' }}
                </button>
                <button 
                  @click="deleteTask" 
                  class="text-red-600 hover:text-red-900 text-xs px-1.5 py-0.5"
                >
                  删除
                </button>
              </div>
            </div>
            <div class="mt-2 text-xs text-gray-500 dark:text-gray-400">
              <div v-if="task.execution?.last_run">上次运行: {{ task.execution.last_run }}</div>
              <div v-if="task.config?.endpoint" class="mt-0.5">端点: {{ task.config.endpoint }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-show="expanded && childTasks.length > 0" class="pl-6 mt-2 space-y-2 relative">
      <!-- 添加垂直连接线 -->
      <div class="absolute left-3 top-0 bottom-0 w-px bg-gray-200 dark:bg-gray-700"></div>
      <div v-for="childTask in childTasks" :key="getTaskId(childTask)" class="relative">
        <!-- 添加水平连接线 -->
        <div class="absolute left-0 top-1/2 w-3 h-px bg-gray-200 dark:bg-gray-700"></div>
        <task-tree-item 
          :task="childTask" 
          :tasks="tasks" 
          @view-detail="$emit('view-detail', $event)"
          @edit-task="$emit('edit-task', $event)"
          @execute-task="$emit('execute-task', $event)"
          @delete-task="$emit('delete-task', $event)"
          @toggle-enabled="$emit('toggle-enabled', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, computed, defineComponent } from 'vue'

type TaskConfig = {
  name?: string;
  schedule_type?: string;
  schedule_time?: string;
  enabled?: boolean;
  endpoint?: string;
  method?: string;
}

type TaskExecution = {
  status?: string;
  last_run?: string;
}

type Task = {
  task_id: string;
  config?: TaskConfig;
  execution?: TaskExecution;
  sub_tasks?: Task[];
  success_rate?: number;
  depends_on?: string[];
  requires?: string[];
  sequence_number?: number;
}

export default defineComponent({
  name: 'TaskTreeItem',
  props: {
    task: {
      type: Object as () => Task,
      required: true
    },
    tasks: {
      type: Array as () => Task[],
      default: () => []
    }
  },
  emits: ['view-detail', 'edit-task', 'execute-task', 'delete-task', 'toggle-enabled'],
  setup(props, { emit }) {
    const expanded = ref(true)

    // 获取子任务，按 sequence_number 排序
    const childTasks = computed(() => {
      const subTasks = props.task.sub_tasks || []
      return subTasks.sort((a, b) => (a.sequence_number || 0) - (b.sequence_number || 0))
    })

    // 计算调度类型标签
    const scheduleTypeLabel = computed(() => {
      const type = props.task.config?.schedule_type
      return type === 'daily' ? '每日' : 
             type === 'chain' ? '链式' : 
             type === 'once' ? '一次性' : 
             type === 'interval' ? '间隔' : type
    })

    // 计算调度类型样式
    const scheduleTypeClass = computed(() => {
      const type = props.task.config?.schedule_type
      return {
        'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-300': type === 'daily',
        'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-300': type === 'chain',
        'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300': type === 'once',
        'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300': type === 'interval'
      }
    })

    // 计算状态样式
    const statusClass = computed(() => {
      const status = props.task.execution?.status
      return {
        'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300': status === 'success',
        'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-300': status === 'running',
        'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300': status === 'error' || status === 'failed'
      }
    })

    // 切换展开状态
    const toggleExpanded = () => {
      expanded.value = !expanded.value
    }

    // 查看详情
    const viewDetail = () => {
      emit('view-detail', props.task.task_id)
    }

    // 编辑任务
    const editTask = () => {
      emit('edit-task', props.task.task_id)
    }

    // 执行任务
    const executeTask = () => {
      emit('execute-task', props.task.task_id)
    }

    // 删除任务
    const deleteTask = () => {
      emit('delete-task', props.task.task_id)
    }

    // 切换启用状态
    const toggleEnabled = () => {
      emit('toggle-enabled', props.task.task_id, !props.task.config?.enabled)
    }

    // 安全地获取任务ID
    const getTaskId = (task: Task | null) => {
      return task?.task_id || Math.random().toString()
    }

    return {
      expanded,
      childTasks,
      scheduleTypeLabel,
      scheduleTypeClass,
      statusClass,
      toggleExpanded,
      viewDetail,
      editTask,
      executeTask,
      deleteTask,
      toggleEnabled,
      getTaskId
    }
  }
})
</script>

<style scoped>
.task-tree-node {
  transition: all 0.2s ease;
}
</style> 