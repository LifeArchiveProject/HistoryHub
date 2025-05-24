<!-- 最爱重温页组件 -->
<template>
  <div class="absolute inset-0">
    <div class="h-full flex items-center justify-center">
      <div class="max-w-7xl w-full mx-auto px-2 py-6 overflow-y-auto">
        <div class="space-y-4">
          <h3 class="text-3xl font-bold text-center bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">
            最爱重温的视频
          </h3>

          <div v-if="viewingData?.insights?.most_watched_videos"
            class="text-sm text-center text-gray-600 dark:text-gray-300 mb-2 px-4"
            v-html="formatInsightText(viewingData.insights.most_watched_videos)"
          >
          </div>

          <!-- 没有重复观看数据的提示 -->
          <div v-if="!viewingData?.watch_counts?.most_watched_videos?.length"
               class="mt-8 text-center py-10 bg-white/50 dark:bg-white/5 backdrop-blur-sm rounded-lg border border-gray-300/50 dark:border-gray-500/50">
            <svg class="w-16 h-16 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 10.5a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1115 0z" />
            </svg>
            <p class="mt-4 text-lg font-medium text-gray-700 dark:text-gray-300">暂无重复观看记录</p>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">你在这一年中很少重复观看相同的视频</p>
            <p class="mt-1 text-sm text-gray-500">每次都在探索新内容的你，真是充满好奇心呢！</p>
          </div>

          <!-- 第一名 -->
          <div v-else-if="viewingData.watch_counts.most_watched_videos[0]"
            class="bg-gradient-to-br from-white/50 via-[#fb7299]/10 to-[#fc9b7a]/20 dark:from-white/5 dark:via-[#fb7299]/20 dark:to-[#fc9b7a]/30 backdrop-blur-sm rounded-lg p-3 transform hover:scale-[1.01] transition-transform cursor-pointer video-item relative overflow-hidden border border-gray-300/50 dark:border-gray-500/50"
            @click="handleVideoClick(viewingData.watch_counts.most_watched_videos[0].bvid)"
          >
            <div class="flex items-start space-x-4">
              <div class="flex-1 min-w-0">
                <div class="text-sm font-medium text-gray-800 dark:text-white hover:text-[#fb7299] transition-colors line-clamp-2">
                  {{ viewingData.watch_counts.most_watched_videos[0].title }}
                </div>
                <div class="mt-1.5 text-xs text-gray-600 dark:text-gray-400 flex items-center space-x-4">
                  <span>UP主：{{ viewingData.watch_counts.most_watched_videos[0].author_name }}</span>
                  <span>观看 {{ viewingData.watch_counts.most_watched_videos[0].watch_count }} 次</span>
                  <span>{{ viewingData.watch_counts.most_watched_videos[0].tag_name }}</span>
                </div>
              </div>
              <div class="flex flex-col items-center justify-center bg-white/30 dark:bg-white/10 backdrop-blur-sm rounded-lg px-2 py-1.5 border border-gray-300/50 dark:border-gray-500/50">
                <div class="text-lg font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent rewatch-interval whitespace-nowrap">
                  {{ Math.round(viewingData.watch_counts.most_watched_videos[0].avg_interval / 3600 / 24) }}
                </div>
                <div class="text-[10px] text-gray-500 whitespace-nowrap">天/次</div>
              </div>
            </div>
          </div>

          <!-- 其余视频 -->
          <div v-if="viewingData.watch_counts.most_watched_videos?.length > 1" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            <div v-for="(video, index) in viewingData.watch_counts.most_watched_videos.slice(1)"
              :key="video.bvid"
              class="backdrop-blur-sm rounded-lg p-2.5 transform hover:scale-[1.02] transition-transform cursor-pointer video-item relative overflow-hidden border border-gray-300/50 dark:border-gray-500/50"
              :class="{
                'bg-gradient-to-br from-white/50 via-[#fc9b7a]/10 to-[#fcd07a]/20 dark:from-white/5 dark:via-[#fc9b7a]/20 dark:to-[#fcd07a]/30': index === 0,
                'bg-gradient-to-br from-white/50 via-[#fcd07a]/10 to-[#fce07a]/20 dark:from-white/5 dark:via-[#fcd07a]/20 dark:to-[#fce07a]/30': index === 1,
                'bg-white/50 dark:bg-white/5': index > 1
              }"
              @click="handleVideoClick(video.bvid)"
            >
              <div class="flex items-start space-x-3">
                <div class="flex-1 min-w-0">
                  <div class="text-xs font-medium text-gray-800 dark:text-white hover:text-[#fb7299] transition-colors line-clamp-2">
                    {{ video.title }}
                  </div>
                  <div class="mt-1 text-[10px] text-gray-600 dark:text-gray-400 flex items-center justify-between">
                    <span>UP主：{{ video.author_name }}</span>
                    <span>{{ video.watch_count }}次</span>
                  </div>
                  <div class="text-[10px] text-gray-500">{{ video.tag_name }}</div>
                </div>
                <div class="flex flex-col items-center justify-center bg-white/30 dark:bg-white/10 backdrop-blur-sm rounded-lg px-2 py-1 ml-1 border border-gray-300/50 dark:border-gray-500/50">
                  <div class="text-sm font-bold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent rewatch-interval whitespace-nowrap">
                    {{ Math.round(video.avg_interval / 3600 / 24) }}
                  </div>
                  <div class="text-[10px] text-gray-500 whitespace-nowrap">天/次</div>
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
import { onMounted, nextTick, watch, ref } from 'vue'
import gsap from 'gsap'
import { openInBrowser } from '@/utils/openUrl.js'

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  }
})

// 用于存储当前视频列表的引用
const videoList = ref([])

const handleVideoClick = async (bvid) => {
  await openInBrowser(`https://www.bilibili.com/video/${bvid}`)
}

// 初始化动画
const initAnimation = () => {
  nextTick(() => {
    if (props.viewingData?.watch_counts?.most_watched_videos?.length > 0) {
      const videoItems = document.querySelectorAll('.video-item')
      if (videoItems.length > 0) {
        gsap.from(videoItems, {
          opacity: 0,
          y: 20,
          duration: 0.5,
          stagger: 0.1,
          ease: 'power2.out',
          delay: 0.2
        })
      }
    }
  })
}

// 监听数据变化
watch(() => props.viewingData?.watch_counts?.most_watched_videos, (newVal) => {
  // 先清空现有数据
  videoList.value = []

  // 在下一个 tick 中更新数据
  nextTick(() => {
    if (newVal) {
      videoList.value = newVal
      initAnimation()
    }
  })
}, { deep: true })

onMounted(() => {
  videoList.value = props.viewingData?.watch_counts?.most_watched_videos || []
  initAnimation()
})

// 格式化洞察文本，为数字添加颜色
const formatInsightText = (text) => {
  if (!text) return '';
  return text.replace(/(\d+(\.\d+)?)/g, '<span class="text-[#fb7299]">$1</span>')
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
