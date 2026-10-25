<!-- UP主完成率分析页组件 -->
<template>
  <div class="absolute inset-0">
    <div class="h-full flex items-center justify-center">
      <div class="max-w-7xl w-full mx-auto px-2 py-4 overflow-y-auto">
        <div class="space-y-4">
          <h3 class="text-3xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
            UP主完成率分析
          </h3>

          <div class="text-sm text-center text-gray-800 dark:text-gray-200 mb-2 space-y-1 px-4">
            <div v-if="viewingData?.insights?.most_valuable_author" v-html="formatInsightText(viewingData.insights.most_valuable_author)">
            </div>
            <div v-if="viewingData?.insights?.highest_completion_author" v-html="formatInsightText(viewingData.insights.highest_completion_author)">
            </div>
            <div v-if="viewingData?.insights?.potential_discovery" v-html="formatInsightText(viewingData.insights.potential_discovery)">
            </div>
            <div v-if="viewingData?.insights?.viewing_behavior_summary" v-html="formatInsightText(viewingData.insights.viewing_behavior_summary)">
            </div>
          </div>

          <!-- 图表容器 -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
            <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-gray-300/50 dark:border-gray-500/50 h-[420px]">
              <h4 class="text-base font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-3">
                最喜欢的UP主
              </h4>
              <v-chart ref="favoriteChartRef" class="h-[360px] w-full" :option="favoriteOption" autoresize @click="handleFavoriteClick" />
            </div>

            <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-gray-300/50 dark:border-gray-500/50 h-[420px]">
              <h4 class="text-base font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-3">
                观看最多的UP主
              </h4>
              <v-chart ref="mostWatchedChartRef" class="h-[360px] w-full" :option="mostWatchedOption" autoresize @click="handleMostWatchedClick" />
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
import { BarChart, LineChart, RadarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent,
  RadarComponent
} from 'echarts/components'
import { use } from 'echarts/core'
import { useDarkMode } from '@/store/darkMode.js'

// 注册必要的组件
use([
  CanvasRenderer,
  BarChart,
  LineChart,
  RadarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  DataZoomComponent,
  RadarComponent
])

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  }
})

const favoriteChartRef = ref(null)
const mostWatchedChartRef = ref(null)
const { isDarkMode } = useDarkMode()

// 获取最喜欢的UP主数据（使用most_valuable_authors）
const sortedFavoriteAuthors = computed(() => {
  if (!props.viewingData?.completion_rates?.most_valuable_authors) return []
  
  return Object.entries(props.viewingData.completion_rates.most_valuable_authors)
    .sort((a, b) => b[1].comprehensive_score - a[1].comprehensive_score)
    .slice(0, 10) // 显示10个UP主
})

// 获取观看最多的UP主数据
const sortedMostWatchedAuthors = computed(() => {
  if (!props.viewingData?.completion_rates?.most_watched_authors) return []
  
  return Object.entries(props.viewingData.completion_rates.most_watched_authors)
    .sort((a, b) => b[1].video_count - a[1].video_count)
    .slice(0, 10)
})

// 最喜欢的UP主雷达图配置
const favoriteOption = computed(() => {
  const data = sortedFavoriteAuthors.value.map(([author, stats]) => ({
    name: author,
    value: [
      stats.comprehensive_score,
      stats.loyalty_score,
      stats.quality_score,
      stats.average_completion_rate,
      stats.fully_watched_rate,
      stats.video_count / 10 // 缩放视频数量以适应雷达图
    ],
    authorMid: stats.author_mid
  }))

  const isDark = !!(isDarkMode && isDarkMode.value)
  const legendTextColor = isDark ? '#bbbbbb' : '#666'
  const axisLabelColor = isDark ? '#bbbbbb' : '#999'
  const axisLineColor = isDark ? '#444' : '#ddd'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText },
      formatter: (params) => {
        const stats = sortedFavoriteAuthors.value.find(([author]) => author === params.name)?.[1]
        if (!stats) return ''
        return `${params.name}<br/>
                综合评分：${stats.comprehensive_score.toFixed(1)}<br/>
                喜爱度评分：${stats.loyalty_score.toFixed(1)}<br/>
                质量评分：${stats.quality_score.toFixed(1)}<br/>
                平均完成率：${stats.average_completion_rate.toFixed(1)}%<br/>
                完整观看率：${stats.fully_watched_rate.toFixed(1)}%<br/>
                视频数量：${stats.video_count}个`
      }
    },
    legend: {
      data: data.map(item => item.name),
      textStyle: { color: legendTextColor, fontSize: 10 },
      left: 'left',
      orient: 'vertical',
      top: 'middle',
      type: 'scroll',
      width: 70
    },
    radar: {
      center: ['65%', '50%'],
      radius: '65%',
      indicator: [
        { name: '综合评分', max: 100 },
        { name: '喜爱度', max: 100 },
        { name: '质量评分', max: 100 },
        { name: '完成率', max: 100 },
        { name: '完整观看率', max: 100 },
        { name: '视频数量', max: 20 }
      ],
      name: {
        textStyle: {
          color: axisLabelColor,
          fontSize: 12,
          fontWeight: 'bold'
        }
      },
      axisLabel: {
        color: axisLabelColor
      },
      axisLine: {
        lineStyle: { color: axisLineColor }
      },
      splitLine: {
        lineStyle: { color: axisLineColor }
      }
    },
    series: [{
      type: 'radar',
      data: data.map((item, index) => {
        const colors = [
          '#fb7299', // 粉色
          '#40a9ff', // 蓝色
          '#66d980', // 绿色
          '#fc9b7a', // 橙色
          '#9254de', // 紫色
          '#ffc53d', // 黄色
          '#ff6b6b', // 红色
          '#4ecdc4', // 青色
          '#45b7d1', // 天蓝色
          '#f39c12'  // 深橙色
        ]
        const color = colors[index % colors.length]
        return {
          ...item,
          itemStyle: {
            color: color
          },
          lineStyle: {
            color: color,
            width: 2
          },
          // 默认不显示背景区域
          emphasis: {
            itemStyle: {
              color: color
            },
            lineStyle: {
              color: color,
              width: 4
            },
            areaStyle: {
              color: color,
              opacity: 0.4
            }
          }
        }
      })
    }]
  }
})

