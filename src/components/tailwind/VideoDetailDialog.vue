<template>
  <van-dialog
    :show="dialogVisible"
    @update:show="updateVisible"
    :title="video?.title || '视频详情'"
    class="video-detail-dialog"
    close-on-click-overlay
    :show-confirm-button="false"
    :style="{ width: '1000px', maxWidth: '90%', position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', borderRadius: '0.5rem', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)' }"
  >
    <div v-if="video" class="p-4 overflow-y-auto bg-transparent" style="height: 600px">
      <!-- 视频基础信息 -->
      <div class="flex flex-col md:flex-row gap-3">
        <!-- 左侧：视频封面 -->
        <div class="md:w-[30%] flex-shrink-0">
          <div class="relative w-full h-28 md:h-32 rounded-lg overflow-hidden">
            <img
              :src="normalizeImageUrl(video.cover || video.covers?.[0])"
              class="w-full h-full object-cover"
              :class="{ 'blur-md': isPrivacyMode }"
              alt="视频封面"
            />
            <!-- 视频时长 -->
            <div class="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
              {{ formatDuration(video.duration) }}
            </div>

            <!-- 进度条 -->
            <div v-if="video.business !== 'article-list' && video.business !== 'article' && video.business !== 'live'"
                 class="absolute bottom-0 left-0 w-full h-1 bg-gray-700/50">
              <div
                class="h-full bg-[#FF6699]"
                :style="{ width: getProgressWidth(video.progress, video.duration) }">
              </div>
            </div>
          </div>

          

          <!-- 视频下载信息 -->
          <div v-if="isVideoDownloaded && downloadedFiles.length > 0" class="mt-3">
            <div class="text-xs text-gray-500 dark:text-gray-400 p-2 bg-pink-50 dark:bg-pink-900/20 rounded-lg">
              <div class="flex items-center mb-1">
                <svg class="w-3 h-3 text-[#fb7299] mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <span class="font-medium text-[#fb7299]">视频已下载</span>
              </div>
              <div v-for="(file, index) in downloadedFiles" :key="index" class="ml-4 truncate" :title="file.file_path">
                {{ file.file_name }} ({{ file.size_mb.toFixed(1) }} MB)
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：视频详情 -->
        <div class="md:w-[70%]">

          <!-- 视频信息 -->
          <div class="space-y-2 text-xs flex flex-col h-28 md:h-32 min-h-0">
            <!-- UP主信息 + 检测信息并排显示 -->
            <div v-if="video.business !== 'cheese' && video.business !== 'pgc'"
                 class="flex items-center space-x-2"
                 @click.stop>
              <div class="flex-shrink-0">
                <img
                  :src="normalizeImageUrl(video.author_face)"
                  alt="author"
                  class="h-7 w-7 cursor-pointer rounded-full transition-all duration-300 hover:scale-110"
                  :class="{ 'blur-md': isPrivacyMode }"
                  @click="openAuthorPage"
                  :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${video.author_name} 的个人空间`"
                />
              </div>
              <div class="flex-1 min-w-0">
                <p
                  class="cursor-pointer text-gray-800 dark:text-gray-200 transition-colors hover:text-[#FF6699]"
                  @click="openAuthorPage"
                  :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${video.author_name} 的个人空间`"
                  v-html="isPrivacyMode ? '******' : video.author_name"
                ></p>
                <p class="text-xs text-gray-500 dark:text-gray-400">UP主</p>
              </div>
              <div class="flex items-center space-x-2 ml-auto">
                <EnvironmentCheck inline compact />
                <div class="hidden sm:block h-4 w-px bg-gray-200 dark:bg-gray-700"></div>
                <!-- DeepSeek 余额（紧凑显示） -->
                <div class="flex items-center space-x-1 text-[11px] text-gray-600">
                  <svg class="w-3.5 h-3.5 text-[#4D6BFE]" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M27.501 8.46875C27.249 8.3457 27.1406 8.58008 26.9932 8.69922C26.9434 8.73828 26.9004 8.78906 26.8584 8.83398C26.4902 9.22852 26.0605 9.48633 25.5 9.45508C24.6787 9.41016 23.9785 9.66797 23.3594 10.2969C23.2275 9.52148 22.79 9.05859 22.125 8.76172C21.7764 8.60742 21.4238 8.45312 21.1807 8.11719C21.0098 7.87891 20.9639 7.61328 20.8779 7.35156C20.8242 7.19336 20.7695 7.03125 20.5879 7.00391C20.3906 6.97266 20.3135 7.13867 20.2363 7.27734C19.9258 7.84375 19.8066 8.46875 19.8174 9.10156C19.8447 10.5234 20.4453 11.6562 21.6367 12.4629C21.7725 12.5547 21.8076 12.6484 21.7646 12.7832C21.6836 13.0605 21.5869 13.3301 21.501 13.6074C21.4473 13.7852 21.3662 13.8242 21.1768 13.7461C20.5225 13.4727 19.957 13.0684 19.458 12.5781C18.6104 11.7578 17.8438 10.8516 16.8877 10.1426C16.6631 9.97656 16.4395 9.82227 16.207 9.67578C15.2314 8.72656 16.335 7.94727 16.5898 7.85547C16.8574 7.75977 16.6826 7.42773 15.8193 7.43164C14.957 7.43555 14.167 7.72461 13.1611 8.10938C13.0137 8.16797 12.8594 8.21094 12.7002 8.24414C11.7871 8.07227 10.8389 8.0332 9.84766 8.14453C7.98242 8.35352 6.49219 9.23633 5.39648 10.7441C4.08105 12.5547 3.77148 14.6133 4.15039 16.7617C4.54883 19.0234 5.70215 20.8984 7.47559 22.3633C9.31348 23.8809 11.4307 24.625 13.8457 24.4824C15.3125 24.3984 16.9463 24.2012 18.7881 22.6406C19.2529 22.8711 19.7402 22.9629 20.5498 23.0332C21.1729 23.0918 21.7725 23.002 22.2373 22.9062C22.9648 22.752 22.9141 22.0781 22.6514 21.9531C20.5186 20.959 20.9863 21.3633 20.5605 21.0371C21.6445 19.752 23.2783 18.418 23.917 14.0977C23.9668 13.7539 23.9238 13.5391 23.917 13.2598C23.9131 13.0918 23.9512 13.0254 24.1445 13.0059C24.6787 12.9453 25.1973 12.7988 25.6738 12.5352C27.0557 11.7793 27.6123 10.5391 27.7441 9.05078C27.7637 8.82422 27.7402 8.58789 27.501 8.46875ZM15.46 21.8613C13.3926 20.2344 12.3906 19.6992 11.9766 19.7227C11.5898 19.7441 11.6592 20.1875 11.7441 20.4766C11.833 20.7617 11.9492 20.959 12.1123 21.209C12.2246 21.375 12.3018 21.623 12 21.8066C11.334 22.2207 10.1768 21.668 10.1221 21.6406C8.77539 20.8477 7.64941 19.7988 6.85547 18.3652C6.08984 16.9844 5.64453 15.5039 5.57129 13.9238C5.55176 13.541 5.66406 13.4062 6.04297 13.3379C6.54199 13.2461 7.05762 13.2266 7.55664 13.2988C9.66602 13.6074 11.4619 14.5527 12.9668 16.0469C13.8262 16.9004 14.4766 17.918 15.1465 18.9121C15.8584 19.9688 16.625 20.9746 17.6006 21.7988C17.9443 22.0879 18.2197 22.3086 18.4824 22.4707C17.6895 22.5586 16.3652 22.5781 15.46 21.8613ZM16.4502 15.4805C16.4502 15.3105 16.5859 15.1758 16.7568 15.1758C16.7949 15.1758 16.8301 15.1836 16.8613 15.1953C16.9033 15.2109 16.9424 15.2344 16.9727 15.2695C17.0273 15.3223 17.0586 15.4004 17.0586 15.4805C17.0586 15.6504 16.9229 15.7852 16.7529 15.7852C16.582 15.7852 16.4502 15.6504 16.4502 15.4805ZM19.5273 17.0625C19.3301 17.1426 19.1328 17.2129 18.9434 17.2207C18.6494 17.2344 18.3281 17.1152 18.1533 16.9688C17.8828 16.7422 17.6895 16.6152 17.6074 16.2168C17.5732 16.0469 17.5928 15.7852 17.623 15.6348C17.6934 15.3105 17.6152 15.1035 17.3877 14.9141C17.2012 14.7598 16.9658 14.7188 16.7061 14.7188C16.6094 14.7188 16.5205 14.6758 16.4541 14.6406C16.3457 14.5859 16.2568 14.4512 16.3418 14.2852C16.3691 14.2324 16.501 14.1016 16.5322 14.0781C16.8838 13.877 17.29 13.9434 17.666 14.0938C18.0146 14.2363 18.2773 14.498 18.6562 14.8672C19.0439 15.3145 19.1133 15.4395 19.334 15.7734C19.5078 16.0371 19.667 16.3066 19.7754 16.6152C19.8408 16.8066 19.7559 16.9648 19.5273 17.0625Z" fill="#4D6BFE" />
                  </svg>
                  <div v-if="deepseekBalance.is_available" class="text-[11px]">
                    <span class="text-gray-500">余额:</span>
                    <span class="font-medium text-[#4D6BFE]">{{ deepseekBalance.balance_infos[0]?.total_balance || '0.00' }}</span>
                    <span class="text-gray-500">{{ deepseekBalance.balance_infos[0]?.currency }}</span>
                  </div>
                  <button @click="refreshDeepSeekBalance" class="p-0.5 text-[#4D6BFE] hover:bg-[#4D6BFE]/10 rounded-full transition-colors duration-200" :title="deepseekBalance.is_available ? '刷新余额' : '点击查询余额'">
                    <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </button>
                </div>
              </div>
              
            </div>

            <!-- 视频分区/观看时间/设备 行已按需求去除 -->

            <!-- 备注 -->
            <div class="mt-2 flex-1 flex flex-col min-h-0">
              <textarea
                v-model="remarkContent"
                @blur="handleRemarkBlur"
                :disabled="isPrivacyMode"
                placeholder="添加备注..."
                rows="2"
                class="w-full flex-1 resize-none px-2 py-1.5 text-xs text-gray-800 dark:text-gray-200 bg-gray-50 dark:bg-gray-700 rounded border border-gray-200 dark:border-gray-600 focus:border-[#fb7299] focus:ring-[#fb7299] transition-colors duration-200"
                :class="{ 'blur-sm': isPrivacyMode }"
              ></textarea>
              <div v-if="remarkTime" class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                上次编辑: {{ formatRemarkTime(remarkTime) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 视频摘要 -->
      <div v-if="video.business === 'archive'" class="mt-6">
        <!-- 标签页 -->
        <div class="border-b border-gray-200 dark:border-gray-700">
          <nav class="flex -mb-px">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="currentTab = tab.id"
              class="px-4 py-2 text-sm font-medium border-b-2 transition-colors duration-200"
              :class="[
                currentTab === tab.id
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              {{ tab.name }}
            </button>
          </nav>
        </div>

        <!-- 标签页内容 -->
        <div class="mt-4">
          <!-- B站AI摘要 -->
          <div v-show="currentTab === 'bilibili'" class="space-y-4">
            <VideoSummary
              :key="videoSummaryKey"
              :bvid="video.bvid"
              :cid="String(video.cid)"
              :upMid="String(video.author_mid)"
            />
          </div>

          <!-- 本地摘要部分 -->
          <div v-show="currentTab === 'local'" class="space-y-6">
            <!-- 检查环境中的加载状态 -->
            <div v-if="isCheckingEnvironment" class="flex items-center justify-center p-6">
              <div class="flex flex-col items-center">
                <div
                  class="animate-spin h-10 w-10 border-4 border-[#fb7299] border-t-transparent rounded-full mb-3"></div>
                <span class="text-gray-600">正在检查系统环境...</span>
              </div>
            </div>

            <!-- 系统资源不足提示 -->
            <div v-else-if="!canRunSpeechToText"
                 class="flex items-center justify-center p-6 bg-red-50 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-lg border border-red-200 dark:border-red-800/60">
              <div class="flex flex-col items-center text-center">
                <svg class="w-12 h-12 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span class="font-medium text-lg mb-2">无法使用本地摘要功能</span>
                <span class="text-sm">{{ systemLimitationReason || '系统资源不足，无法运行语音转文字功能' }}</span>
              </div>
            </div>

            <!-- CUDA不可用提示 -->
            <div v-if="!cudaAvailable && cudaSetupGuide && showCudaGuide"
                 class="flex flex-col p-6 bg-yellow-50 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 rounded-lg border border-yellow-100 dark:border-yellow-800/60">
              <div class="flex items-center mb-4">
                <svg class="w-8 h-8 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <h3 class="font-medium text-lg">CUDA 不可用</h3>
                  <p class="text-sm">本地摘要功能可以使用，但速度会较慢。安装CUDA可以显著提升处理速度。</p>
                </div>
              </div>

              <div class="mt-2">
                <h4 class="font-medium mb-2">CUDA 安装指南</h4>
                <pre
                  class="text-xs bg-gray-100 dark:bg-gray-900 dark:text-gray-300 border border-gray-200 dark:border-gray-700 p-3 rounded-md overflow-auto max-h-60 whitespace-pre-wrap">{{ cudaSetupGuide
                  }}</pre>
              </div>

              <div class="mt-4 flex justify-end">
                <button
                  @click="showCudaGuide = false"
                  class="px-4 py-2 bg-yellow-600 text-white rounded-md text-sm hover:bg-yellow-700 transition-colors"
                >
                  我已了解，继续使用
                </button>
              </div>
            </div>

            <!-- 只有在系统资源足够且CUDA可用或用户已确认时才显示以下内容 -->
            <template v-else-if="canRunSpeechToText && (!cudaAvailable ? !showCudaGuide : true)">
              <!-- 本地摘要显示部分 -->
              <div v-if="hasLocalSummary" class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-base font-medium text-gray-900 dark:text-gray-100">本地摘要</h3>
                  <!-- DeepSeek余额显示 -->
                  <div class="flex items-center space-x-2">
                    <svg class="w-4 h-4 text-[#4D6BFE]" viewBox="0 0 30 30" fill="none"
                         xmlns="http://www.w3.org/2000/svg">
                      <path
                        d="M27.501 8.46875C27.249 8.3457 27.1406 8.58008 26.9932 8.69922C26.9434 8.73828 26.9004 8.78906 26.8584 8.83398C26.4902 9.22852 26.0605 9.48633 25.5 9.45508C24.6787 9.41016 23.9785 9.66797 23.3594 10.2969C23.2275 9.52148 22.79 9.05859 22.125 8.76172C21.7764 8.60742 21.4238 8.45312 21.1807 8.11719C21.0098 7.87891 20.9639 7.61328 20.8779 7.35156C20.8242 7.19336 20.7695 7.03125 20.5879 7.00391C20.3906 6.97266 20.3135 7.13867 20.2363 7.27734C19.9258 7.84375 19.8066 8.46875 19.8174 9.10156C19.8447 10.5234 20.4453 11.6562 21.6367 12.4629C21.7725 12.5547 21.8076 12.6484 21.7646 12.7832C21.6836 13.0605 21.5869 13.3301 21.501 13.6074C21.4473 13.7852 21.3662 13.8242 21.1768 13.7461C20.5225 13.4727 19.957 13.0684 19.458 12.5781C18.6104 11.7578 17.8438 10.8516 16.8877 10.1426C16.6631 9.97656 16.4395 9.82227 16.207 9.67578C15.2314 8.72656 16.335 7.94727 16.5898 7.85547C16.8574 7.75977 16.6826 7.42773 15.8193 7.43164C14.957 7.43555 14.167 7.72461 13.1611 8.10938C13.0137 8.16797 12.8594 8.21094 12.7002 8.24414C11.7871 8.07227 10.8389 8.0332 9.84766 8.14453C7.98242 8.35352 6.49219 9.23633 5.39648 10.7441C4.08105 12.5547 3.77148 14.6133 4.15039 16.7617C4.54883 19.0234 5.70215 20.8984 7.47559 22.3633C9.31348 23.8809 11.4307 24.625 13.8457 24.4824C15.3125 24.3984 16.9463 24.2012 18.7881 22.6406C19.2529 22.8711 19.7402 22.9629 20.5498 23.0332C21.1729 23.0918 21.7725 23.002 22.2373 22.9062C22.9648 22.752 22.9141 22.0781 22.6514 21.9531C20.5186 20.959 20.9863 21.3633 20.5605 21.0371C21.6445 19.752 23.2783 18.418 23.917 14.0977C23.9668 13.7539 23.9238 13.5391 23.917 13.2598C23.9131 13.0918 23.9512 13.0254 24.1445 13.0059C24.6787 12.9453 25.1973 12.7988 25.6738 12.5352C27.0557 11.7793 27.6123 10.5391 27.7441 9.05078C27.7637 8.82422 27.7402 8.58789 27.501 8.46875ZM15.46 21.8613C13.3926 20.2344 12.3906 19.6992 11.9766 19.7227C11.5898 19.7441 11.6592 20.1875 11.7441 20.4766C11.833 20.7617 11.9492 20.959 12.1123 21.209C12.2246 21.375 12.3018 21.623 12 21.8066C11.334 22.2207 10.1768 21.668 10.1221 21.6406C8.77539 20.8477 7.64941 19.7988 6.85547 18.3652C6.08984 16.9844 5.64453 15.5039 5.57129 13.9238C5.55176 13.541 5.66406 13.4062 6.04297 13.3379C6.54199 13.2461 7.05762 13.2266 7.55664 13.2988C9.66602 13.6074 11.4619 14.5527 12.9668 16.0469C13.8262 16.9004 14.4766 17.918 15.1465 18.9121C15.8584 19.9688 16.625 20.9746 17.6006 21.7988C17.9443 22.0879 18.2197 22.3086 18.4824 22.4707C17.6895 22.5586 16.3652 22.5781 15.46 21.8613ZM16.4502 15.4805C16.4502 15.3105 16.5859 15.1758 16.7568 15.1758C16.7949 15.1758 16.8301 15.1836 16.8613 15.1953C16.9033 15.2109 16.9424 15.2344 16.9727 15.2695C17.0273 15.3223 17.0586 15.4004 17.0586 15.4805C17.0586 15.6504 16.9229 15.7852 16.7529 15.7852C16.582 15.7852 16.4502 15.6504 16.4502 15.4805ZM19.5273 17.0625C19.3301 17.1426 19.1328 17.2129 18.9434 17.2207C18.6494 17.2344 18.3281 17.1152 18.1533 16.9688C17.8828 16.7422 17.6895 16.6152 17.6074 16.2168C17.5732 16.0469 17.5928 15.7852 17.623 15.6348C17.6934 15.3105 17.6152 15.1035 17.3877 14.9141C17.2012 14.7598 16.9658 14.7188 16.7061 14.7188C16.6094 14.7188 16.5205 14.6758 16.4541 14.6406C16.3457 14.5859 16.2568 14.4512 16.3418 14.2852C16.3691 14.2324 16.501 14.1016 16.5322 14.0781C16.8838 13.877 17.29 13.9434 17.666 14.0938C18.0146 14.2363 18.2773 14.498 18.6562 14.8672C19.0439 15.3145 19.1133 15.4395 19.334 15.7734C19.5078 16.0371 19.667 16.3066 19.7754 16.6152C19.8408 16.8066 19.7559 16.9648 19.5273 17.0625Z"
                        fill="#4D6BFE" />
                    </svg>
                    <div v-if="deepseekBalance.is_available" class="text-xs">
                      <span class="text-gray-500">余额:</span>
                      <span
                        class="font-medium text-[#4D6BFE]">{{ deepseekBalance.balance_infos[0]?.total_balance || '0.00'
                        }}</span>
                      <span class="text-gray-500">{{ deepseekBalance.balance_infos[0]?.currency }}</span>
                    </div>
                    <button
                      @click="refreshDeepSeekBalance"
                      class="p-1 text-[#4D6BFE] hover:bg-[#4D6BFE]/10 rounded-full transition-colors duration-200"
                      :title="deepseekBalance.is_available ? '刷新余额' : '点击查询余额'"
                    >
                      <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- 处理信息和Token信息 -->
                <div class="mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div class="text-xs text-gray-500 dark:text-gray-400 space-y-2">
                    <p>处理用时：{{ Math.round(localSummaryData?.processing_time || 0) }}秒</p>
                    <p>使用模型：{{ localSummaryData?.from_deepseek ? 'DeepSeek' : 'GPT' }}</p>
                    <div class="border-t border-gray-200 my-2 pt-2">
                      <p class="font-medium mb-1">Token 使用统计：</p>
                      <p>• 提示词：{{ localSummaryData?.tokens_used?.prompt_tokens || 0 }} tokens</p>
                      <p>• 生成内容：{{ localSummaryData?.tokens_used?.completion_tokens || 0 }} tokens</p>
                      <p>• 总计：{{ localSummaryData?.tokens_used?.total_tokens || 0 }} tokens</p>
                      <p v-if="localSummaryData?.tokens_used?.prompt_tokens_details?.cached_tokens">
                        • 命中缓存：{{ localSummaryData?.tokens_used?.prompt_tokens_details?.cached_tokens }} tokens
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 摘要内容 -->
                <div class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-line">
                  <div v-if="localSummaryData?.summary" class="space-y-4">
                    <template v-for="(section, index) in localSummaryData.summary.split('\n')" :key="index">
                      <div v-if="hasTimeStamp(section)"
                           class="cursor-pointer hover:bg-[#fb7299]/10 hover:text-[#fb7299] transition-colors duration-200 px-2 py-1 rounded"
                           @click="handleTimeClick(section)">
                        <span class="text-[#fb7299]">{{ extractTimeStamp(section) }}</span>
                        <span>{{ section.replace(extractTimeStamp(section), '') }}</span>
                      </div>
                      <div v-else>{{ section }}</div>
                    </template>
                  </div>
                </div>
              </div>

              <!-- 音频文件状态检查 -->
              <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
                <div class="flex items-start justify-between">
                  <div class="flex items-start space-x-2">
                    <div v-if="isCheckingAudio" class="flex items-center space-x-2 text-gray-500 dark:text-gray-400">
                      <div
                        class="animate-spin h-4 w-4 border-2 border-gray-300 border-t-transparent rounded-full"></div>
                      <span>正在检查音频文件...</span>
                    </div>
                    <template v-else>
                      <div v-if="audioPath" class="flex-1">
                        <div class="flex items-center space-x-2">
                          <svg class="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                          </svg>
                          <span class="text-sm font-medium text-gray-900 dark:text-gray-100">已找到音频文件</span>
                        </div>
                        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400 break-all">{{ audioPath }}</p>
                      </div>
                      <div v-else class="flex-1">
                        <div class="flex items-center space-x-2">
                          <svg class="w-5 h-5 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                          </svg>
                          <span class="text-sm font-medium text-gray-900 dark:text-gray-100">未找到音频文件</span>
                        </div>
                        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">请下载音频文件</p>
                      </div>
                    </template>
                  </div>
                  <!-- 下载按钮 -->
                  <button
                    v-if="!audioPath && !isCheckingAudio"
                    @click="handleShowDownload"
                    class="px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-md hover:bg-[#fb7299]/90"
                  >
                    下载音频
                  </button>
                </div>

                <!-- 已存在的转录文件信息 -->
                <div v-if="hasExistingStt" class="mt-4 border-t pt-4">
                  <div class="flex items-center space-x-2">
                    <svg class="w-5 h-5 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span class="text-sm font-medium text-gray-900">已找到转录文件</span>
                  </div>
                  <p v-if="sttFilePath" class="mt-1 text-xs text-gray-500 break-all">{{ sttFilePath }}</p>
                </div>
              </div>

              <!-- 转录状态和结果横幅 -->
              <div
                v-if="transcriptionStatus && (isTranscribing || transcriptionResult || transcriptionStatus !== '音频文件已找到，可以开始转录')"
                class="rounded-lg p-4" :class="{
                'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-900/30': isTranscribing,
                'bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-900/30': transcriptionResult && !isTranscribing,
                'bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700': !transcriptionResult && !isTranscribing
              }">
                <div class="flex items-center space-x-3">
                  <div v-if="isTranscribing" class="flex-shrink-0">
                    <svg class="animate-spin h-5 w-5 text-blue-500" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor"
                            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  </div>
                  <div v-else-if="transcriptionResult" class="flex-shrink-0">
                    <svg class="h-5 w-5 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                  <div class="flex-1">
                    <p class="text-sm font-medium" :class="{
                      'text-blue-700 dark:text-blue-300': isTranscribing,
                      'text-green-700 dark:text-green-300': transcriptionResult && !isTranscribing,
                      'text-gray-700 dark:text-gray-300': !transcriptionResult && !isTranscribing
                    }">{{ transcriptionStatus }}</p>

                    <div v-if="transcriptionResult && !isTranscribing" class="mt-2 grid grid-cols-3 gap-4">
                      <div class="text-xs text-gray-600">
                        <span class="font-medium">视频时长：</span>
                        {{ formatDuration(transcriptionResult.duration) }}
                      </div>
                      <div class="text-xs text-gray-600">
                        <span class="font-medium">处理用时：</span>
                        {{ Math.round(transcriptionResult.processingTime) }}秒
                      </div>
                      <div class="text-xs text-gray-600">
                        <span class="font-medium">检测语言：</span>
                        {{ transcriptionResult.languageDetected === 'zh' ? '中文' : '英文' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 生成摘要按钮和状态 -->
              <div v-if="!isTranscribing && (hasExistingStt || transcriptionResult)">
                <button
                  @click="startGeneratingSummary"
                  :disabled="isSummarizing"
                  class="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-md hover:bg-[#fb7299]/90 disabled:opacity-50"
                >
                  <svg v-if="isSummarizing" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none"
                       viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isSummarizing ? '正在生成摘要...' : '生成摘要' }}
                </button>
                <p v-if="isSummarizing" class="mt-2 text-sm text-gray-500 text-center">
                  正在使用AI分析视频内容，请稍候...
                </p>
              </div>

              <!-- 模型选择部分 -->
              <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
                <div class="flex items-center justify-between mb-2">
                  <h4 class="text-base font-medium text-gray-900 dark:text-gray-100">选择语音识别模型</h4>
                  <button
                    @click="startTranscription"
                    :disabled="!selectedModel || !selectedModel.is_downloaded || isTranscribing"
                    class="px-3 py-1.5 text-xs md:text-sm font-medium text-white rounded-md hover:bg-[#fb7299]/90 disabled:opacity-50 disabled:cursor-not-allowed"
                    :class="isTranscribing ? 'bg-blue-500' : 'bg-[#fb7299]'"
                  >
                    <span v-if="isTranscribing" class="flex items-center">
                      <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      正在转换中...
                    </span>
                    <span v-else>开始音频转文字</span>
                  </button>
                </div>

                

                <!-- 长视频警告 -->
                <div v-if="video && video.duration > 1800"
                     class="mb-4 p-3 bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-100 dark:border-yellow-800/60 rounded-lg">
                  <div class="flex items-start">
                    <svg class="w-5 h-5 text-yellow-600 mt-0.5 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24"
                         stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <div>
                      <p class="text-sm font-medium text-yellow-800 dark:text-yellow-300">长视频警告</p>
                      <p class="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
                        该视频时长超过30分钟，音频转文字后可能产生大量文本。这可能导致上下文过长，使AI无法接受请求。请谨慎操作
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 语言选择 -->
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">选择语言</label>
                  <div class="grid grid-cols-2 gap-2">
                    <button
                      @click="selectedLanguage = 'zh'"
                      class="px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200"
                      :class="[
                        selectedLanguage === 'zh'
                          ? 'bg-[#fb7299] text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                      ]"
                    >
                      中文
                    </button>
                    <button
                      @click="selectedLanguage = 'en'"
                      class="px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200"
                      :class="[
                        selectedLanguage === 'en'
                          ? 'bg-[#fb7299] text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      ]"
                    >
                      英文
                    </button>
                  </div>
                </div>

                <!-- 模型列表 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="model in whisperModels"
                       :key="model.name"
                       @click="selectModel(model)"
                       @mouseenter="hoveredModel = model"
                       @mouseleave="hoveredModel = null"
                       class="relative border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:border-[#fb7299]"
                       :class="[
                         selectedModel?.name === model.name ? 'border-[#fb7299] bg-pink-50 dark:bg-pink-900/20' : 'border-gray-200 dark:border-gray-700',
                         !model.is_downloaded ? 'opacity-50' : ''
                       ]"
                  >
                    <div class="flex items-start justify-between">
                      <div>
                        <h5 class="text-sm font-medium text-gray-900 dark:text-gray-100">
                          {{ model.description }}
                          <span
                            v-if="model.name === 'tiny' || (model.description && model.description.includes('极小型'))"
                            class="ml-2 inline-flex items-center px-1.5 py-0.5 rounded bg-[#fb7299]/10 text-[#fb7299] text-[10px]"
                          >推荐</span>
                        </h5>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ model.params_size }}</p>
                        <p v-if="model.is_downloaded" class="text-xs text-gray-400 dark:text-gray-500 mt-1 truncate" :title="model.path">
                          {{ model.path }}
                        </p>
                      </div>
                      <div v-if="model.is_downloaded"
                           class="flex-shrink-0 text-green-600">
                        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    </div>

                    <p class="mt-2 text-xs text-gray-600 dark:text-gray-400">{{ model.recommended_use }}</p>

                    <!-- 已下载模型的删除按钮 -->
                    <div
                      v-if="model.is_downloaded && hoveredModel && hoveredModel.name === model.name && !isDeletingModel"
                      class="absolute top-2 right-2 z-10">
                      <button @click.stop="showModelDeleteConfirm(model)"
                              class="p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors duration-200">
                        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>

                    <!-- 删除模型中状态 -->
                    <div v-if="isDeletingModel && modelToDelete && modelToDelete.name === model.name"
                         class="absolute inset-0 bg-white/80 dark:bg-gray-900/70 backdrop-blur-sm flex items-center justify-center rounded-lg">
                      <div class="flex flex-col items-center space-y-2">
                        <div
                          class="animate-spin h-6 w-6 border-2 border-red-500 border-t-transparent rounded-full"></div>
                        <span class="text-sm text-red-500">删除中...</span>
                      </div>
                    </div>

                    <!-- 未下载提示 -->
                    <div v-if="!model.is_downloaded"
                         class="absolute inset-0 bg-white/80 dark:bg-gray-900/70 backdrop-blur-sm flex items-center justify-center rounded-lg">
                      <!-- 下载按钮 -->
                      <div v-if="hoveredModel && hoveredModel.name === model.name && !isDownloadingModel"
                           class="flex flex-col items-center space-y-2"
                           @click.stop="showModelDownloadConfirm(model)">
                        <button
                          class="px-3 py-1.5 bg-[#fb7299] text-white rounded-md text-sm hover:bg-[#fb7299]/90 transition-colors duration-200">
                          下载模型
                        </button>
                        <span class="text-xs text-gray-500">{{ model.params_size }}</span>
                      </div>
                      <!-- 下载中状态 -->
                      <div v-else-if="isDownloadingModel && downloadingModel && downloadingModel.name === model.name"
                           class="flex flex-col items-center space-y-2">
                        <div
                          class="animate-spin h-6 w-6 border-2 border-[#fb7299] border-t-transparent rounded-full"></div>
                        <span class="text-sm text-[#fb7299]">下载中...</span>
                      </div>
                      <!-- 默认状态 -->
                      <span v-else class="text-sm text-gray-500">需要下载</span>
                    </div>
                  </div>
                </div>

                
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载中 -->
    <div v-else class="p-6 flex justify-center">
      <div class="animate-spin h-8 w-8 border-4 border-[#fb7299] border-t-transparent rounded-full"></div>
    </div>

    <!-- 下载对话框组件 -->
    <DownloadDialog
      v-model:show="showDownloadDialog"
      :video-info="{
        title: video?.title || '',
        author: video?.author_name || '',
        bvid: video?.bvid || '',
        cover: video?.cover || video?.covers?.[0] || '',
        cid: video?.cid || 0
      }"
      :default-only-audio="currentTab === 'local'"
      @download-complete="handleDownloadComplete"
    />

    <!-- 下载模型确认对话框 -->
    <van-dialog
      v-model:show="showDownloadConfirm"
      title="下载模型确认"
      show-cancel-button
      @confirm="startDownloadModel"
    >
      <div class="p-4">
        <p class="text-gray-700 dark:text-gray-300 mb-3">您确定要下载{{ modelToDownload?.description }}吗？</p>
        <div v-if="modelToDownload" class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-3 rounded-lg">
          <p class="font-medium text-gray-900 dark:text-gray-100">{{ modelToDownload.description }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ modelToDownload.params_size }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ modelToDownload.recommended_use }}</p>
        </div>
        <p class="mt-3 text-sm text-gray-500 dark:text-gray-400">下载模型将占用一定的磁盘空间</p>
      </div>
    </van-dialog>

    <!-- 模型删除确认对话框 -->
    <van-dialog
      v-model:show="showDeleteConfirm"
      title="删除模型确认"
      show-cancel-button
      @confirm="startDeleteModel"
    >
      <div class="p-4">
        <p class="text-gray-700 dark:text-gray-300 mb-3">您确定要删除{{ modelToDelete?.description }}吗？</p>
        <div v-if="modelToDelete" class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 p-3 rounded-lg">
          <p class="font-medium text-gray-900 dark:text-gray-100">{{ modelToDelete.description }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ modelToDelete.params_size }}</p>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">{{ modelToDelete.recommended_use }}</p>
        </div>
        <p class="mt-3 text-sm text-gray-500 dark:text-gray-400">删除模型将释放磁盘空间</p>
      </div>
    </van-dialog>
  </van-dialog>

  <!-- 视频下载对话框 -->
  <DownloadDialog
    v-model:show="showDownloadDialog"
    :video-info="{
      title: video?.title || '',
      author: video?.author || '',
      bvid: video?.bvid || '',
      cover: video?.cover || video?.covers?.[0] || '',
      cid: video?.cid || 0
    }"
    :default-only-audio="currentTab === 'local'"
    @download-complete="handleDownloadComplete"
  />
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { showNotify, showDialog } from 'vant'
import { usePrivacyStore } from '../../store/privacy'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'
import {
  updateVideoRemark,
  getWhisperModels,
  findAudioPath,
  transcribeAudio,
  checkSttFile,
  summarizeByCid,
  checkLocalSummary,
  downloadWhisperModel,
  deleteWhisperModel,
  checkAudioToTextEnvironment,
  getDeepSeekBalance,
  checkSystemResources,
  checkVideoDownload,
} from '../../api/api'
import VideoSummary from './VideoSummary.vue'
import EnvironmentCheck from './EnvironmentCheck.vue'
import DownloadDialog from './DownloadDialog.vue'
import 'vant/es/dialog/style'
import { openInBrowser } from '@/utils/openUrl.js'
import { normalizeImageUrl } from '@/utils/imageUrl.js'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  video: {
    type: Object,
    default: null,
  },
  remarkData: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:modelValue', 'remark-updated'])

