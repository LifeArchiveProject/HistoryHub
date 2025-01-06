<template>
  <analytics-layout>
    <!-- 固定在顶部的导航 -->
    <div class="fixed top-0 left-0 right-0 z-50">
      <div class="bg-white/5 backdrop-blur-md border-b border-white/10 dark:bg-black/5 dark:border-gray-800/50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex justify-between items-center h-16">
            <h1 class="text-2xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
              {{ selectedYear }}年度回顾
            </h1>
            <div class="flex items-center space-x-4">
              <select
                v-model="selectedYear"
                class="w-24 bg-white/10 backdrop-blur text-gray-800 dark:text-white border border-white/20 dark:border-gray-700 rounded-lg px-3 py-1 focus:ring-2 focus:ring-[#fb7299] focus:border-transparent transition-colors duration-200"
                :disabled="loading"
              >
                <option v-for="year in availableYears" :key="year" :value="year">
                  {{ year }}年
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="relative h-full pt-16">
      <!-- 页面容器 -->
      <div class="h-full">
        <Transition mode="out-in" name="fade">
          <!-- 开场页 -->
          <HeroPage v-if="currentPage === 0" key="hero" :year="selectedYear" />

          <!-- 数据概览页 -->
          <OverviewPage v-else-if="currentPage === 1" key="overview" :viewing-data="viewingData" />

          <!-- 连续观看页 -->
          <StreakPage v-else-if="currentPage === 2" key="streak" :viewing-data="viewingData" />

          <!-- 时间分析页 -->
          <TimeAnalysisPage v-else-if="currentPage === 3" key="time-analysis" :viewing-data="viewingData" />

          <!-- 最爱重温页 -->
          <RewatchPage v-else-if="currentPage === 4" key="rewatch" :viewing-data="viewingData" />

          <!-- 视频完成率分析页 -->
          <OverallCompletionPage v-else-if="currentPage === 5" key="overall-completion" :viewing-data="viewingData" />

          <!-- UP主完成率分析页 -->
          <AuthorCompletionPage v-else-if="currentPage === 6" key="author-completion" :viewing-data="viewingData" />

          <!-- 标签分析页 -->
          <TagsPage v-else-if="currentPage === 7" key="tags" :viewing-data="viewingData" />

          <!-- 时间分布分析页 -->
          <TimeDistributionPage v-else-if="currentPage === 8" key="time-distribution" :viewing-data="viewingData" />

          <!-- 月度趋势页 -->
          <MonthlyPage v-else-if="currentPage === 9" key="monthly" :viewing-data="viewingData" />

          <!-- 视频时长分析页 -->
          <DurationAnalysisPage v-else-if="currentPage === 10" key="duration-analysis" :viewing-data="viewingData" />

          <!-- 标题分析页 -->
          <TitleAnalysisPage v-else-if="currentPage === 11" key="title-analysis" :title-analytics="analyticsData" />
        </Transition>
      </div>
    </div>
  </analytics-layout>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'
import { getAvailableYears, getTitleAnalytics, getViewingAnalytics } from '../../../api/api.js'
import HeroPage from '../analytics/pages/HeroPage.vue'
import OverviewPage from '../analytics/pages/OverviewPage.vue'
import StreakPage from '../analytics/pages/StreakPage.vue'
import TimeAnalysisPage from '../analytics/pages/TimeAnalysisPage.vue'
import RewatchPage from '../analytics/pages/RewatchPage.vue'
import OverallCompletionPage from '../analytics/pages/OverallCompletionPage.vue'
import AuthorCompletionPage from '../analytics/pages/AuthorCompletionPage.vue'
import TagsPage from '../analytics/pages/TagsPage.vue'
import TimeDistributionPage from '../analytics/pages/TimeDistributionPage.vue'
import MonthlyPage from '../analytics/pages/MonthlyPage.vue'
import DurationAnalysisPage from '../analytics/pages/DurationAnalysisPage.vue'
import TitleAnalysisPage from '../analytics/pages/TitleAnalysisPage.vue'
import AnalyticsLayout from '../analytics/layout/AnalyticsLayout.vue'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
} from 'echarts/components'
import { use } from 'echarts/core'
import 'echarts-wordcloud'

// 注册必要的组件
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
])

// 状态
const selectedYear = ref(new Date().getFullYear() - 1)
const availableYears = ref([])
const loading = ref(true)
const analyticsData = ref(null)
const viewingData = ref(null)
const currentPage = ref(0)
const isTransitioning = ref(false)

// 滚动和触摸相关状态
let touchStartX = 0
let touchStartY = 0
let lastWheelTime = 0
const wheelThreshold = 30 // 降低滚动阈值
const wheelCooldown = 800 // 增加冷却时间以适应新的动画持续时间

