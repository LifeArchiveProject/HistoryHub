<!-- 视频整体完成率分析页组件 -->
<template>
  <div class="space-y-4">
    <h3 class="text-3xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      视频完成率分析
    </h3>

    <div v-if="viewingData?.insights?.overall_completion" 
      class="text-base text-center text-gray-600 dark:text-gray-300 mb-4"
    >
      <template v-for="(part, index) in formattedInsights" :key="index">
        <span v-if="part.type === 'text'" v-html="part.content"></span>
        <span v-else :class="[
          'font-bold',
          part.metric === 'average' ? 'text-[#fb7299]' : 
          part.metric === 'fully' ? 'text-[#fc9b7a]' : 
          'text-[#40a9ff]'
        ]">{{ part.content }}</span>
      </template>
    </div>

    <div class="grid grid-cols-7 gap-4">
      <!-- 完成率分布图表 -->
      <div class="col-span-3 bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-gray-300/50 dark:border-gray-500/50">
        <h4 class="text-lg font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-3">完成率分布</h4>
        <v-chart ref="completionDistributionRef" class="h-[280px] w-full" :option="completionDistributionOption" autoresize />
      </div>

      <!-- 时长分布完成率 -->
      <div class="col-span-4 bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-gray-300/50 dark:border-gray-500/50">
        <h4 class="text-lg font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-3">时长分布完成率</h4>
        <v-chart ref="durationCompletionRef" class="h-[280px] w-full" :option="durationCompletionOption" autoresize />
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

const completionDistributionRef = ref(null)
const durationCompletionRef = ref(null)

// 格式化总结文字，为数字添加颜色
const formattedInsights = computed(() => {
  if (!props.viewingData?.insights?.overall_completion) return []
  
  const text = props.viewingData.insights.overall_completion
  const parts = []
  
  // 使用正则表达式匹配数字
  const regex = /(\d+(?:\.\d+)?%)/g
  let lastIndex = 0
  let match
  let metricIndex = 0
  const metrics = ['average', 'fully', 'not_started']
  
  while ((match = regex.exec(text)) !== null) {
    // 添加数字前的文本
    if (match.index > lastIndex) {
      parts.push({
        type: 'text',
        content: text.substring(lastIndex, match.index)
      })
    }
    
    // 添加数字（带颜色）
    parts.push({
      type: 'number',
      content: match[0],
      metric: metrics[metricIndex]
    })
    
    lastIndex = match.index + match[0].length
    metricIndex++
  }
  
  // 添加剩余的文本
  if (lastIndex < text.length) {
    parts.push({
      type: 'text',
      content: text.substring(lastIndex)
    })
  }
  
  return parts
})

// 完成率分布图表配置
const completionDistributionOption = computed(() => {
  if (!props.viewingData?.completion_rates?.completion_distribution) return {}
  
  const data = Object.entries(props.viewingData.completion_rates.completion_distribution)
    .map(([range, count]) => ({
      name: range,
      value: count
    }))
  
  const { isDarkMode } = useDarkMode()
  const isDark = !!(isDarkMode && isDarkMode.value)
  const legendTextColor = isDark ? '#bbbbbb' : '#666'
  const labelTextColor = isDark ? '#e5e7eb' : '#333'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText },
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'middle',
      textStyle: { color: legendTextColor, fontSize: '12px' }
    },
    series: [{
      type: 'pie',
      radius: ['35%', '65%'],
      center: ['40%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 4
      },
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '14',
          fontWeight: 'bold',
          color: labelTextColor
        }
      },
      labelLine: {
        show: false
      },
      data: data.map((item, index) => ({
        ...item,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: `rgba(251, 114, 153, ${Math.max(0.4, 0.9 - index * 0.1)})` },
            { offset: 1, color: `rgba(252, 155, 122, ${Math.max(0.4, 0.9 - index * 0.1)})` }
          ])
        }
      }))
    }]
  }
})

