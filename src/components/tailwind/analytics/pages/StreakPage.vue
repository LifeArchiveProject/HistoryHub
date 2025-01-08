<!-- 连续观看记录页组件 -->
<template>
  <div class="space-y-6">
    <h3 class="text-4xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
      连续观看记录
    </h3>
    
    <div v-if="viewingData?.insights?.continuity" 
      class="text-lg text-center text-gray-600 dark:text-gray-300 mb-8"
    >
      {{ viewingData.insights.continuity }}
    </div>

    <div class="grid grid-cols-2 gap-8">
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
        <div class="text-4xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent streak-number">{{ viewingData.viewing_continuity.max_streak }}天</div>
        <div class="text-lg text-gray-600 dark:text-gray-400 mt-2">最长连续观看</div>
        <div class="mt-4 text-sm text-gray-500">
          {{ viewingData.viewing_continuity.longest_streak_period.start }} 至 
          {{ viewingData.viewing_continuity.longest_streak_period.end }}
        </div>
      </div>
      <div class="bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-gray-300/50 dark:border-gray-500/50">
        <div class="text-4xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent streak-number">{{ viewingData.viewing_continuity.current_streak }}天</div>
        <div class="text-lg text-gray-600 dark:text-gray-400 mt-2">当前连续观看</div>
        <div class="mt-4 text-sm text-gray-500">
          开始于 {{ viewingData.viewing_continuity.current_streak_start }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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
</script> 