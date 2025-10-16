<template>
  <div class="mx-auto mb-5 mt-8 max-w-4xl lm:text-xs">
    <div class="flex justify-between items-center space-x-4 lm:mx-5">
      <button
        @click="handlePageChange(currentPage - 1)"
        :disabled="currentPage === 1"
        class="flex items-center text-gray-500 dark:text-gray-400 hover:text-[#fb7299] disabled:opacity-40 disabled:cursor-not-allowed transition-colors px-3 py-2"
      >
        <svg class="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        <span class="hidden sm:inline">上一页</span>
      </button>

      <div class="flex items-center text-gray-700 dark:text-gray-300 lm:text-xs">
        <div class="relative mx-1 inline-block">
          <input
            ref="pageInput"
            type="number"
            v-model="currentPageInput"
            @keyup.enter="handleJumpPage"
            @blur="handleJumpPage"
            @focus="handleFocus"
            min="1"
            :max="totalPages"
            class="h-8 w-12 rounded border border-gray-200 dark:border-gray-600 px-2 text-center text-gray-700 dark:text-gray-300 dark:bg-gray-800 transition-colors [appearance:textfield] hover:border-[#fb7299] focus:border-[#fb7299] focus:outline-none focus:ring-1 focus:ring-[#fb7299]/30 lm:h-6 lm:w-10 lm:text-xs [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
          />
        </div>
        <span class="text-gray-500 dark:text-gray-400 mx-1">/ {{ totalPages }}</span>
      </div>

      <button
        @click="handlePageChange(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="flex items-center text-gray-500 dark:text-gray-400 hover:text-[#fb7299] disabled:opacity-40 disabled:cursor-not-allowed transition-colors px-3 py-2"
      >
        <span class="hidden sm:inline">下一页</span>
        <svg class="w-5 h-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
  },
  totalPages: {
    type: Number,
    required: true,
  },
  // 是否使用路由导航（首页使用，搜索页不使用）
  useRouting: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['page-change'])
const router = useRouter()
const route = useRoute()

const currentPageInput = ref(props.currentPage.toString())

// 监听 props 变化更新输入框
watch(
  () => props.currentPage,
  (newPage) => {
    currentPageInput.value = newPage.toString()
  }
)

// 处理页码变化
const handlePageChange = (newPage) => {
  if (newPage >= 1 && newPage <= props.totalPages) {
    if (props.useRouting) {
      // 检查当前是否在搜索页面
      if (route.name && (route.name === 'Search' || route.name === 'SearchPage')) {
        // 搜索页面的路由导航
        if (newPage === 1) {
          router.push(`/search/${route.params.keyword}`)
        } else {
          router.push(`/search/${route.params.keyword}/page/${newPage}`)
        }
      } else {
        // 首页的路由导航
        if (newPage === 1) {
          router.push('/')
        } else {
          router.push(`/page/${newPage}`)
        }
      }
    } else {
      emit('page-change', newPage)
    }
  }
}

// 处理输入框获得焦点
const handleFocus = (event) => {
  event.target.select()
}

// 处理跳转
const handleJumpPage = () => {
  const targetPage = parseInt(currentPageInput.value)
  if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= props.totalPages) {
    if (targetPage !== props.currentPage) {
      handlePageChange(targetPage)
    }
  } else {
    currentPageInput.value = props.currentPage.toString()
  }
}
</script>

<style scoped>
button {
  transition: color 0.3s ease;
}
</style>
