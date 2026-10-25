<!-- 数据概览页组件 -->
<template>
  <div class="space-y-12">
    <h3 class="text-3xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      年度观看数据
    </h3>

    <div class="text-base text-center text-gray-600 dark:text-gray-300 space-y-3">
      <!-- 总体活动总结（放在最前面） -->
      <div v-if="viewingData?.insights?.overall_activity"
        v-html="formatInsightText(viewingData.insights.overall_activity)"
      >
      </div>

      <!-- 按指定顺序合并所有总结，用逗号分隔 -->
      <div>
        <span v-if="viewingBehaviorData?.report?.total_summary" v-html="formatInsightText(viewingBehaviorData.report.total_summary)"></span>
        <span v-if="viewingBehaviorData?.report?.total_summary && viewingBehaviorData?.report?.category_summary">, </span>
        <span v-if="viewingBehaviorData?.report?.category_summary" v-html="formatInsightText(viewingBehaviorData.report.category_summary)"></span>
        <span v-if="(viewingBehaviorData?.report?.total_summary || viewingBehaviorData?.report?.category_summary) && viewingBehaviorData?.report?.device_summary">, </span>
        <span v-if="viewingBehaviorData?.report?.device_summary" v-html="formatInsightText(viewingBehaviorData.report.device_summary)"></span>
        <span v-if="(viewingBehaviorData?.report?.total_summary || viewingBehaviorData?.report?.category_summary || viewingBehaviorData?.report?.device_summary) && viewingBehaviorData?.report?.up_summary">, </span>
        <span v-if="viewingBehaviorData?.report?.up_summary" v-html="formatInsightText(viewingBehaviorData.report.up_summary)"></span>
        <span v-if="(viewingBehaviorData?.report?.total_summary || viewingBehaviorData?.report?.category_summary || viewingBehaviorData?.report?.device_summary || viewingBehaviorData?.report?.up_summary) && viewingBehaviorData?.report?.time_slot_summary">, </span>
        <span v-if="viewingBehaviorData?.report?.time_slot_summary" v-html="formatInsightText(viewingBehaviorData.report.time_slot_summary)"></span>
        <span v-if="(viewingBehaviorData?.report?.total_summary || viewingBehaviorData?.report?.category_summary || viewingBehaviorData?.report?.device_summary || viewingBehaviorData?.report?.up_summary || viewingBehaviorData?.report?.time_slot_summary) && viewingBehaviorData?.report?.late_night_summary">, </span>
        <span v-if="viewingBehaviorData?.report?.late_night_summary" v-html="formatInsightText(viewingBehaviorData.report.late_night_summary)"></span>
      </div>
    </div>

    <!-- 年度观看热力图 -->
    <div class="space-y-8">
     <div class="flex justify-center items-center text-sm text-gray-500 dark:text-gray-400 space-x-6">
       <div class="flex items-center">
         <span class="inline-block w-3 h-3 rounded-sm bg-[#FFECF1] dark:bg-[#4B1F2C] mr-1"></span>
         <span>1-10</span>
       </div>
       <div class="flex items-center">
         <span class="inline-block w-3 h-3 rounded-sm bg-[#FFB3CA] dark:bg-[#7A2D47] mr-1"></span>
         <span>11-50</span>
       </div>
       <div class="flex items-center">
         <span class="inline-block w-3 h-3 rounded-sm bg-[#FF8CB0] dark:bg-[#B3476A] mr-1"></span>
         <span>51-100</span>
       </div>
       <div class="flex items-center">
         <span class="inline-block w-3 h-3 rounded-sm bg-[#FF6699] dark:bg-[#E35C8B] mr-1"></span>
         <span>101-200</span>
       </div>
       <div class="flex items-center">
         <span class="inline-block w-3 h-3 rounded-sm bg-[#E84B85] dark:bg-[#FF7FA8] mr-1"></span>
         <span>201+</span>
       </div>
     </div>
      <div ref="heatmapChartRef" class="w-full h-[320px]"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import { getYearlyAnalysis, getViewingBehavior } from '@/api/api.js'
import { useDarkMode } from '@/store/darkMode.js'

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  }
})

const heatmapChartRef = ref(null)
let heatmapChart = null
const yearlyData = ref(null)
const viewingBehaviorData = ref(null)
const { isDarkMode } = useDarkMode()

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}

// 获取日期范围内的所有日期
const getDateRange = (year) => {
  const start = new Date(Date.UTC(year, 0, 1))
  const end = new Date(Date.UTC(year, 11, 31))
  const dates = []
  let current = start

  while (current <= end) {
    const date = current.toISOString().split('T')[0]
    dates.push(date)
    current = new Date(Date.UTC(current.getUTCFullYear(), current.getUTCMonth(), current.getUTCDate() + 1))
  }

  return dates
}

// 获取年度分析数据
const fetchYearlyData = async (year) => {
  if (!year) return

  try {
    const response = await getYearlyAnalysis(year)
    if (response.data.status === 'success') {
      yearlyData.value = response.data
      initHeatmapChart()
    } else {
      console.error('获取年度数据失败:', response.data.message)
    }
  } catch (error) {
    console.error('获取年度数据出错:', error)
  }
}