// 时长分布完成率图表配置
const durationCompletionOption = computed(() => {
  if (!props.viewingData?.completion_rates?.duration_based_stats) return {}
  
  const data = Object.entries(props.viewingData.completion_rates.duration_based_stats)
    .map(([duration, stats]) => ({
      duration: duration.replace(/\([^)]*\)/, ''),
      completion: stats.average_completion_rate,
      count: stats.video_count,
      fully_watched_rate: stats.fully_watched_rate
    }))
    .sort((a, b) => {
      const order = ['短视频', '中等视频', '长视频']
      return order.indexOf(a.duration) - order.indexOf(b.duration)
    })
  
  const { isDarkMode } = useDarkMode()
  const isDark = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDark ? '#bbbbbb' : '#999'
  const axisLineColor = isDark ? '#888888' : '#666'
  const splitLineColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.1)'
  const legendTextColor = isDark ? '#bbbbbb' : '#666'
  const labelTextColor = isDark ? '#e5e7eb' : '#333'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText },
      formatter: (params) => {
        const completion = params.find(p => p.seriesName === '完成率')
        const count = params.find(p => p.seriesName === '视频数量')
        const fully = params.find(p => p.seriesName === '完整观看率')
        return `${params[0].name}<br/>
                完成率：${completion.value}%<br/>
                完整观看率：${fully.value}%<br/>
                视频数量：${count.value}个`
      }
    },
    legend: {
      data: ['完成率', '完整观看率', '视频数量'],
      textStyle: { color: legendTextColor, fontSize: '12px' },
      padding: [0, 0, 0, 0]
    },
    grid: {
      top: '40px',
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.duration),
      axisLine: { lineStyle: { color: axisLineColor } },
      axisLabel: { color: axisLabelColor, fontSize: '12px' }
    },
    yAxis: [{
      type: 'value',
      name: '百分比',
      min: 0,
      max: 100,
      axisLine: { lineStyle: { color: axisLineColor } },
      axisLabel: {
        color: axisLabelColor,
        formatter: '{value}%',
        fontSize: '12px'
      },
      splitLine: { lineStyle: { color: splitLineColor } }
    }, {
      type: 'value',
      name: '视频数量',
      axisLine: { lineStyle: { color: axisLineColor } },
      axisLabel: { color: axisLabelColor, fontSize: '12px' },
      splitLine: { show: false }
    }],
    series: [{
      name: '完成率',
      type: 'bar',
      barWidth: '20%',
      data: data.map((item, index) => ({
        value: item.completion,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
            { offset: 0, color: `rgba(251, 114, 153, ${Math.max(0.4, 0.9 - index * 0.2)})` },
            { offset: 1, color: `rgba(252, 155, 122, ${Math.max(0.4, 0.9 - index * 0.2)})` }
          ])
        }
      })),
      label: {
        show: true,
        position: 'top',
        formatter: '{c}%',
        fontSize: '12px',
        color: labelTextColor
      }
    }, {
      name: '完整观看率',
      type: 'bar',
      barWidth: '20%',
      data: data.map((item, index) => ({
        value: item.fully_watched_rate,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
            { offset: 0, color: `rgba(64, 169, 255, ${Math.max(0.4, 0.9 - index * 0.2)})` },
            { offset: 1, color: `rgba(128, 208, 255, ${Math.max(0.4, 0.9 - index * 0.2)})` }
          ])
        }
      })),
      label: {
        show: true,
        position: 'top',
        formatter: '{c}%',
        fontSize: '12px',
        color: labelTextColor,
        textBorderWidth: 0,
        textBorderColor: 'transparent',
        textShadowBlur: 0,
        textShadowColor: 'transparent'
      }
    }, {
      name: '视频数量',
      type: 'line',
      yAxisIndex: 1,
      smooth: true,
      symbolSize: 6,
      lineStyle: { width: 2 },
      itemStyle: { color: '#fc9b7a' },
      data: data.map(item => item.count)
    }]
  }
})

onMounted(() => {
  const charts = [
    completionDistributionRef.value,
    durationCompletionRef.value
  ]

  if (charts.every(chart => chart)) {
    gsap.from(charts.map(chart => chart.$el), {
      opacity: 0,
      y: 20,
      duration: 0.5,
      stagger: 0.1,
      ease: 'power2.out',
      delay: 0.2
    })
  }
})
</script> 