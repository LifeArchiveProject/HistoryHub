<!-- 热门视频分区分布分析页组件 -->
<template>
  <div class="space-y-4">
    <h3 class="text-xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      热门视频分区分布分析
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
    <div v-else-if="distributionData" class="space-y-4">

      <!-- 洞察文本 -->
      <div class="text-center text-gray-600 dark:text-gray-300">
        <div class="text-sm leading-relaxed" v-html="formatInsightText(distributionData.insights.join('，'))"></div>
      </div>

      <!-- 可视化图表 -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-2 -mx-4">
        <!-- 分区分布统计卡片 -->
        <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-gray-300/50 dark:border-gray-500/50">
          <h4 class="text-base font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-2 text-center">
            分区分布统计
          </h4>
          <div ref="chartRef" class="h-[500px] px-4"></div>
        </div>

        <!-- 热门分区列表 -->
        <div v-if="distributionData.popular_categories && distributionData.popular_categories.length > 0"
             class="lg:col-span-2 bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-3 border border-gray-300/50 dark:border-gray-500/50">
          <h4 class="text-base font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent mb-2">
            热门分区排行 (前10个)
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-2 h-[460px] overflow-y-auto">
            <div v-for="(category, index) in distributionData.popular_categories" :key="index"
                 class="flex items-center p-2 bg-gray-50/50 dark:bg-gray-800/50 rounded-lg hover:bg-gray-100/50 dark:hover:bg-gray-700/50 transition-colors">
              <div class="flex-1 min-w-0">
                <div class="font-medium text-gray-900 dark:text-gray-100 truncate text-sm flex items-center justify-between">
                  <span>{{ category.category_name }}</span>
                  <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">
                    <span class="text-[#fb7299] font-semibold">{{ category.total_popular }}</span> 个热门视频
                  </span>
                </div>
                <!-- 显示该分区的热门视频 -->
                <div v-if="category.videos && category.videos.length > 0" class="mt-2 space-y-1">
                  <div v-for="(video, vIndex) in category.videos.slice(0, 2)" :key="vIndex"
                       @click="openVideo(video.bvid)"
                       class="text-xs text-gray-600 dark:text-gray-400 hover:text-[#fb7299] cursor-pointer truncate">
                    • {{ video.title }}
                  </div>
                  <div v-if="category.videos.length > 2" class="text-xs text-gray-400">
                    还有 {{ category.videos.length - 2 }} 个视频...
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
import { getCategoryPopularDistribution } from '../../../../api/api.js'

const props = defineProps({
  selectedYear: {
    type: Number,
    default: () => new Date().getFullYear()
  },
  distributionData: {
    type: Object,
    default: null
  }
})

const loading = ref(true)
const error = ref(null)
const distributionData = ref(null)
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

// 获取分区分布数据
const fetchDistributionData = async (year) => {
  if (!year) return

  // 如果父组件已经传递了数据，直接使用
  if (props.distributionData) {
    distributionData.value = props.distributionData.distribution_analysis
    loading.value = false
    await initCharts()
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await getCategoryPopularDistribution(year)
    if (response.data.status === 'success') {
      distributionData.value = response.data.data.distribution_analysis
      await initCharts()
    } else {
      error.value = response.data.message || '获取数据失败'
    }
  } catch (err) {
    console.error('获取热门视频分区分布数据出错:', err)
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
  if (!chartRef.value || !distributionData.value) return

  if (chart) {
    chart.dispose()
  }

  chart = echarts.init(chartRef.value)

  const categories = distributionData.value.popular_categories || []
  
  // 准备饼图数据
  const data = categories.map(category => ({
    name: category.category_name,
    value: category.total_popular
  }))

  // 生成颜色数组
  const colors = [
    '#fb7299', '#fc9b7a', '#ff6b9d', '#f093fb', '#f5576c',
    '#4facfe', '#00f2fe', '#43e97b', '#38f9d7', '#ffecd2'
  ]

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: function(params) {
        const percentage = params.percent
        return `${params.name}: ${params.value} 个热门视频 (${percentage}%)`
      }
    },
    legend: {
      bottom: '1%',
      left: 'center',
      textStyle: {
        color: '#666',
        fontSize: 9
      },
      type: 'scroll',
      pageIconColor: '#fb7299',
      pageIconInactiveColor: '#ccc',
      pageTextStyle: {
        color: '#666'
      },
      itemWidth: 12,
      itemHeight: 8
    },
    series: [
      {
        name: '分区分布',
        type: 'pie',
        radius: '45%',
        center: ['50%', '48%'],
        label: {
          show: true,
          position: 'outside',
          formatter: function(params) {
            if (params.percent < 3) return '' // 小于3%不显示标签，避免过于拥挤
            return `${params.name}\n${params.value}个`
          },
          fontSize: 11,
          color: '#333',
          fontWeight: '500',
          lineHeight: 14
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
          length: 20,
          length2: 15,
          smooth: true
        },
        data: data.map((item, index) => ({
          ...item,
          itemStyle: {
            color: colors[index % colors.length]
          }
        }))
      }
    ]
  }

  chart.setOption(option)
}

// 监听年份变化
watch(() => props.selectedYear, (newYear) => {
  fetchDistributionData(newYear)
}, { immediate: true })

// 监听父组件传递的数据变化
watch(() => props.distributionData, (newData) => {
  if (newData) {
    distributionData.value = newData.distribution_analysis
    loading.value = false
    initCharts()
  }
}, { immediate: true })

// 组件挂载时获取数据
onMounted(() => {
  fetchDistributionData(props.selectedYear)
})
</script>
