<!-- 视频下载弹窗 -->
<template>
  <!-- 将通知容器放置在最外层，确保z-index最高 -->
  <Teleport to="body">
    <div class="notification-container fixed top-0 left-0 right-0 z-[999999]"></div>
  </Teleport>

  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 z-[9999] flex items-center justify-center">
      <!-- 遮罩层 -->
      <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="handleClose"></div>

      <!-- 弹窗内容 -->
      <div
        class="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl w-[96vw] max-w-5xl h-[95vh] z-10 overflow-hidden flex flex-col">
        <!-- 关闭按钮 -->
        <button
          @click="handleClose"
          class="absolute right-4 top-4 text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 z-20 p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- 页眉区域：包含Yutto致谢和FFmpeg状态 -->
        <div
          class="px-6 py-3 flex items-center justify-between bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center space-x-3">
            <img src="https://yutto.nyakku.moe/logo-mini.svg" alt="Yutto Logo" class="w-6 h-6">
            <div class="flex flex-col">
              <p class="text-xs text-gray-700 dark:text-gray-300">下载功能通过 <a href="https://yutto.nyakku.moe/"
                                                                                  target="_blank"
                                                                                  class="text-[#fb7299] hover:text-[#fb7299]/80 font-medium">Yutto</a>
                实现</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">感谢 Yutto 开发团队的开源贡献</p>
            </div>
          </div>

          <!-- FFmpeg 状态 -->
          <div v-if="ffmpegStatus" class="flex-shrink-0">
            <div v-if="ffmpegStatus.installed"
                 class="flex items-center space-x-1 p-1.5 bg-green-50 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-lg text-xs">
              <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <div>
                <p class="font-medium">FFmpeg 已安装</p>
                <p class="text-xs">{{ ffmpegStatus.version }}</p>
              </div>
            </div>
            <div v-else class="group relative">
              <div class="flex flex-col space-y-1">
                <div
                  class="flex items-center space-x-1 p-1.5 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-400 rounded-lg text-xs">
                  <svg class="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <p class="font-medium">FFmpeg 未安装</p>
                </div>
                <div class="text-xs text-gray-600 dark:text-gray-400">
                  <p>
                    <a
                      href="https://yutto.nyakku.moe/guide/quick-start#ffmpeg-%E4%B8%8B%E8%BD%BD%E4%B8%8E%E9%85%8D%E7%BD%AE"
                      target="_blank"
                      class="text-[#fb7299] hover:text-[#fb7299]/80">
                      点击查看Yutto说明 →
                    </a>
                  </p>
                </div>
              </div>
              <div class="hidden group-hover:block hover:block absolute right-0 top-full h-2 w-full"></div>
              <div
                class="hidden group-hover:block hover:block absolute right-0 top-[calc(100%+0.5rem)] w-[500px] p-3 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-30 text-xs">
                <p class="font-medium text-gray-900 dark:text-gray-100 mb-2">安装指南：</p>
                <div v-if="ffmpegStatus?.install_guide" class="space-y-1 whitespace-pre-wrap">
                  <div v-for="(line, index) in installGuideLines" :key="index" class="flex items-start space-x-1">
                    <template v-if="isCommand(line)">
                      <div class="flex-1 bg-gray-50 dark:bg-gray-900 p-1.5 rounded break-all">
                        <code class="text-gray-700 dark:text-gray-300">{{ getCommandContent(line) }}</code>
                      </div>
                      <button @click="copyToClipboard(getCommandContent(line))"
                              class="text-[#fb7299] hover:text-[#fb7299]/80 p-1 rounded-md hover:bg-[#fb7299]/10 flex-shrink-0"
                              title="点击复制命令">
                        <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                        </svg>
                      </button>
                    </template>
                    <template v-else>
                      <p class="text-gray-600 dark:text-gray-400 break-all">{{ line }}</p>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 主内容区域 -->
        <div class="flex-1 overflow-y-auto">
          <div class="px-6 pt-3 pb-4">
            <!-- 标题 -->
            <div class="mb-2">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
                {{ getDownloadTitle() }}
              </h3>
              <p v-if="downloadStarted" class="text-sm text-gray-500 dark:text-gray-400">
                {{ isDownloading ? '正在下载：' : (downloadError ? '下载出错：' : '下载完成：') }} {{ currentVideoTitle }}
              </p>
              <p v-else class="text-sm text-gray-500 dark:text-gray-400">
                {{ videoInfo.title }}
              </p>
              <!-- 收藏夹视频总数 -->
              <p v-if="isFavoriteFolder" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                共 {{ favoritePageInfo.totalCount || props.videoInfo.total_videos || favoriteVideos.length }}
                个视频，当前进度：{{ currentVideoIndex + 1
                }}/{{ favoritePageInfo.totalCount || props.videoInfo.total_videos || favoriteVideos.length }}
              </p>
              <!-- 批量下载视频总数 -->
              <p v-if="props.isBatchDownload" class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                共 {{ props.batchVideos.length }} 个视频，当前进度：{{ props.currentVideoIndex + 1
                }}/{{ props.batchVideos.length }}
              </p>
            </div>

            <!-- 视频信息 -->
            <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-4">
              <div class="flex items-start space-x-4">
                <div class="w-32 h-20 flex-shrink-0 overflow-hidden rounded-lg">
                  <img :src="currentVideoCover" :alt="currentVideoTitle"
                       class="w-full h-full object-cover transition-transform hover:scale-105">
                </div>
                <div class="flex-1 min-w-0">
                  <p v-if="!isFavoriteFolder" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    UP主：{{ props.isBatchDownload ? currentVideoAuthor : props.videoInfo.author || '未知' }}</p>
                  <p v-if="!isFavoriteFolder" class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    BV号：{{ props.isBatchDownload ? currentVideoBvid : props.videoInfo.bvid || '未知' }}</p>

                  <!-- 基础下载选项 -->
                  <div class="flex flex-wrap gap-4 items-center mt-3">
                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="downloadCover"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                      >
                      <span class="text-sm text-gray-700 dark:text-gray-300">下载并合成视频封面</span>
                    </label>
                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="onlyAudio"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                      >
                      <span class="text-sm text-gray-700 dark:text-gray-300">仅下载音频</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <!-- 高级选项切换按钮 -->
            <div v-if="!showAdvancedOptions" class="mb-2">
              <button
                @click="showAdvancedOptions = true"
                class="w-full flex items-center justify-center py-2.5 px-4 text-sm bg-white border border-gray-200 rounded-lg hover:bg-gray-50 /50 transition-colors group shadow-sm"
              >
                <div class="flex items-center space-x-3">
                  <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span class="font-medium text-gray-700 ">高级下载选项</span>
                  <div class="flex-grow"></div>
                  <div class="flex items-center space-x-1 text-xs text-[#fb7299]">
                    <span>展开</span>
                    <svg class="w-4 h-4 transform transition-transform group-hover:translate-y-0.5 duration-300"
                         fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </button>
            </div>

            <!-- 高级下载选项区域 -->
            <div
              class="bg-white rounded-lg border border-gray-200 mb-2 overflow-hidden shadow-sm transition-all duration-300"
              :class="{
 'max-h-[1000px] opacity-100': showAdvancedOptions,
 'max-h-0 opacity-0 border-0': !showAdvancedOptions
 }"
            >
              <!-- 高级选项标题 -->
              <div class="bg-gray-50 /50 p-3 flex justify-between items-center border-b border-gray-200 ">
                <div class="flex items-center space-x-2">
                  <svg class="w-4 h-4 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <h4 class="text-sm font-medium text-gray-800 ">高级下载选项</h4>
                </div>

                <!-- 隐藏按钮 -->
                <button
                  @click="showAdvancedOptions = false"
                  class="flex items-center space-x-1 px-2.5 py-1.5 rounded-md text-xs text-gray-600 hover:bg-gray-100 hover:text-[#fb7299] transition-all duration-200 group"
                >
                  <span>收起选项</span>
                  <svg class="w-4 h-4 transition-transform group-hover:-translate-y-0.5 duration-300" fill="none"
                       viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                </button>
              </div>

              <div class="p-3">
                <!-- 基础参数区块 -->
                <div class="mb-3">
                  <h5 class="text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide flex items-center">
                    <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                    视频和音频质量
                  </h5>
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <!-- 视频清晰度 -->
                    <div>
                      <label class="block text-xs text-gray-600 mb-1">视频清晰度</label>
                      <CustomDropdown
                        v-model="advancedOptions.video_quality"
                        :options="videoQualityOptions"
                        :selected-text="getVideoQualityText(advancedOptions.video_quality)"
                        custom-class="w-full text-xs"
                      />
                      <div class="text-xs text-gray-500 mt-1 text-[10px]">
                        yutto会尽可能满足清晰度要求，如不存在会自动调节
                      </div>
                    </div>

                    <!-- 音频码率 -->
                    <div>
                      <label class="block text-xs text-gray-600 mb-1">音频码率</label>
                      <CustomDropdown
                        v-model="advancedOptions.audio_quality"
                        :options="audioQualityOptions"
                        :selected-text="getAudioQualityText(advancedOptions.audio_quality)"
                        custom-class="w-full text-xs"
                      />
                    </div>

                    <!-- 输出格式 -->
                    <div>
                      <label class="block text-xs text-gray-600 mb-1">输出格式</label>
                      <CustomDropdown
                        v-model="advancedOptions.output_format"
                        :options="outputFormatOptions"
                        :selected-text="getOutputFormatText(advancedOptions.output_format)"
                        custom-class="w-full text-xs"
                      />
                    </div>
                  </div>
                </div>

                <!-- 编码参数区块 -->
                <div class="mb-3">
                  <h5 class="text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide flex items-center">
                    <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                    </svg>
                    编码选项
                  </h5>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <!-- 视频编码 -->
                    <div>
                      <label class="block text-xs text-gray-600 mb-1">视频编码</label>
                      <CustomDropdown
                        v-model="advancedOptions.vcodec"
                        :options="vcodecOptions"
                        :selected-text="getVcodecText(advancedOptions.vcodec)"
                        custom-class="w-full text-xs"
                      />
                    </div>

                    <!-- 音频编码 -->
                    <div>
                      <label class="block text-xs text-gray-600 mb-1">音频编码</label>
                      <CustomDropdown
                        v-model="advancedOptions.acodec"
                        :options="acodecOptions"
                        :selected-text="getAcodecText(advancedOptions.acodec)"
                        custom-class="w-full text-xs"
                      />
                    </div>
                  </div>
                </div>

                <!-- 资源选项区块 -->
                <div>
                  <h5 class="text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide flex items-center">
                    <svg class="w-3 h-3 mr-1 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    资源选择
                  </h5>
                  <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                    <!-- 第一行 -->
                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.video_only"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="onlyAudio"
                      >
                      <span class="text-xs text-gray-700 ">仅下载视频流</span>
                    </label>

                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.no_danmaku"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="advancedOptions.danmaku_only"
                      >
                      <span class="text-xs text-gray-700 ">不生成弹幕</span>
                    </label>

                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.danmaku_only"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="advancedOptions.no_danmaku"
                      >
                      <span class="text-xs text-gray-700 ">仅生成弹幕</span>
                    </label>

                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.no_subtitle"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="advancedOptions.subtitle_only"
                      >
                      <span class="text-xs text-gray-700 ">不生成字幕</span>
                    </label>

                    <!-- 第二行 -->
                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.subtitle_only"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="advancedOptions.no_subtitle"
                      >
                      <span class="text-xs text-gray-700 ">仅生成字幕</span>
                    </label>

                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.with_metadata"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="advancedOptions.metadata_only"
                      >
                      <span class="text-xs text-gray-700 ">生成元数据</span>
                    </label>

                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.metadata_only"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="advancedOptions.with_metadata"
                      >
                      <span class="text-xs text-gray-700 ">仅生成元数据</span>
                    </label>

                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.no_cover"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="!downloadCover || advancedOptions.save_cover || advancedOptions.cover_only"
                      >
                      <span class="text-xs text-gray-700 ">不生成封面</span>
                    </label>

                    <!-- 第三行 -->
                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.save_cover"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="!downloadCover || advancedOptions.cover_only || advancedOptions.no_cover"
                      >
                      <span class="text-xs text-gray-700 ">单独保存封面</span>
                    </label>

                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.cover_only"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                        :disabled="!downloadCover || advancedOptions.save_cover || advancedOptions.no_cover"
                      >
                      <span class="text-xs text-gray-700 ">仅生成封面</span>
                    </label>

                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="advancedOptions.no_chapter_info"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                      >
                      <span class="text-xs text-gray-700 ">不生成章节</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <!-- 下载日志 -->
            <div
              class="w-full bg-gray-50 rounded-lg p-2 pb-0 font-mono text-[11px] overflow-y-auto border border-gray-200 "
              :class="showAdvancedOptions ? 'h-[calc(100vh-588px)] min-h-[130px]' : 'h-[calc(100vh-418px)] min-h-[180px]'"
              ref="logContainer">
              <div v-if="!downloadStarted" class="text-gray-500 flex items-center justify-center h-full">
                <div class="text-center">
                  <svg class="w-8 h-8 mx-auto mb-0 text-gray-400 " fill="none" viewBox="0 0 24 24"
                       stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                          d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p>点击下方按钮开始下载...</p>
                </div>
              </div>
              <div v-else>
                <div v-for="(log, index) in downloadLogs" :key="index" class="whitespace-pre break-all leading-5 py-0.5 last:pb-0"
                     :class="{
 'text-gray-600 ': !log.includes('ERROR') && !log.includes('下载完成') && !log.includes('WARN'),
 'text-red-500 ': log.includes('ERROR'),
 'text-green-500 ': log.includes('下载完成'),
 'text-yellow-500 dark:text-yellow-400': log.includes('WARN'),
 }">{{ log }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 页脚区域：状态和按钮 -->
        <div class="bg-gray-50 border-t border-gray-200 py-2 px-6 flex items-center justify-between">
          <div class="text-xs font-medium" :class="{
 'text-gray-500 ': !downloadStarted,
 'text-red-500 ': downloadError,
 'text-green-500 ': !isDownloading && downloadStarted && !downloadError,
 'text-[#fb7299]': isDownloading
 }">
            {{ downloadStatus }}
          </div>
          <div class="flex space-x-3">
            <button
              @click="handleClose"
              class="px-3 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
              :disabled="isDownloading"
            >
              {{ isDownloading ? '下载中...' : '关闭' }}
            </button>
            <button
              v-if="!downloadStarted || downloadError"
              @click="startDownload"
              class="px-3 py-1.5 text-xs font-medium text-white bg-[#fb7299] rounded-md hover:bg-[#fb7299]/90 disabled:opacity-50 transition-colors"
              :disabled="isDownloading"
            >
              {{ downloadError ? '重试' : '开始下载' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onUnmounted, nextTick } from 'vue'
import {
  downloadVideo,
  checkFFmpeg,
  downloadFavorites,
  getFavoriteContents,
  downloadUserVideos,
  batchDownloadVideos,
  downloadCollection,
} from '@/api/api.js'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import CustomDropdown from '@/components/tailwind/CustomDropdown.vue'

defineOptions({
  name: 'DownloadDialog',
})

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  videoInfo: {
    type: Object,
    required: true,
    default: () => ({
      title: '',
      author: '',
      bvid: '',
      cover: '',
      cid: 0,
    }),
  },
  // 当为 true 时，弹窗打开时默认勾选“仅下载音频”
  defaultOnlyAudio: {
    type: Boolean,
    default: false,
  },
  // 添加 UP 主视频列表参数
  upUserVideos: {
    type: Array,
    default: () => [],
  },
  // 批量下载参数
  isBatchDownload: {
    type: Boolean,
    default: false,
  },
  batchVideos: {
    type: Array,
    default: () => [],
  },
  // 当前下载的视频索引
  currentVideoIndex: {
    type: Number,
    default: 0,
  },
})

