<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- 标题和总结部分 -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
          标题长度分析
        </h2>
        <div class="mt-4 text-gray-600 dark:text-gray-300 max-w-3xl mx-auto" v-if="titleAnalytics && titleAnalytics.length_analysis">
          <p class="mb-2" v-if="titleAnalytics.length_analysis.insights && titleAnalytics.length_analysis.insights[0]" v-html="formatInsightText(titleAnalytics.length_analysis.insights[0])"></p>
          <p v-if="titleAnalytics.length_analysis.insights && titleAnalytics.length_analysis.insights[1]" v-html="formatInsightText(titleAnalytics.length_analysis.insights[1])"></p>
        </div>
      </div>

      <!-- 主要内容区域 - 使用网格布局 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 左侧：标题长度分布图 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6">
          <h3 class="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-4">标题长度分布</h3>
          <div ref="distributionChartRef" class="w-full h-[300px]"></div>
        </div>

        <!-- 右侧：完成率分析图 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6">
          <h3 class="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-4">标题长度与完成率关系</h3>
          <div ref="completionChartRef" class="w-full h-[300px]"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import * as echarts from 'echarts/core'
import { useDarkMode } from '@/store/darkMode.js'

const props = defineProps({
  titleAnalytics: {
    type: Object,
    required: true
  }
})

const distributionChartRef = ref(null)
const completionChartRef = ref(null)
let distributionChart = null
let completionChart = null
const { isDarkMode } = useDarkMode()

// 初始化标题长度分布图
const initDistributionChart = () => {
  if (!distributionChartRef.value || !props.titleAnalytics?.length_analysis?.length_stats) return

  if (distributionChart) {
    distributionChart.dispose()
  }
  distributionChart = echarts.init(distributionChartRef.value)

  const lengthStats = props.titleAnalytics.length_analysis.length_stats
  const data = Object.entries(lengthStats)
    .sort(([a], [b]) => {
      const numA = parseInt(a.split('-')[0])
      const numB = parseInt(b.split('-')[0])
      return numA - numB
    })
    .map(([range, stats]) => ({
      name: range,
      value: stats.count
    }))

  const isDark = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDark ? '#e5e7eb' : '#4B5563'
  const splitLineColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.1)'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipTextColor = isDark ? '#ffffff' : '#111111'

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipTextColor },
      formatter: '{b}: {c}个视频'
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        color: axisLabelColor,
        interval: 1,
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '视频数量',
      axisLabel: {
        color: axisLabelColor
      },
      splitLine: { lineStyle: { color: splitLineColor } }
    },
    series: [
      {
        data: data.map(item => item.value),
        type: 'bar',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#fb7299' },
            { offset: 1, color: '#fc9b7a' }
          ])
        }
      }
    ]
  }

  distributionChart.setOption(option)
}

// 初始化完成率分析图
const initCompletionChart = () => {
  if (!completionChartRef.value || !props.titleAnalytics?.length_analysis?.length_stats) return

  if (completionChart) {
    completionChart.dispose()
  }
  completionChart = echarts.init(completionChartRef.value)

  const lengthStats = props.titleAnalytics.length_analysis.length_stats
  const data = Object.entries(lengthStats)
    .sort(([a], [b]) => {
      const numA = parseInt(a.split('-')[0])
      const numB = parseInt(b.split('-')[0])
      return numA - numB
    })
    .map(([range, stats]) => ({
      name: range,
      value: (stats.avg_completion_rate * 100).toFixed(1)
    }))

  const isDark = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDark ? '#e5e7eb' : '#4B5563'
  const splitLineColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.1)'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipTextColor = isDark ? '#ffffff' : '#111111'

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipTextColor },
      formatter: '{b}: {c}%'
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        color: axisLabelColor,
        interval: 1,
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '平均完成率',
      axisLabel: {
        color: axisLabelColor,
        formatter: '{value}%'
      },
      splitLine: { lineStyle: { color: splitLineColor } }
    },
    series: [
      {
        data: data.map(item => item.value),
        type: 'line',
        smooth: true,
        symbolSize: 8,
        lineStyle: {
          width: 3,
          color: '#fb7299'
        },
        itemStyle: {
          color: '#fb7299'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(251, 114, 153, 0.3)' },
            { offset: 1, color: 'rgba(252, 155, 122, 0.1)' }
          ])
        }
      }
    ]
  }

  completionChart.setOption(option)
}

// 监听窗口大小变化
const handleResize = () => {
  if (distributionChart) {
    distributionChart.resize()
  }
  if (completionChart) {
    completionChart.resize()
  }
}

onMounted(() => {
  initDistributionChart()
  initCompletionChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (distributionChart) {
    distributionChart.dispose()
  }
  if (completionChart) {
    completionChart.dispose()
  }
})

// 监听数据变化
watch(() => props.titleAnalytics, () => {
  if (distributionChart) {
    initDistributionChart()
  }
  if (completionChart) {
    initCompletionChart()
  }
}, { deep: true })

watch(() => isDarkMode.value, () => {
  initDistributionChart()
  initCompletionChart()
})

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}
</script>