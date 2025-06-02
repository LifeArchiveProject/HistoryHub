<!-- 时间分析页组件 -->
<template>
  <div class="min-h-screen py-8 px-2">
    <div class="max-w-7xl mx-auto">
      <!-- 更大的标题 -->
      <h3 class="text-3xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-4">
        观看时间分析
      </h3>

      <!-- 移动到标题下方的总结文字 -->
      <div class="text-center mb-8 mt-4 space-y-2 max-w-5xl mx-auto">
        <!-- 单日观看记录洞察 -->
        <div v-if="viewingData?.insights?.daily_record" class="text-gray-600 dark:text-gray-300" v-html="formatInsightText(viewingData.insights.daily_record)">
        </div>

        <!-- 时段偏好洞察 -->
        <div v-if="viewingData?.insights?.time_preference" class="text-gray-600 dark:text-gray-300 mt-2" v-html="formatInsightText(viewingData.insights.time_preference)">
        </div>

        <!-- 如果没有新洞察，显示默认文本 -->
        <div v-else class="text-gray-600 dark:text-gray-300" v-html="formatInsightText('正在分析您的观看时间偏好...')">
        </div>
      </div>

      <!-- 合并的时间分布与时段活跃度卡片 -->
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
        <!-- 时段分布图表 -->
        <div ref="timeDistributionChartRef" class="w-full h-[180px]"></div>

        <!-- 统计信息 -->
        <div class="grid grid-cols-2 gap-6 mt-6">
          <div class="bg-white/30 dark:bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-gray-300/50 dark:border-gray-500/50">
            <div class="text-sm text-gray-600 dark:text-gray-400">单日最长观看</div>
            <div class="text-lg font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mt-2">
              {{ formatDuration(viewingData?.time_investment?.max_duration_day?.total_duration || 0) }}
            </div>
            <div class="flex justify-between items-center mt-2">
              <span class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(viewingData?.time_investment?.max_duration_day?.date || '') }}</span>
              <span class="text-sm text-gray-600 dark:text-gray-300" v-html="formatInsightText((viewingData?.time_investment?.max_duration_day?.video_count || 0) + '个视频')"></span>
            </div>
          </div>
          <div class="bg-white/30 dark:bg-white/10 backdrop-blur-sm rounded-xl p-4 border border-gray-300/50 dark:border-gray-500/50">
            <div class="text-sm text-gray-600 dark:text-gray-400">日均观看时长</div>
            <div class="text-lg font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mt-2">
              {{ formatDuration(viewingData?.time_investment?.avg_daily_duration || 0) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'

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

const timeDistributionChartRef = ref(null)
let timeDistributionChart = null

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}

const formatDuration = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  return `${hours}小时${minutes}分钟`
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

// 获取时段对应的颜色
const getTimeSlotColor = (slot) => {
  switch(slot) {
    case '上午': return '#7afc8c'; // 绿色
    case '下午': return '#fc9b7a'; // 橙色
    case '晚上': return '#fb7299'; // 粉色
    case '深夜': return '#7a9efc'; // 蓝色
    default: return '#fb7299';
  }
}

// 原始观看行为接口已禁用，数据通过props传入

const initTimeDistributionChart = () => {
  if (!timeDistributionChartRef.value || !props.viewingData?.daily_time_slots) return

  const timeData = props.viewingData.daily_time_slots
  const hours = Object.keys(timeData)
  const counts = Object.values(timeData)

  timeDistributionChart = echarts.init(timeDistributionChartRef.value)
  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      top: '8%',
      left: '1%',
      right: '1%',
      bottom: '5%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: hours,
      axisLine: {
        lineStyle: {
          color: 'rgba(156, 163, 175, 0.5)'
        }
      },
      axisLabel: {
        color: 'rgba(107, 114, 128, 0.8)',
        rotate: 45,
        fontSize: 10,
        interval: 1
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: 'rgba(156, 163, 175, 0.5)'
        }
      },
      axisLabel: {
        color: 'rgba(107, 114, 128, 0.8)',
        fontSize: 10
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(229, 231, 235, 0.2)'
        }
      }
    },
    series: [
      {
        name: '观看数量',
        type: 'bar',
        data: counts,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#fb7299' },
            { offset: 1, color: '#fc9b7a' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#fc9b7a' },
              { offset: 1, color: '#fb7299' }
            ])
          }
        },
        barWidth: '70%',
        animation: true
      }
    ]
  }

  timeDistributionChart.setOption(option)
}

onMounted(() => {
  initTimeDistributionChart()

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    timeDistributionChart?.resize()
  })
})

// 监听数据变化
watch(() => props.viewingData, () => {
  initTimeDistributionChart()
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