const emit = defineEmits(['update:show', 'download-complete', 'update:currentVideoIndex'])

// 下载相关状态
const downloadStarted = ref(false)
const isDownloading = ref(false)
const downloadError = ref(false)
const downloadLogs = ref([])
// 控制高级选项的显示状态
const showAdvancedOptions = ref(false)

// 下载状态文本
const downloadStatus = computed(() => {
  if (!downloadStarted.value) return '准备就绪'
  if (downloadError.value) return '下载出错'
  if (isDownloading.value) return '下载中...'
  return '下载完成'
})

// 获取下载标题
const getDownloadTitle = () => {
  if (props.videoInfo.is_collection_download) {
    return '下载合集'
  } else if (props.isBatchDownload) {
    return '批量下载视频'
  } else if (isFavoriteFolder.value) {
    return '下载收藏夹'
  } else {
    return '下载视频'
  }
}

// 日志容器引用
const logContainer = ref(null)

// FFmpeg 状态
const ffmpegStatus = ref(null)

// 检查 FFmpeg 安装状态
const checkFFmpegStatus = async () => {
  try {
    const response = await checkFFmpeg()
    if (response.data) {
      ffmpegStatus.value = {
        installed: response.data.status === 'success',
        version: response.data.version,
        path: response.data.path,
        os_info: response.data.os_info,
        install_guide: response.data.install_guide,
      }
    }
  } catch (error) {
    console.error('检查 FFmpeg 失败:', error)
  }
}

