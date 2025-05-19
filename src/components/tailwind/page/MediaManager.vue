<template>
  <div class="min-h-screen bg-gray-50/30">
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 主内容卡片 -->
        <div class="bg-white rounded-lg overflow-hidden">
          <!-- 标签导航 - 修改为设置页风格 -->
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-6 px-4 overflow-x-auto" aria-label="媒体管理选项卡">
              <button
                @click="activeTab = 'videos'"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'videos'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                <span>视频管理</span>
              </button>

              <button
                @click="activeTab = 'images'"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'images'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>图片管理</span>
              </button>

              <button
                @click="activeTab = 'remarks'"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'remarks'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <span>我的备注</span>
              </button>

              <button
                @click="activeTab = 'comments'"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'comments'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <span>我的评论</span>
              </button>

              <button
                @click="activeTab = 'details'"
                class="py-3 px-1 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'details'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>视频详情</span>
              </button>
            </nav>
          </div>

          <!-- 内容区域 -->
          <div class="transition-all duration-300 p-5">
            <!-- 图片管理 -->
            <div v-if="activeTab === 'images'" class="animate-fadeIn">
              <Images />
            </div>

            <!-- 视频管理 -->
            <div v-if="activeTab === 'videos'" class="animate-fadeIn">
              <!-- ArtPlayer致谢 - 只在视频标签显示 -->
              <div class="mb-4 flex items-center justify-center h-9 px-3 py-0 bg-[#fb7299]/5 rounded-md border border-[#fb7299]/20">
                <a href="https://github.com/zhw2590582/ArtPlayer" target="_blank" rel="noopener noreferrer" class="flex items-center hover:opacity-80 transition-opacity mr-1.5">
                  <img src="https://artplayer.org/document/logo.png" alt="ArtPlayer Logo" class="h-3.5 mr-1.5" />
                </a>
                <span class="text-xs text-gray-700">视频播放通过
                  <a
                    href="https://github.com/zhw2590582/ArtPlayer"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="text-[#fb7299] font-medium hover:underline"
                  >
                    ArtPlayer
                  </a>
                  项目实现，感谢ArtPlayer团队的开源贡献
                </span>
              </div>
              <Downloads />
            </div>

            <!-- 我的备注 -->
            <div v-if="activeTab === 'remarks'" class="animate-fadeIn">
              <History :defaultShowRemarks="true" />
            </div>

            <!-- 我的评论 -->
            <div v-if="activeTab === 'comments'" class="animate-fadeIn">
              <Comments />
            </div>

            <!-- 视频详情管理 -->
            <div v-if="activeTab === 'details'" class="animate-fadeIn">
              <VideoDetailsManager />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Images from './Images.vue'
import Downloads from './Downloads.vue'
import VideoDetailsManager from './VideoDetailsManager.vue'
import History from './History.vue'
import Comments from './Comments.vue'

const route = useRoute()

// 当前激活的标签
const activeTab = ref('videos')

// 监听路由变化以更新激活的标签
watch(
  () => route.query.tab,
  (tab) => {
    if (tab && ['images', 'videos', 'remarks', 'comments', 'details'].includes(tab)) {
      activeTab.value = tab
    }
  },
  { immediate: true }
)

// 组件挂载时根据URL初始化标签
onMounted(() => {
  const { tab } = route.query
  if (tab && ['images', 'videos', 'remarks', 'comments', 'details'].includes(tab)) {
    activeTab.value = tab
  }
})
</script>

<style scoped>
.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>