// 在脚本顶部导入部分之后加入这个ref
const videoSummaryKey = ref(0)

// 使用计算属性处理dialog可见性
const dialogVisible = computed(() => props.modelValue)
const updateVisible = (value) => {
  emit('update:modelValue', value)

  // 当对话框关闭时重置状态
  if (!value) {
    // 重置标签页到默认的B站摘要tab
    currentTab.value = 'bilibili'

    // 重置摘要相关状态
    isCheckingEnvironment.value = false
    canRunSpeechToText.value = false
    cudaAvailable.value = false
    cudaSetupGuide.value = ''
    showCudaGuide.value = true
    audioPath.value = null
    isCheckingAudio.value = false
    isTranscribing.value = false
    transcriptionResult.value = null
    isSummarizing.value = false
    summaryStatus.value = ''
    summaryResult.value = null
    hasExistingStt.value = false
    sttFilePath.value = null
    hasLocalSummary.value = false
    localSummaryData.value = null

    // 通过改变key值强制重新创建摘要组件
    videoSummaryKey.value += 1
  } else {
    // 弹窗打开时默认刷新一次 DeepSeek 余额，防止不显示
    refreshDeepSeekBalance()
  }
}

// 监听弹窗显隐，进入弹窗即刷新一次余额（不依赖标签页）
watch(() => props.modelValue, (visible) => {
  if (visible) {
    refreshDeepSeekBalance()
  }
})