// 下载封面选项
const downloadCover = ref(true)
// 仅下载音频选项
const onlyAudio = ref(false)
// 高级选项
const advancedOptions = ref({
  // 基础参数
  video_quality: null,
  audio_quality: null,
  vcodec: null,
  acodec: null,
  download_vcodec_priority: null,
  output_format: null,
  output_format_audio_only: null,

  // 资源选择参数
  video_only: false,
  danmaku_only: false,
  no_danmaku: false,
  subtitle_only: false,
  no_subtitle: false,
  with_metadata: false,
  metadata_only: false,
  no_cover: false,
  save_cover: false,
  cover_only: false,
  no_chapter_info: false,
})

// 当前正在下载的视频信息
const currentVideoTitle = ref('')
const currentVideoCover = ref('')
const currentVideoAuthor = ref('')
const currentVideoBvid = ref('')

const videoTitles = ref([]) // 存储所有检测到的视频标题

// 存储收藏夹中所有视频信息
const favoriteVideos = ref([])
// 当前正在下载的视频索引
const currentVideoIndex = ref(-1)
// 收藏夹的页码信息
const favoritePageInfo = ref({
  page: 1,
  pageSize: 40,
  totalCount: 0,
  totalPage: 0,
  hasMore: false,
})
// 加载收藏夹内容状态
const loadingFavorites = ref(false)