// 获取观看行为数据
const fetchViewingBehavior = async (year) => {
  if (!year) return

  try {
    const response = await getViewingBehavior(year, true)
    if (response.data && response.data.status === 'success') {
      viewingBehaviorData.value = response.data.data
    }
  } catch (error) {
    console.error('获取观看行为数据失败:', error)
  }
}

const initHeatmapChart = () => {
  if (!heatmapChartRef.value || !yearlyData.value?.data?.daily_count) return

  const year = props.viewingData?.year
  if (!year) return

  const dailyData = yearlyData.value.data.daily_count
  const allDates = getDateRange(year)

  // 将数据转换为热力图所需的格式
  const data = allDates.map(date => {
    const count = dailyData[date] || 0
    return [date, count]
  })

  // 如果已经存在图表实例，先销毁它
  if (heatmapChart) {
    heatmapChart.dispose()
  }

  // 深色模式颜色方案
  const isDark = !!(isDarkMode && isDarkMode.value)
  const calendarItemColor = isDark ? 'rgba(255, 255, 255, 0.06)' : 'rgba(255, 255, 255, 0.5)'
  const calendarBorderColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(238, 238, 238, 0.8)'
  const axisLabelColor = isDark ? '#bbbbbb' : '#666666'
  const tooltipBg = isDark ? 'rgba(28, 28, 28, 0.9)' : 'rgba(255, 255, 255, 0.95)'
  const tooltipText = isDark ? '#ffffff' : '#111111'

  heatmapChart = echarts.init(heatmapChartRef.value)
  const option = {
    animation: true,
    tooltip: {
      show: true,
      trigger: 'item',
      backgroundColor: tooltipBg,
      borderColor: '#fb7299',
      textStyle: {
        color: tooltipText,
        fontSize: 14
      },
      formatter: function(params) {
        const date = params.value[0]
        const count = params.value[1]
        const secondsMap = (yearlyData.value && yearlyData.value.data && yearlyData.value.data.daily_watch_seconds) || {}
        const seconds = secondsMap[date] || 0
        const h = Math.floor(seconds / 3600)
        const m = Math.floor((seconds % 3600) / 60)
        const s = seconds % 60
        let timeStr
        if (h > 0) {
          timeStr = `${h}小时${String(m).padStart(2, '0')}分${String(s).padStart(2, '0')}秒`
        } else if (m > 0) {
          timeStr = `${m}分${String(s).padStart(2, '0')}秒`
        } else {
          timeStr = `${s}秒`
        }
        return `${date} : ${count}个视频 · 观看时长 ${timeStr}`
      }
    },
    visualMap: {
      show: false,
      type: 'piecewise',
      pieces: isDark ? [
        { min: 1, max: 10, color: '#4B1F2C' },
        { min: 11, max: 50, color: '#7A2D47' },
        { min: 51, max: 100, color: '#B3476A' },
        { min: 101, max: 200, color: '#E35C8B' },
        { min: 201, max: 9999, color: '#FF7FA8' }
      ] : [
        { min: 1, max: 10, color: '#FFECF1' },
        { min: 11, max: 50, color: '#FFB3CA' },
        { min: 51, max: 100, color: '#FF8CB0' },
        { min: 101, max: 200, color: '#FF6699' },
        { min: 201, max: 9999, color: '#E84B85' }
      ]
    },
    calendar: {
      top: 30,
      left: 60,
      right: 60,
      cellSize: [16, 16],
      range: [`${year}-01-01`, `${year}-12-31`],
      itemStyle: {
        color: calendarItemColor,
        borderColor: calendarBorderColor,
        borderWidth: 1
      },
      yearLabel: { show: false },
      dayLabel: {
        firstDay: 0,
        nameMap: ['日', '一', '二', '三', '四', '五', '六'],
        color: axisLabelColor,
        fontSize: 12,
        margin: 12
      },
      monthLabel: {
        nameMap: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
        color: axisLabelColor,
        fontSize: 12,
        align: 'center',
        margin: 15
      },
      splitLine: {
        show: false
      }
    },
    series: [{
      type: 'heatmap',
      coordinateSystem: 'calendar',
      data: data,
      label: {
        show: false
      },
      emphasis: {
        itemStyle: {
          borderColor: '#fb7299',
          borderWidth: 2
        }
      }
    }]
  }

  heatmapChart.setOption(option)
}

onMounted(() => {
  if (props.viewingData?.year) {
    fetchYearlyData(props.viewingData.year)
    fetchViewingBehavior(props.viewingData.year)
  }

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    heatmapChart?.resize()
  })
})

// 监听数据变化
watch(() => yearlyData.value, () => {
  if (props.viewingData?.year) {
    initHeatmapChart()
  }
}, { deep: true })

// 监听深色模式变化，重绘图表
watch(() => isDarkMode.value, () => {
  initHeatmapChart()
})

// 监听年份变化
watch(() => props.viewingData?.year, (newYear) => {
  if (newYear) {
    fetchYearlyData(newYear)
    fetchViewingBehavior(newYear)
  }
}, { immediate: true })
</script>

<style>
.dark .echarts {
  filter: brightness(0.9);
}
</style>
