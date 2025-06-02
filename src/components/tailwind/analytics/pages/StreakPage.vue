<!-- 连续观看记录页组件 -->
<template>
  <div class="space-y-6">
    <h3 class="text-4xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      连续观看记录
    </h3>

    <div v-if="viewingData?.insights?.continuity"
      class="text-lg text-center text-gray-600 dark:text-gray-300 mb-8"
      v-html="formatInsightText(viewingData.insights.continuity)"
    >
    </div>

    <div v-if="viewingData?.viewing_continuity" class="grid grid-cols-2 gap-8">
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
        <div class="text-4xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent streak-number">{{ viewingData.viewing_continuity.max_streak || 0 }}天</div>
        <div class="text-lg text-gray-600 dark:text-gray-400 mt-2">最长连续观看</div>
        <div v-if="viewingData.viewing_continuity.longest_streak_period" class="mt-4 text-sm text-gray-500">
          {{ viewingData.viewing_continuity.longest_streak_period.start }} 至
          {{ viewingData.viewing_continuity.longest_streak_period.end }}
        </div>
      </div>
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
        <div class="text-4xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent streak-number">{{ viewingData.viewing_continuity.current_streak || 0 }}天</div>
        <div class="text-lg text-gray-600 dark:text-gray-400 mt-2">当前连续观看</div>
        <div v-if="viewingData.viewing_continuity.current_streak_start" class="mt-4 text-sm text-gray-500">
          开始于 {{ viewingData.viewing_continuity.current_streak_start }}
        </div>
      </div>
    </div>

    <!-- 数据加载中或无数据时的提示 -->
    <div v-else class="text-center text-gray-500 dark:text-gray-400">
      正在加载连续观看数据...
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import gsap from 'gsap'

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  }
})

onMounted(() => {
  // 数字动画效果
  const streakNumbers = document.querySelectorAll('.streak-number')
  streakNumbers.forEach(el => {
    const finalValue = parseInt(el.textContent)
    gsap.fromTo(el,
      { textContent: 0 },
      {
        duration: 2,
        textContent: finalValue,
        snap: { textContent: 1 },
        ease: 'power1.out'
      }
    )
  })
})

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}
</script>