// 是否是收藏夹
const isFavoriteFolder = computed(() => {
  return !!props.videoInfo.is_favorite_folder
})

// 预加载收藏夹所有视频
const preloadFavoriteVideos = async () => {
  if (!isFavoriteFolder.value || !props.videoInfo.fid) return

  try {
    loadingFavorites.value = true
    downloadLogs.value.push('INFO 正在获取收藏夹内容，请稍候...')

    // 先获取基本信息，确定总视频数
    try {
      const initialResponse = await getFavoriteContents({
        media_id: props.videoInfo.fid,
        pn: 1,
        ps: 1, // 只获取一个视频，主要是为了拿到总数
      })

      if (initialResponse.data && initialResponse.data.status === 'success' && initialResponse.data.data) {
        // 更新总数信息
        favoritePageInfo.value.totalCount = initialResponse.data.data.total || props.videoInfo.total_videos || 0
        favoritePageInfo.value.totalPage = Math.ceil(favoritePageInfo.value.totalCount / 40)

        console.log('收藏夹总视频数:', favoritePageInfo.value.totalCount)
        console.log('总页数:', favoritePageInfo.value.totalPage)

        downloadLogs.value.push(`INFO 收藏夹共有 ${favoritePageInfo.value.totalCount} 个视频，开始获取视频信息`)
      }
    } catch (error) {
      console.error('获取收藏夹基本信息失败:', error)
    }

    // 如果仍然没有总数信息，使用props中的值
    if (!favoritePageInfo.value.totalCount) {
      favoritePageInfo.value.totalCount = props.videoInfo.total_videos || 0
      favoritePageInfo.value.totalPage = Math.ceil(favoritePageInfo.value.totalCount / 40)
    }

    let allVideos = []
    let page = 1
    let maxPages = Math.min(favoritePageInfo.value.totalPage || 5, 10) // 最多获取10页，避免过多请求
    let hasMore = page <= maxPages

    // 如果视频总数超过200个，提示用户
    if (favoritePageInfo.value.totalCount > 200) {
      downloadLogs.value.push(`WARN 收藏夹视频数量较多(${favoritePageInfo.value.totalCount}个)，将只预加载部分视频信息`)
      downloadLogs.value.push('INFO 下载过程中会自动更新视频信息')
    }

    while (hasMore) {
      try {
        downloadLogs.value.push(`INFO 正在获取第${page}页视频信息...`)

        const response = await getFavoriteContents({
          media_id: props.videoInfo.fid,
          pn: page,
          ps: 40, // 每页40条
        })

        if (response.data && response.data.status === 'success' && response.data.data) {
          const data = response.data.data

          // 更新总视频数，避免后续请求
          if (page === 1 && data.total) {
            favoritePageInfo.value.totalCount = data.total
            favoritePageInfo.value.totalPage = Math.ceil(data.total / (data.pagesize || 40))
          }

          if (data.medias && Array.isArray(data.medias)) {
            // 合并结果
            const newVideos = data.medias.map(item => ({
              title: item.title || '',
              cover: item.cover || '',
              bvid: item.bvid || '',
              cid: item.cid || 0,
              author: item.upper?.name || '',
              avid: item.id || 0,
            }))

            allVideos = allVideos.concat(newVideos)

            // 更新日志，显示当前进度
            downloadLogs.value.push(`INFO 已获取 ${allVideos.length}/${favoritePageInfo.value.totalCount} 个视频信息`)
          }

          // 判断是否还有更多页
          page++
          hasMore = page <= maxPages && page <= favoritePageInfo.value.totalPage

          // 大型收藏夹时，避免请求过多页面
          if (page > 5 && favoritePageInfo.value.totalCount > 200) {
            downloadLogs.value.push(`INFO 已获取前${page - 1}页视频信息，剩余信息将在下载过程中更新`)
            hasMore = false
          }

          // 休眠一段时间，避免触发API限制
          if (hasMore) {
            await new Promise(resolve => setTimeout(resolve, 500))
          }
        } else {
          downloadLogs.value.push('ERROR 获取收藏夹内容失败，将使用实时日志更新视频信息')
          hasMore = false
        }
      } catch (error) {
        console.error(`获取收藏夹内容第${page}页失败:`, error)
        downloadLogs.value.push(`ERROR 获取第${page}页内容失败，可能触发了API限制`)
        hasMore = false
      }
    }

    favoriteVideos.value = allVideos

    if (allVideos.length < favoritePageInfo.value.totalCount) {
      downloadLogs.value.push(`INFO 已预加载 ${allVideos.length}/${favoritePageInfo.value.totalCount} 个视频信息，剩余视频将在下载过程中更新`)
    } else {
      downloadLogs.value.push(`INFO 收藏夹内容获取完成，共 ${allVideos.length} 个视频`)
    }

  } catch (error) {
    console.error('加载收藏夹内容失败:', error)
    downloadLogs.value.push('ERROR 获取收藏夹内容失败，将使用实时日志更新视频信息')
  } finally {
    loadingFavorites.value = false
  }
}

