<!-- 时间分析页组件 -->
<template>
  <div class="space-y-4 h-screen overflow-hidden">
    <h3 class="text-2xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      观看时间分析
    </h3>

    <!-- 时间洞察卡片 - 压缩高度 -->
    <div class="text-center text-sm max-w-4xl mx-auto">
      <div v-if="viewingData?.insights?.daily_record" class="text-gray-600 dark:text-gray-300" v-html="formatInsightText(viewingData.insights.daily_record)">
      </div>
    </div>

    <!-- 时间统计卡片矩阵 - 压缩高度 -->
    <div class="grid grid-cols-4 gap-3">
      <div class="bg-gradient-to-br from-[#fb7299]/10 to-[#fc9b7a]/10 backdrop-blur-sm rounded-lg p-3 border border-gray-300/30 dark:border-gray-500/30">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-600 dark:text-gray-400">单日最长</p>
            <p class="text-lg font-bold text-[#fb7299]">{{ formatDurationShort(viewingData?.time_investment?.max_duration_day?.total_duration || 0) }} <span class="text-xs text-gray-500 font-normal">{{ formatDate(viewingData?.time_investment?.max_duration_day?.date || '') }}</span></p>
          </div>
          <div class="w-8 h-8 bg-[#fb7299]/20 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-[#fb7299]" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-[#fc9b7a]/10 to-[#fb7299]/10 backdrop-blur-sm rounded-lg p-3 border border-gray-300/30 dark:border-gray-500/30">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-600 dark:text-gray-400">日均时长</p>
            <p class="text-lg font-bold text-[#fc9b7a]">{{ formatDurationShort(viewingData?.time_investment?.avg_daily_duration || 0) }}</p>
          </div>
          <div class="w-8 h-8 bg-[#fc9b7a]/20 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-[#fc9b7a]" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-[#fb7299]/10 to-[#fc9b7a]/10 backdrop-blur-sm rounded-lg p-3 border border-gray-300/30 dark:border-gray-500/30">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-600 dark:text-gray-400">最活跃时段</p>
            <p class="text-lg font-bold text-[#fb7299]">{{ getPeakTimeSlot() }}</p>
          </div>
          <div class="w-8 h-8 bg-[#fb7299]/20 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-[#fb7299]" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-[#fc9b7a]/10 to-[#fb7299]/10 backdrop-blur-sm rounded-lg p-3 border border-gray-300/30 dark:border-gray-500/30">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-600 dark:text-gray-400">深夜观看</p>
            <p class="text-lg font-bold text-[#fc9b7a]">{{ getNightWatchCount() }}次</p>
          </div>
          <div class="w-8 h-8 bg-[#fc9b7a]/20 rounded-full flex items-center justify-center">
            <svg class="w-4 h-4 text-[#fc9b7a]" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要图表区域 - 单个柱状图 -->
    <div class="flex-1">
      <!-- 24小时观看分布柱状图 -->
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
        <h4 class="text-xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-4 text-center">24小时观看分布</h4>
        <div ref="barChartRef" class="h-[280px]"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import * as echarts from 'echarts'
import gsap from 'gsap'

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  },
  selectedYear: {
    type: Number,
    default: () => new Date().getFullYear()
  }
})

// 图表引用
const barChartRef = ref(null)

// 图表实例
let barChart = null

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}

const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}小时${minutes}分钟`
}

// 短格式时长显示
const formatDurationShort = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  if (hours > 0) {
    return `${hours}h${minutes}m`
  }
  return `${minutes}m`
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

// 获取最活跃时段
const getPeakTimeSlot = () => {
  if (!props.viewingData?.daily_time_slots) return '未知'
  const timeData = props.viewingData.daily_time_slots
  const maxHour = Object.keys(timeData).reduce((a, b) => timeData[a] > timeData[b] ? a : b)
  const hour = parseInt(maxHour.replace('时', ''))

  if (hour >= 6 && hour < 12) return '上午'
  if (hour >= 12 && hour < 18) return '下午'
  if (hour >= 18 && hour < 24) return '晚上'
  return '深夜'
}

// 获取深夜观看次数
const getNightWatchCount = () => {
  if (!props.viewingData?.daily_time_slots) return 0
  const timeData = props.viewingData.daily_time_slots
  let nightCount = 0

  Object.keys(timeData).forEach(hour => {
    const h = parseInt(hour.replace('时', ''))
    if (h >= 0 && h < 6) {
      nightCount += timeData[hour]
    }
  })

  return nightCount
}

// 获取时段对应的颜色
const getTimeSlotColor = (hour) => {
  const h = parseInt(hour.replace('时', ''))
  if (h >= 6 && h < 12) return '#7afc8c' // 上午-绿色
  if (h >= 12 && h < 18) return '#fc9b7a' // 下午-橙色
  if (h >= 18 && h < 24) return '#fb7299' // 晚上-粉色
  return '#7a9efc' // 深夜-蓝色
}

// 初始化24小时柱状图
const initBarChart = () => {
  if (!barChartRef.value || !props.viewingData?.daily_time_slots) return

  barChart = echarts.init(barChartRef.value)
  const timeData = props.viewingData.daily_time_slots

  // 准备24小时数据
  const hours = []
  const counts = []

  for (let i = 0; i < 24; i++) {
    const hour = `${i}时`
    hours.push(`${i}:00`)
    counts.push(timeData[hour] || 0)
  }

  const barOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        const hour = parseInt(params[0].name.split(':')[0])
        let period = '深夜'
        if (hour >= 6 && hour < 12) period = '上午'
        else if (hour >= 12 && hour < 18) period = '下午'
        else if (hour >= 18 && hour < 24) period = '晚上'

        return `${params[0].name} (${period})<br/>观看次数: ${params[0].value}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: hours,
      axisLabel: {
        color: '#666',
        fontSize: 12,
        interval: 2 // 每隔2小时显示一个标签
      },
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#666',
        fontSize: 12
      },
      axisLine: {
        lineStyle: {
          color: '#ddd'
        }
      },
      splitLine: {
        lineStyle: {
          color: '#f0f0f0'
        }
      }
    },
    series: [{
      name: '观看次数',
      type: 'bar',
      data: counts.map((count, index) => ({
        value: count,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: getTimeSlotColor(`${index}时`) },
            { offset: 1, color: getTimeSlotColor(`${index}时`) + '80' }
          ])
        }
      })),
      barWidth: '60%',
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowOffsetY: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }

  barChart.setOption(barOption)
}



onMounted(() => {
  initBarChart()

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    barChart?.resize()
  })
})

// 监听数据变化
watch(() => props.viewingData, () => {
  if (props.viewingData) {
    initBarChart()
  }
}, { deep: true })
</script>

<style>
/* 流光动画效果 */
@keyframes flow-light {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.animate-flow-light {
  position: relative;
}

.animate-flow-light::before,
.animate-flow-light-delay-1::before,
.animate-flow-light-delay-2::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 200%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.1),
    transparent
  );
  animation: flow-light 5s infinite linear;
}

.animate-flow-light-delay-1::before {
  animation-delay: 1s;
}

.animate-flow-light-delay-2::before {
  animation-delay: 2s;
}
</style>
