<!-- UP主完成率分析页组件 -->
<template>
  <div class="absolute inset-0">
    <div class="h-full flex items-center justify-center">
      <div class="max-w-7xl w-full mx-auto px-2 py-6 overflow-y-auto">
        <div class="space-y-6">
          <h3 class="text-3xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
            UP主完成率分析
          </h3>

          <div class="text-sm text-center text-gray-600 dark:text-gray-300 mb-2 space-y-2 px-4">
            <div v-if="viewingData?.insights?.most_watched_author">
              {{ viewingData.insights.most_watched_author }}
            </div>
            <div v-if="viewingData?.insights?.highest_completion_author">
              {{ viewingData.insights.highest_completion_author }}
            </div>
          </div>

          <!-- 图表容器 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
            <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-gray-300/50 dark:border-gray-500/50">
              <h4 class="text-lg font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-1">
                观看最多的UP主
              </h4>
              <v-chart ref="mostWatchedChartRef" class="h-[320px] w-full" :option="mostWatchedOption" autoresize @click="handleMostWatchedClick" />
            </div>

            <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-gray-300/50 dark:border-gray-500/50">
              <h4 class="text-lg font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-1">
                完成率最高的UP主
              </h4>
              <v-chart ref="highestCompletionChartRef" class="h-[320px] w-full" :option="highestCompletionOption" autoresize @click="handleHighestCompletionClick" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import VChart from 'vue-echarts'
import * as echarts from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent
} from 'echarts/components'
import { use } from 'echarts/core'

// 注册必要的组件
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent
])

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  }
})

const mostWatchedChartRef = ref(null)
const highestCompletionChartRef = ref(null)

// 获取观看最多的UP主数据
const sortedMostWatchedAuthors = computed(() => {
  if (!props.viewingData?.completion_rates?.most_watched_authors) return []
  
  return Object.entries(props.viewingData.completion_rates.most_watched_authors)
    .sort((a, b) => b[1].video_count - a[1].video_count)
    .slice(0, 10)
})

// 获取完成率最高的UP主数据
const sortedHighestCompletionAuthors = computed(() => {
  if (!props.viewingData?.completion_rates?.highest_completion_authors) return []
  
  return Object.entries(props.viewingData.completion_rates.highest_completion_authors)
    .sort((a, b) => b[1].average_completion_rate - a[1].average_completion_rate)
    .slice(0, 10)
})

// 观看最多的UP主图表配置
const mostWatchedOption = computed(() => {
  const data = sortedMostWatchedAuthors.value.map(([author, stats]) => ({
    author,
    videoCount: stats.video_count,
    completionRate: stats.average_completion_rate,
    fullyWatched: stats.fully_watched,
    authorMid: stats.author_mid
  }))

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const videoCount = params.find(p => p.seriesName === '观看视频数')
        const completionRate = params.find(p => p.seriesName === '平均完成率')
        const fullyWatched = params.find(p => p.seriesName === '完整观看数')
        return `${params[0].name}<br/>
                观看视频数：${videoCount.value}个<br/>
                完整观看数：${fullyWatched.value}个<br/>
                平均完成率：${completionRate.value}%`
      }
    },
    legend: {
      data: ['观看视频数', '完整观看数', '平均完成率'],
      textStyle: { color: '#666' },
      padding: [0, 0, 5, 0]
    },
    grid: {
      top: '40px',
      left: '3%',
      right: '8%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#666' } },
      axisLabel: { color: '#999' },
      splitLine: { lineStyle: { color: 'rgba(0, 0, 0, 0.1)' } }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.author),
      axisLine: { lineStyle: { color: '#666' } },
      axisLabel: {
        show: true,
        color: '#666',
        formatter: (value) => value
      },
      inverse: true,
      triggerEvent: true,
      emphasis: {
        focus: 'series',
        label: {
          show: true,
          color: '#fb7299',
          fontWeight: 'bold'
        }
      }
    },
    series: [
      {
        name: '观看视频数',
        type: 'bar',
        data: data.map((item, index) => ({
          value: item.videoCount,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
              { offset: 0, color: `rgba(251, 114, 153, ${Math.max(0.4, 0.9 - index * 0.05)})` },
              { offset: 1, color: `rgba(252, 155, 122, ${Math.max(0.4, 0.9 - index * 0.05)})` }
            ])
          }
        }))
      },
      {
        name: '完整观看数',
        type: 'bar',
        data: data.map((item, index) => ({
          value: item.fullyWatched,
          itemStyle: {
            color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
              { offset: 0, color: `rgba(64, 169, 255, ${Math.max(0.4, 0.9 - index * 0.05)})` },
              { offset: 1, color: `rgba(128, 208, 255, ${Math.max(0.4, 0.9 - index * 0.05)})` }
            ])
          }
        }))
      },
      {
        name: '平均完成率',
        type: 'line',
        yAxisIndex: 0,
        data: data.map(item => ({
          value: item.completionRate.toFixed(1),
          symbolSize: 8,
          itemStyle: { color: '#fc9b7a' }
        })),
        lineStyle: { width: 3 },
        symbol: 'circle'
      }
    ]
  }
})