// 监听日志变化，提取视频顺序索引
watch(() => downloadLogs.value, async (logs) => {
  if (!logs || logs.length === 0) return

  // 获取最新的日志信息
  const latestLog = logs[logs.length - 1]
  console.log('处理新日志:', latestLog)

  // 检查是否是下载完成信息
  if (latestLog === '下载完成') {
    console.log('收藏夹下载全部完成')
    // 确保显示最后一个视频
    if (isFavoriteFolder.value && favoriteVideos.value.length > 0) {
      currentVideoIndex.value = favoriteVideos.value.length - 1
      const lastVideo = favoriteVideos.value[currentVideoIndex.value]
      currentVideoTitle.value = lastVideo.title
      currentVideoCover.value = lastVideo.cover || ''
    }
    return
  }

  // 检查是否为视频序号信息 [n/total]
  const indexMatch = latestLog.match(/\[(\d+)\/(\d+)\]/)
  if (indexMatch) {
    const index = parseInt(indexMatch[1], 10) - 1 // 索引从0开始
    const total = parseInt(indexMatch[2], 10)
    console.log(`检测到视频索引: ${index + 1}/${total}`)

    // 提取完整的视频标题
    const titleMatch = latestLog.match(/\[(\d+)\/(\d+)\]\s+(.+)/)
    if (titleMatch) {
      const videoTitle = titleMatch[3].trim()
      console.log('检测到视频标题:', videoTitle)
      currentVideoTitle.value = videoTitle

      // 更新索引和封面
      if (isFavoriteFolder.value && favoriteVideos.value.length > 0) {
        if (index >= 0 && index < favoriteVideos.value.length) {
          currentVideoIndex.value = index
          const videoInfo = favoriteVideos.value[index]
          if (videoInfo && videoInfo.cover) {
            currentVideoCover.value = videoInfo.cover
          }
        }
      } else {
        // 搜索封面
        trySearchCover(videoTitle)
      }
    }
    return
  }

  // 检查是否为"开始处理视频"
  const processingMatch = latestLog.match(/INFO\s+开始处理视频\s+(.+)/)
  if (processingMatch) {
    const videoTitle = processingMatch[1].trim()
    console.log('检测到开始处理视频:', videoTitle)

    // 更新当前视频标题
    currentVideoTitle.value = videoTitle

    // 查找匹配的视频
    if (isFavoriteFolder.value && favoriteVideos.value.length > 0) {
      const videoIndex = favoriteVideos.value.findIndex(v => v.title === videoTitle)
      if (videoIndex >= 0) {
        currentVideoIndex.value = videoIndex
        const videoInfo = favoriteVideos.value[videoIndex]
        if (videoInfo && videoInfo.cover) {
          currentVideoCover.value = videoInfo.cover
        }
      } else {
        // 没找到匹配的视频，尝试搜索封面
        trySearchCover(videoTitle)
      }
    } else {
      // 没有预加载数据，搜索封面
      trySearchCover(videoTitle)
    }
    return
  }

  // 检查是否为"合并完成"
  if (latestLog.includes('INFO 合并完成！')) {
    console.log('检测到视频合并完成')

    // 预测下一个视频
    const nextIndex = currentVideoIndex.value + 1
    if (isFavoriteFolder.value && favoriteVideos.value.length > 0 && nextIndex < favoriteVideos.value.length) {
      // 等待短暂时间，看是否会有新的视频标题出现
      setTimeout(() => {
        // 再次检查最新的几条日志
        const recentLogs = downloadLogs.value.slice(-5).join('\n')
        // 如果没有新的视频标题信息，则主动切换到下一个视频
        if (!recentLogs.includes('[') || !recentLogs.includes('/')) {
          console.log(`准备切换到下一个视频, 索引: ${nextIndex + 1}/${favoriteVideos.value.length}`)
          currentVideoIndex.value = nextIndex
          const nextVideo = favoriteVideos.value[nextIndex]
          if (nextVideo) {
            currentVideoTitle.value = nextVideo.title
            currentVideoCover.value = nextVideo.cover || props.videoInfo.cover
          }
        }
      }, 300)
    }
    return
  }

  // 检查是否为"下载完成！"
  if (latestLog.includes('INFO 下载完成！')) {
    console.log('检测到视频下载完成')
    // 这里不做处理，等待"合并完成"的消息
    return
  }
}, { deep: true })

// 辅助函数：尝试搜索视频封面
const trySearchCover = async (videoTitle) => {
  if (!videoTitle) return

  // 此函数不再实际执行搜索操作，只记录日志
  console.log('UP主投稿模式-图片加载失败，使用原始封面:', currentVideoCover.value)
}

// 监听 show 变化
watch(() => props.show, async (isVisible) => {
  if (isVisible) {
    // 输出调试信息
    console.log('DownloadDialog 弹窗打开，接收到的视频信息:', JSON.stringify(props.videoInfo, null, 2))

    // 初始化
    currentVideoTitle.value = props.videoInfo.title
    currentVideoCover.value = props.videoInfo.pic || props.videoInfo.cover
    currentVideoAuthor.value = props.videoInfo.author || ''
    currentVideoBvid.value = props.videoInfo.bvid || ''
    console.log('设置封面图片路径:', currentVideoCover.value)
    videoTitles.value = []
    currentVideoIndex.value = -1
    favoriteVideos.value = []

    // 如果是收藏夹，预加载收藏夹内容
    if (isFavoriteFolder.value && props.videoInfo.fid) {
      await preloadFavoriteVideos()
    }

    // 在弹窗打开时检查 FFmpeg
    checkFFmpegStatus()

    // 根据传入的默认开关设置仅下载音频
    if (props.defaultOnlyAudio) {
      onlyAudio.value = true
    }
  }
})