const { isPrivacyMode } = usePrivacyStore()

// 备注相关
const remarkContent = ref('')
const originalRemark = ref('')
const remarkTime = ref(null)

// 格式化时间戳
const formatTimestamp = (timestamp) => {
  if (!timestamp) return '时间未知'

  try {
    const date = new Date(timestamp * 1000)
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    })
  } catch (error) {
    console.error('格式化时间戳失败:', error)
    return '时间未知'
  }
}

// 格式化备注时间
const formatRemarkTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// 格式化时长
const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完'
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0')
  const secs = String(seconds % 60).padStart(2, '0')
  return `${minutes}:${secs}`
}

// 计算进度条宽度百分比
const getProgressWidth = (progress, duration) => {
  if (!duration || duration <= 0 || !progress || progress < 0) return '0%'
  const percentage = Math.min(100, (progress / duration) * 100)
  return `${percentage}%`
}

// 获取设备类型
const getDeviceType = (dt) => {
  if (dt === 1 || dt === 3 || dt === 5 || dt === 7) return '手机'
  if (dt === 2 || dt === 33) return '电脑'
  if (dt === 4 || dt === 6) return '平板'
  return '未知设备'
}

// 获取业务类型
const getBusinessType = (business) => {
  const businessTypes = {
    archive: '稿件',
    cheese: '课堂',
    pgc: '电影',
    live: '直播',
    'article-list': '专栏',
    article: '专栏',
  }
  return businessTypes[business] || '其他类型'
}

