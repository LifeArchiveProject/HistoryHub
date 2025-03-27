<template>
  <div class="min-h-screen bg-gray-50/50">
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 页面标题 -->
        <div class="mb-6">
          <h1 class="text-3xl font-bold text-gray-800 flex items-center">
            <span class="bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">媒体管理</span>
          </h1>
          <p class="text-gray-500 mt-2">管理您的图片和视频文件</p>
        </div>
        
        <!-- 主内容卡片 -->
        <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
          <!-- 标签导航 -->
          <div class="flex bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
            <button 
              @click="activeTab = 'images'"
              class="relative py-4 px-6 focus:outline-none group"
            >
              <div 
                class="absolute bottom-0 left-0 w-full h-0.5 bg-[#fb7299] transform origin-left transition-transform duration-300"
                :class="activeTab === 'images' ? 'scale-x-100' : 'scale-x-0'"
              ></div>
              <div 
                class="flex items-center transition-all duration-300"
                :class="activeTab === 'images' ? 'text-[#fb7299]' : 'text-gray-600 group-hover:text-gray-900'"
              >
                <div class="p-2 rounded-lg mr-2 transition-all duration-300"
                     :class="activeTab === 'images' ? 'bg-[#fb7299]/10' : 'bg-transparent group-hover:bg-gray-200/50'">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm font-medium">图片管理</div>
                  <div class="text-xs" :class="activeTab === 'images' ? 'text-[#fb7299]/70' : 'text-gray-500'">封面与头像</div>
                </div>
              </div>
            </button>
            
            <button 
              @click="activeTab = 'videos'"
              class="relative py-4 px-6 focus:outline-none group"
            >
              <div 
                class="absolute bottom-0 left-0 w-full h-0.5 bg-[#fb7299] transform origin-left transition-transform duration-300"
                :class="activeTab === 'videos' ? 'scale-x-100' : 'scale-x-0'"
              ></div>
              <div 
                class="flex items-center transition-all duration-300"
                :class="activeTab === 'videos' ? 'text-[#fb7299]' : 'text-gray-600 group-hover:text-gray-900'"
              >
                <div class="p-2 rounded-lg mr-2 transition-all duration-300"
                     :class="activeTab === 'videos' ? 'bg-[#fb7299]/10' : 'bg-transparent group-hover:bg-gray-200/50'">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm font-medium">视频管理</div>
                  <div class="text-xs" :class="activeTab === 'videos' ? 'text-[#fb7299]/70' : 'text-gray-500'">视频与音频</div>
                </div>
              </div>
            </button>
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
              <div class="mb-4 flex items-center justify-center p-3 bg-gray-50 rounded-lg border border-gray-100">
                <a href="https://github.com/zhw2590582/ArtPlayer" target="_blank" rel="noopener noreferrer" class="flex items-center hover:opacity-80 transition-opacity mr-2">
                  <img src="https://artplayer.org/document/logo.png" alt="ArtPlayer Logo" class="h-5 mr-2" />
                </a>
                <span class="text-xs text-gray-600">视频播放通过
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
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Images from './Images.vue'
import Downloads from './Downloads.vue'

// 当前激活的标签
const activeTab = ref('images')
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