// 重置状态
const resetState = () => {
  downloadStarted.value = false
  isDownloading.value = false
  downloadError.value = false
  downloadLogs.value = []
  currentVideoTitle.value = props.videoInfo.title
  currentVideoCover.value = props.videoInfo.pic || props.videoInfo.cover
  currentVideoAuthor.value = props.videoInfo.author || ''
  currentVideoBvid.value = props.videoInfo.bvid || ''
  videoTitles.value = []
  currentVideoIndex.value = -1
  favoriteVideos.value = []
  // 重置高级选项的显示状态
  showAdvancedOptions.value = true

  // 重置高级选项
  advancedOptions.value = {
    // 基础参数
    video_quality: null,
    audio_quality: null,
    vcodec: null,
    acodec: null,
    download_vcodec_priority: null,
    output_format: null,
    output_format_audio_only: null,

    // 资源选择参数
    video_only: false,
    danmaku_only: false,
    no_danmaku: false,
    subtitle_only: false,
    no_subtitle: false,
    with_metadata: false,
    metadata_only: false,
    no_cover: false,
    save_cover: false,
    cover_only: false,
    no_chapter_info: false,
  }
}

// 显示下载完成通知
const showDownloadCompleteNotify = () => {
  showNotify({
    type: 'success',
    message: '下载已完成',
    position: 'top',
    duration: 2000,
    teleport: '.notification-container',
  })
}