// 初始化备注内容
const initRemark = () => {
  if (!props.video) return

  const key = `${props.video.bvid}_${props.video.view_at}`
  const data = props.remarkData[key]

  if (data) {
    remarkContent.value = data.remark || ''
    remarkTime.value = data.remark_time || null
    originalRemark.value = remarkContent.value // 保存原始值
  } else {
    remarkContent.value = ''
    remarkTime.value = null
    originalRemark.value = ''
  }
}

// 处理备注失去焦点
const handleRemarkBlur = async () => {
  // 如果内容没有变化，不发送请求
  if (remarkContent.value === originalRemark.value || !props.video) {
    return
  }

  try {
    const response = await updateVideoRemark(
      props.video.bvid,
      props.video.view_at,
      remarkContent.value,
    )

    if (response.data.success || response.data.status === 'success') {
      if (remarkContent.value) { // 只在有内容时显示提示
        showNotify({
          type: 'success',
          message: '备注已保存',
        })
      }

      originalRemark.value = remarkContent.value // 更新原始值
      remarkTime.value = response.data.data.remark_time // 更新备注时间

      // 通知父组件备注已更新
      emit('remark-updated', {
        bvid: props.video.bvid,
        view_at: props.video.view_at,
        remark: remarkContent.value,
        remark_time: response.data.data.remark_time,
      })
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `保存备注失败：${error.message}`,
    })
    remarkContent.value = originalRemark.value // 恢复原始值
  }
}

