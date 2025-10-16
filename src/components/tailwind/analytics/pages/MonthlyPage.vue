<!-- 月度趋势页组件 -->
<template>
  <div class="space-y-6">
    <h3 class="text-4xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      月度观看趋势
    </h3>

    <div v-if="viewingData?.insights?.monthly_pattern" 
      class="text-lg text-center text-gray-600 dark:text-gray-300 mb-8"
      v-html="formatInsightText(viewingData.insights.monthly_pattern)"
    >
    </div>

    <!-- 月度趋势图表 -->
    <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
      <h4 class="text-xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-4">月度趋势</h4>
      <div class="h-[220px]">
        <v-chart ref="chartRef" class="h-full w-full" :option="monthlyOption" autoresize />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import gsap from 'gsap'
import VChart from 'vue-echarts'
import * as echarts from 'echarts/core'
import { useDarkMode } from '@/store/darkMode.js'

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  }
})

const chartRef = ref(null)

const monthlyOption = computed(() => {
  const { isDarkMode } = useDarkMode()
  const isDark = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDark ? '#bbbbbb' : '#999999'
  const axisLineColor = isDark ? '#888888' : '#666666'
  const splitLineColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.1)'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  if (!props.viewingData?.monthly_stats) return {}
  
  const data = Object.entries(props.viewingData.monthly_stats)
    .sort(([a], [b]) => a.localeCompare(b))
  
  return {
    tooltip: {
      trigger: 'axis',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText }
    },
    grid: {
      top: '15%',
      left: '8%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(([month]) => month),
      axisLine: { lineStyle: { color: axisLineColor } },
      axisLabel: { color: axisLabelColor }
    },
    yAxis: {
      type: 'value',
      name: '观看次数',
      axisLine: { lineStyle: { color: axisLineColor } },
      axisLabel: { color: axisLabelColor },
      splitLine: { lineStyle: { color: splitLineColor } }
    },
    series: [{
      data: data.map(([, count]) => count),
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 2.5,
        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
          { offset: 0, color: 'rgba(251, 114, 153, 0.9)' },
          { offset: 1, color: 'rgba(252, 155, 122, 0.9)' }
        ])
      },
      areaStyle: {
        opacity: 0.15,
        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
          { offset: 0, color: 'rgba(251, 114, 153, 0.4)' },
          { offset: 1, color: 'rgba(252, 155, 122, 0)' }
        ])
      },
      symbolSize: 6,
      symbol: 'circle',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
          { offset: 0, color: 'rgba(251, 114, 153, 0.9)' },
          { offset: 1, color: 'rgba(252, 155, 122, 0.9)' }
        ])
      }
    }]
  }
})

onMounted(() => {
  if (chartRef.value) {
    gsap.from(chartRef.value.$el, {
      opacity: 0,
      y: 20,
      duration: 0.5,
      ease: 'power2.out',
      delay: 0.2
    })
  }
})

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}
</script> 