// 观看最多的UP主散点图配置
const mostWatchedOption = computed(() => {
  const data = sortedMostWatchedAuthors.value.map(([author, stats]) => ([
    stats.video_count,
    stats.average_completion_rate,
    stats.fully_watched,
    author,
    stats.author_mid
  ]))

  const isDarkMW = !!(isDarkMode && isDarkMode.value)
  const axisLabelColor = isDarkMW ? '#bbbbbb' : '#999'
  const axisLineColor = isDarkMW ? '#888888' : '#666'
  const splitLineColor = isDarkMW ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.1)'
  const tooltipBg = isDarkMW ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDarkMW ? '#ffffff' : '#111111'
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: { color: tooltipText },
      formatter: (params) => {
        return `${params.data[3]}<br/>
                观看视频数：${params.data[0]}个<br/>
                平均完成率：${params.data[1].toFixed(1)}%<br/>
                完整观看数：${params.data[2]}个`
      }
    },
    grid: {
      top: '10%',
      left: '12%',
      right: '8%',
      bottom: '15%'
    },
    xAxis: {
      type: 'value',
      name: '观看视频数',
      nameLocation: 'middle',
      nameGap: 25,
      axisLine: { lineStyle: { color: axisLineColor } },
      axisLabel: { color: axisLabelColor },
      splitLine: { lineStyle: { color: splitLineColor } }
    },
    yAxis: {
      type: 'value',
      name: '平均完成率(%)',
      nameLocation: 'middle',
      nameGap: 35,
      axisLine: { lineStyle: { color: axisLineColor } },
      axisLabel: { color: axisLabelColor },
      splitLine: { lineStyle: { color: splitLineColor } }
    },
    series: [{
      type: 'scatter',
      symbolSize: (data) => Math.sqrt(data[2]) * 3, // 根据完整观看数调整点的大小
      data: data,
      itemStyle: {
        color: (params) => {
          const colors = ['#fb7299', '#40a9ff', '#66d980', '#fc9b7a', '#9254de', '#ffc53d']
          return colors[params.dataIndex % colors.length]
        },
        opacity: 0.8
      },
      emphasis: {
        focus: 'item',
        itemStyle: {
          opacity: 1,
          borderColor: '#333',
          borderWidth: 2
        }
      }
    }]
  }
})

// 点击事件处理函数
const handleFavoriteClick = (params) => {
  if (params.componentType === 'series') {
    const authorData = sortedFavoriteAuthors.value.find(([author]) => author === params.name)
    if (authorData?.[1]?.author_mid) {
      handleAuthorClick(authorData[1].author_mid)
    }
  }
}

const handleMostWatchedClick = (params) => {
  if (params.componentType === 'series') {
    const authorData = sortedMostWatchedAuthors.value.find(([author]) => author === params.data[3])
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
  const favoriteChart = favoriteChartRef.value
  const mostWatchedChart = mostWatchedChartRef.value

  // 雷达图点击事件（通过ECharts内置事件处理）
  if (favoriteChart) {
    favoriteChart.chart.on('click', (params) => {
      if (params.componentType === 'series') {
        const authorData = sortedFavoriteAuthors.value.find(([author]) => author === params.name)
        if (authorData?.[1]?.author_mid) {
          handleAuthorClick(authorData[1].author_mid)
        }
      }
    })
  }

  // 散点图点击事件（通过ECharts内置事件处理）
  if (mostWatchedChart) {
    mostWatchedChart.chart.on('click', (params) => {
      if (params.componentType === 'series') {
        const authorData = sortedMostWatchedAuthors.value.find(([author]) => author === params.data[3])
        if (authorData?.[1]?.author_mid) {
          handleAuthorClick(authorData[1].author_mid)
        }
      }
    })
  }
})

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}
</script>

<style scoped>
.echarts :deep(.yAxis) {
  cursor: pointer;
}
</style>