// 在B站打开视频
const openInBilibili = async () => {
  if (!props.video) return

  let url = ''

  switch (props.video.business) {
    case 'archive':
      url = `https://www.bilibili.com/video/${props.video.bvid}`
      break
    case 'article':
      url = `https://www.bilibili.com/read/cv${props.video.oid}`
      break
    case 'article-list':
      url = `https://www.bilibili.com/read/readlist/rl${props.video.oid}`
      break
    case 'live':
      url = `https://live.bilibili.com/${props.video.oid}`
      break
    case 'pgc':
      url = props.video.uri || `https://www.bilibili.com/bangumi/play/ep${props.video.epid}`
      break
    case 'cheese':
      url = props.video.uri || `https://www.bilibili.com/cheese/play/ep${props.video.epid}`
      break
    default:
      console.warn('未知的业务类型:', props.video.business)
      return
  }

  if (url) {
    await openInBrowser(url)
  }
}

// 打开UP主页面
const openAuthorPage = async () => {
  if (!props.video || !props.video.author_mid) return
  const url = `https://space.bilibili.com/${props.video.author_mid}`
  await openInBrowser(url)
}

// 监听video变化，初始化备注
watch(() => props.video, () => {
  if (props.video) {
    initRemark()
  }
}, { deep: true, immediate: true })

