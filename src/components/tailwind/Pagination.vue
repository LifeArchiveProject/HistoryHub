<template>
  <div class="mx-auto mb-5 mt-8 max-w-4xl lm:text-xs">
    <div class="flex justify-between space-x-4 lm:mx-5">
      <button
        @click="handlePageChange(currentPage - 1)"
        :disabled="currentPage === 1"
        class="rounded-md bg-[#00A1D6] px-1 py-2 text-white disabled:cursor-not-allowed disabled:opacity-50 lm:px-1 lm:py-2 lm:text-xs"
      >
        上一页
      </button>

      <div class="flex items-center text-gray-700 lm:text-xs">
        <span>第</span>
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
            class="h-8 w-16 cursor-pointer rounded border border-gray-300 px-1 text-center transition-colors [appearance:textfield] hover:border-[#00A1D6] focus:border-[#00A1D6] focus:outline-none focus:ring-1 focus:ring-[#00A1D6] lm:h-6 lm:w-12 lm:text-xs [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
          />
        </div>
        <span>页 / 共 {{ totalPages }} 页</span>
      </div>

      <button
        @click="handlePageChange(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="rounded-md bg-[#00A1D6] px-1 py-2 text-white disabled:cursor-not-allowed disabled:opacity-50 lm:px-1 lm:py-2 lm:text-xs"
      >
        下一页
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

const emit = defineEmits(['update:currentPage'])
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
      emit('update:currentPage', newPage)
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
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #008ec1;
}
</style>