// 完成率最高的UP主图表配置
const highestCompletionOption = computed(() => {
  const data = sortedHighestCompletionAuthors.value.map(([author, stats]) => ({
    author,
    videoCount: stats.video_count,
    completionRate: stats.average_completion_rate,
    fullyWatched: stats.fully_watched,
    fullyWatchedRate: stats.fully_watched_rate,
    authorMid: stats.author_mid
  }))

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      formatter: (params) => {
        const completionRate = params.find(p => p.seriesName === '平均完成率')
        const fullyWatchedRate = params.find(p => p.seriesName === '完整观看率')
        const videoCount = params.find(p => p.seriesName === '视频数量')
        return `${params[0].name}<br/>
                平均完成率：${completionRate.value}%<br/>
                完整观看率：${fullyWatchedRate.value}%<br/>
                视频数量：${videoCount.value}个`
      }
    },
    legend: {
      data: ['平均完成率', '完整观看率', '视频数量'],
      textStyle: { color: '#666' },
      padding: [0, 0, 5, 0]
    },
    grid: {
      top: '40px',
      left: '3%',
      right: '8%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      axisLine: { lineStyle: { color: '#666' } },
      axisLabel: {
        color: '#999',
        formatter: '{value}%'
      },
      splitLine: { lineStyle: { color: 'rgba(0, 0, 0, 0.1)' } }
    },
    yAxis: {
      type: 'category',
      data: data.map(item => item.author),
      axisLine: { lineStyle: { color: '#666' } },
      axisLabel: {
        show: true,
        color: '#666',
        formatter: (value) => value
      },
      inverse: true,
      triggerEvent: true,
      emphasis: {
        focus: 'series',
        label: {
          show: true,
          color: '#fb7299',
          fontWeight: 'bold'
        }
      }
    },
    series: [
      {
        name: '平均完成率',
        type: 'bar',
        data: data.map((item, index) => ({
          value: item.completionRate.toFixed(1),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
              { offset: 0, color: `rgba(251, 114, 153, ${Math.max(0.4, 0.9 - index * 0.05)})` },
              { offset: 1, color: `rgba(252, 155, 122, ${Math.max(0.4, 0.9 - index * 0.05)})` }
            ])
          }
        }))
      },
      {
        name: '完整观看率',
        type: 'bar',
        data: data.map((item, index) => ({
          value: item.fullyWatchedRate.toFixed(1),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
              { offset: 0, color: `rgba(64, 169, 255, ${Math.max(0.4, 0.9 - index * 0.05)})` },
              { offset: 1, color: `rgba(128, 208, 255, ${Math.max(0.4, 0.9 - index * 0.05)})` }
            ])
          }
        }))
      },
      {
        name: '视频数量',
        type: 'line',
        yAxisIndex: 0,
        data: data.map(item => ({
          value: item.videoCount,
          symbolSize: 8,
          itemStyle: { color: '#fc9b7a' }
        })),
        lineStyle: { width: 3 },
        symbol: 'circle'
      }
    ]
  }
})

