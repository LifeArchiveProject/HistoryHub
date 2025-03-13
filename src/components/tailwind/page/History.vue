<template>
  <!-- 主要内容区域 -->
  <div>
    <!-- 导航栏 -->
    <Navbar
      v-if="currentContent === 'history' && !showRemarks"
      @refresh-data="refreshData"
      v-model:date="date"
      v-model:category="category"
      v-model:business="business"
      v-model:businessLabel="businessLabel"
      :total="total"
      @click-date="show = true"
      :layout="layout"
      @change-layout="layout = $event"
      :is-batch-mode="isBatchMode"
      :show-remarks="showRemarks"
      @toggle-batch-mode="isBatchMode = !isBatchMode"
      @toggle-remarks="showRemarks = !showRemarks"
    />

    <!-- 内容区域 -->
    <div>
      <div class="mx-auto max-w-7xl sm:px-2 lg:px-8">
        <div class="">
          <!-- 历史记录内容 -->
          <HistoryContent
            v-if="currentContent === 'history' && !showRemarks"
            ref="historyContentRef"
            :selected-year="selectedYear"
            :page="page"
            @update:total-pages="totalPages = $event"
            @update:total="total = $event"
            @update:date="date = $event"
            @update:category="category = $event"
            v-model:show="show"
            v-model:showBottom="showBottom"
            :layout="layout"
            :date="date"
            :category="category"
            :business="business"
            :is-batch-mode="isBatchMode"
          />

          <!-- 备注列表内容 -->
          <Remarks v-else-if="showRemarks" />

          <!-- 设置内容 -->
          <Settings v-else-if="currentContent === 'settings'" />
        </div>

        <!-- 分页组件 -->
        <div v-if="currentContent === 'history' && !showRemarks && total > 0" class="mx-auto mb-5 mt-8 max-w-4xl">
          <Pagination :current-page="page" :total-pages="totalPages" :use-routing="true" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from '../Navbar.vue'
import HistoryContent from '../HistoryContent.vue'
import Pagination from '../Pagination.vue'
import Settings from '../Settings.vue'
import Remarks from './Remarks.vue'

// 定义 props
const props = defineProps({
  defaultShowRemarks: {
    type: Boolean,
    default: false
  }
})

// 当前显示的内容
const currentContent = ref('history')

// 路由对象
const router = useRouter()
const route = useRoute()

// 状态
const page = ref(1)
const totalPages = ref(1)
const selectedYear = ref(new Date().getFullYear())
const show = ref(false)
const showBottom = ref(false)
const date = ref('')
const total = ref(0)
const category = ref('')
const layout = ref('list')
const isBatchMode = ref(false)
const showRemarks = ref(false)
const business = ref('')
const businessLabel = ref('')

// 组件引用
const historyContentRef = ref(null)

// 刷新数据方法
const refreshData = async () => {
  console.log('History - refreshData 被调用')
  console.log('当前日期:', date.value)
  console.log('当前分区:', category.value)
  console.log('当前业务类型:', business.value)
  try {
    if (historyContentRef.value && typeof historyContentRef.value.refreshData === 'function') {
      await historyContentRef.value.refreshData()
    } else if (historyContentRef.value && typeof historyContentRef.value.fetchHistoryByDateRange === 'function') {
      await historyContentRef.value.fetchHistoryByDateRange()
    } else {
      console.error('刷新数据失败: HistoryContent 组件的 refreshData 方法不可用')
    }
  } catch (error) {
    console.error('刷新数据失败:', error)
  }
}

// 监听 date 和 category 的变化
watch([date, category], ([newDate, newCategory], [oldDate, oldCategory]) => {
  console.log('History - date/category 变化:', {
    date: { old: oldDate, new: newDate },
    category: { old: oldCategory, new: newCategory }
  })
})

// 监听路由变化
watch(
  () => route.path,
  (path) => {
    if (path === '/settings') {
      currentContent.value = 'settings'
      showRemarks.value = false
    } else if (path === '/remarks') {
      currentContent.value = 'history'
      showRemarks.value = true
    } else if (path === '/' || path.startsWith('/page/')) {
      currentContent.value = 'history'
      showRemarks.value = false
    }
  },
  { immediate: true }
)

// 组件挂载时设置初始状态
onMounted(() => {
  // 设置初始的备注显示状态
  if (props.defaultShowRemarks || route.path === '/remarks') {
    showRemarks.value = true
  }

  // 确保路由参数是单个字符串并进行类型转换
  const pageParam = Array.isArray(route.params.pageNumber)
    ? route.params.pageNumber[0]
    : route.params.pageNumber
  page.value = parseInt(pageParam) || 1

  if (page.value !== 1 && !route.path.startsWith('/remarks')) {
    router.push(`/page/${page.value}`)
  }
})

// 修改路由参数监听部分
watch(
  [() => route.params.pageNumber, () => route.path],
  ([newPage, path], [oldPage, oldPath]) => {
    if (newPage === oldPage && path === oldPath) return

    if (path === '/') {
      if (page.value !== 1) {
        page.value = 1
      }
    } else if (newPage) {
      // 确保 newPage 是单个字符串
      const pageStr = Array.isArray(newPage) ? newPage[0] : newPage
      const pageNum = parseInt(pageStr)
      if (page.value !== pageNum) {
        page.value = pageNum
      }
    }
  },
  { immediate: true }
)
</script>

<style scoped>
@keyframes bounce-x {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(4px);
  }
}

.animate-bounce-x {
  animation: bounce-x 1.5s infinite;
}
</style>
