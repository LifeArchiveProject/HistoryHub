<!-- 视频下载界面 -->
<template>
  <div class="p-6 bg-white min-h-screen">
    <!-- 搜索区域 - 使用与首页一致的搜索栏，去掉背景、边框和顶部内容 -->
    <div class="mx-auto max-w-6xl mb-6 mt-12">
      <div class="p-4">
        <!-- 搜索框和类型选择 -->
        <div class="flex flex-col md:flex-row gap-4">
          <!-- 搜索框容器 -->
          <div class="w-full flex">
            <div class="flex items-center rounded-md border border-gray-300 bg-white focus-within:border-[#fb7299] transition-colors duration-200 flex-grow">
              <!-- 下载类型选择 -->
              <div class="h-10 pl-2 flex items-center">
                <CustomDropdown
                  v-model="downloadType"
                  :options="downloadTypeOptions"
                  :selected-text="getDownloadTypeLabel(downloadType)"
                  @change="onDownloadTypeChange"
                  custom-class="h-full border-none !shadow-none !p-0 !m-0 !rounded-none !pr-1"
                  :min-width="120"
                  :use-fixed-width="false"
                >
                  <template #trigger-content>
                    <span class="text-[#fb7299] text-sm flex items-center whitespace-nowrap">{{ getDownloadTypeLabel(downloadType) }}</span>
                  </template>
                </CustomDropdown>
              </div>

              <!-- 分隔线 -->
              <div class="h-5 w-px bg-gray-200 mx-1"></div>

              <!-- 输入框 -->
              <input
                v-model="inputValue"
                @keyup.enter="handleDownload"
                type="search"
                :placeholder="downloadType === 'video' ? '输入BV号或完整视频链接' : '输入UP主UID'"
                class="h-10 w-full border-none bg-transparent px-2 pr-3 text-gray-700 focus:outline-none focus:ring-0 text-sm leading-none"
              />
            </div>

            <!-- 搜索按钮 - 增加左边距 -->
            <button
              @click="handleDownload"
              :disabled="!inputValue"
              class="flex-shrink-0 bg-[#fb7299] hover:bg-[#fb7299]/90 text-white px-4 py-2 rounded-md font-medium transition-colors duration-200 flex items-center justify-center ml-4"
            >
              <span class="flex items-center">
                <svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
                </svg>
                下载视频
              </span>
            </button>
          </div>
        </div>

        <p class="mt-2 text-xs text-gray-500">
          {{ downloadType === 'video' ? '支持完整链接或 BV 号，例如：BV1xx411c7mD' : '在 UP 主空间页面 URL 中查看 UID' }}
        </p>
      </div>
    </div>

    <!-- 空状态提示 -->
    <div v-if="!inputValue" class="mx-auto max-w-6xl mt-24 flex flex-col items-center justify-center text-center">
      <div class="w-24 h-24 text-gray-300 mb-4">
        <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">开始下载视频</h3>
      <p class="text-sm text-gray-500 max-w-md">
        {{ downloadType === 'video'
          ? '请输入视频的 BV 号或完整链接，支持单个视频下载'
          : '请输入 UP 主的 UID，支持批量下载 UP 主的所有投稿视频' }}
      </p>
    </div>

    <!-- 视频信息卡片（仅当有视频信息且输入框有内容时显示） -->
    <div v-if="hasVideoInfo && inputValue" class="mx-auto max-w-6xl">
      <div class="mb-6 overflow-hidden">
        <!-- 视频信息卡片内容 -->
        <div class="p-4 flex flex-col">
          <!-- 视频数据统计和提示信息合并在同一行 -->
          <div class="flex flex-wrap items-center gap-4 mb-4">
            <!-- 播放量 -->
            <div class="flex items-center">
              <svg class="view-icon w-4 h-4 text-gray-600 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M10 4.040041666666666C7.897383333333334 4.040041666666666 6.061606666666667 4.147 4.765636666666667 4.252088333333334C3.806826666666667 4.32984 3.061106666666667 5.0637316666666665 2.9755000000000003 6.015921666666667C2.8803183333333333 7.074671666666667 2.791666666666667 8.471183333333332 2.791666666666667 9.998333333333333C2.791666666666667 11.525566666666668 2.8803183333333333 12.922083333333333 2.9755000000000003 13.9808C3.061106666666667 14.932983333333334 3.806826666666667 15.666916666666667 4.765636666666667 15.744683333333336C6.061611666666668 15.849716666666666 7.897383333333334 15.956666666666667 10 15.956666666666667C12.10285 15.956666666666667 13.93871666666667 15.849716666666666 15.234766666666667 15.74461666666667C16.193416666666668 15.66685 16.939000000000004 14.933216666666667 17.024583333333336 13.981216666666668C17.11975 12.922916666666667 17.208333333333332 11.526666666666666 17.208333333333332 9.998333333333333C17.208333333333332 8.470083333333333 17.11975 7.073818333333334 17.024583333333336 6.015513333333334C16.939000000000004 5.063538333333333 16.193416666666668 4.329865000000001 15.234766666666667 4.252118333333334C13.93871666666667 4.147016666666667 12.10285 4.040041666666666 10 4.040041666666666zM4.684808333333334 3.255365C6.001155 3.14862 7.864583333333334 3.0400416666666668 10 3.0400416666666668C12.13565 3.0400416666666668 13.999199999999998 3.148636666666667 15.315566666666667 3.2553900000000002C16.753416666666666 3.3720016666666672 17.890833333333333 4.483195 18.020583333333335 5.925965000000001C18.11766666666667 7.005906666666667 18.208333333333336 8.433 18.208333333333336 9.998333333333333C18.208333333333336 11.56375 18.11766666666667 12.990833333333335 18.020583333333335 14.0708C17.890833333333333 15.513533333333331 16.753416666666666 16.624733333333335 15.315566666666667 16.74138333333333C13.999199999999998 16.848116666666666 12.13565 16.95666666666667 10 16.95666666666667C7.864583333333334 16.95666666666667 6.001155 16.848116666666666 4.684808333333334 16.7414C3.2467266666666665 16.624750000000002 2.1092383333333338 15.513266666666667 1.9795200000000002 14.070383333333334C1.8823900000000002 12.990000000000002 1.7916666666666667 11.562683333333334 1.7916666666666667 9.998333333333333C1.7916666666666667 8.434066666666666 1.8823900000000002 7.00672 1.9795200000000002 5.926381666666667C2.1092383333333338 4.483463333333334 3.2467266666666665 3.371976666666667 4.684808333333334 3.255365z" fill="currentColor"></path>
                <path d="M12.23275 9.1962C12.851516666666667 9.553483333333332 12.851516666666667 10.44665 12.232683333333332 10.803866666666666L9.57975 12.335600000000001C8.960983333333335 12.692816666666667 8.1875 12.246250000000002 8.187503333333334 11.531733333333333L8.187503333333334 8.4684C8.187503333333334 7.753871666666667 8.960983333333335 7.307296666666667 9.57975 7.66456L12.23275 9.1962z" fill="currentColor"></path>
              </svg>
              <span class="text-sm font-medium text-gray-600">{{ formatCount(videoInfo.stat?.view) }}</span>
            </div>

            <!-- 弹幕数 -->
            <div class="flex items-center">
              <svg class="dm-icon w-4 h-4 text-gray-600 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                <path d="M10 4.040041666666666C7.897383333333334 4.040041666666666 6.061606666666667 4.147 4.765636666666667 4.252088333333334C3.806826666666667 4.32984 3.061106666666667 5.0637316666666665 2.9755000000000003 6.015921666666667C2.8803183333333333 7.074671666666667 2.791666666666667 8.471183333333332 2.791666666666667 9.998333333333333C2.791666666666667 11.525566666666668 2.8803183333333333 12.922083333333333 2.9755000000000003 13.9808C3.061106666666667 14.932983333333334 3.806826666666667 15.666916666666667 4.765636666666667 15.744683333333336C6.061611666666668 15.849716666666666 7.897383333333334 15.956666666666667 10 15.956666666666667C12.10285 15.956666666666667 13.93871666666667 15.849716666666666 15.234766666666667 15.74461666666667C16.193416666666668 15.66685 16.939000000000004 14.933216666666667 17.024583333333336 13.981216666666668C17.11975 12.922916666666667 17.208333333333332 11.526666666666666 17.208333333333332 9.998333333333333C17.208333333333332 8.470083333333333 17.11975 7.073818333333334 17.024583333333336 6.015513333333334C16.939000000000004 5.063538333333333 16.193416666666668 4.329865000000001 15.234766666666667 4.252118333333334C13.93871666666667 4.147016666666667 12.10285 4.040041666666666 10 4.040041666666666zM4.684808333333334 3.255365C6.001155 3.14862 7.864583333333334 3.0400416666666668 10 3.0400416666666668C12.13565 3.0400416666666668 13.999199999999998 3.148636666666667 15.315566666666667 3.2553900000000002C16.753416666666666 3.3720016666666672 17.890833333333333 4.483195 18.020583333333335 5.925965000000001C18.11766666666667 7.005906666666667 18.208333333333336 8.433 18.208333333333336 9.998333333333333C18.208333333333336 11.56375 18.11766666666667 12.990833333333335 18.020583333333335 14.0708C17.890833333333333 15.513533333333331 16.753416666666666 16.624733333333335 15.315566666666667 16.74138333333333C13.999199999999998 16.848116666666666 12.13565 16.95666666666667 10 16.95666666666667C7.864583333333334 16.95666666666667 6.001155 16.848116666666666 4.684808333333334 16.7414C3.2467266666666665 16.624750000000002 2.1092383333333338 15.513266666666667 1.9795200000000002 14.070383333333334C1.8823900000000002 12.990000000000002 1.7916666666666667 11.562683333333334 1.7916666666666667 9.998333333333333C1.7916666666666667 8.434066666666666 1.8823900000000002 7.00672 1.9795200000000002 5.926381666666667C2.1092383333333338 4.483463333333334 3.2467266666666665 3.371976666666667 4.684808333333334 3.255365z" fill="currentColor"></path>
                <path d="M13.291666666666666 8.833333333333334L8.166666666666668 8.833333333333334C7.890526666666666 8.833333333333334 7.666666666666666 8.609449999999999 7.666666666666666 8.333333333333334C7.666666666666666 8.057193333333334 7.890526666666666 7.833333333333334 8.166666666666668 7.833333333333334L13.291666666666666 7.833333333333334C13.567783333333335 7.833333333333334 13.791666666666668 8.057193333333334 13.791666666666668 8.333333333333334C13.791666666666668 8.609449999999999 13.567783333333335 8.833333333333334 13.291666666666666 8.833333333333334z" fill="currentColor"></path>
                <path d="M14.541666666666666 12.166666666666666L9.416666666666668 12.166666666666666C9.140550000000001 12.166666666666666 8.916666666666666 11.942783333333333 8.916666666666666 11.666666666666668C8.916666666666666 11.390550000000001 9.140550000000001 11.166666666666668 9.416666666666668 11.166666666666668L14.541666666666666 11.166666666666668C14.817783333333335 11.166666666666668 15.041666666666668 11.390550000000001 15.041666666666668 11.666666666666668C15.041666666666668 11.942783333333333 14.817783333333335 12.166666666666666 14.541666666666666 12.166666666666666z" fill="currentColor"></path>
                <path d="M6.5 8.333333333333334C6.5 8.609449999999999 6.27614 8.833333333333334 6 8.833333333333334L5.458333333333333 8.833333333333334C5.182193333333334 8.833333333333334 4.958333333333334 8.609449999999999 4.958333333333334 8.333333333333334C4.958333333333334 8.057193333333334 5.182193333333334 7.833333333333334 5.458333333333333 7.833333333333334L6 7.833333333333334C6.27614 7.833333333333334 6.5 8.057193333333334 6.5 8.333333333333334z" fill="currentColor"></path>
                <path d="M7.750000000000001 11.666666666666668C7.750000000000001 11.942783333333333 7.526140000000001 12.166666666666666 7.25 12.166666666666666L6.708333333333334 12.166666666666666C6.432193333333334 12.166666666666666 6.208333333333334 11.942783333333333 6.208333333333334 11.666666666666668C6.208333333333334 11.390550000000001 6.432193333333334 11.166666666666668 6.708333333333334 11.166666666666668L7.25 11.166666666666668C7.526140000000001 11.166666666666668 7.750000000000001 11.390550000000001 7.750000000000001 11.666666666666668z" fill="currentColor"></path>
              </svg>
              <span class="text-sm font-medium text-gray-600">{{ formatCount(videoInfo.stat?.danmaku) }}</span>
            </div>

            <!-- 发布时间 -->
            <div v-if="videoInfo.pubdate" class="flex items-center">
              <svg class="w-4 h-4 text-gray-600 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <span class="text-sm font-medium text-gray-600">{{ formatDetailedTimestamp(videoInfo.pubdate) }}</span>
            </div>

            <!-- 警告/提示信息 -->
            <div v-if="videoInfo.argue_info?.argue_msg"
                 class="inline-flex items-center bg-yellow-50 px-2 py-1 rounded text-xs text-yellow-700">
              <span class="mr-1">提示：</span>{{ videoInfo.argue_info.argue_msg }}
            </div>

            <!-- 荣誉信息 - 修改样式 -->
            <div v-if="videoInfo.honor_reply?.honor && videoInfo.honor_reply.honor.length > 0"
                 class="inline-flex flex-wrap gap-4">
              <div v-for="(honor, index) in videoInfo.honor_reply.honor"
                   :key="index"
                   class="text-xs px-2 py-1 bg-[#fff7e9] text-[#ffb027] rounded-md flex items-center">
                <svg width="16" height="16" viewBox="0 0 16 13" fill="none" xmlns="http://www.w3.org/2000/svg" class="honor-icon mr-1" data-v-b37c19ce=""><path fill-rule="evenodd" clip-rule="evenodd" d="M0.69043 3.9539C0.69043 2.62399 1.76853 1.5459 3.09843 1.5459L3.09843 2.23389C3.09843 2.89885 3.63748 3.4379 4.30243 3.4379C4.96739 3.4379 5.50643 2.89885 5.50643 2.2339V1.5459H10.4944V2.23389C10.4944 2.89885 11.0335 3.4379 11.6984 3.4379C12.3634 3.4379 12.9024 2.89885 12.9024 2.2339L12.9024 1.5459C14.2323 1.5459 15.3104 2.62399 15.3104 3.9539V10.5759C15.3104 11.9058 14.2323 12.9839 12.9024 12.9839H3.09843C1.76853 12.9839 0.69043 11.9058 0.69043 10.5759V3.9539ZM8.59407 5.73981C8.26159 5.73981 7.99207 6.00934 7.99207 6.34181C7.99207 6.67429 8.26159 6.9438 8.59407 6.9438H13.4101C13.7425 6.9438 14.0121 6.67429 14.0121 6.34181C14.0121 6.00934 13.7425 5.73981 13.4101 5.73981H8.59407ZM7.99207 9.35182C7.99207 9.01935 8.26159 8.74982 8.59407 8.74982H13.4101C13.7425 8.74982 14.0121 9.01935 14.0121 9.35182C14.0121 9.6843 13.7425 9.95381 13.4101 9.95381H8.59407C8.26159 9.95381 7.99207 9.6843 7.99207 9.35182ZM2.23794 6.80617L3.04621 6.68384L3.4095 5.92297C3.61412 5.4928 4.20532 5.4928 4.40994 5.92297L4.77212 6.68384L5.5815 6.80617C6.00636 6.87022 6.19423 7.37784 5.95382 7.71812L5.89065 7.79341L5.30428 8.38548L5.44316 9.22243C5.5161 9.66373 5.10432 10.0072 4.71637 9.86957L4.63378 9.83257L3.90972 9.43657L3.18566 9.83257C2.8037 10.0409 2.36159 9.74072 2.36788 9.31535L2.37628 9.22243L2.51404 8.38548L1.92879 7.79341C1.62136 7.48247 1.75692 6.95721 2.14419 6.82854L2.23794 6.80617Z" fill="currentColor"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M4.31965 1.02979V1.88979V1.02979Z" fill="currentColor"></path> <path d="M4.31965 1.02979V1.88979" stroke-width="1.72" stroke-linecap="round" stroke-linejoin="round" stroke="currentColor"></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M11.7415 1.02979V1.88979V1.02979Z" fill="currentColor"></path> <path d="M11.7415 1.02979V1.88979" stroke-width="1.72" stroke-linecap="round" stroke-linejoin="round" stroke="currentColor"></path></svg>
                {{ honor.desc }}
              </div>
            </div>
          </div>

          <div class="flex flex-col md:flex-row space-x-0 md:space-x-4">
            <!-- 左侧封面 -->
            <div class="w-full md:w-1/3 mb-4 md:mb-0 flex flex-col">
              <div class="relative aspect-video bg-gray-200 rounded-lg overflow-hidden">
                <img
                  v-if="videoInfo.pic"
                  :src="videoInfo.pic"
                  :alt="videoInfo.title"
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                  <svg class="w-16 h-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                </div>

                <!-- 视频时长标记 -->
                <div v-if="videoInfo.duration" class="absolute bottom-1 right-1 rounded bg-black/50 px-1 py-0.5 text-xs font-semibold text-white">
                  {{ formatDuration(videoInfo.duration) }}
                </div>

                <!-- 视频数据统计 - 播放、弹幕、评论放在封面上与时长同一行 -->
                <div class="absolute bottom-1 left-1 flex space-x-2">
                </div>
              </div>

              <!-- 视频互动数据统计 - 点赞、投币、收藏、分享 -->
              <div class="grid grid-cols-4 gap-2 mt-6">
                <div class="flex items-center justify-center text-gray-700">
                  <svg class="w-5 h-5 mr-1" width="36" height="36" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
                      <path fill-rule="evenodd" clip-rule="evenodd" d="M9.77234 30.8573V11.7471H7.54573C5.50932 11.7471 3.85742 13.3931 3.85742 15.425V27.1794C3.85742 29.2112 5.50932 30.8573 7.54573 30.8573H9.77234ZM11.9902 30.8573V11.7054C14.9897 10.627 16.6942 7.8853 17.1055 3.33591C17.2666 1.55463 18.9633 0.814421 20.5803 1.59505C22.1847 2.36964 23.243 4.32583 23.243 6.93947C23.243 8.50265 23.0478 10.1054 22.6582 11.7471H29.7324C31.7739 11.7471 33.4289 13.402 33.4289 15.4435C33.4289 15.7416 33.3928 16.0386 33.3215 16.328L30.9883 25.7957C30.2558 28.7683 27.5894 30.8573 24.528 30.8573H11.9911H11.9902Z" fill="currentColor"/>
                    </svg>
                  <span class="text-sm font-medium">{{ formatCount(videoInfo.stat?.like) }}</span>
                </div>
                <div class="flex items-center justify-center text-gray-700">
                  <svg class="w-5 h-5 mr-1" width="28" height="28" viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg">
                      <path fill-rule="evenodd" clip-rule="evenodd" d="M14.045 25.5454C7.69377 25.5454 2.54504 20.3967 2.54504 14.0454C2.54504 7.69413 7.69377 2.54541 14.045 2.54541C20.3963 2.54541 25.545 7.69413 25.545 14.0454C25.545 17.0954 24.3334 20.0205 22.1768 22.1771C20.0201 24.3338 17.095 25.5454 14.045 25.5454ZM9.66202 6.81624H18.2761C18.825 6.81624 19.27 7.22183 19.27 7.72216C19.27 8.22248 18.825 8.62807 18.2761 8.62807H14.95V10.2903C17.989 10.4444 20.3766 12.9487 20.3855 15.9916V17.1995C20.3854 17.6997 19.9799 18.1052 19.4796 18.1052C18.9793 18.1052 18.5738 17.6997 18.5737 17.1995V15.9916C18.5667 13.9478 16.9882 12.2535 14.95 12.1022V20.5574C14.95 21.0577 14.5444 21.4633 14.0441 21.4633C13.5437 21.4633 13.1382 21.0577 13.1382 20.5574V12.1022C11.1 12.2535 9.52148 13.9478 9.51448 15.9916V17.1995C9.5144 17.6997 9.10883 18.1052 8.60856 18.1052C8.1083 18.1052 7.70273 17.6997 7.70265 17.1995V15.9916C7.71158 12.9487 10.0992 10.4444 13.1382 10.2903V8.62807H9.66202C9.11309 8.62807 8.66809 8.22248 8.66809 7.72216C8.66809 7.22183 9.11309 6.81624 9.66202 6.81624Z" fill="currentColor"/>
                    </svg>
                  <span class="text-sm font-medium">{{ formatCount(videoInfo.stat?.coin) }}</span>
                </div>
                <div class="flex items-center justify-center text-gray-700">
                  <svg class="w-5 h-5 mr-1" width="28" height="28" viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg">
                      <path fill-rule="evenodd" clip-rule="evenodd" d="M19.8071 9.26152C18.7438 9.09915 17.7624 8.36846 17.3534 7.39421L15.4723 3.4972C14.8998 2.1982 13.1004 2.1982 12.4461 3.4972L10.6468 7.39421C10.1561 8.36846 9.25639 9.09915 8.19315 9.26152L3.94016 9.91102C2.63155 10.0734 2.05904 11.6972 3.04049 12.6714L6.23023 15.9189C6.96632 16.6496 7.29348 17.705 7.1299 18.7605L6.39381 23.307C6.14844 24.6872 7.62063 25.6614 8.84745 25.0119L12.4461 23.0634C13.4276 22.4951 14.6544 22.4951 15.6359 23.0634L19.2345 25.0119C20.4614 25.6614 21.8518 24.6872 21.6882 23.307L20.8703 18.7605C20.7051 17.705 21.0339 16.6496 21.77 15.9189L24.9597 12.6714C25.9412 11.6972 25.3687 10.0734 24.06 9.91102L19.8071 9.26152Z" fill="currentColor"/>
                    </svg>
                  <span class="text-sm font-medium">{{ formatCount(videoInfo.stat?.favorite) }}</span>
                </div>
                <div class="flex items-center justify-center text-gray-700">
                  <svg class="w-5 h-5 mr-1" width="28" height="28" viewBox="0 0 28 28" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12.6058 10.3326V5.44359C12.6058 4.64632 13.2718 4 14.0934 4C14.4423 4 14.78 4.11895 15.0476 4.33606L25.3847 12.7221C26.112 13.3121 26.2087 14.3626 25.6007 15.0684C25.5352 15.1443 25.463 15.2144 25.3847 15.2779L15.0476 23.6639C14.4173 24.1753 13.4791 24.094 12.9521 23.4823C12.7283 23.2226 12.6058 22.8949 12.6058 22.5564V18.053C7.59502 18.053 5.37116 19.9116 2.57197 23.5251C2.47607 23.6489 2.00031 23.7769 2.00031 23.2122C2.00031 16.2165 3.90102 10.3326 12.6058 10.3326Z" fill="currentColor"/>
                  </svg>
                  <span class="text-sm font-medium">{{ formatCount(videoInfo.stat?.share) }}</span>
                </div>
              </div>
            </div>

            <!-- 右侧信息 -->
            <div class="w-full md:w-2/3 flex flex-col">
              <!-- 视频标题可点击 -->
              <a
                :href="`https://www.bilibili.com/video/${videoInfo.bvid}`"
                target="_blank"
                class="text-xl font-bold text-gray-900 mb-6 line-clamp-2 hover:text-[#fb7299] transition-colors duration-200"
              >
                {{ videoInfo.title }}
              </a>

              <!-- 作者信息区域 - UP 主可点击 -->
              <div v-if="videoInfo.owner" class="flex items-center mb-6 space-x-2">
                <a
                  :href="`https://space.bilibili.com/${videoInfo.owner.mid}`"
                  target="_blank"
                  class="flex items-center space-x-2 hover:text-[#fb7299] transition-colors duration-200"
                >
                  <img
                    v-if="videoInfo.owner.face"
                    :src="videoInfo.owner.face"
                    :alt="videoInfo.owner.name"
                    class="w-10 h-10 rounded-full object-cover border border-gray-200"
                  />
                  <div class="text-sm font-medium text-gray-900">{{ videoInfo.owner.name || '未知作者' }}</div>
                </a>
              </div>

              <!-- 视频动态信息 - 在作者信息下方，添加提示文字 -->
              <div v-if="videoInfo.dynamic" class="mb-6 text-xs bg-blue-50 border border-blue-200 px-2 py-1 rounded text-blue-700">
                <span class="font-medium mr-1">视频同步发布的动态：</span>{{ videoInfo.dynamic }}
              </div>

              <!-- 视频基本信息 -->
              <div class="mb-6 grid grid-cols-4 gap-2">
                <!-- 分区 显示 tname-tname_v2 -->
                <div v-if="videoInfo.tname" class="flex items-center text-gray-700 text-sm">
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  <span>{{ videoInfo.tname + (videoInfo.tname_v2 ? `-${videoInfo.tname_v2}` : '') }}</span>
                </div>

                <!-- 视频类型 -->
                <div v-if="videoInfo.copyright !== undefined" class="flex items-center text-gray-700 text-sm">
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <span>{{ videoInfo.copyright === 1 ? '原创' : '转载' }}</span>
                </div>

                <!-- 清晰度 -->
                <div v-if="videoInfo.dimension" class="flex items-center text-gray-700 text-sm">
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  </svg>
                  <span>{{ videoInfo.dimension.width }}x{{ videoInfo.dimension.height }}</span>
                </div>

                <!-- 评论数 -->
                <div v-if="videoInfo.stat?.reply" class="flex items-center text-gray-700 text-sm">
                  <svg class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>{{ formatCount(videoInfo.stat?.reply) }} 条评论</span>
                </div>
              </div>

              <!-- 多 P 信息 -->
              <div v-if="videoInfo.pages && videoInfo.pages.length > 1" class="mb-5">
                <h4 class="text-sm font-semibold text-gray-900 mb-5">分 P 列表</h4>
                <div class="max-h-40 overflow-y-auto border border-gray-200 rounded-md">
                  <div
                    v-for="(page, index) in videoInfo.pages"
                    :key="index"
                    class="flex items-center p-2 text-sm hover:bg-gray-100 border-b border-gray-100 last:border-b-0"
                  >
                    <span class="mr-2 bg-gray-200 text-gray-700 w-6 h-6 flex items-center justify-center rounded-full text-xs">{{ page.page }}</span>
                    <span class="mr-auto truncate">{{ page.part }}</span>
                    <span class="text-gray-500 text-xs">{{ formatDuration(page.duration) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 视频简介 - 移动到外层，占据整行 -->
          <div v-if="videoInfo.desc" class="mt-3">
            <h4 class="text-sm font-semibold text-gray-900 mb-2">视频简介</h4>
            <p class="text-sm text-gray-600 bg-gray-50 p-2 rounded-md max-h-32 overflow-y-auto whitespace-pre-wrap">{{ videoInfo.desc }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 用户视频列表 -->
    <div v-if="downloadType === 'user' && inputValue" class="mt-6">
      <UserVideos :mid="inputValue" />
    </div>

    <!-- 下载对话框 -->
    <DownloadDialog
      v-model:show="showDownloadDialog"
      :video-info="downloadVideoInfo"
      :up-user-videos="upUserVideosList"
      @download-complete="handleDownloadComplete"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import { getLoginStatus, downloadVideo, downloadUserVideos, getVideoInfo } from '../../../api/api'
import DownloadDialog from '../DownloadDialog.vue'
import SimpleSearchBar from '../SimpleSearchBar.vue'
import CustomDropdown from '../CustomDropdown.vue'
import UserVideos from '../UserVideos.vue'

// 下载类型
const downloadType = ref('video')
const inputValue = ref('')

// 下载类型选项
const downloadTypeOptions = [
  { value: 'video', label: '单个视频' },
  { value: 'user', label: 'UP 主投稿' }
]

// 获取显示文本
const getDownloadTypeLabel = (value) => {
  const option = downloadTypeOptions.find(opt => opt.value === value)
  return option ? option.label : '单个视频'
}

// 处理下载类型变更
const onDownloadTypeChange = (value) => {
  downloadType.value = value
  inputValue.value = '' // 清空输入框
  videoInfo.value = {} // 重置视频信息
}

// 下载选项
const downloadCover = ref(true)
const onlyAudio = ref(false)

// 下载状态
const isDownloading = ref(false)
const showDownloadDialog = ref(false)

// 视频信息
const videoInfo = ref({})
const hasVideoInfo = computed(() => !!videoInfo.value?.bvid)

// 下载对话框的视频信息
const downloadVideoInfo = ref({})

// 添加用于存储UP主视频列表的ref
const upUserVideosList = ref([])

// 从 BV 链接提取 BV 号
const extractBvid = (input) => {
  // 如果已经是 BV 开头的格式，直接返回
  if (/^BV[a-zA-Z0-9]{10}$/.test(input)) {
    return input
  }

  // 尝试从 URL 中提取 BV 号
  const match = input.match(/\/video\/(BV[a-zA-Z0-9]{10})/)
  if (match && match[1]) {
    return match[1]
  }

  return input // 返回原始输入，让后端处理错误
}

// 监听输入框内容变化，自动提取并获取视频信息
watch(inputValue, async (newValue) => {
  if (downloadType.value === 'video') {
    if (newValue) {
      const extractedBvid = extractBvid(newValue)
      if (/^BV[a-zA-Z0-9]{10}$/.test(extractedBvid)) {
        // 自动获取视频信息
        await handleVideoInfo(extractedBvid)
      }
    } else {
      // 当输入框被清空时，重置视频信息
      videoInfo.value = {}
    }
  }
})

// 获取视频信息单独拆分成函数
const handleVideoInfo = async (bvid) => {
  isDownloading.value = true
  try {
    // 获取视频详细信息
    const response = await getVideoInfo({ bvid })
    if (response.data.status === 'success') {
      videoInfo.value = response.data.data
      console.log('获取到视频信息：', videoInfo.value)
    } else {
      throw new Error(response.data.message || '获取视频信息失败')
    }
  } catch (error) {
    console.error('处理失败：', error)
    showNotify({ type: 'danger', message: error.message || '获取信息失败' })
  } finally {
    isDownloading.value = false
  }
}

// 处理下载
const handleDownload = async () => {
  try {
    if (!inputValue.value) return

    isDownloading.value = true

    // 检查登录状态
    const loginResponse = await getLoginStatus()
    if (loginResponse.data.code !== 0 || !loginResponse.data.data.isLogin) {
      showNotify({ type: 'warning', message: '请先登录 B 站账号' })
      return
    }

    if (downloadType.value === 'video') {
      // 如果已有视频信息，直接开始下载
      if (hasVideoInfo.value) {
        startDownload()
      } else {
        // 没有视频信息，先获取信息再开始下载
        const extractedBvid = extractBvid(inputValue.value)
        await handleVideoInfo(extractedBvid)
        if (hasVideoInfo.value) {
          startDownload()
        }
      }
    } else {
      // 用户投稿下载 - 先获取视频列表信息
      try {
        console.log('获取UP主视频信息，UID:', inputValue.value)
        const { getUserVideos } = await import('../../../api/api')

        // 先获取第一个视频以获取封面
        const response = await getUserVideos({
          mid: inputValue.value,
          pn: 1,
          ps: 1 // 只获取第一个视频，用于显示封面
        })

        console.log('获取UP主视频响应:', response.data)

        // 检查响应
        if (response.data.status === 'success' &&
            response.data.data.list.vlist &&
            response.data.data.list.vlist.length > 0) {

          const firstVideo = response.data.data.list.vlist[0]
          console.log('第一个视频信息:', firstVideo)
          console.log('视频封面URL:', firstVideo.pic)

          // 使用第一个视频的信息
          downloadVideoInfo.value = {
            title: `UP 主 ${firstVideo.author || inputValue.value} 的全部投稿视频`,
            author: firstVideo.author || '',
            bvid: firstVideo.bvid || '',
            pic: firstVideo.pic || '',
            cover: firstVideo.pic || '',
            cid: 0,
            // 特殊字段标识这是用户视频下载
            is_user_videos: true,
            user_id: inputValue.value
          }

          console.log('准备显示下载弹窗，传递的视频信息:', downloadVideoInfo.value)
          console.log('检查封面URL是否正确:', downloadVideoInfo.value.pic)

          // 开始预加载更多视频的信息，获取页数和投稿总数
          await fetchUpUserVideosList(inputValue.value)
        } else {
          console.warn('未获取到UP主视频信息，使用默认值')
          // 使用默认信息
          downloadVideoInfo.value = {
            title: `UP 主 ${inputValue.value} 的全部投稿视频`,
            author: '',
            bvid: '',
            cover: '',
            pic: '',
            cid: 0,
            // 特殊字段标识这是用户视频下载
            is_user_videos: true,
            user_id: inputValue.value
          }
        }
      } catch (error) {
        console.error('获取UP主视频信息失败:', error)
        // 使用默认信息
        downloadVideoInfo.value = {
          title: `UP 主 ${inputValue.value} 的全部投稿视频`,
          author: '',
          bvid: '',
          cover: '',
          pic: '',
          cid: 0,
          // 特殊字段标识这是用户视频下载
          is_user_videos: true,
          user_id: inputValue.value
        }
      }

      // 显示下载对话框
      showDownloadDialog.value = true
    }
  } catch (error) {
    console.error('处理失败：', error)
    showNotify({ type: 'danger', message: error.message || '处理失败' })
    isDownloading.value = false
  }
}

// 获取UP主的视频列表，预加载视频数据
const fetchUpUserVideosList = async (userId) => {
  try {
    const { getUserVideos } = await import('../../../api/api')

    // 先获取第一页，确定总视频数
    const response = await getUserVideos({
      mid: userId,
      pn: 1,
      ps: 30
    })

    if (!response.data || response.data.status !== 'success') {
      console.warn('获取UP主视频列表失败')
      return
    }

    // 保存第一页的视频
    const videos = response.data.data.list.vlist || []
    upUserVideosList.value = videos

    // 尝试获取总页数
    const count = response.data.data.page?.count || 0
    if (count > 30) {
      // 如果总数超过30个，只预加载前2页
      const totalPages = Math.min(3, Math.ceil(count / 30))

      for (let page = 2; page <= totalPages; page++) {
        try {
          const pageResponse = await getUserVideos({
            mid: userId,
            pn: page,
            ps: 30
          })

          if (pageResponse.data && pageResponse.data.status === 'success') {
            const pageVideos = pageResponse.data.data.list.vlist || []
            upUserVideosList.value = [...upUserVideosList.value, ...pageVideos]
          }

          // 防止频繁请求
          await new Promise(resolve => setTimeout(resolve, 300))
        } catch (err) {
          console.error(`获取第${page}页UP主视频列表失败:`, err)
        }
      }
    }

    console.log(`已预加载 ${upUserVideosList.value.length} 个视频信息`)
  } catch (error) {
    console.error('预加载UP主视频列表失败:', error)
  }
}

// 格式化时长
const formatDuration = (seconds) => {
  if (!seconds) return '未知时长'

  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const remainingSeconds = seconds % 60

  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
  } else {
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }
}

// 格式化时间戳为秒级时间显示
const formatDetailedTimestamp = (timestamp) => {
  if (!timestamp) return '未知时间'

  const date = new Date(timestamp * 1000)
  const year = date.getFullYear()
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const day = date.getDate().toString().padStart(2, '0')
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  const seconds = date.getSeconds().toString().padStart(2, '0')

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// 格式化数字（播放、点赞等）
const formatCount = (count) => {
  if (!count && count !== 0) return '0'

  if (count >= 10000) {
    return (count / 10000).toFixed(1) + '万'
  }

  return count.toString()
}

// 开始下载
const startDownload = () => {
  try {
    console.log('开始下载，类型:', downloadType.value)

    if (downloadType.value === 'video') {
      // 设置视频信息
      downloadVideoInfo.value = {
        title: videoInfo.value.title,
        author: videoInfo.value.owner?.name || '',
        bvid: videoInfo.value.bvid,
        cover: videoInfo.value.pic,
        pic: videoInfo.value.pic,
        cid: videoInfo.value.cid
      }
      console.log('设置单个视频下载信息:', downloadVideoInfo.value)
    } else {
      // 此时应该已经在 handleDownload 中设置了用户投稿下载信息
      // 确保必要的字段存在
      if (!downloadVideoInfo.value.is_user_videos) {
        console.warn('用户视频下载信息不完整，重新设置')
        downloadVideoInfo.value = {
          ...downloadVideoInfo.value,
          is_user_videos: true,
          user_id: inputValue.value
        }
      }
      console.log('用户视频下载信息:', downloadVideoInfo.value)
    }

    // 显示下载对话框
    showDownloadDialog.value = true
  } catch (error) {
    console.error('开始下载失败：', error)
    showNotify({ type: 'danger', message: error.message || '开始下载失败' })
  }
}

// 处理下载完成
const handleDownloadComplete = () => {
  showNotify({ type: 'success', message: '下载任务已完成' })
  // 不自动重置输入，让用户可以再次点击下载
}
</script>

<style scoped>
/* 移除搜索框的默认样式 */
input[type="search"]::-webkit-search-decoration,
input[type="search"]::-webkit-search-cancel-button,
input[type="search"]::-webkit-search-results-button,
input[type="search"]::-webkit-search-results-decoration {
  display: none;
}

/* 移除输入框的默认 focus 样式 */
input:focus {
  box-shadow: none !important;
  outline: none !important;
}

:deep(.custom-dropdown-trigger) {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
}

/* 确保下拉菜单按钮文本不会折行 */
:deep(.custom-dropdown-trigger span) {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>