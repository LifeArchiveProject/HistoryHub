<template>
  <van-dialog
    :show="show"
    @update:show="$emit('update:show', $event)"
    :title="title"
    width="90%"
    :show-confirm-button="false"
    class="select-dialog"
  >
    <template #title>
      <div class="flex items-center justify-between px-4">
        <span>{{ title }}</span>
        <button
          @click="$emit('update:show', false)"
          class="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </template>

    <div class="p-4">
      <!-- 搜索框 -->
      <div class="mb-4 flex items-center space-x-2">
        <div class="flex-1 relative">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="searchPlaceholder"
            class="w-full pl-8 pr-3 py-1.5 text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-1 focus:ring-[#fb7299] focus:border-[#fb7299]"
          />
          <svg class="w-4 h-4 text-gray-400 absolute left-2.5 top-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <button
            v-if="searchQuery"
            @click="resetSearch"
            class="absolute right-2 top-2 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <!-- 方法过滤器 -->
        <select
          v-if="showMethodFilter"
          v-model="methodFilter"
          class="text-sm border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-1 focus:ring-[#fb7299] focus:border-[#fb7299] py-1.5 pl-2 pr-8"
        >
          <option value="ALL">全部</option>
          <option value="GET">GET</option>
          <option value="POST">POST</option>
          <option value="PUT">PUT</option>
          <option value="DELETE">DELETE</option>
        </select>
      </div>

      <!-- 列表内容 -->
      <div class="custom-scrollbar max-h-[45vh] overflow-y-auto pr-2">
        <div v-for="(items, group) in filteredGroupedItems" :key="group" class="mb-4">
          <div 
            class="flex items-center justify-between cursor-pointer mb-2 bg-gray-100 dark:bg-gray-800 p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700"
            @click="toggleGroup(group)"
          >
            <div class="flex items-center space-x-2">
              <span class="text-sm font-medium text-gray-800 dark:text-gray-100">{{ group || '未分类' }}</span>
              <span class="text-xs text-gray-600 dark:text-gray-400">({{ items.length }}个)</span>
            </div>
            <svg 
              class="w-4 h-4 text-gray-600 transform transition-transform duration-200"
              :class="{ 'rotate-90': expandedGroups[group] }"
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
          
          <div v-show="expandedGroups[group]" class="space-y-1 pl-2 border-l-2 border-gray-100 dark:border-gray-700">
            <div 
              v-for="item in items" 
              :key="item.id"
              @click="selectItem(item)"
              class="p-2 hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer rounded-md transition-colors"
              :class="{'bg-[#fb7299]/10 hover:bg-[#fb7299]/20': isSelected(item)}"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="text-sm font-medium text-gray-900 dark:text-gray-100">{{ item.name || '' }}</div>
                  <div class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{{ item.description || '' }}</div>
                </div>
                <div v-if="item.method" class="ml-3">
                  <span class="px-2 py-0.5 text-xs font-medium rounded-full" 
                        :class="{
                          'bg-blue-100 text-blue-800': item.method === 'GET',
                          'bg-green-100 text-green-800': item.method === 'POST',
                          'bg-yellow-100 text-yellow-800': item.method === 'PUT',
                          'bg-red-100 text-red-800': item.method === 'DELETE'
                        }">
                    {{ item.method }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </van-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import 'vant/es/dialog/style'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    default: () => []
  },
  groupBy: {
    type: String,
    default: 'tags'
  },
  selected: {
    type: [String, Array],
    default: null
  },
  multiple: {
    type: Boolean,
    default: false
  },
  showMethodFilter: {
    type: Boolean,
    default: false
  },
  searchPlaceholder: {
    type: String,
    default: '搜索...'
  }
})

const emit = defineEmits(['update:show', 'select', 'update:selected'])

const searchQuery = ref('')
const methodFilter = ref('ALL')
const expandedGroups = ref({})
const selectedItems = ref(props.multiple ? [] : null)

// 初始化选中状态
watch(() => props.selected, (newVal) => {
  selectedItems.value = props.multiple ? (Array.isArray(newVal) ? newVal : []) : newVal
}, { immediate: true })

// 更新格式化任务项的函数以适应新的数据结构
const formatTaskItem = (task) => {
  const formattedTask = {
    id: task.id || task.operationId || task.path,
    name: task.name || task.summary || task.path,
    description: task.description || task.path,
    method: task.method || 'GET',
    tags: Array.isArray(task.tags) ? task.tags : [],
    enabled: task.enabled,
    execution: task.execution || {},
    config: task.config || {},
    parent_id: task.parent_id,
    sub_tasks: task.sub_tasks || [],
    sequence_number: task.sequence_number
  }
  return formattedTask
}

// 分组和过滤数据
const filteredGroupedItems = computed(() => {
  let filtered = props.items.map(formatTaskItem)

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(item => 
      (item.name && item.name.toLowerCase().includes(query)) ||
      (item.description && item.description.toLowerCase().includes(query))
    )
  }

  // 方法过滤
  if (props.showMethodFilter && methodFilter.value !== 'ALL') {
    filtered = filtered.filter(item => item.method === methodFilter.value)
  }

  // 分组
  const grouped = {}
  filtered.forEach(item => {
    if (props.groupBy === 'tags' && Array.isArray(item.tags) && item.tags.length > 0) {
      item.tags.forEach(tag => {
        if (!grouped[tag]) {
          grouped[tag] = []
        }
        grouped[tag].push(item)
      })
    } else {
      const group = item[props.groupBy] || '未分类'
      if (!grouped[group]) {
        grouped[group] = []
      }
      grouped[group].push(item)
    }
  })

  return grouped
})

// 切换分组展开状态
const toggleGroup = (group) => {
  expandedGroups.value[group] = !expandedGroups.value[group]
}

// 重置搜索
const resetSearch = () => {
  searchQuery.value = ''
  methodFilter.value = 'ALL'
  // 重置所有分组为展开状态
  Object.keys(filteredGroupedItems.value).forEach(group => {
    expandedGroups.value[group] = true
  })
}

// 选择项目
const selectItem = (item) => {
  if (props.multiple) {
    const index = selectedItems.value.indexOf(item.id)
    if (index === -1) {
      selectedItems.value.push(item.id)
    } else {
      selectedItems.value.splice(index, 1)
    }
  } else {
    selectedItems.value = item.id
    emit('update:show', false)
  }
  emit('select', item)
  emit('update:selected', selectedItems.value)
}

// 判断是否选中
const isSelected = (item) => {
  if (props.multiple) {
    return selectedItems.value.includes(item.id)
  }
  return selectedItems.value === item.id
}

// 监听显示状态，重置搜索和展开所有分组
watch(() => props.show, (newVal) => {
  if (newVal) {
    resetSearch()
  }
})
</script>

<style scoped>
.select-dialog :deep(.van-dialog) {
  max-height: 80vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.select-dialog :deep(.van-dialog__header) {
  flex-shrink: 0;
  padding: 12px 16px;
  font-size: 14px;
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