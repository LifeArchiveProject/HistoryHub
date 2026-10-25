<template>
  <div class="relative" :style="containerStyle">
    <button 
      ref="triggerBtn"
      @click.stop="toggleDropdown" 
      type="button"
      :class="[
        'custom-dropdown-trigger w-full py-1.5 px-2 border border-gray-300 dark:border-gray-600 rounded-md text-xs text-gray-800 dark:text-gray-200 focus:border-[#fb7299] focus:outline-none focus:ring focus:ring-[#fb7299]/20 flex items-center justify-between bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200',
        customClass,
        'whitespace-nowrap overflow-hidden'
      ]"
    >
      <slot name="trigger-content">
        <span class="truncate mr-1">{{ selectedText }}</span>
      </slot>
      <svg class="w-3 h-3 text-[#fb7299] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>
    
    <!-- 下拉菜单 -->
    <div 
      v-if="showDropdown" 
      @click.stop
      class="fixed z-50 mt-1 rounded-lg bg-white dark:bg-gray-800 shadow-lg ring-1 ring-black ring-opacity-5 dark:ring-white/10 border border-gray-200 dark:border-gray-700 focus:outline-none max-w-[90vw]"
      :style="dropdownStyle"
    >
      <div class="py-1 max-h-60 overflow-auto">
        <slot>
          <button
            v-for="(option, index) in options" 
            :key="index"
            @click.stop="selectOption(option.value)"
            class="w-full px-2 py-1 text-xs text-left hover:bg-[#fb7299]/5 hover:text-[#fb7299] transition-colors flex items-center whitespace-nowrap"
            :class="{'text-[#fb7299] bg-[#fb7299]/5 font-medium': modelValue === option.value}"
          >
            {{ option.label }}
          </button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  options: {
    type: Array,
    default: () => []
  },
  selectedText: {
    type: String,
    default: '请选择'
  },
  customClass: {
    type: String,
    default: ''
  },
  minWidth: {
    type: Number,
    default: 120
  },
  useFixedWidth: {
    type: Boolean,
    default: false
  },
  buttonWidth: {
    type: [String, Number],
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

// 计算容器样式（包括宽度控制）
const containerStyle = computed(() => {
  if (props.buttonWidth) {
    return {
      width: typeof props.buttonWidth === 'number' ? `${props.buttonWidth}px` : props.buttonWidth
    }
  }
  return {}
})

const triggerBtn = ref(null)
const showDropdown = ref(false)
const dropdownStyle = ref({})

// 切换下拉菜单
const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value
  
  if (showDropdown.value) {
    // 计算位置
    calculateDropdownPosition()
  }
}

// 选择选项
const selectOption = (value) => {
  emit('update:modelValue', value)
  emit('change', value)
  showDropdown.value = false
}

// 计算下拉菜单位置
const calculateDropdownPosition = () => {
  setTimeout(() => {
    if (triggerBtn.value) {
      const rect = triggerBtn.value.getBoundingClientRect()
      // 使用按钮自身的宽度或指定的最小宽度，不自动放大
      const width = props.useFixedWidth ? rect.width : Math.max(rect.width, props.minWidth || 80)
      
      // 获取视口宽度，确保菜单不会超出边界
      const viewportWidth = window.innerWidth
      let left = rect.left
      
      // 如果下拉菜单右边缘超出视口，调整位置
      if (left + width > viewportWidth - 10) {
        left = Math.max(10, viewportWidth - width - 10)
      }
      
      dropdownStyle.value = {
        top: `${rect.bottom + window.scrollY}px`,
        left: `${left}px`,
        width: `${width}px`,
        maxWidth: viewportWidth - 20 + 'px' // 确保不会超过视口宽度
      }
    }
  }, 0)
}

// 点击外部关闭下拉菜单
const closeDropdown = (event) => {
  if (triggerBtn.value && !triggerBtn.value.contains(event.target)) {
    showDropdown.value = false
  }
}

// 处理窗口大小变化
const handleResize = () => {
  if (showDropdown.value) {
    calculateDropdownPosition()
  }
}

// 处理滚动事件
const handleScroll = () => {
  if (showDropdown.value) {
    calculateDropdownPosition()
  }
}

onMounted(() => {
  document.addEventListener('click', closeDropdown)
  window.addEventListener('resize', handleResize)
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdown)
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('scroll', handleScroll)
})

// 监听modelValue变化
watch(() => props.modelValue, (newVal) => {
  // 如果需要在值变化时做额外处理
})
</script>

<style scoped>
/* 任何自定义样式 */
</style> 