<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- 标题和总结部分 -->
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
          标题互动分析
        </h2>
        <div class="mt-4 text-gray-600 dark:text-gray-300 max-w-3xl mx-auto" v-if="titleAnalytics && titleAnalytics.interaction_analysis">
          <p class="mb-2" v-if="titleAnalytics.interaction_analysis.insights && titleAnalytics.interaction_analysis.insights[0]" v-html="formatInsightText(titleAnalytics.interaction_analysis.insights[0])"></p>
          <p v-if="titleAnalytics.interaction_analysis.insights && titleAnalytics.interaction_analysis.insights[1]" v-html="formatInsightText(titleAnalytics.interaction_analysis.insights[1])"></p>
        </div>
      </div>

      <!-- 互动数据分析 -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- 左侧：关键词互动率排名 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6">
          <h3 class="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-4">关键词互动率排名</h3>
          <div ref="keywordInteractionChartRef" class="w-full h-[360px]"></div>
        </div>

        <!-- 右侧：互动类型分布 -->
        <div class="bg-white/5 backdrop-blur-sm rounded-xl p-6">
          <h3 class="text-xl font-semibold text-gray-600 dark:text-gray-300 mb-4">互动类型分布</h3>
          <div ref="interactionTypeChartRef" class="w-full h-[360px]"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { useDarkMode } from '@/store/darkMode.js'

const props = defineProps({
  titleAnalytics: {
    type: Object,
    required: true
  }
})

const keywordInteractionChartRef = ref(null)
const interactionTypeChartRef = ref(null)
let keywordInteractionChart = null
let interactionTypeChart = null
const { isDarkMode } = useDarkMode()

// 初始化关键词互动率图表
const initKeywordInteractionChart = () => {
  if (!keywordInteractionChartRef.value || !props.titleAnalytics?.interaction_analysis?.interaction_stats) return

  if (keywordInteractionChart) {
    keywordInteractionChart.dispose()
  }
  keywordInteractionChart = echarts.init(keywordInteractionChartRef.value)
  const stats = props.titleAnalytics.interaction_analysis.interaction_stats
  const data = Object.entries(stats)
    .filter(([key]) => key !== '其他') // 过滤掉"其他"类别
    .map(([type, data]) => ({
      name: type,
      value: data.avg_completion_rate,
      keywords: data.keywords || []
    }))
    .sort((a, b) => b.value - a.value)

  const isDark = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDark ? '#e5e7eb' : '#4B5563'
  const splitLineColor = isDark ? 'rgba(255, 255, 255, 0.08)' : '#E5E7EB'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText },
      formatter: (params) => {
        const [param] = params
        const keywords = data.find(item => item.name === param.name)?.keywords || []
        return `${param.name}<br/>
                互动率: ${(param.value * 100).toFixed(1)}%<br/>
                关键词: ${keywords.join('、') || '暂无关键词'}`
      },
      confine: true
    },
    grid: {
      left: '15%',
      right: '8%',
      bottom: '8%',
      top: '8%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLabel: {
        formatter: (value) => `${(value * 100).toFixed(1)}%`,
        color: axisLabelColor
      },
      splitLine: {
        lineStyle: {
          color: splitLineColor
        }
      }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        color: axisLabelColor,
        width: 80,
        overflow: 'truncate'
      }
    },
    series: [
      {
        name: '互动率',
        type: 'bar',
        data: data.map(item => item.value),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#fb7299' },
            { offset: 1, color: '#fc9b7a' }
          ])
        }
      }
    ]
  }

  keywordInteractionChart.setOption(option)
}

// 初始化互动类型分布图表
const initInteractionTypeChart = () => {
  if (!interactionTypeChartRef.value || !props.titleAnalytics?.interaction_analysis?.interaction_stats) return

  if (interactionTypeChart) {
    interactionTypeChart.dispose()
  }
  interactionTypeChart = echarts.init(interactionTypeChartRef.value)
  const stats = props.titleAnalytics.interaction_analysis.interaction_stats
  const data = Object.entries(stats)
    .map(([type, data]) => ({
      name: type,
      value: data.count,
      rate: data.avg_completion_rate
    }))
    .sort((a, b) => b.value - a.value)

  const isDark = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDark ? '#e5e7eb' : '#4B5563'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText },
      formatter: (params) => {
        return `${params.name}<br/>
                数量: ${params.value}个视频<br/>
                平均完成率: ${(data.find(item => item.name === params.name)?.rate * 100).toFixed(1)}%`
      },
      confine: true
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: {
        color: axisLabelColor
      }
    },
    grid: {
      left: '10%',
      containLabel: true
    },
    series: [
      {
        type: 'pie',
        radius: ['30%', '60%'],
        center: ['45%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            formatter: '{b}\n{d}%',
            fontSize: '14',
            fontWeight: 'bold'
          }
        },
        data: data
      }
    ]
  }

  interactionTypeChart.setOption(option)
}

// 监听窗口大小变化
const handleResize = () => {
  keywordInteractionChart?.resize()
  interactionTypeChart?.resize()
}

onMounted(() => {
  initKeywordInteractionChart()
  initInteractionTypeChart()
  window.addEventListener('resize', handleResize)
})

// 监听数据变化
watch(
  () => props.titleAnalytics,
  () => {
    initKeywordInteractionChart()
    initInteractionTypeChart()
  },
  { deep: true }
)

// 深色模式切换时重绘图表
watch(() => isDarkMode.value, () => {
  initKeywordInteractionChart()
  initInteractionTypeChart()
})

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}
</script>