// 页面配置
const pages = [
  { name: '开场', color: '#fb7299' },
  { name: '数据概览', color: '#fc9b7a' },
  { name: '连续观看', color: '#fb7299' },
  { name: '时间分析', color: '#fc9b7a' },
  { name: '最爱重温', color: '#fb7299' },
  { name: '视频完成率', color: '#fc9b7a' },
  { name: 'UP主完成率', color: '#fb7299' },
  { name: '标签分析', color: '#fc9b7a' },
  { name: '时间分布', color: '#fb7299' },
  { name: '月度趋势', color: '#fc9b7a' },
  { name: '视频时长分析', color: '#fb7299' },
  { name: '标题分析', color: '#fc9b7a' }
]

// 监听页面切换
watch(currentPage, (newPage, oldPage) => {
  // 减少过渡动画时间
  isTransitioning.value = true
  setTimeout(() => {
      isTransitioning.value = false
  }, 300)
})

// 键盘导航
const handleKeydown = (e) => {
  if (e.key === 'ArrowRight' && currentPage.value < pages.length - 1) {
    currentPage.value++
  } else if (e.key === 'ArrowLeft' && currentPage.value > 0) {
    currentPage.value--
  }
}

// 修改页面切换处理
const handlePageTransition = (newPage) => {
  if (isTransitioning.value) return
  currentPage.value = newPage
}

// 修改滚轮事件处理
const handleWheel = (e) => {
  const now = Date.now()
  if (isTransitioning.value || now - lastWheelTime < wheelCooldown) return

  const deltaY = Math.abs(e.deltaY)
  if (deltaY < wheelThreshold) return

  lastWheelTime = now

  if (e.deltaY > 0 && currentPage.value < pages.length - 1) {
    handlePageTransition(currentPage.value + 1)
  } else if (e.deltaY < 0 && currentPage.value > 0) {
    handlePageTransition(currentPage.value - 1)
  }
}

// 修改触摸事件处理
const handleTouchStart = (e) => {
  if (isTransitioning.value) return
  touchStartX = e.touches[0].clientX
  touchStartY = e.touches[0].clientY
}

const handleTouchMove = (e) => {
  if (isTransitioning.value) return
  e.preventDefault() // 防止页面滚动
}

const handleTouchEnd = (e) => {
  if (isTransitioning.value) return

  const touchEndX = e.changedTouches[0].clientX
  const touchEndY = e.changedTouches[0].clientY
  const deltaX = touchEndX - touchStartX
  const deltaY = touchEndY - touchStartY

  if (Math.abs(deltaY) > Math.abs(deltaX)) {
    if (Math.abs(deltaY) < 50) return

    if (deltaY < 0 && currentPage.value < pages.length - 1) {
      handlePageTransition(currentPage.value + 1)
    } else if (deltaY > 0 && currentPage.value > 0) {
      handlePageTransition(currentPage.value - 1)
    }
  }
}

// 获取数据方法
const fetchAvailableYears = async () => {
  try {
    const response = await getAvailableYears()
    if (response.data.status === 'success') {
      availableYears.value = response.data.data
      if (!availableYears.value.includes(selectedYear.value)) {
        selectedYear.value = availableYears.value[0]
      }
    }
  } catch (error) {
    console.error('获取可用年份失败:', error)
  }
}

const fetchAnalyticsData = async () => {
  loading.value = true
  try {
    console.log('Fetching analytics data for year:', selectedYear.value)
    const [titleResponse, viewingResponse] = await Promise.all([
      getTitleAnalytics(selectedYear.value),
      getViewingAnalytics(selectedYear.value)
    ])

    if (titleResponse.data.status === 'success') {
      analyticsData.value = titleResponse.data.data
    }

    if (viewingResponse.data.status === 'success') {
      viewingData.value = viewingResponse.data.data
    }
  } catch (error) {
    console.error('获取分析数据失败:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    await Promise.all([
      fetchAvailableYears(),
      fetchAnalyticsData()
    ])
  } finally {
    loading.value = false
  }
}

// 监听年份变化
watch(selectedYear, async (newYear) => {
  if (newYear) {
    await refreshData()
  }
})

// 生命周期钩子
onMounted(async () => {
  await refreshData()
  window.addEventListener('wheel', handleWheel, { passive: false })
  window.addEventListener('touchstart', handleTouchStart)
  window.addEventListener('touchmove', handleTouchMove, { passive: false })
  window.addEventListener('touchend', handleTouchEnd)
})

onUnmounted(() => {
  window.removeEventListener('wheel', handleWheel)
  window.removeEventListener('touchstart', handleTouchStart)
  window.removeEventListener('touchmove', handleTouchMove)
  window.removeEventListener('touchend', handleTouchEnd)
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 添加过渡效果 */
select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23fb7299' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

select:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(251, 114, 153, 0.2);
}

@media (prefers-color-scheme: dark) {
  select {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  }
}
</style>
