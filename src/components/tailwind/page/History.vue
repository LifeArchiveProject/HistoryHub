<template>
  <div>
    <!-- 导航栏 -->
    <Navbar />

    <!-- 主要内容区域 -->
    <div class="mx-auto max-w-7xl sm:px-2 lg:px-8">
      <div class="pt-20">
        <HistoryContent
          :selected-year="selectedYear"
          :page="page"
          @update:total-pages="totalPages = $event"
          @update:total="total = $event"
        />
      </div>

      <!-- 分页组件 -->
      <div class="mx-auto mb-5 mt-8 max-w-4xl">
        <Pagination :current-page="page" :total-pages="totalPages" :use-routing="true" />
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