const tabs = [
  { id: 'bilibili', name: 'B站AI摘要' },
  { id: 'local', name: '使用本地摘要' },
]
const currentTab = ref('bilibili')

// Whisper模型相关
const whisperModels = ref([])
const selectedModel = ref(null)
const transcriptionStatus = ref('')
const audioPath = ref(null)
const isCheckingAudio = ref(false)
const showDownloadDialog = ref(false)
const selectedLanguage = ref('zh')
const isTranscribing = ref(false)
const transcriptionResult = ref(null)
const isSummarizing = ref(false)
const summaryStatus = ref('')
const summaryResult = ref(null)

// 模型下载相关状态
const downloadingModel = ref(null) // 当前正在下载的模型
const isDownloadingModel = ref(false) // 是否正在下载模型
const showDownloadConfirm = ref(false) // 是否显示下载确认对话框
const modelToDownload = ref(null) // 要下载的模型
const hoveredModel = ref(null) // 当前悬停的模型

// 模型删除相关状态
const isDeletingModel = ref(false) // 是否正在删除模型
const showDeleteConfirm = ref(false) // 是否显示删除确认对话框
const modelToDelete = ref(null) // 要删除的模型

// 显示下载对话框
const handleShowDownload = () => {
  if (!props.video) return
  showDownloadDialog.value = true
}

