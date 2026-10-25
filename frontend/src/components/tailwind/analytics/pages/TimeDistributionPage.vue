<!-- 时间分布页组件 -->
<template>
  <div class="space-y-6">
    <h3 class="text-4xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      时间分布分析
    </h3>

    <div class="text-lg text-center text-gray-600 dark:text-gray-300 mb-8 space-y-2">
      <div v-if="viewingData?.insights?.weekly_pattern" v-html="formatInsightText(viewingData.insights.weekly_pattern)"></div>
      <div v-if="viewingData?.insights?.seasonal_pattern" v-html="formatInsightText(viewingData.insights.seasonal_pattern)"></div>
    </div>

    <!-- 图表容器 -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 周度分布图表 -->
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
        <h4 class="text-xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-4">周度分布</h4>
        <div class="h-[220px]">
          <v-chart ref="weeklyChartRef" class="h-full w-full" :option="weeklyOption" autoresize />
        </div>
      </div>

      <!-- 季节分布图表 -->
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
        <h4 class="text-xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-4">季节分布</h4>
        <div class="h-[220px]">
          <v-chart ref="seasonalChartRef" class="h-full w-full" :option="seasonalOption" autoresize />
        </div>
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

const weeklyChartRef = ref(null)
const seasonalChartRef = ref(null)
const { isDarkMode } = useDarkMode()

// 周度分布配置
const weeklyOption = computed(() => {
  if (!props.viewingData?.weekly_stats) return {}
  
  const weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  const data = weekdays.map(day => props.viewingData.weekly_stats[day] || 0)
  
  return {
    tooltip: {
      trigger: 'axis',
      backgroundColor: (isDarkMode && isDarkMode.value) ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)',
      borderColor: '#fb7299',
      textStyle: { color: (isDarkMode && isDarkMode.value) ? '#ffffff' : '#111111' }
    },
    grid: {
      top: '15%',
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: weekdays,
      axisLine: { lineStyle: { color: (isDarkMode && isDarkMode.value) ? '#888888' : '#666' } },
      axisLabel: { color: (isDarkMode && isDarkMode.value) ? '#bbbbbb' : '#999' }
    },
    yAxis: {
      type: 'value',
      name: '观看次数',
      axisLine: { lineStyle: { color: (isDarkMode && isDarkMode.value) ? '#888888' : '#666' } },
      axisLabel: { color: (isDarkMode && isDarkMode.value) ? '#bbbbbb' : '#999' },
      splitLine: { lineStyle: { color: (isDarkMode && isDarkMode.value) ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.1)' } }
    },
    series: [{
      data: data,
      type: 'bar',
      barWidth: '60%',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
          { offset: 0, color: 'rgba(251, 114, 153, 0.9)' },
          { offset: 1, color: 'rgba(252, 155, 122, 0.9)' }
        ]),
        borderRadius: [8, 8, 0, 0]
      },
      label: {
        show: true,
        position: 'top',
        color: (isDarkMode && isDarkMode.value) ? '#cccccc' : '#666',
        formatter: '{c}次'
      }
    }]
  }
})

// 季节分布配置
const seasonalOption = computed(() => {
  if (!props.viewingData?.seasonal_patterns) return {}
  
  const data = Object.entries(props.viewingData.seasonal_patterns)
    .map(([season, stats]) => ({
      name: season,
      value: stats.view_count,
      avg_duration: Math.round(stats.avg_duration)
    }))
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: (isDarkMode && isDarkMode.value) ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)',
      borderColor: '#fb7299',
      textStyle: { color: (isDarkMode && isDarkMode.value) ? '#ffffff' : '#111111' },
      formatter: (params) => {
        const data = params[0]
        return `${data.name}<br/>
                观看次数：${data.value}<br/>
                平均时长：${data.data.avg_duration}秒`
      }
    },
    grid: {
      top: '15%',
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLine: { lineStyle: { color: (isDarkMode && isDarkMode.value) ? '#888888' : '#666' } },
      axisLabel: { color: (isDarkMode && isDarkMode.value) ? '#bbbbbb' : '#999' }
    },
    yAxis: {
      type: 'value',
      name: '观看次数',
      axisLine: { lineStyle: { color: (isDarkMode && isDarkMode.value) ? '#888888' : '#666' } },
      axisLabel: { color: (isDarkMode && isDarkMode.value) ? '#bbbbbb' : '#999' },
      splitLine: { lineStyle: { color: (isDarkMode && isDarkMode.value) ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.1)' } }
    },
    series: [{
      data: data.map((item, index) => ({
        ...item,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
            { offset: 0, color: `rgba(251, 114, 153, ${Math.max(0.4, 0.9 - index * 0.05)})` },
            { offset: 1, color: `rgba(252, 155, 122, ${Math.max(0.4, 0.9 - index * 0.05)})` }
          ])
        }
      })),
      type: 'bar',
      barWidth: '60%',
      label: {
        show: true,
        position: 'top',
        color: (isDarkMode && isDarkMode.value) ? '#cccccc' : '#666',
        formatter: '{c}次'
      }
    }]
  }
})

onMounted(() => {
  if (weeklyChartRef.value && seasonalChartRef.value) {
    gsap.from([
      weeklyChartRef.value.$el,
      seasonalChartRef.value.$el
    ], {
      opacity: 0,
      y: 20,
      duration: 0.5,
      stagger: 0.1,
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