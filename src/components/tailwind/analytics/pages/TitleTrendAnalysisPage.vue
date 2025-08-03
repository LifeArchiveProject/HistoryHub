<template>
  <div class="min-h-screen py-4 px-1 sm:px-2 lg:px-3">
    <div class="max-w-full mx-auto">
      <!-- 标题和总结部分 -->
      <div class="text-center mb-4">
        <h2 class="text-3xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
          标题趋势分析
        </h2>
        <div class="mt-3 text-gray-600 max-w-3xl mx-auto" v-if="titleAnalytics && titleAnalytics.trend_analysis">
          <p class="mb-2" v-if="titleAnalytics.trend_analysis.insights && titleAnalytics.trend_analysis.insights[0]" v-html="formatInsightText(titleAnalytics.trend_analysis.insights[0])"></p>
          <p v-if="titleAnalytics.trend_analysis.insights && titleAnalytics.trend_analysis.insights[1]" v-html="formatInsightText(titleAnalytics.trend_analysis.insights[1])"></p>
        </div>
      </div>

      <!-- 月度热门关键词 -->
      <div class="bg-white/5 backdrop-blur-sm rounded-xl p-2">
        <div class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-2">
          <div v-for="(trends, month) in getSortedMonthlyTrends()" 
               :key="month" 
               class="bg-white/5 backdrop-blur-sm rounded-xl p-3">
            <h4 class="font-medium text-gray-600 mb-2">{{ formatMonth(month) }}</h4>
            <div class="space-y-1.5">
              <div v-for="([keyword, count], index) in trends.top_keywords.slice(0, 5)" 
                   :key="keyword"
                   class="flex items-center justify-between text-sm">
                <div class="flex items-center space-x-2">
                  <div class="w-1.5 h-1.5 rounded-full" :style="{ backgroundColor: colors[index % colors.length] }"></div>
                  <span class="text-gray-600">{{ keyword }}</span>
                </div>
                <span class="text-gray-600 text-xs">{{ count }}次</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  titleAnalytics: {
    type: Object,
    required: true
  }
})

// 颜色数组
const colors = [
  '#fb7299', // 粉色
  '#fc9b7a', // 橙色
  '#7a9efc', // 蓝色
  '#7afc8c', // 绿色
  '#fc7ab3'  // 粉紫色
]

// 获取排序后的月度趋势数据
const getSortedMonthlyTrends = () => {
  if (!props.titleAnalytics?.trend_analysis?.monthly_trends) return {}
  const trends = props.titleAnalytics.trend_analysis.monthly_trends
  return Object.fromEntries(
    Object.entries(trends)
      .sort(([a], [b]) => a.localeCompare(b))
  )
}

// 格式化月份显示
const formatMonth = (month) => {
  return month.replace('-', '年') + '月'
}

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}
</script> 