// 获取Whisper模型列表
const fetchWhisperModels = async () => {
  try {
    const response = await getWhisperModels()
    // 对模型进行排序：多语言模型在前，英语模型在后
    whisperModels.value = response.data.sort((a, b) => {
      // 如果一个是英语模型（包含.en），一个不是，将非英语模型排在前面
      const aIsEnglish = a.name.includes('.en')
      const bIsEnglish = b.name.includes('.en')
      if (aIsEnglish !== bIsEnglish) {
        return aIsEnglish ? 1 : -1
      }
      // 如果都是同类型（都是英语或都是多语言），按照大小排序（tiny -> base -> small -> medium -> large）
      const sizeOrder = ['tiny', 'base', 'small', 'medium', 'large-v1', 'large-v2', 'large-v3']
      const aBaseName = a.name.replace('.en', '')
      const bBaseName = b.name.replace('.en', '')
      return sizeOrder.indexOf(aBaseName) - sizeOrder.indexOf(bBaseName)
    })

    // 选择推荐的模型
    if (whisperModels.value.length > 0) {
      // 选择tiny模型
      const tinyModel = whisperModels.value.find(model =>
        model.name === 'tiny' && model.is_downloaded,
      )

      // 如果找到tiny模型，选择它
      if (tinyModel) {
        selectModel(tinyModel)
      } else {
        // 如果没有找到tiny模型，选择第一个下载好的模型
        const firstDownloadedModel = whisperModels.value.find(model => model.is_downloaded)
        if (firstDownloadedModel) {
          selectModel(firstDownloadedModel)
        }
      }
    }
  } catch (error) {
    console.error('获取Whisper模型列表失败:', error)
    showNotify({
      type: 'danger',
      message: '获取模型列表失败',
    })
  }
}

// 选择模型
const selectModel = (model) => {
  if (model.is_downloaded) {
    selectedModel.value = model
  } else {
    showNotify({
      type: 'warning',
      message: '该模型尚未下载，请选择已下载的模型',
    })
  }
}

// 获取音频文件路径
const checkAudioFile = async () => {
  try {
    isCheckingAudio.value = true
    transcriptionStatus.value = '检查音频文件...'
    const response = await findAudioPath(props.video.cid)
    audioPath.value = response.data.audio_path
    if (audioPath.value) {
      transcriptionStatus.value = '音频文件已找到，可以开始转录'
    }
    return true
  } catch (error) {
    console.error('查找音频文件失败:', error)
    transcriptionStatus.value = ''
    return false
  } finally {
    isCheckingAudio.value = false
  }
}

// 在 script setup 部分添加
const hasExistingStt = ref(false)
const sttFilePath = ref(null)

// 检查是否存在转换后的文件
const checkExistingStt = async () => {
  try {
    if (!props.video?.cid) return

    const response = await checkSttFile(props.video.cid)
    if (response.data.success) {
      hasExistingStt.value = response.data.exists
      sttFilePath.value = response.data.file_path

      if (response.data.exists) {
        transcriptionStatus.value = '已存在转换后的文件'
      }
    }
  } catch (error) {
    console.error('检查转换文件失败:', error)
  }
}

// 在 script setup 部分添加新的响应式变量
const localSummaryData = ref(null)
const hasLocalSummary = ref(false)

// 添加检查本地摘要的函数
const checkLocalSummaryFile = async () => {
  try {
    if (!props.video?.cid) return

    const response = await checkLocalSummary(props.video.cid)
    if (response.data.exists) {
      hasLocalSummary.value = true
      localSummaryData.value = response.data.full_response
      transcriptionStatus.value = '已找到本地摘要'
    }
  } catch (error) {
    console.error('检查本地摘要失败:', error)
  }
}

// 修改 watch currentTab
watch(currentTab, async (newTab) => {
  if (newTab === 'local') {
    // 首先检查环境
    isCheckingEnvironment.value = true
    canRunSpeechToText.value = false
    cudaSetupGuide.value = ''

    try {
      // 1. 检查系统资源
      const resourceResponse = await checkSystemResources()
      canRunSpeechToText.value = resourceResponse.data.can_run_speech_to_text
      systemLimitationReason.value = resourceResponse.data.limitation_reason

      // 2. 如果系统资源足够，再检查CUDA
      if (canRunSpeechToText.value) {
        const cudaResponse = await checkAudioToTextEnvironment()
        cudaAvailable.value = cudaResponse.data.system_info.cuda_available
        cudaSetupGuide.value = cudaResponse.data.system_info.cuda_setup_guide || ''

        // 只有在系统资源足够时才加载其他内容
        fetchWhisperModels()
        await checkAudioFile()
        await checkExistingStt()
        await checkLocalSummaryFile()
        await refreshDeepSeekBalance()
      }
    } catch (error) {
      console.error('检查系统资源失败:', error)
      canRunSpeechToText.value = false
      systemLimitationReason.value = '检查系统资源失败: ' + (error.message || '未知错误')
    } finally {
      isCheckingEnvironment.value = false
    }
  }
})

// 修改 startTranscription 函数
const startTranscription = async () => {
  if (!selectedModel.value) {
    showNotify({
      type: 'warning',
      message: '请先选择一个模型',
    })
    return
  }

  if (!audioPath.value) {
    await checkAudioFile()
    if (!audioPath.value) {
      return
    }
  }

  // 检查视频时长，如果超过30分钟，显示额外确认
  if (props.video && props.video.duration > 1800) {
    const result = await showDialog({
      title: '长视频警告',
      message: '该视频时长超过30分钟，转录后可能产生大量文本，导致AI无法处理。是否继续？',
      showCancelButton: true,
    })

    if (!result) {
      return
    }
  }

  if (hasExistingStt.value) {
    const result = await showDialog({
      title: '提示',
      message: '已存在转换后的文件，是否重新转换？',
      showCancelButton: true,
    })

    if (!result) {
      return
    }
  }

  try {
    isTranscribing.value = true
    transcriptionStatus.value = '准备开始转换...'
    const response = await transcribeAudio({
      audio_path: audioPath.value,
      model_size: selectedModel.value.name,
      language: selectedLanguage.value,
      cid: props.video.cid,
    })

    if (response.data.success || response.data.status === 'success') {
      transcriptionStatus.value = '转录任务已开始，正在处理中...'
      showNotify({
        type: 'success',
        message: '转录任务已开始',
      })
      handleTranscriptionComplete(response.data)
    } else {
      isTranscribing.value = false
      showNotify({
        type: 'danger',
        message: response.data.message || '开始转录失败',
      })
    }
  } catch (error) {
    console.error('转录失败:', error)
    transcriptionStatus.value = `转录失败: ${error.message || '未知错误'}`
    isTranscribing.value = false
  }
}

// 检查转录状态
const handleTranscriptionComplete = async (response) => {
  isTranscribing.value = false
  transcriptionStatus.value = '转录完成'
  transcriptionResult.value = {
    duration: response.duration,
    processingTime: response.processing_time,
    languageDetected: response.language_detected,
  }

  showNotify({
    type: 'success',
    message: '转录完成',
  })

  // 重置摘要相关状态
  summaryStatus.value = ''
  summaryResult.value = null
  isSummarizing.value = false

  // 转录完成后，刷新标签内容
  await checkExistingStt()
  await checkLocalSummaryFile()
}

