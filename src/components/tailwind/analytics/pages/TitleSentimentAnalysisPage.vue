<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- 标题和总结部分 -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
          标题情感分析
        </h2>
        <div class="mt-4 text-gray-600 dark:text-gray-300 max-w-3xl mx-auto" v-if="titleAnalytics && titleAnalytics.sentiment_analysis">
          <p class="mb-2" v-if="titleAnalytics.sentiment_analysis.insights && titleAnalytics.sentiment_analysis.insights[0]" v-html="formatInsightText(titleAnalytics.sentiment_analysis.insights[0])"></p>
          <p v-if="titleAnalytics.sentiment_analysis.insights && titleAnalytics.sentiment_analysis.insights[1]" v-html="formatInsightText(titleAnalytics.sentiment_analysis.insights[1])"></p>
        </div>
      </div>

      <!-- 主要内容区域 - 使用网格布局 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 左侧：情感分布饼图 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6">
          <h3 class="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-4">情感分布</h3>
          <div ref="distributionChartRef" class="w-full h-[300px]"></div>
        </div>

        <!-- 右侧：完成率对比图 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6">
          <h3 class="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-4">情感与完成率关系</h3>
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

// 初始化情感分布饼图
const initDistributionChart = () => {
  if (!distributionChartRef.value || !props.titleAnalytics?.sentiment_analysis?.sentiment_stats) return

  if (distributionChart) {
    distributionChart.dispose()
  }
  distributionChart = echarts.init(distributionChartRef.value)

  const sentimentStats = props.titleAnalytics.sentiment_analysis.sentiment_stats
  const data = Object.entries(sentimentStats).map(([sentiment, stats]) => ({
    name: sentiment,
    value: stats.count
  }))

  const isDark = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDark ? '#e5e7eb' : '#4B5563'
  const legendTextColor = axisLabelColor
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}个视频 ({d}%)',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText }
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: {
        color: legendTextColor
      }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold',
            color: axisLabelColor
          }
        },
        labelLine: {
          show: false
        },
        data: data.map(item => ({
          ...item,
          itemStyle: {
            color: item.name === '积极' ? '#fb7299' : 
                  item.name === '消极' ? '#fc9b7a' : 
                  '#9ca3af'
          }
        }))
      }
    ]
  }

  distributionChart.setOption(option)
}

// 初始化完成率对比图
const initCompletionChart = () => {
  if (!completionChartRef.value || !props.titleAnalytics?.sentiment_analysis?.sentiment_stats) return

  if (completionChart) {
    completionChart.dispose()
  }
  completionChart = echarts.init(completionChartRef.value)

  const sentimentStats = props.titleAnalytics.sentiment_analysis.sentiment_stats
  const data = Object.entries(sentimentStats)
    .sort(([, a], [, b]) => b.avg_completion_rate - a.avg_completion_rate)
    .map(([sentiment, stats]) => ({
      name: sentiment,
      value: (stats.avg_completion_rate * 100).toFixed(1)
    }))

  const isDark = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDark ? '#e5e7eb' : '#4B5563'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText },
      formatter: '{b}: {c}%'
    },
    grid: {
      top: '10%',
      left: '15%',
      right: '5%',
      bottom: '15%'
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        color: axisLabelColor
      }
    },
    yAxis: {
      type: 'value',
      name: '平均完成率',
      axisLabel: {
        color: axisLabelColor,
        formatter: '{value}%'
      }
    },
    series: [
      {
        data: data.map(item => ({
          value: item.value,
          itemStyle: {
            color: item.name === '积极' ? '#fb7299' : 
                  item.name === '消极' ? '#fc9b7a' : 
                  '#9ca3af'
          }
        })),
        type: 'bar',
        barWidth: '40%',
        label: {
          show: true,
          position: 'top',
          color: axisLabelColor,
          formatter: '{c}%'
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

// 深色模式切换时重绘图表
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