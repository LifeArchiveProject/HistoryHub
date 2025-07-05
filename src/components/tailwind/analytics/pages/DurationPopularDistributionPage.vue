<!-- 热门视频时长分布分析页组件 -->
<template>
  <div class="space-y-4">
    <h3 class="text-xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      热门视频时长分布分析
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
    <div v-else-if="durationData" class="space-y-4">

      <!-- 洞察文本 -->
      <div class="text-center text-gray-600 dark:text-gray-300">
        <div class="text-sm leading-relaxed" v-html="formatInsightText(durationData.insights.join('，'))"></div>
      </div>

      <!-- 可视化图表 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-2 -mx-4">
        <!-- 时长分布统计卡片 -->
        <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-gray-300/50 dark:border-gray-500/50">
          <h4 class="text-base font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-2 text-center">
            时长分布统计
          </h4>
          <div ref="chartRef" class="h-[320px] px-4"></div>
        </div>

        <!-- 热门时长类型列表 -->
        <div v-if="durationData.popular_duration_videos && durationData.popular_duration_videos.length > 0"
             class="lg:col-span-2 bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-gray-300/50 dark:border-gray-500/50">
          <h4 class="text-base font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-2">
            热门时长类型排行 (前4个)
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2 h-[350px] overflow-y-auto">
            <div v-for="(durationType, index) in durationData.popular_duration_videos" :key="index"
                 class="flex items-center p-2 bg-gray-50/50 dark:bg-gray-800/50 rounded-lg hover:bg-gray-100/50 dark:hover:bg-gray-700/50 transition-colors">
              <div class="flex-1 min-w-0">
                <div class="font-medium text-gray-900 dark:text-gray-100 truncate text-sm flex items-center justify-between">
                  <span>{{ durationType.duration_type }}</span>
                  <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">
                    <span class="text-[#fb7299] font-semibold">{{ durationType.count }}</span> 个热门视频
                  </span>
                </div>
                <!-- 显示该时长类型的热门视频 -->
                <div v-if="durationType.videos && durationType.videos.length > 0" class="mt-2 space-y-1">
                  <div v-for="(video, vIndex) in durationType.videos.slice(0, 2)" :key="vIndex"
                       @click="openVideo(video.bvid)"
                       class="text-xs text-gray-600 dark:text-gray-400 hover:text-[#fb7299] cursor-pointer truncate">
                    • {{ video.title }} ({{ video.formatted_duration }})
                  </div>
                  <div v-if="durationType.videos.length > 2" class="text-xs text-gray-400">
                    还有 {{ durationType.videos.length - 2 }} 个视频...
                  </div>
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
import { getDurationPopularDistribution } from '../../../../api/api.js'

const props = defineProps({
  selectedYear: {
    type: Number,
    default: () => new Date().getFullYear()
  },
  durationData: {
    type: Object,
    default: null
  }
})

const loading = ref(true)
const error = ref(null)
const durationData = ref(null)
const chartRef = ref(null)
let chart = null

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299] font-semibold">$1</span>')
}

// 打开视频
const openVideo = (bvid) => {
  if (bvid) {
    window.open(`https://www.bilibili.com/video/${bvid}`, '_blank')
  }
}

// 获取时长分布数据
const fetchDurationData = async (year) => {
  if (!year) return

  // 如果父组件已经传递了数据，直接使用
  if (props.durationData) {
    durationData.value = props.durationData.duration_analysis
    loading.value = false
    await initCharts()
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await getDurationPopularDistribution(year)
    if (response.data.status === 'success') {
      durationData.value = response.data.data.duration_analysis
      await initCharts()
    } else {
      error.value = response.data.message || '获取数据失败'
    }
  } catch (err) {
    console.error('获取热门视频时长分布数据出错:', err)
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
  if (!chartRef.value || !durationData.value) return

  if (chart) {
    chart.dispose()
  }

  chart = echarts.init(chartRef.value)

  const durationStats = durationData.value.duration_stats || []
  
  // 准备柱状图数据
  const data = durationStats.map(stat => ({
    name: stat.duration_type,
    value: stat.count,
    percentage: stat.percentage
  }))

  // 生成颜色数组
  const colors = ['#fb7299', '#fc9b7a', '#ff6b9d', '#f093fb']

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: function(params) {
        const param = params[0]
        return `${param.name}: ${param.value} 个热门视频 (${param.data.percentage}%)`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '8%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.name),
      axisLabel: {
        color: '#666',
        fontSize: 11,
        interval: 0,
        rotate: 0
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
        fontSize: 10
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
    series: [
      {
        name: '热门视频数量',
        type: 'bar',
        data: data.map((item, index) => ({
          ...item,
          itemStyle: {
            color: colors[index % colors.length]
          }
        })),
        label: {
          show: true,
          position: 'top',
          formatter: '{c}个',
          fontSize: 10,
          color: '#333'
        },
        barWidth: '60%'
      }
    ]
  }

  chart.setOption(option)
}

// 监听年份变化
watch(() => props.selectedYear, (newYear) => {
  fetchDurationData(newYear)
}, { immediate: true })

// 监听父组件传递的数据变化
watch(() => props.durationData, (newData) => {
  if (newData) {
    durationData.value = newData.duration_analysis
    loading.value = false
    initCharts()
  }
}, { immediate: true })

// 组件挂载时获取数据
onMounted(() => {
  fetchDurationData(props.selectedYear)
})
</script>
