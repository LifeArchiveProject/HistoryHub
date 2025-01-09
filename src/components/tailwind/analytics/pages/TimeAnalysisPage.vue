<!-- 时间分析页组件 -->
<template>
  <div class="space-y-4">
    <h3 class="text-2xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      观看时间分析
    </h3>

    <!-- 时间模式洞察 -->
    <div class="text-base text-center text-gray-600 dark:text-gray-300 mb-6 space-y-2">
      <div v-if="viewingData?.insights?.time_pattern"
        v-html="formatInsightText(viewingData.insights.time_pattern)"
      ></div>
      <div v-if="viewingData?.insights?.peak_day">
        {{ viewingData.insights.peak_day }}
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 观看时间分布图表 -->
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 flex flex-col border border-gray-300/50 dark:border-gray-500/50">
        <div class="flex items-start justify-between mb-4">
          <h4 class="text-base font-medium text-gray-800 dark:text-white">每日观看时段分布</h4>
          <!-- 单日最高记录 -->
          <div class="text-right bg-white/30 dark:bg-white/10 rounded-lg p-2.5 border border-gray-300/50 dark:border-gray-500/50">
            <div class="text-sm text-gray-600 dark:text-gray-400">单日最高</div>
            <div class="text-xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent record-number">
              {{ viewingData.max_daily_record.view_count }}
            </div>
            <div class="text-xs text-gray-500">
              {{ formatDate(viewingData.max_daily_record.date) }}
            </div>
          </div>
        </div>
        <div ref="timeDistributionChartRef" class="w-full flex-1 min-h-[10rem]"></div>
        <!-- 添加统计信息 -->
        <div class="grid grid-cols-2 gap-4 mt-4">
          <div class="bg-white/30 dark:bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-gray-300/50 dark:border-gray-500/50">
            <div class="text-xs text-gray-600 dark:text-gray-400">单日最长观看</div>
            <div class="text-base font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mt-1">
              {{ formatDuration(viewingData.time_investment.max_duration_day.total_duration) }}
            </div>
            <div class="flex justify-between items-center mt-1">
              <span class="text-xs text-gray-500 dark:text-gray-400">{{ formatDate(viewingData.time_investment.max_duration_day.date) }}</span>
              <span class="text-xs text-gray-600 dark:text-gray-300">{{ viewingData.time_investment.max_duration_day.video_count }}个视频</span>
            </div>
          </div>
          <div class="bg-white/30 dark:bg-white/10 backdrop-blur-sm rounded-lg p-3 border border-gray-300/50 dark:border-gray-500/50">
            <div class="text-xs text-gray-600 dark:text-gray-400">日均观看时长</div>
            <div class="text-base font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mt-1">
              {{ formatDuration(viewingData.time_investment.avg_daily_duration) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 观看时长投资统计 -->
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 flex flex-col border border-gray-300/50 dark:border-gray-500/50">
        <div class="text-base font-medium text-gray-800 dark:text-white mb-4">观看高峰时段</div>
        <div class="flex-1">
          <!-- 第一个时段占据整行 -->
          <div v-if="viewingData.peak_hours[0]"
            class="relative bg-gradient-to-r from-[#fb7299]/5 to-[#fc9b7a]/5 dark:from-[#fb7299]/10 dark:to-[#fc9b7a]/10 backdrop-blur-sm rounded-lg p-5 mb-4 border border-gray-300/50 dark:border-gray-500/50 overflow-hidden animate-flow-light"
          >
            <div class="flex items-center justify-between relative z-10">
              <span class="text-lg font-medium text-[#fb7299]">TOP 1</span>
              <div class="text-right">
                <div class="text-gray-800 dark:text-white text-xl mb-1">{{ viewingData.peak_hours[0].hour }}</div>
                <div class="text-gray-600 dark:text-gray-400 text-sm">{{ viewingData.peak_hours[0].view_count }}次观看</div>
              </div>
            </div>
          </div>
          <!-- 其余时段以2x2网格展示 -->
          <div class="grid grid-cols-2 gap-4">
            <div v-for="(peak, index) in viewingData.peak_hours.slice(1)" :key="index"
              :class="[
                'relative backdrop-blur-sm rounded-lg p-4 border border-gray-300/50 dark:border-gray-500/50 overflow-hidden',
                index === 0 ? 'bg-gradient-to-r from-[#fc9b7a]/5 to-[#fcd07a]/5 dark:from-[#fc9b7a]/10 dark:to-[#fcd07a]/10 animate-flow-light-delay-1' :
                index === 1 ? 'bg-gradient-to-r from-[#fcd07a]/5 to-[#fce07a]/5 dark:from-[#fcd07a]/10 dark:to-[#fce07a]/10 animate-flow-light-delay-2' :
                'bg-white/30 dark:bg-white/10'
              ]"
            >
              <div class="flex items-center justify-between mb-2 relative z-10">
                <span class="text-base font-medium" :class="[
                  index === 0 ? 'text-[#fc9b7a]' :
                  index === 1 ? 'text-[#fcd07a]' :
                  'text-gray-800 dark:text-white'
                ]">TOP {{ index + 2 }}</span>
                <span class="text-gray-800 dark:text-white text-base">{{ peak.hour }}</span>
              </div>
              <div class="text-xs text-gray-600 dark:text-gray-400 text-right relative z-10">{{ peak.view_count }}次观看</div>
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
      top: '10%',
      left: '3%',
      right: '4%',
      bottom: '3%',
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
        rotate: 45
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
        color: 'rgba(107, 114, 128, 0.8)'
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
        barWidth: '60%',
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
    rgba(251, 114, 153, 0.1),
    rgba(252, 155, 122, 0.1),
    transparent
  );
  animation: flow-light 4s linear infinite;
}

.animate-flow-light-delay-1::before {
  animation: flow-light 4s linear infinite;
  animation-delay: -1s;
}

.animate-flow-light-delay-2::before {
  animation: flow-light 4s linear infinite;
  animation-delay: -2s;
}

/* 其他样式保持不变 */
.dark .echarts {
  filter: brightness(0.9);
}
</style>
