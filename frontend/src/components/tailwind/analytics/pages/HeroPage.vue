<!-- 开场页组件 -->
<template>
  <div class="absolute inset-0">
    <div class="h-full flex items-center justify-center relative">
      <div class="text-center space-y-8" ref="heroContent">
        <div class="relative inline-block">
          <h2 class="text-6xl font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">你的B站时光机</h2>
          <div class="absolute -inset-1 bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] opacity-10 blur-xl"></div>
        </div>
        <p class="text-2xl text-gray-600 dark:text-gray-300">让我们开启{{ year }}年的回忆之旅</p>
        <div class="text-gray-500 dark:text-gray-400 animate-bounce mt-12">
          <span class="block">向下滑动开始探索</span>
          <svg class="w-6 h-6 mx-auto mt-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
          </svg>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import gsap from 'gsap'

const props = defineProps({
  year: {
    type: Number,
    required: true
  }
})

const heroContent = ref(null)

onMounted(() => {
  // 开场动画
  gsap.from(heroContent.value.children, {
    opacity: 0,
    y: 30,
    duration: 1,
    stagger: 0.2,
    ease: 'power3.out'
  })
})
</script> 