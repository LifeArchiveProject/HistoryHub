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
          >
            {{ viewingData.insights.most_watched_videos }}
          </div>

          <!-- 第一名 -->
          <div v-if="viewingData.watch_counts.most_watched_videos[0]"
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
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
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
import { onMounted } from 'vue'
import gsap from 'gsap'

const props = defineProps({
  viewingData: {
    type: Object,
    required: true
  }
})

const handleVideoClick = (bvid) => {
  window.open(`https://www.bilibili.com/video/${bvid}`, '_blank')
}

onMounted(() => {
  const videoItems = document.querySelectorAll('.video-item')
  gsap.from(videoItems, {
    opacity: 0,
    y: 20,
    duration: 0.5,
    stagger: 0.1,
    ease: 'power2.out',
    delay: 0.2
  })
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
