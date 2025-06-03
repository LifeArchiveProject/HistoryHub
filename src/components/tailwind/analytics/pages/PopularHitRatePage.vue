<!-- 热门视频命中率分析页组件 -->
<template>
  <div class="space-y-4">
    <h3 class="text-xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      热门视频命中率分析
    </h3>

    <!-- 加载状态 -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#fb7299]"></div>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-lg">{{ error }}</div>
    </div>

    <!-- 主要内容 -->
    <div v-else-if="hitRateData" class="space-y-4">

      <!-- 洞察文本 -->
      <div class="text-center text-gray-600 dark:text-gray-300">
        <div class="text-sm leading-relaxed" v-html="formatInsightText(hitRateData.insights.join('，'))"></div>
      </div>

      <!-- 可视化图表 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <!-- 命中率统计卡片 -->
        <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-gray-300/50 dark:border-gray-500/50">
          <h4 class="text-base font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-2 text-center">
            观看时机分析
          </h4>
          <div ref="chartRef" class="h-[460px]"></div>
        </div>

        <!-- 热门视频列表 -->
        <div v-if="hitRateData.popular_videos && hitRateData.popular_videos.length > 0"
             class="lg:col-span-2 bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-gray-300/50 dark:border-gray-500/50">
          <h4 class="text-base font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-2">
            你观看过的热门视频 (前10个)
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2 h-[460px] overflow-y-auto">
            <div v-for="(video, index) in hitRateData.popular_videos" :key="index"
                 @click="openVideo(video.bvid)"
                 class="flex items-center p-2 bg-gray-50/50 dark:bg-gray-800/50 rounded-lg hover:bg-gray-100/50 dark:hover:bg-gray-700/50 cursor-pointer transition-colors">
              <div class="flex-1 min-w-0">
                <div class="font-medium text-gray-900 dark:text-gray-100 truncate text-xs">{{ video.title }}</div>
                <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  <span>{{ video.author }}</span>
                  <span class="ml-2">{{ formatDate(video.view_at) }}</span>
                </div>
              </div>
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
import { getPopularHitRate } from '../../../../api/api.js'

const props = defineProps({
  selectedYear: {
    type: Number,
    default: () => new Date().getFullYear()
  },
  hitRateData: {
    type: Object,
    default: null
  }
})

const loading = ref(true)
const error = ref(null)
const hitRateData = ref(null)
const chartRef = ref(null)
let chart = null

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299] font-semibold">$1</span>')
}

// 格式化日期
const formatDate = (timestamp) => {
  return new Date(timestamp * 1000).toLocaleDateString('zh-CN')
}

// 打开视频
const openVideo = (bvid) => {
  if (bvid) {
    window.open(`https://www.bilibili.com/video/${bvid}`, '_blank')
  }
}

// 获取热门命中率数据
const fetchHitRateData = async (year) => {
  if (!year) return

  // 如果父组件已经传递了数据，直接使用
  if (props.hitRateData) {
    hitRateData.value = props.hitRateData.hit_rate_analysis
    loading.value = false
    await initCharts()
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await getPopularHitRate(year)
    if (response.data.status === 'success') {
      hitRateData.value = response.data.data.hit_rate_analysis
      await initCharts()
    } else {
      error.value = response.data.message || '获取数据失败'
    }
  } catch (err) {
    console.error('获取热门命中率数据出错:', err)
    error.value = '获取数据时发生错误'
  } finally {
    loading.value = false
  }
}

// 初始化图表
const initCharts = async () => {
  await new Promise(resolve => setTimeout(resolve, 100)) // 等待DOM更新
  initChart()
}

// 初始化图表
const initChart = () => {
  if (!chartRef.value || !hitRateData.value) return

  if (chart) {
    chart.dispose()
  }

  chart = echarts.init(chartRef.value)

  const timingData = hitRateData.value.time_pattern_analysis || {}

  const data = [
    { name: '立即观看', value: timingData.immediate_watch || 0 },
    { name: '热门期观看', value: timingData.trending_watch || 0 }
  ]

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        const percentage = params.percent
        return `${params.name}: ${params.value} 个 (${percentage}%)`
      }
    },
    legend: {
      bottom: '8%',
      left: 'center',
      textStyle: {
        color: '#666',
        fontSize: 12
      }
    },
    series: [
      {
        name: '观看时机',
        type: 'pie',
        radius: '70%',
        center: ['50%', '45%'],
        label: {
          show: true,
          position: 'outside',
          formatter: function(params) {
            return `${params.name}\n${params.value}个\n${params.percent}%`
          },
          fontSize: 11,
          color: '#333'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '13',
            fontWeight: 'bold'
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        labelLine: {
          show: true,
          length: 15,
          length2: 10
        },
        data: data.map((item, index) => ({
          ...item,
          itemStyle: {
            color: ['#fb7299', '#fc9b7a'][index]
          }
        }))
      }
    ]
  }

  chart.setOption(option)
}

// 监听年份变化
watch(() => props.selectedYear, (newYear) => {
  fetchHitRateData(newYear)
}, { immediate: true })

// 监听父组件传递的数据变化
watch(() => props.hitRateData, (newData) => {
  if (newData) {
    hitRateData.value = newData.hit_rate_analysis
    loading.value = false
    initCharts()
  }
}, { immediate: true })

// 组件挂载时获取数据
onMounted(() => {
  fetchHitRateData(props.selectedYear)
})
</script>
