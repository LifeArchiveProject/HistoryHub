<template>
  <div>
    <!-- 导航栏 -->
    <Navbar
      @refresh-data="refreshData"
      :date="date"
      :total="total"
      :category="category"
      @click-date="show = true"
      @click-category="showBottom = true"
    />

    <!-- 主要内容区域 -->
    <div class="pt-[4.5em] smd:pt-20">
      <div class="mx-auto max-w-7xl sm:px-2 lg:px-8">
        <div class="">
          <HistoryContent
            ref="historyContentRef"
            :selected-year="selectedYear"
            :page="page"
            @update:total-pages="totalPages = $event"
            @update:total="total = $event"
            @update:date="date = $event"
            @update:category="category = $event"
            v-model:show="show"
            v-model:showBottom="showBottom"
          />
        </div>

        <!-- 分页组件 -->
        <div class="mx-auto mb-5 mt-8 max-w-4xl">
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

// 路由对象
const router = useRouter()
const route = useRoute()

// 状态变量
const page = ref(1)
const totalPages = ref(0)
const total = ref(0)
const currentYear = new Date().getFullYear()
const selectedYear = ref(currentYear)
const historyContentRef = ref(null)
const date = ref('')
const category = ref('')
const show = ref(false)
const showBottom = ref(false)

// 刷新数据的方法
const refreshData = async () => {
  try {
    console.log('开始刷新数据')
    console.log('historyContentRef:', historyContentRef.value)

    if (historyContentRef.value) {
      console.log('可用的方法:', Object.keys(historyContentRef.value))
      await historyContentRef.value.fetchHistoryByDateRange()
      console.log('数据刷新完成')
    } else {
      console.warn('historyContentRef 不存在')
    }
  } catch (error) {
    console.error('刷新数据失败:', error)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  // 确保路由参数是单个字符串并进行类型转换
  const pageParam = Array.isArray(route.params.pageNumber)
    ? route.params.pageNumber[0]
    : route.params.pageNumber
  page.value = parseInt(pageParam) || 1

  if (page.value !== 1) {
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