// 点击事件处理函数
const handleMostWatchedClick = (params) => {
  if (params.componentType === 'yAxis') {
    const authorData = sortedMostWatchedAuthors.value.find(([author]) => author === params.value)
    if (authorData?.[1]?.author_mid) {
      handleAuthorClick(authorData[1].author_mid)
    }
  }
}

const handleHighestCompletionClick = (params) => {
  if (params.componentType === 'yAxis') {
    const authorData = sortedHighestCompletionAuthors.value.find(([author]) => author === params.value)
    if (authorData?.[1]?.author_mid) {
      handleAuthorClick(authorData[1].author_mid)
    }
  }
}

const handleAuthorClick = (mid) => {
  window.open(`https://space.bilibili.com/${mid}`, '_blank')
}

// 添加事件监听
onMounted(() => {
  const mostWatchedChart = mostWatchedChartRef.value
  const highestCompletionChart = highestCompletionChartRef.value

  if (mostWatchedChart) {
    mostWatchedChart.chart.getZr().on('mousemove', (params) => {
      const pointInPixel = [params.offsetX, params.offsetY]
      const pointInGrid = mostWatchedChart.chart.convertFromPixel({ yAxisIndex: 0 }, pointInPixel)
      
      if (pointInGrid) {
        const yIndex = Math.floor(pointInGrid[1])
        const authors = sortedMostWatchedAuthors.value
        if (yIndex >= 0 && yIndex < authors.length) {
          mostWatchedChart.chart.getZr().setCursorStyle('pointer')
        } else {
          mostWatchedChart.chart.getZr().setCursorStyle('default')
        }
      }
    })

    mostWatchedChart.chart.getZr().on('click', (params) => {
      const pointInPixel = [params.offsetX, params.offsetY]
      const pointInGrid = mostWatchedChart.chart.convertFromPixel({ yAxisIndex: 0 }, pointInPixel)
      
      if (pointInGrid) {
        const yIndex = Math.floor(pointInGrid[1])
        const authors = sortedMostWatchedAuthors.value
        if (yIndex >= 0 && yIndex < authors.length) {
          const authorData = authors[yIndex]
          if (authorData?.[1]?.author_mid) {
            handleAuthorClick(authorData[1].author_mid)
          }
        }
      }
    })
  }

  if (highestCompletionChart) {
    highestCompletionChart.chart.getZr().on('mousemove', (params) => {
      const pointInPixel = [params.offsetX, params.offsetY]
      const pointInGrid = highestCompletionChart.chart.convertFromPixel({ yAxisIndex: 0 }, pointInPixel)
      
      if (pointInGrid) {
        const yIndex = Math.floor(pointInGrid[1])
        const authors = sortedHighestCompletionAuthors.value
        if (yIndex >= 0 && yIndex < authors.length) {
          highestCompletionChart.chart.getZr().setCursorStyle('pointer')
        } else {
          highestCompletionChart.chart.getZr().setCursorStyle('default')
        }
      }
    })

    highestCompletionChart.chart.getZr().on('click', (params) => {
      const pointInPixel = [params.offsetX, params.offsetY]
      const pointInGrid = highestCompletionChart.chart.convertFromPixel({ yAxisIndex: 0 }, pointInPixel)
      
      if (pointInGrid) {
        const yIndex = Math.floor(pointInGrid[1])
        const authors = sortedHighestCompletionAuthors.value
        if (yIndex >= 0 && yIndex < authors.length) {
          const authorData = authors[yIndex]
          if (authorData?.[1]?.author_mid) {
            handleAuthorClick(authorData[1].author_mid)
          }
        }
      }
    })
  }
})
</script>

<style scoped>
.echarts {
  :deep(.yAxis) {
    cursor: pointer;
  }
}
</style> 