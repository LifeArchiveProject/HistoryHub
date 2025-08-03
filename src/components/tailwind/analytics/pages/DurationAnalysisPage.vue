<!-- 视频时长分析页组件 -->
<template>
  <div class="space-y-6">
    <h3 class="text-4xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      视频时长分析
    </h3>

    <div v-if="viewingData?.insights?.duration_preference"
      class="text-lg text-center text-gray-600 dark:text-gray-300 mb-8"
      v-html="formatInsightText(viewingData.insights.duration_preference)"
    >
    </div>

    <!-- 时长分布图表 -->
    <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
      <h4 class="text-xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-4">时长分布</h4>
      <div class="h-[300px]">
        <v-chart ref="chartRef" class="h-full w-full" :option="durationDistributionOption" autoresize />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import gsap from 'gsap'
import VChart from 'vue-echarts'
import * as echarts from 'echarts/core'

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  }
})

const chartRef = ref(null)

const durationDistributionOption = computed(() => {
  if (!props.viewingData?.duration_correlation) return {}

  const periods = ['凌晨', '上午', '下午', '晚上']
  const types = ['短视频', '中等视频', '长视频']
  const data = periods.map(period => {
    const periodData = props.viewingData.duration_correlation[period]
    return types.map(type => ({
      period,
      type,
      value: periodData[type].video_count,
      avg_duration: Math.round(periodData[type].avg_duration / 60)
    }))
  }).flat()

  const typeColors = {
    '短视频': {
      from: 'rgba(251, 114, 153, 0.9)',
      to: 'rgba(252, 155, 122, 0.9)'
    },
    '中等视频': {
      from: 'rgba(64, 169, 255, 0.9)',
      to: 'rgba(128, 208, 255, 0.9)'
    },
    '长视频': {
      from: 'rgba(82, 196, 26, 0.9)',
      to: 'rgba(144, 217, 79, 0.9)'
    }
  }

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(28, 28, 28, 0.9)',
      borderColor: '#fb7299',
      textStyle: { color: '#fff' },
      formatter: (params) => {
        const period = params[0].axisValue
        let result = `${period}<br/>`
        params.forEach(param => {
          const data = param.data
          result += `${param.seriesName}：${data.value}个 (平均${data.avg_duration}分钟)<br/>`
        })
        return result
      }
    },
    legend: {
      data: types,
      top: 0,
      textStyle: { color: '#666' },
      itemStyle: {
        borderWidth: 0
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
      data: periods,
      axisLine: { lineStyle: { color: '#666' } },
      axisLabel: { color: '#999' }
    },
    yAxis: {
      type: 'value',
      name: '视频数量',
      axisLine: { lineStyle: { color: '#666' } },
      axisLabel: { color: '#999' },
      splitLine: { lineStyle: { color: 'rgba(0, 0, 0, 0.1)' } }
    },
    series: types.map(type => ({
      name: type,
      type: 'bar',
      stack: 'total',
      emphasis: {
        focus: 'series'
      },
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 1, 0, 0, [
          { offset: 0, color: typeColors[type].from },
          { offset: 1, color: typeColors[type].to }
        ])
      },
      data: periods.map(period => {
        return data.find(d => d.period === period && d.type === type)
      })
    }))
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