// 开始下载
const startDownload = async () => {
  try {
    // 如果 FFmpeg 未安装，显示错误提示
    if (ffmpegStatus.value && !ffmpegStatus.value.installed) {
      downloadLogs.value.push('ERROR: FFmpeg 未安装，请先安装 FFmpeg')
      downloadError.value = true
      return
    }

    // 重置状态
    downloadStarted.value = true
    isDownloading.value = true
    downloadError.value = false
    downloadLogs.value = []

    // 隐藏高级选项，让日志显示在更靠上的位置
    showAdvancedOptions.value = false

    // 首次显示正在使用预加载的视频
    if (isFavoriteFolder.value && favoriteVideos.value.length > 0) {
      downloadLogs.value.push(`INFO 将使用预加载的 ${favoriteVideos.value.length} 个视频信息进行下载`)

      // 立即设置第一个视频的信息
      currentVideoIndex.value = 0
      const firstVideo = favoriteVideos.value[0]
      if (firstVideo) {
        currentVideoTitle.value = firstVideo.title
        currentVideoCover.value = firstVideo.cover || props.videoInfo.cover
      }
    } else {
      // 设置当前视频信息
      currentVideoTitle.value = props.videoInfo.title
      currentVideoCover.value = props.videoInfo.pic || props.videoInfo.cover
    }

    // 检查是否是用户视频下载请求
    if (props.videoInfo.is_user_videos) {
      // 使用传入的UP主视频列表
      if (props.upUserVideos && props.upUserVideos.length > 0) {
        console.log('使用预加载的UP主视频列表:', props.upUserVideos.length)
        favoriteVideos.value = props.upUserVideos.map(video => ({
          title: video.title || '',
          cover: video.pic || '',
          bvid: video.bvid || '',
          author: video.author || '',
        }))
      }

      // 发起用户视频下载请求并处理实时消息
      await downloadUserVideos({
        user_id: props.videoInfo.user_id,
        download_cover: downloadCover.value,
        only_audio: onlyAudio.value,
        // 添加高级选项
        ...advancedOptions.value,
      }, (content) => {
        console.log('收到用户视频下载消息:', content)
        downloadLogs.value.push(content)

        // 检查是否为视频标题信息 [n/5] 视频标题
        const upVideoTitleMatch = content.match(/\[(\d+)\/(\d+)\]\s+(.+)/)
        if (upVideoTitleMatch) {
          const index = parseInt(upVideoTitleMatch[1], 10) - 1 // 索引从0开始
          const total = parseInt(upVideoTitleMatch[2], 10)
          const videoTitle = upVideoTitleMatch[3].trim()
          console.log('检测到UP主视频标题:', videoTitle, `${index + 1}/${total}`)
          currentVideoTitle.value = videoTitle

          // 尝试从预加载的视频列表中找到匹配的视频以获取封面
          if (favoriteVideos.value.length > 0) {
            // 尝试使用索引直接获取
            if (index >= 0 && index < favoriteVideos.value.length) {
              const matchedVideo = favoriteVideos.value[index]
              if (matchedVideo && matchedVideo.cover) {
                console.log('找到匹配视频:', matchedVideo.title)
                console.log('更新视频封面:', matchedVideo.cover)
                currentVideoCover.value = matchedVideo.cover
                currentVideoIndex.value = index
              }
            } else {
              // 如果索引无效，尝试通过标题匹配
              const videoByTitle = favoriteVideos.value.find(v => v.title === videoTitle)
              if (videoByTitle && videoByTitle.cover) {
                console.log('通过标题找到匹配视频:', videoByTitle.title)
                console.log('更新视频封面:', videoByTitle.cover)
                currentVideoCover.value = videoByTitle.cover
                currentVideoIndex.value = favoriteVideos.value.indexOf(videoByTitle)
              }
            }
          }
        }

        // 检查是否为"开始处理视频"
        const processingMatch = content.match(/INFO\s+开始处理视频\s+(.+)/)
        if (processingMatch) {
          const videoTitle = processingMatch[1].trim()
          console.log('检测到开始处理UP主视频:', videoTitle)
          currentVideoTitle.value = videoTitle

          // 尝试从预加载的视频列表中找到匹配的视频以获取封面
          if (favoriteVideos.value.length > 0) {
            const videoByTitle = favoriteVideos.value.find(v => v.title === videoTitle)
            if (videoByTitle && videoByTitle.cover) {
              console.log('根据处理信息找到匹配视频:', videoByTitle.title)
              console.log('更新视频封面:', videoByTitle.cover)
              currentVideoCover.value = videoByTitle.cover
              currentVideoIndex.value = favoriteVideos.value.indexOf(videoByTitle)
            }
          }
        }

        // 检查下载状态
        if (content.includes('下载完成') && !content.includes('INFO')) {
          isDownloading.value = false
          // 显示下载完成通知
          showDownloadCompleteNotify()
          emit('download-complete')
        } else if (content.includes('ERROR')) {
          downloadError.value = true
          isDownloading.value = false
        }

        // 自动滚动到底部
        nextTick(() => {
          scrollToBottom()
        })
      })
    }
    // 检查是否是收藏夹下载请求
    else if (props.videoInfo.is_favorite_folder) {
      // 发起收藏夹下载请求并处理实时消息
      await downloadFavorites({
        user_id: props.videoInfo.user_id,
        fid: props.videoInfo.fid,
        download_cover: downloadCover.value,
        only_audio: onlyAudio.value,
        // 添加高级选项
        ...advancedOptions.value,
      }, (content) => {
        console.log('收到收藏夹下载消息:', content)
        downloadLogs.value.push(content)

        // 检查下载状态
        if (content.includes('下载完成') && !content.includes('INFO')) {
          isDownloading.value = false
          // 显示下载完成通知
          showDownloadCompleteNotify()
          emit('download-complete')
        } else if (content.includes('ERROR')) {
          downloadError.value = true
          isDownloading.value = false
        }

        // 自动滚动到底部
        nextTick(() => {
          scrollToBottom()
        })
      })
    } else if (props.isBatchDownload && props.batchVideos.length > 0) {
      // 批量下载多个视频
      downloadLogs.value.push(`INFO 开始批量下载，共 ${props.batchVideos.length} 个视频`)

      // 设置初始视频信息
      if (props.batchVideos.length > 0 && props.currentVideoIndex < props.batchVideos.length) {
        const currentVideo = props.batchVideos[props.currentVideoIndex]
        currentVideoTitle.value = currentVideo.title || currentVideo.bvid
        currentVideoCover.value = currentVideo.cover || props.videoInfo.cover
        currentVideoAuthor.value = currentVideo.author || props.videoInfo.author || ''
        currentVideoBvid.value = currentVideo.bvid || props.videoInfo.bvid || ''
      }

      // 发起批量下载请求
      await batchDownloadVideos({
        videos: props.batchVideos,
        download_cover: downloadCover.value,
        only_audio: onlyAudio.value,
        // 添加高级选项
        ...advancedOptions.value,
      }, (content) => {
        console.log('收到批量下载消息:', content)
        downloadLogs.value.push(content)

        // 检查是否包含当前下载的视频信息
        const currentVideoMatch = content.match(/正在下载第\s+(\d+)\/(\d+)\s+个视频:\s+(.+)/)
        if (currentVideoMatch) {
          const index = parseInt(currentVideoMatch[1], 10) - 1
          const total = parseInt(currentVideoMatch[2], 10)
          const title = currentVideoMatch[3].trim()

          console.log(`正在下载第 ${index + 1}/${total} 个视频: ${title}`)

          // 更新当前视频信息
          if (index >= 0 && index < props.batchVideos.length) {
            currentVideoIndex.value = index
            currentVideoTitle.value = title
            const video = props.batchVideos[index]
            if (video) {
              if (video.cover) {
                currentVideoCover.value = video.cover
              }
              if (video.author) {
                currentVideoAuthor.value = video.author
              }
              if (video.bvid) {
                currentVideoBvid.value = video.bvid
              }
            }
            // 通知父组件当前视频索引已更新
            emit('update:currentVideoIndex', index)
          }
        }

        // 检查下载状态
        if (content.includes('批量下载完成') || (content.includes('下载完成') && !content.includes('INFO'))) {
          isDownloading.value = false
          // 显示下载完成通知
          showDownloadCompleteNotify()
          emit('download-complete')
        } else if (content.includes('ERROR')) {
          downloadError.value = true
          isDownloading.value = false
        }

        // 自动滚动到底部
        nextTick(() => {
          scrollToBottom()
        })
      })
    } else if (props.videoInfo.is_collection_download) {
      // 合集下载
      console.log('开始合集下载:', props.videoInfo)

      await downloadCollection({
        url: props.videoInfo.original_url,
        cid: props.videoInfo.cid,
        download_cover: downloadCover.value,
        only_audio: onlyAudio.value,
        // 添加高级选项
        ...advancedOptions.value,
      }, (content) => {
        console.log('收到合集下载消息:', content)
        downloadLogs.value.push(content)

        // 检查下载状态
        if (content.includes('下载完成')) {
          isDownloading.value = false
          // 显示下载完成通知
          showDownloadCompleteNotify()
          emit('download-complete')
        } else if (content.includes('ERROR')) {
          downloadError.value = true
          isDownloading.value = false
        }

        // 自动滚动到底部
        nextTick(() => {
          scrollToBottom()
        })
      })
    } else {
      // 发起单个视频下载请求并处理实时消息
      await downloadVideo(
        props.videoInfo.bvid,
        null,
        (content) => {
          console.log('收到消息:', content)
          downloadLogs.value.push(content)

          // 检查下载状态
          if (content.includes('下载完成')) {
            isDownloading.value = false
            // 显示下载完成通知
            showDownloadCompleteNotify()
            emit('download-complete')
          } else if (content.includes('ERROR')) {
            downloadError.value = true
            isDownloading.value = false
          }

          // 自动滚动到底部
          nextTick(() => {
            scrollToBottom()
          })
        },
        downloadCover.value,
        onlyAudio.value,
        props.videoInfo.cid,
        // 添加高级选项
        advancedOptions.value,
      )
    }
  } catch (error) {
    console.error('下载失败:', error)
    downloadError.value = true
    isDownloading.value = false
    const errorLines = error.message.split('\n')
    for (const line of errorLines) {
      downloadLogs.value.push(`ERROR: ${line}`)
    }
  }
}

