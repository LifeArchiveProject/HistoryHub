<template>
  <div class="task-tree-node">
    <div class="flex items-start">
      <div class="flex items-center">
        <div class="w-6 h-6 flex items-center justify-center">
          <button 
            v-if="childTasks.length > 0" 
            @click="toggleExpanded" 
            class="w-5 h-5 rounded hover:bg-gray-100 flex items-center justify-center focus:outline-none"
          >
            <svg 
              class="w-4 h-4 text-gray-500 transform transition-transform duration-200" 
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
          <div class="bg-white border border-gray-200 rounded-lg shadow-sm p-3 hover:border-[#fb7299] transition-colors duration-200">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <span class="font-medium text-sm">{{ task.name }}</span>
                <div class="flex items-center space-x-1">
                  <span 
                    :class="scheduleTypeClass" 
                    class="px-1.5 py-0.5 rounded-full text-xs"
                  >
                    {{ scheduleTypeLabel }}
                  </span>
                  <span 
                    v-if="task.status" 
                    :class="statusClass" 
                    class="px-1.5 py-0.5 rounded-full text-xs"
                  >
                    {{ task.status }}
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
                  v-if="task.enabled !== undefined"
                  @click="toggleEnabled" 
                  :class="task.enabled ? 'text-orange-600 hover:text-orange-900' : 'text-teal-600 hover:text-teal-900'"
                  class="text-xs px-1.5 py-0.5"
                >
                  {{ task.enabled ? '禁用' : '启用' }}
                </button>
                <button 
                  @click="deleteTask" 
                  class="text-red-600 hover:text-red-900 text-xs px-1.5 py-0.5"
                >
                  删除
                </button>
              </div>
            </div>
            <div class="mt-2 text-xs text-gray-500" v-if="task.last_run">
              上次运行: {{ task.last_run }}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-show="expanded && childTasks.length > 0" class="pl-6 mt-2 space-y-2 relative">
      <!-- 添加垂直连接线 -->
      <div class="absolute left-3 top-0 bottom-0 w-px bg-gray-200"></div>
      <div v-for="childTask in childTasks" :key="getTaskId(childTask)" class="relative">
        <!-- 添加水平连接线 -->
        <div class="absolute left-0 top-1/2 w-3 h-px bg-gray-200"></div>
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

<script>
export default {
  name: 'TaskTreeItem',
  props: {
    task: {
      type: Object,
      required: true
    },
    tasks: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      expanded: true
    }
  },
  computed: {
    // 找出依赖于当前任务的子任务
    childTasks() {
      return this.tasks.filter((t) => {
        // 使用更基本的JavaScript方式安全地访问属性
        const dependencies = [];
        if (t && typeof t === 'object') {
          if ('depends_on' in t && Array.isArray(t['depends_on'])) {
            dependencies.push(...t['depends_on']);
          } else if ('requires' in t && Array.isArray(t['requires'])) {
            dependencies.push(...t['requires']);
          }
        }
        return this.task && this.task.task_id && dependencies.includes(this.task.task_id);
      });
    },
    scheduleTypeLabel() {
      const type = this.task.schedule_type || (this.task.schedule && this.task.schedule.type);
      return type === 'daily' ? '每日' : 
             type === 'chain' ? '链式' : 
             type === 'once' ? '一次性' : type;
    },
    scheduleTypeClass() {
      const type = this.task.schedule_type || (this.task.schedule && this.task.schedule.type);
      return {
        'bg-blue-100 text-blue-800': type === 'daily',
        'bg-purple-100 text-purple-800': type === 'chain',
        'bg-green-100 text-green-800': type === 'once'
      };
    },
    statusClass() {
      return {
        'bg-green-100 text-green-800': this.task.status === '配置完成' || this.task.status === 'success',
        'bg-yellow-100 text-yellow-800': this.task.status === '执行中',
        'bg-red-100 text-red-800': this.task.status === '失败' || this.task.status === 'error'
      };
    }
  },
  methods: {
    toggleExpanded() {
      this.expanded = !this.expanded;
    },
    viewDetail() {
      this.$emit('view-detail', this.task.task_id);
    },
    editTask() {
      this.$emit('edit-task', this.task.task_id);
    },
    executeTask() {
      this.$emit('execute-task', this.task.task_id);
    },
    deleteTask() {
      this.$emit('delete-task', this.task.task_id);
    },
    toggleEnabled() {
      this.$emit('toggle-enabled', this.task.task_id, !this.task.enabled);
    },
    // 安全地获取任务ID
    getTaskId(task) {
      return task && typeof task === 'object' && 'task_id' in task ? task.task_id : Math.random().toString();
    }
  }
}
</script>

<style scoped>
.task-tree-node {
  transition: all 0.2s ease;
}
</style> 