// 添加生成摘要的函数
const startGeneratingSummary = async () => {
  try {
    // 检查视频时长，如果超过30分钟，显示额外确认
    if (props.video && props.video.duration > 1800) {
      const result = await showDialog({
        title: '长视频警告',
        message: '该视频时长超过30分钟，转录文本可能过长，导致AI无法处理摘要请求。是否继续？',
        showCancelButton: true,
      })

      if (!result) {
        return
      }
    }

    isSummarizing.value = true
    summaryStatus.value = '正在生成摘要...'

    const response = await summarizeByCid(props.video.cid)
    if (response.data.success || response.data.status === 'success') {
      summaryStatus.value = '摘要生成完成'
      summaryResult.value = response.data.summary
      showNotify({
        type: 'success',
        message: '摘要生成完成',
      })

      // 摘要生成完成后，刷新标签内容
      await checkLocalSummaryFile()
    } else {
      summaryStatus.value = '摘要生成失败：' + (response.data.message || '未知错误')
      showNotify({
        type: 'warning',
        message: '摘要生成失败',
      })
    }
  } catch (error) {
    console.error('生成摘要失败:', error)
    summaryStatus.value = '摘要生成失败：' + (error.message || '未知错误')
    showNotify({
      type: 'danger',
      message: '生成摘要失败：' + (error.message || '未知错误'),
    })
  } finally {
    isSummarizing.value = false
  }
}

// 在 script setup 部分添加
const environmentCheck = ref(null)
const isCheckingEnvironment = ref(true)
const canRunSpeechToText = ref(false)
const systemLimitationReason = ref('')
const cudaAvailable = ref(false)
const cudaSetupGuide = ref('')
const showCudaGuide = ref(true)  // 默认显示CUDA安装指南

// 处理环境检查结果
const handleEnvironmentCheck = (result) => {
  isCheckingEnvironment.value = false
  canRunSpeechToText.value = result.canRun
  systemLimitationReason.value = result.limitationReason
}

// 修改 handleTimeClick 函数和添加 hasTimeStamp 函数
const hasTimeStamp = (text) => {
  return /\d{2}:\d{2}[-–]\d{2}:\d{2}/.test(text)
}

const handleTimeClick = async (section) => {
  const timeMatch = section.match(/(\d{2}):(\d{2})[-–](\d{2}):(\d{2})/)
  if (timeMatch) {
    const startMinutes = parseInt(timeMatch[1])
    const startSeconds = parseInt(timeMatch[2])
    const startTime = startMinutes * 60 + startSeconds

    // 构建B站视频URL并跳转
    const url = `https://www.bilibili.com/video/${props.video.bvid}?t=${startTime}`
    await openInBrowser(url)
  }
}

// 提取时间戳的函数
const extractTimeStamp = (text) => {
  const match = text.match(/(\d{2}:\d{2}[-–]\d{2}:\d{2})/)
  return match ? match[1] : ''
}

// 处理下载完成事件
const handleDownloadComplete = async () => {
  // 下载完成后，刷新标签内容
  checkAudioFile()
  checkExistingStt()
  checkLocalSummaryFile()

  // 重新检查视频下载状态
  await checkIsVideoDownloaded()

  showNotify({
    type: 'success',
    message: '下载完成',
    duration: 2000,
  })
}

// 下载模型确认对话框相关
const showModelDownloadConfirm = (model) => {
  modelToDownload.value = model
  showDownloadConfirm.value = true
}

const startDownloadModel = async () => {
  if (!modelToDownload.value) return

  try {
    isDownloadingModel.value = true
    downloadingModel.value = modelToDownload.value
    const response = await downloadWhisperModel(modelToDownload.value.name)
    if (response.data.success || response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message || '模型下载成功',
      })
      // 下载完成后，刷新模型列表
      fetchWhisperModels()
    } else {
      showNotify({
        type: 'danger',
        message: response.data.message || '模型下载失败',
      })
    }
  } catch (error) {
    console.error('下载模型失败:', error)
    showNotify({
      type: 'danger',
      message: '下载模型失败',
    })
  } finally {
    isDownloadingModel.value = false
    downloadingModel.value = null
  }
}

// 模型删除确认对话框相关
const showModelDeleteConfirm = (model) => {
  modelToDelete.value = model
  showDeleteConfirm.value = true
}

const startDeleteModel = async () => {
  if (!modelToDelete.value) return

  try {
    isDeletingModel.value = true
    const response = await deleteWhisperModel(modelToDelete.value.name)
    if (response.data.success || response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message || '模型删除成功',
      })
      // 删除完成后，刷新模型列表
      fetchWhisperModels()
    } else {
      showNotify({
        type: 'danger',
        message: response.data.message || '模型删除失败',
      })
    }
  } catch (error) {
    console.error('删除模型失败:', error)
    showNotify({
      type: 'danger',
      message: '删除模型失败',
    })
  } finally {
    isDeletingModel.value = false
    modelToDelete.value = null
  }
}

// DeepSeek相关状态
const deepseekBalance = ref({
  is_available: false,
  balance_infos: [],
})

// 添加刷新DeepSeek余额的方法
const refreshDeepSeekBalance = async () => {
  try {
    const response = await getDeepSeekBalance()
    deepseekBalance.value = response.data
  } catch (error) {
    console.error('获取DeepSeek余额失败:', error)
    deepseekBalance.value = { is_available: false }
  }
}

// 下载相关
const isVideoDownloaded = ref(false)
const downloadedFiles = ref([])

// 检查视频是否已下载
const checkIsVideoDownloaded = async () => {
  try {
    // 如果没有CID，则无法检查
    if (!props.video?.cid) return

    const response = await checkVideoDownload(props.video.cid)
    if (response.data && response.data.status === 'success') {
      isVideoDownloaded.value = response.data.downloaded

      if (isVideoDownloaded.value && response.data.files) {
        downloadedFiles.value = response.data.files
      } else {
        downloadedFiles.value = []
      }
    }
  } catch (error) {
    console.error('检查视频下载状态出错:', error)
    isVideoDownloaded.value = false
    downloadedFiles.value = []
  }
}

// 监听视频变化，检查下载状态
watch(() => props.video?.cid, (newCid) => {
  if (newCid) {
    checkIsVideoDownloaded()
  } else {
    isVideoDownloaded.value = false
    downloadedFiles.value = []
  }
})
</script>

<style>
.video-detail-dialog :deep(.van-dialog) {
  border-radius: 0.5rem;
  overflow: hidden;
}

/* 对话框正文背景与页面正文一致 */
.video-detail-dialog :deep(.van-dialog__content) {
  background-color: #ffffff; /* light */
}
.dark .video-detail-dialog :deep(.van-dialog__content) {
  background-color: #1f2937; /* gray-800 */
}

.video-detail-dialog :deep(.van-dialog__header) {
  padding: 12px 16px;
  background-color: #ffffff; /* light: white 与正文一致 */
  border-bottom: 1px solid #e5e7eb; /* gray-200 */
  color: #111827; /* gray-900 */
}
.dark .video-detail-dialog :deep(.van-dialog__header) {
  background-color: #1f2937; /* dark: gray-800 与正文一致 */
  border-bottom: 1px solid #374151; /* gray-700 */
  color: #e5e7eb; /* gray-200 */
}
</style>