// 滚动到底部的优化实现
const scrollToBottom = () => {
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
}

// 监听日志变化
watch(() => downloadLogs.value.length, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

// 处理关闭弹窗
const handleClose = () => {
  if (isDownloading.value) {
    if (!confirm('下载正在进行中，确定要关闭吗？')) {
      return
    }
  }

  // 如果下载已完成且没有错误，触发下载完成事件
  if (downloadStarted.value && !isDownloading.value && !downloadError.value) {
    emit('download-complete')
  }

  emit('update:show', false)
  // 重置状态
  resetState()
}

// 监听show变化
watch(() => props.show, (newVal) => {
  if (!newVal) {
    handleClose()
  } else {
    // 在弹窗打开时检查 FFmpeg
    checkFFmpegStatus()
    // 初始化当前视频标题和封面
    currentVideoTitle.value = props.videoInfo.title
    currentVideoCover.value = props.videoInfo.pic || props.videoInfo.cover
  }
})

// 组件卸载时清理
onUnmounted(() => {
  // 重置状态
  resetState()
})

// 复制到剪贴板函数
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showNotify({
      type: 'success',
      message: '命令已复制到剪贴板',
      position: 'top',
      duration: 2000,
      teleport: '.notification-container',
    })
  } catch (err) {
    console.error('复制失败:', err)
    showNotify({
      type: 'danger',
      message: '复制失败，请手动复制',
      position: 'top',
      duration: 2000,
      teleport: '.notification-container',
    })
  }
}

// 处理安装指南的行
const installGuideLines = computed(() => {
  if (!ffmpegStatus.value?.install_guide) return []
  return ffmpegStatus.value.install_guide.split('\n').filter(line => line.trim())
})

// 判断是否为命令行
const isCommand = (line) => {
  return line.trim().startsWith('yum') ||
    line.trim().startsWith('sudo') ||
    line.trim().startsWith('apt') ||
    line.trim().startsWith('brew')
}

// 获取命令内容
const getCommandContent = (line) => {
  return line.trim()
}

// 下拉菜单选项定义
const videoQualityOptions = [
  { label: '默认', value: null },
  { label: '127: 8K 超高清', value: '127' },
  { label: '126: 杜比视界', value: '126' },
  { label: '125: HDR 真彩', value: '125' },
  { label: '120: 4K 超清', value: '120' },
  { label: '116: 1080P 60帧', value: '116' },
  { label: '112: 1080P 高码率', value: '112' },
  { label: '100: 智能修复', value: '100' },
  { label: '80: 1080P 高清', value: '80' },
  { label: '74: 720P 60帧', value: '74' },
  { label: '64: 720P 高清', value: '64' },
  { label: '32: 480P 清晰', value: '32' },
  { label: '16: 360P 流畅', value: '16' },
]

const audioQualityOptions = [
  { label: '默认', value: null },
  { label: '30251: Hi-Res', value: '30251' },
  { label: '30255: 杜比音效', value: '30255' },
  { label: '30250: 杜比全景声', value: '30250' },
  { label: '30280: 320kbps', value: '30280' },
  { label: '30232: 128kbps', value: '30232' },
  { label: '30216: 64kbps', value: '30216' },
]

const vcodecOptions = [
  { label: '默认 (avc:copy)', value: null },
  { label: '下载AVC(H.264):直接复制', value: 'avc:copy' },
  { label: '下载HEVC(H.265):直接复制', value: 'hevc:copy' },
  { label: '下载AV1:直接复制', value: 'av1:copy' },
  { label: '下载AVC(H.264):转码为H.264', value: 'avc:h264' },
  { label: '下载HEVC(H.265):转码为H.265', value: 'hevc:hevc' },
  { label: '下载AV1:转码为AV1', value: 'av1:av1' },
]

const acodecOptions = [
  { label: '默认 (mp4a:copy)', value: null },
  { label: '下载MP4A:直接复制', value: 'mp4a:copy' },
  { label: '下载MP4A:转码为AAC', value: 'mp4a:aac' },
  { label: '下载MP4A:转码为MP3', value: 'mp4a:mp3' },
  { label: '下载MP4A:转码为FLAC', value: 'mp4a:flac' },
]

const outputFormatOptions = [
  { label: '默认', value: null },
  { label: '自动推断', value: 'infer' },
  { label: 'MP4', value: 'mp4' },
  { label: 'MKV', value: 'mkv' },
  { label: 'MOV', value: 'mov' },
]

const audioOutputFormatOptions = [
  { label: '默认', value: null },
  { label: '自动推断', value: 'infer' },
  { label: 'M4A', value: 'm4a' },
  { label: 'AAC', value: 'aac' },
  { label: 'MP3', value: 'mp3' },
  { label: 'FLAC', value: 'flac' },
]

// 获取选项文本的方法
const getVideoQualityText = (value) => {
  const option = videoQualityOptions.find(opt => opt.value === value)
  return option ? option.label : '默认'
}

const getAudioQualityText = (value) => {
  const option = audioQualityOptions.find(opt => opt.value === value)
  return option ? option.label : '默认'
}

const getVcodecText = (value) => {
  const option = vcodecOptions.find(opt => opt.value === value)
  return option ? option.label : '默认'
}

const getAcodecText = (value) => {
  const option = acodecOptions.find(opt => opt.value === value)
  return option ? option.label : '默认'
}

const getOutputFormatText = (value) => {
  const option = outputFormatOptions.find(opt => opt.value === value)
  return option ? option.label : '默认'
}

const getAudioOutputFormatText = (value) => {
  const option = audioOutputFormatOptions.find(opt => opt.value === value)
  return option ? option.label : '默认'
}
</script>

<style scoped>
/* 当弹窗显示时禁用页面滚动 */
:global(body) {
  overflow: hidden;
}
</style>
