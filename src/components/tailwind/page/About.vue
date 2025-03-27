<template>
  <div class="min-h-screen bg-gray-50/50">
    <div class="py-6">
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 页面标题 -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-gray-800 flex items-center">
            <span class="bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent">关于本项目</span>
          </h1>
          <p class="text-gray-500 mt-2">哔哩哔哩历史记录管理与分析工具</p>
        </div>
        
        <!-- 主内容 -->
        <div class="space-y-8">
          <!-- 项目介绍卡片 -->
          <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100 p-6">
            <h2 class="text-xl font-medium text-gray-800 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              项目简介
            </h2>
            <div class="text-gray-600 space-y-3">
              <p>
                此项目是一个哔哩哔哩历史记录管理与分析工具，帮助用户更好地管理和分析自己的B站观看历史。基于Vue 3构建，通过现代的界面设计提供强大的功能，包括历史记录查询、视频下载、数据分析等多项功能。
              </p>

              <div class="mt-4 space-y-3">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2 text-[#fb7299]" fill="currentColor" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                  </svg>
                  <span class="text-gray-500 w-24 flex-shrink-0">前端项目</span>
                  <a href="https://github.com/LifeArchiveProject/BiliHistoryFrontend" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline break-all">https://github.com/LifeArchiveProject/BiliHistoryFrontend</a>
                </div>
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2 text-[#fb7299]" fill="currentColor" viewBox="0 0 24 24">
                    <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                  </svg>
                  <span class="text-gray-500 w-24 flex-shrink-0">后端项目</span>
                  <a href="https://github.com/LifeArchiveProject/HistoryHub" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline break-all">https://github.com/LifeArchiveProject/HistoryHub</a>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 技术致谢卡片 -->
          <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100 p-6">
            <h2 class="text-xl font-medium text-gray-800 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              技术致谢
            </h2>
            
            <div class="text-gray-600 space-y-4 mt-4">
              <ul class="list-disc pl-5 space-y-2">
                <li><a href="https://github.com/SocialSisterYi/bilibili-API-collect" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">bilibili-API-collect</a> - 没有它就没有这个项目</li>
                <li><a href="https://yutto.nyakku.moe/" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">Yutto</a> - 可爱的B站视频下载工具</li>
                <li><a href="https://github.com/SYSTRAN/faster-whisper" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">FasterWhisper</a> - 音频转文字</li>
                <li><a href="https://github.com/deepseek-ai/DeepSeek-R1" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">DeepSeek</a> - DeepSeek AI API</li>
                <li><a href="https://github.com/zhw2590582/ArtPlayer" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">ArtPlayer</a> - 强大且灵活的HTML5视频播放器</li>
                <li>所有贡献者</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// 没有需要特殊处理的逻辑，这是一个纯展示页面
</script>

<style scoped>
/* 可能的额外样式 */
</style>