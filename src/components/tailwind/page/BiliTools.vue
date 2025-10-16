<template>
  <div class="min-h-screen bg-gray-50/30 dark:bg-gray-900">
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- 主内容卡片 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700">
          <!-- 标签导航 -->
          <div class="border-b border-gray-200 dark:border-gray-700">
            <nav class="-mb-px flex px-6 overflow-x-auto" aria-label="B站工具选项卡">
              <button
                @click="activeTab = 'video-stats'"
                class="py-4 px-3 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'video-stats'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <span>视频观看总时长</span>
              </button>

              <button
                @click="activeTab = 'video-download'"
                class="ml-8 py-4 px-3 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'video-download'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                <span>视频下载</span>
              </button>

              <button
                @click="activeTab = 'comment-query'"
                class="ml-8 py-4 px-3 border-b-2 font-medium text-sm flex items-center space-x-2"
                :class="activeTab === 'comment-query'
                  ? 'border-[#fb7299] text-[#fb7299]'
                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'"
              >
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <span>评论查询</span>
              </button>
            </nav>
          </div>

          <!-- 内容区域 -->
          <div class="transition-all duration-300">
            <!-- 视频观看时长信息 -->
            <div v-if="activeTab === 'video-stats'" class="animate-fadeIn">
              <div class="bg-white dark:bg-gray-800">
                <!-- 致谢信息 -->
                <div class="mb-3 flex items-center justify-center h-7 px-3 py-0 bg-[#fb7299]/5 rounded-md border border-[#fb7299]/20 mx-6 mt-4">
                  <a href="https://www.xiaoheihe.cn/app/user/profile/55542982" target="_blank" rel="noopener noreferrer" class="flex items-center hover:opacity-80 transition-opacity mr-1.5">
                    <img src="https://imgheybox.max-c.com/avatar/2025/02/16/20a399e3b78c0db29b5ec14361b3e348.png?imageMogr2/thumbnail/400x400%3E" alt="shengyI头像" class="h-5 w-5 rounded-full mr-1.5" />
                  </a>
                  <span class="text-xs text-gray-700 dark:text-gray-300">感谢小黑盒用户
                    <a
                      href="https://www.xiaoheihe.cn/app/bbs/link/153880174"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="text-[#fb7299] font-medium hover:underline"
                    >
                      shengyI
                    </a>
                    提供思路
                  </span>
                </div>

                <!-- 输入表单 -->
                <div class="px-4 py-4 border-b border-gray-100 dark:border-gray-700">
                  <h2 class="text-base font-medium text-gray-900 dark:text-gray-100 mb-2">视频时长信息查询</h2>
                  <p class="text-xs text-gray-600 dark:text-gray-400 mb-3">
                    输入B站视频BV号，查询该视频的观看时长信息。<span class="text-[#fb7299] font-medium">注意：只有被UP主添加到合集(season_id)的视频才能查询到观看时长数据。</span>
                  </p>

                  <div class="relative">
                    <input
                      v-model="bvid"
                      type="text"
                      placeholder="输入视频BV号，例如：BV1hu411h7ot"
                      class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-transparent text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#fb7299] focus:border-transparent pr-10"
                      @input="debouncedFetchVideoStats"
                    />
                    <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                      <svg v-if="loading" class="animate-spin h-5 w-5 text-[#fb7299]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                    </div>
                  </div>

                  <div class="mt-3 flex items-center">
                    <input
                      type="checkbox"
                      id="use-sessdata"
                      v-model="useSessdata"
                      class="h-4 w-4 text-[#fb7299] focus:ring-[#fb7299] border-gray-300 rounded"
                      @change="bvid && debouncedFetchVideoStats()"
                    />
                    <label for="use-sessdata" class="ml-2 block text-sm text-gray-600">
                      使用登录状态查询（用于需要登录才能查看的视频）
                    </label>
                  </div>
                </div>

                <!-- 结果展示 -->
                <div v-if="videoStats" class="px-6 py-5">
                  <!-- 如果是合集视频 -->
                  <div v-if="videoStats.status === 'success'">
                    <!-- 查询的视频信息 -->
                    <div v-if="queriedVideo" class="mb-4 bg-white dark:bg-gray-800 border border-[#fb7299]/20 rounded-lg overflow-hidden">
                      <div class="bg-[#fb7299]/5 px-3 py-2 border-b border-[#fb7299]/20">
                        <h3 class="text-sm font-medium text-gray-900 flex items-center">
                          <svg class="w-4 h-4 mr-1.5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                          </svg>
                          查询视频详情
                        </h3>
                      </div>
                      <div class="p-3">
                        <div class="flex flex-col md:flex-row">
                          <div class="md:w-52 flex-shrink-0 mb-3 md:mb-0">
                            <img
                              :src="queriedVideo.cover"
                              class="w-full h-28 md:h-32 object-cover rounded shadow-sm"
                              alt="视频封面"
                            />
                          </div>
                          <div class="md:ml-4 flex-1">
                            <h4 class="text-sm font-medium text-gray-900 hover:text-[#fb7299]">
                              <a :href="`https://www.bilibili.com/video/${queriedVideo.bvid}`" target="_blank">{{ queriedVideo.title }}</a>
                            </h4>
                            <p class="text-xs text-gray-500 mt-1">BV: {{ queriedVideo.bvid }}</p>

                            <div class="mt-3 grid grid-cols-2 md:grid-cols-5 gap-2">
                              <div class="bg-gray-50 dark:bg-gray-700 p-2 rounded-lg">
                                <p class="text-xs text-gray-500">视频时长</p>
                                <p class="text-sm font-semibold text-gray-900">{{ formatDuration(queriedVideo.duration) }}</p>
                              </div>
                              <div class="bg-gray-50 dark:bg-gray-700 p-2 rounded-lg">
                                <p class="text-xs text-gray-500">观看次数</p>
                                <p class="text-sm font-semibold text-gray-900">{{ formatNumber(queriedVideo.vv) }}</p>
                              </div>
                              <div class="bg-gray-50 dark:bg-gray-700 p-2 rounded-lg">
                                <p class="text-xs text-gray-500">总观看时长</p>
                                <p class="text-sm font-semibold text-[#fb7299]">
                                  {{ formatDurationHours(queriedVideo.vt) }}
                                </p>
                                <p class="text-xs text-gray-500">{{ formatDurationDays(queriedVideo.vt) }}</p>
                              </div>
                              <div class="bg-gray-50 dark:bg-gray-700 p-2 rounded-lg">
                                <p class="text-xs text-gray-500">平均观看时长</p>
                                <p class="text-sm font-semibold text-gray-900">
                                  {{ formatDuration(Math.round((queriedVideo.vt * 60) / queriedVideo.vv)) }}
                                </p>
                              </div>
                              <div class="bg-gray-50 p-2 rounded-lg">
                                <p class="text-xs text-gray-500">完播率</p>
                                <p class="text-sm font-semibold text-gray-900">
                                  {{ secondsToPercent(Math.round((queriedVideo.vt * 60) / queriedVideo.vv), queriedVideo.duration) }}%
                                </p>
                                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-1">
                                  <div
                                    class="bg-[#fb7299] h-1.5 rounded-full"
                                    :style="`width: ${Math.min(100, Math.round(((queriedVideo.vt * 60) / queriedVideo.vv) / queriedVideo.duration * 100))}%`"
                                  ></div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- 视频列表 -->
                    <div class="mt-4">
                      <h3 class="text-base font-medium text-gray-900 mb-3 flex items-center">
                        <svg class="w-4 h-4 mr-2 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
                        </svg>
                        视频列表
                      </h3>
                      <div class="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
                        <table class="min-w-full divide-y divide-gray-200">
                          <thead class="bg-gray-50 dark:bg-gray-800">
                            <tr>
                              <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">视频信息</th>
                              <th
                                scope="col"
                                class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                                @click="sortBy('duration')"
                              >
                                <div class="flex items-center">
                                  时长
                                  <svg
                                    v-if="sortKey === 'duration'"
                                    class="w-3 h-3 ml-1"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                  >
                                    <path
                                      stroke-linecap="round"
                                      stroke-linejoin="round"
                                      stroke-width="2"
                                      :d="sortDirection === 'asc'
                                        ? 'M5 15l7-7 7 7'
                                        : 'M19 9l-7 7-7-7'"
                                    />
                                  </svg>
                                </div>
                              </th>
                              <th
                                scope="col"
                                class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                                @click="sortBy('vv')"
                              >
                                <div class="flex items-center">
                                  观看次数
                                  <svg
                                    v-if="sortKey === 'vv'"
                                    class="w-3 h-3 ml-1"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                  >
                                    <path
                                      stroke-linecap="round"
                                      stroke-linejoin="round"
                                      stroke-width="2"
                                      :d="sortDirection === 'asc'
                                        ? 'M5 15l7-7 7 7'
                                        : 'M19 9l-7 7-7-7'"
                                    />
                                  </svg>
                                </div>
                              </th>
                              <th
                                scope="col"
                                class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                                @click="sortBy('vt')"
                              >
                                <div class="flex items-center">
                                  总观看时长
                                  <svg
                                    v-if="sortKey === 'vt'"
                                    class="w-3 h-3 ml-1"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                  >
                                    <path
                                      stroke-linecap="round"
                                      stroke-linejoin="round"
                                      stroke-width="2"
                                      :d="sortDirection === 'asc'
                                        ? 'M5 15l7-7 7 7'
                                        : 'M19 9l-7 7-7-7'"
                                    />
                                  </svg>
                                </div>
                              </th>
                              <th
                                scope="col"
                                class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                                @click="sortBy('avgWatchTime')"
                              >
                                <div class="flex items-center">
                                  平均观看时长
                                  <svg
                                    v-if="sortKey === 'avgWatchTime'"
                                    class="w-3 h-3 ml-1"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                  >
                                    <path
                                      stroke-linecap="round"
                                      stroke-linejoin="round"
                                      stroke-width="2"
                                      :d="sortDirection === 'asc'
                                        ? 'M5 15l7-7 7 7'
                                        : 'M19 9l-7 7-7-7'"
                                    />
                                  </svg>
                                </div>
                              </th>
                              <th
                                scope="col"
                                class="px-3 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                                @click="sortBy('finishRate')"
                              >
                                <div class="flex items-center">
                                  完播率
                                  <svg
                                    v-if="sortKey === 'finishRate'"
                                    class="w-3 h-3 ml-1"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                  >
                                    <path
                                      stroke-linecap="round"
                                      stroke-linejoin="round"
                                      stroke-width="2"
                                      :d="sortDirection === 'asc'
                                        ? 'M5 15l7-7 7 7'
                                        : 'M19 9l-7 7-7-7'"
                                    />
                                  </svg>
                                </div>
                              </th>

                            </tr>
                          </thead>
                          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                            <tr v-for="video in sortedVideos" :key="video.bvid" class="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                              :class="{'bg-[#fb7299]/5 border-l-4 border-[#fb7299]': video.bvid === bvid}"
                            >
                              <td class="px-3 py-2 whitespace-nowrap">
                                <div class="flex items-center">
                                  <div class="flex-shrink-0 h-10 w-16">
                                    <img class="h-10 w-16 object-cover rounded shadow-sm" :src="normalizeImageUrl(video.cover)" alt="" />
                                  </div>
                                  <div class="ml-3 max-w-xs">
                                    <div class="text-xs font-medium text-gray-900 dark:text-gray-100 truncate hover:text-[#fb7299]" :title="video.title">
                                      <a :href="`https://www.bilibili.com/video/${video.bvid}`" target="_blank">{{ video.title }}</a>
                                    </div>
                                    <div class="text-xs text-gray-500">BV: {{ video.bvid }}</div>
                                  </div>
                                </div>
                              </td>
                              <td class="px-3 py-2 whitespace-nowrap">
                                <div class="text-xs text-gray-900 dark:text-gray-100">{{ formatDuration(video.duration) }}</div>
                              </td>
                              <td class="px-3 py-2 whitespace-nowrap">
                                <div class="text-xs text-gray-900 dark:text-gray-100 font-medium">{{ formatNumber(video.vv) }}</div>
                              </td>
                              <td class="px-3 py-2 whitespace-nowrap">
                                <div class="text-xs font-medium text-[#fb7299]">{{ formatDurationHours(video.vt) }}</div>
                                <div class="text-xs text-gray-500">{{ formatDurationDays(video.vt) }}</div>
                              </td>
                              <td class="px-3 py-2 whitespace-nowrap">
                                <div class="text-xs text-gray-900 dark:text-gray-100">{{ formatDuration(Math.round((video.vt * 60) / video.vv)) }}</div>
                              </td>
                              <td class="px-3 py-2 whitespace-nowrap">
                                <div class="text-xs text-gray-900 dark:text-gray-100">{{ secondsToPercent(Math.round((video.vt * 60) / video.vv), video.duration) }}%</div>
                                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1 mt-1">
                                  <div class="bg-[#fb7299] h-1 rounded-full" :style="`width: ${Math.min(100, Math.round(((video.vt * 60) / video.vv) / video.duration * 100))}%`"></div>
                                </div>
                              </td>

                            </tr>
                          </tbody>
                        </table>

                      </div>
                    </div>
                  </div>

                  <!-- 如果不是合集视频 -->
                  <div v-else-if="videoStats.status === 'info'" class="p-5">
                    <div class="bg-blue-50 p-4 rounded-lg flex">
                      <svg class="w-5 h-5 text-blue-400 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <p class="text-sm text-blue-700">{{ videoStats.message }}</p>
                    </div>
                  </div>

                  <!-- 如果发生错误 -->
                  <div v-else-if="videoStats.status === 'error'" class="p-5">
                    <div class="bg-red-50 p-4 rounded-lg flex">
                      <svg class="w-5 h-5 text-red-400 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <p class="text-sm text-red-700">{{ videoStats.message }}</p>
                    </div>
                  </div>
                </div>

                <!-- 加载中状态 -->
                <div v-if="loading && !videoStats" class="flex justify-center items-center py-16">
                  <div class="animate-spin h-10 w-10 border-4 border-[#fb7299] border-t-transparent rounded-full"></div>
                  <p class="ml-4 text-gray-600">正在获取视频数据...</p>
                </div>

                <!-- 空状态 -->
                <div v-if="!loading && !videoStats" class="flex flex-col items-center justify-center py-16 px-6 text-center">
                  <svg class="w-16 h-16 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  <p class="mt-4 text-gray-500">输入视频BV号后查询观看时长信息</p>
                </div>
              </div>
            </div>

            <!-- 视频下载 -->
            <div v-if="activeTab === 'video-download'" class="animate-fadeIn">
              <VideoDownloader />
            </div>

            <!-- 评论查询 -->
            <div v-if="activeTab === 'comment-query'" class="animate-fadeIn">
              <div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                <!-- 用户ID输入区域 -->
                <div class="mb-6 bg-transparent">
                  <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-3">B站评论查询</h2>
                  <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    输入B站用户UID，查询该用户的全部评论记录。
                  </p>

                  <div class="flex space-x-3">
                    <div class="flex-1">
                      <div class="relative">
                        <input
                          v-model="queryUserId"
                          type="text"
                          placeholder="输入用户UID，例如：12345678"
                          class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-transparent text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-[#fb7299] focus:border-transparent pr-10"
                          @keyup.enter="fetchUserComments()"
                        />
                        <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                          <svg v-if="commentLoading" class="animate-spin h-5 w-5 text-[#fb7299]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <button
                            v-else
                            @click="fetchUserComments()"
                            class="text-[#fb7299] hover:text-[#fb7299]/80 transition-colors"
                          >
                            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 筛选区域 -->
                <div v-if="comments.length > 0 || commentLoading" class="mb-6 bg-transparent">
                  <div class="mb-4">
                    <!-- 总评论数显示 -->
                    <div class="mb-3 flex items-center text-sm text-gray-600">
                      <span>共</span>
                      <span class="mx-1 text-[#fb7299] font-medium">{{ commentTotal }}</span>
                      <span>条评论</span>
                    </div>

                    <div class="flex flex-nowrap items-center space-x-2">
                      <!-- 关键词搜索 -->
                      <div class="flex-1 min-w-0">
                        <div class="relative">
                          <div class="flex h-9 items-center rounded-md border border-gray-300 dark:border-gray-600 bg-transparent focus-within:border-[#fb7299] transition-colors duration-200">
                            <!-- 搜索图标 -->
                            <div class="pl-3 text-gray-400">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                              </svg>
                            </div>

                            <!-- 输入框 -->
                            <input
                              v-model="commentKeyword"
                              type="search"
                              placeholder="搜索评论内容..."
                              class="h-full w-full border-none bg-transparent px-2 pr-3 text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-0 text-xs leading-none"
                              @keyup.enter="handleCommentSearch"
                            />
                          </div>
                        </div>
                      </div>

                      <!-- 评论类型筛选 -->
                      <div class="w-24 flex-shrink-0">
                        <div class="relative">
                          <button
                            @click="toggleCommentTypeDropdown"
                            type="button"
                            class="w-full py-1.5 px-2 border border-gray-300 dark:border-gray-600 rounded-md text-xs text-gray-800 dark:text-gray-200 bg-transparent focus:border-[#fb7299] focus:outline-none focus:ring focus:ring-[#fb7299]/20 flex items-center justify-between transition-colors duration-200 h-9 whitespace-nowrap overflow-hidden"
                          >
                            <span class="truncate mr-1">{{ getCommentTypeText(commentType) }}</span>
                            <svg class="w-3 h-3 text-[#fb7299] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                          </button>

                          <!-- 评论类型下拉菜单 -->
                          <div
                            v-if="showCommentTypeDropdown"
                            class="absolute z-10 mt-1 w-full rounded-md bg-white dark:bg-gray-800 shadow-lg ring-1 ring-black ring-opacity-5 dark:ring-white/10 focus:outline-none"
                          >
                            <div class="py-1">
                              <button
                                v-for="option in commentTypeOptions"
                                :key="option.value"
                                @click="selectCommentType(option.value)"
                                class="w-full px-2 py-1 text-xs text-left hover:bg-[#fb7299]/5 hover:text-[#fb7299] transition-colors flex items-center whitespace-nowrap"
                                :class="{'text-[#fb7299] bg-[#fb7299]/5 font-medium': commentType === option.value}"
                              >
                                {{ option.label }}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- 内容类型筛选 -->
                      <div class="w-24 flex-shrink-0">
                        <div class="relative">
                          <button
                            @click="toggleContentTypeDropdown"
                            type="button"
                            class="w-full py-1.5 px-2 border border-gray-300 dark:border-gray-600 rounded-md text-xs text-gray-800 dark:text-gray-200 bg-transparent focus:border-[#fb7299] focus:outline-none focus:ring focus:ring-[#fb7299]/20 flex items-center justify-between transition-colors duration-200 h-9 whitespace-nowrap overflow-hidden"
                          >
                            <span class="truncate mr-1">{{ getContentTypeText(contentTypeFilter) }}</span>
                            <svg class="w-3 h-3 text-[#fb7299] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                            </svg>
                          </button>

                          <!-- 内容类型下拉菜单 -->
                          <div
                            v-if="showContentTypeDropdown"
                            class="absolute z-10 mt-1 w-full rounded-md bg-white dark:bg-gray-800 shadow-lg ring-1 ring-black ring-opacity-5 dark:ring-white/10 focus:outline-none"
                          >
                            <div class="py-1">
                              <button
                                v-for="option in contentTypeOptions"
                                :key="option.value"
                                @click="selectContentType(option.value)"
                                class="w-full px-2 py-1 text-xs text-left hover:bg-[#fb7299]/5 hover:text-[#fb7299] transition-colors flex items-center whitespace-nowrap"
                                :class="{'text-[#fb7299] bg-[#fb7299]/5 font-medium': contentTypeFilter === option.value}"
                              >
                                {{ option.label }}
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 评论列表 -->
                <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
                  <!-- 评论项 -->
                  <div v-if="!commentLoading && comments.length > 0" class="divide-y divide-gray-100">
                    <div v-for="comment in comments" :key="comment.rpid" class="p-4 md:p-6">
                      <div class="space-y-2">
                        <!-- 评论内容 -->
                        <p class="text-gray-800 text-sm md:text-base whitespace-pre-wrap leading-relaxed">{{ comment.message }}</p>

                        <!-- 评论元数据 -->
                        <div class="flex items-center justify-between text-xs text-gray-500">
                          <div class="flex items-center space-x-3">
                            <span :class="comment.type === 1 ? 'text-[#fb7299]' : 'text-[#fb7299]'">
                              {{ getCommentTypeDisplay(comment.type) }}
                            </span>
                            <span>{{ comment.time_str }}</span>
                          </div>

                          <a
                            :href="getCommentLink(comment)"
                            target="_blank"
                            class="text-[#fb7299] hover:text-[#fb7299]/80 transition-colors"
                          >
                            查看原文 →
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- 加载状态 -->
                  <div v-if="commentLoading" class="flex justify-center items-center py-16">
                    <div class="flex flex-col items-center">
                      <div class="animate-spin h-8 w-8 border-3 border-[#fb7299] border-t-transparent rounded-full"></div>
                      <p class="text-gray-500 text-sm mt-4">加载评论中...</p>
                    </div>
                  </div>

                  <!-- 空状态 -->
                  <div v-if="!commentLoading && comments.length === 0" class="flex justify-center items-center py-16">
                    <div class="flex flex-col items-center">
                      <div class="bg-[#fb7299]/5 rounded-full p-3 mb-3">
                        <svg class="w-8 h-8 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                        </svg>
                      </div>
                      <p class="text-gray-600 dark:text-gray-300 font-medium">暂无评论数据</p>
                      <p v-if="hasActiveCommentFilters" class="text-gray-500 dark:text-gray-400 text-sm mt-1 text-center max-w-sm">
                        尝试调整搜索条件
                      </p>
                      <button
                        v-if="hasActiveCommentFilters"
                        @click="clearCommentFilters"
                        class="mt-4 px-4 py-2 text-white bg-[#fb7299] hover:bg-[#fb7299]/90 rounded-md text-sm transition-colors"
                      >
                        清除筛选
                      </button>
                    </div>
                  </div>
                </div>

                <!-- 分页控件 -->
                <div v-if="commentTotalPages > 0" class="mt-6 flex justify-center">
                  <div class="mx-auto mb-5 mt-8 max-w-4xl lm:text-xs">
                    <div class="flex justify-between items-center space-x-4 lm:mx-5">
                      <button
                        @click="handleCommentPageChange(commentCurrentPage - 1)"
                        :disabled="commentCurrentPage === 1"
                        class="flex items-center text-gray-500 hover:text-[#fb7299] disabled:opacity-40 disabled:cursor-not-allowed transition-colors px-3 py-2"
                      >
                        <svg class="w-5 h-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                        </svg>
                        <span class="hidden sm:inline">上一页</span>
                      </button>

                      <div class="flex items-center text-gray-700 lm:text-xs">
                        <div class="relative mx-1 inline-block">
                          <input
                            type="number"
                            v-model="commentPageInput"
                            @keyup.enter="handleCommentJumpPage"
                            @blur="handleCommentJumpPage"
                            @focus="$event.target.select()"
                            min="1"
                            :max="commentTotalPages"
                            class="h-8 w-12 rounded border border-gray-200 dark:border-gray-600 px-2 text-center text-gray-700 dark:text-gray-200 bg-transparent transition-colors [appearance:textfield] hover:border-[#fb7299] focus:border-[#fb7299] focus:outline-none focus:ring-1 focus:ring-[#fb7299]/30 lm:h-6 lm:w-10 lm:text-xs [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                          />
                        </div>
                        <span class="text-gray-500 mx-1">/ {{ commentTotalPages }}</span>
                      </div>

                      <button
                        @click="handleCommentPageChange(commentCurrentPage + 1)"
                        :disabled="commentCurrentPage === commentTotalPages"
                        class="flex items-center text-gray-500 hover:text-[#fb7299] disabled:opacity-40 disabled:cursor-not-allowed transition-colors px-3 py-2"
                      >
                        <span class="hidden sm:inline">下一页</span>
                        <svg class="w-5 h-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                      </button>
                    </div>
                  </div>
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
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute } from 'vue-router'
import VideoDownloader from './VideoDownloader.vue'
import { showNotify } from 'vant'
import 'vant/es/notify/style'
import { getVideoSeasonInfo, getComments } from '../../../api/api'
import { normalizeImageUrl } from '@/utils/imageUrl.js'

const route = useRoute()

// 当前激活的标签
const activeTab = ref('video-stats')

// 监听路由变化以更新激活的标签
watch(
  () => route.query.tab,
  (tab) => {
    if (tab && ['video-stats', 'video-download', 'comment-query'].includes(tab)) {
      activeTab.value = tab
    }
  },
  { immediate: true }
)

// 组件挂载时根据URL初始化标签
onMounted(() => {
  const { tab } = route.query
  if (tab && ['video-stats', 'video-download', 'comment-query'].includes(tab)) {
    activeTab.value = tab
  }
})

// 视频观看时长数据
const bvid = ref('')
const videoStats = ref(null)
const loading = ref(false)
const useSessdata = ref(true)

// 排序状态
const sortKey = ref('vt')  // 默认按总观看时长排序
const sortDirection = ref('desc')  // 默认降序

// 查询的视频信息
const queriedVideo = computed(() => {
  if (!videoStats.value || !videoStats.value.videos || !bvid.value) return null
  return videoStats.value.videos.find(v => v.bvid.toLowerCase() === bvid.value.toLowerCase())
})

// 计算合集总观看时长
const totalWatchTime = computed(() => {
  if (!videoStats.value || !videoStats.value.videos) return 0
  return videoStats.value.videos.reduce((total, video) => total + video.vt, 0)
})

// 排序后的视频列表
const sortedVideos = computed(() => {
  if (!videoStats.value || !videoStats.value.videos) return []

  const videos = [...videoStats.value.videos]

  return videos.sort((a, b) => {
    let aValue, bValue

    if (sortKey.value === 'avgWatchTime') {
      aValue = a.vt / a.vv
      bValue = b.vt / b.vv
    } else if (sortKey.value === 'finishRate') {
      // 计算完播率：平均观看时长(秒) / 视频时长(秒) * 100
      aValue = Math.min(100, Math.round(((a.vt * 60) / a.vv) / a.duration * 100))
      bValue = Math.min(100, Math.round(((b.vt * 60) / b.vv) / b.duration * 100))
    } else {
      aValue = a[sortKey.value]
      bValue = b[sortKey.value]
    }

    if (sortDirection.value === 'asc') {
      return aValue - bValue
    } else {
      return bValue - aValue
    }
  })
})

// 切换排序
const sortBy = (key) => {
  if (sortKey.value === key) {
    // 如果已经是按这个键排序，则切换方向
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    // 否则切换排序字段，默认降序
    sortKey.value = key
    sortDirection.value = 'desc'
  }
}

// 防抖函数
let timeout = null
const debouncedFetchVideoStats = () => {
  clearTimeout(timeout)
  timeout = setTimeout(() => {
    if (bvid.value.trim().length >= 10) {  // BV号至少10个字符
      fetchVideoStats()
    }
  }, 800)  // 800ms延迟
}

// 获取视频观看时长信息
const fetchVideoStats = async () => {
  if (!bvid.value || bvid.value.trim().length < 10) {
    return
  }

  loading.value = true
  videoStats.value = null

  try {
    // 使用api.js中定义的方法
    const response = await getVideoSeasonInfo({
      bvid: bvid.value.trim(),
      use_sessdata: useSessdata.value
    })
    videoStats.value = response.data

    // 初始设置合适的排序
    if (videoStats.value && videoStats.value.status === 'success') {
      sortKey.value = 'vt'
      sortDirection.value = 'desc'
    }
  } catch (error) {
    console.error('获取视频观看时长信息失败:', error)
    videoStats.value = {
      status: 'error',
      message: error.response?.data?.message || '获取视频信息失败，请检查网络连接或稍后重试'
    }
  } finally {
    loading.value = false
  }
}

// 格式化数字
const formatNumber = (num) => {
  return new Intl.NumberFormat('zh-CN').format(num)
}

// 格式化时长 (分钟 -> mm:ss)
const formatDuration = (minutes) => {
  // 视频时长仍然是秒级的，所以保持不变
  const mins = Math.floor(minutes / 60)
  const remainingSeconds = minutes % 60
  return `${mins}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 格式化时长 (分钟 -> 小时)
const formatDurationHours = (minutes) => {
  // 后端返回的是分钟级别的数据
  const hours = Math.floor(minutes / 60)
  const remainingMinutes = minutes % 60
  return `${hours} 小时 ${remainingMinutes} 分钟`
}

// 格式化时长 (分钟 -> 天/月/年)
const formatDurationDays = (minutes) => {
  const days = Math.floor(minutes / (60 * 24)) // 一天有 24*60 分钟

  if (days >= 365) {
    // 超过365天显示为年
    const years = Math.floor(days / 365)
    const remainingDays = days % 365
    if (remainingDays > 30) {
      const months = Math.floor(remainingDays / 30)
      return `约 ${years} 年 ${months} 个月`
    } else {
      return `约 ${years} 年 ${remainingDays} 天`
    }
  } else if (days >= 30) {
    // 超过30天显示为月
    const months = Math.floor(days / 30)
    const remainingDays = days % 30
    return `约 ${months} 个月 ${remainingDays} 天`
  } else if (days > 0) {
    // 显示为天和小时
    const hours = Math.floor((minutes % (60 * 24)) / 60)
    return `约 ${days} 天 ${hours} 小时`
  }

  return '' // 如果不足1天，不显示
}

// 计算完播率百分比
const secondsToPercent = (watchedSeconds, totalSeconds) => {
  if (!totalSeconds) return 0
  // watchedSeconds 是从分钟转换为秒的平均观看时长
  // totalSeconds 是视频总时长（秒）
  return Math.min(100, Math.round((watchedSeconds / totalSeconds) * 100))
}

// ===== 评论查询功能 =====
// 评论查询数据
const queryUserId = ref('')
const comments = ref([])
const commentLoading = ref(false)
const commentCurrentPage = ref(1)
const commentPageSize = ref(20)
const commentTotal = ref(0)
const commentTotalPages = ref(0)
const commentKeyword = ref('')
const commentType = ref('all')
const contentTypeFilter = ref('0')
const commentPageInput = ref('1')

// 下拉菜单状态
const showCommentTypeDropdown = ref(false)
const showContentTypeDropdown = ref(false)

// 下拉菜单选项数据
const commentTypeOptions = [
  { value: 'all', label: '全部' },
  { value: 'root', label: '一级' },
  { value: 'reply', label: '二级' }
]

const contentTypeOptions = [
  { value: '0', label: '全部' },
  { value: '1', label: '视频' },
  { value: '17', label: '动态' },
  { value: '11', label: '旧动态' }
]

// 是否有活跃的评论筛选条件
const hasActiveCommentFilters = computed(() => {
  return commentKeyword.value !== '' || commentType.value !== 'all' || contentTypeFilter.value !== '0'
})

// 获取评论类型显示文本
const getCommentTypeText = (type) => {
  const option = commentTypeOptions.find(opt => opt.value === type)
  return option ? option.label : '全部'
}

// 获取内容类型显示文本
const getContentTypeText = (type) => {
  const option = contentTypeOptions.find(opt => opt.value === type)
  return option ? option.label : '全部'
}

// 获取评论类型显示文本（单个评论）
const getCommentTypeDisplay = (type) => {
  switch (type) {
    case 1:
      return '视频评论'
    case 11:
    case 17:
      return '动态评论'
    default:
      return '其他评论'
  }
}

// 获取评论链接
const getCommentLink = (comment) => {
  const { type, oid, rpid } = comment

  switch (type) {
    case 1: // 视频评论
      return `https://www.bilibili.com/video/av${oid}#reply${rpid}`
    case 11: // 动态评论类型11
      return `https://t.bilibili.com/${oid}?type=2#reply${rpid}`
    case 17: // 动态评论类型17
      return `https://t.bilibili.com/${oid}#reply${rpid}`
    default:
      return '#'
  }
}

// 切换评论类型下拉菜单
const toggleCommentTypeDropdown = () => {
  showCommentTypeDropdown.value = !showCommentTypeDropdown.value
  showContentTypeDropdown.value = false
}

// 切换内容类型下拉菜单
const toggleContentTypeDropdown = () => {
  showContentTypeDropdown.value = !showContentTypeDropdown.value
  showCommentTypeDropdown.value = false
}

// 选择评论类型
const selectCommentType = (value) => {
  commentType.value = value
  showCommentTypeDropdown.value = false
  commentCurrentPage.value = 1
  fetchUserComments()
}

// 选择内容类型
const selectContentType = (value) => {
  contentTypeFilter.value = value
  showContentTypeDropdown.value = false
  commentCurrentPage.value = 1
  fetchUserComments()
}

// 获取用户评论列表
const fetchUserComments = async () => {
  if (!queryUserId.value) {
    showNotify({
      type: 'warning',
      message: '请输入用户UID'
    })
    return
  }

  commentLoading.value = true

  try {
    const response = await getComments(
      queryUserId.value,
      commentCurrentPage.value,
      commentPageSize.value,
      commentType.value,
      commentKeyword.value,
      contentTypeFilter.value
    )

    if (response.data) {
      comments.value = response.data.comments || []
      commentTotal.value = response.data.total || 0
      commentTotalPages.value = response.data.total_pages || 0
      commentPageInput.value = commentCurrentPage.value.toString()
    }
  } catch (error) {
    console.error('获取评论列表失败:', error)
    showNotify({
      type: 'danger',
      message: error.response?.data?.message || '获取评论列表失败'
    })
    comments.value = []
    commentTotal.value = 0
    commentTotalPages.value = 0
  } finally {
    commentLoading.value = false
  }
}

// 处理评论搜索
const handleCommentSearch = () => {
  commentCurrentPage.value = 1
  fetchUserComments()
}

// 处理评论页码变化
const handleCommentPageChange = (newPage) => {
  if (newPage >= 1 && newPage <= commentTotalPages.value) {
    commentCurrentPage.value = newPage
    fetchUserComments()
  }
}

// 处理评论跳转页
const handleCommentJumpPage = () => {
  const targetPage = parseInt(commentPageInput.value)
  if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= commentTotalPages.value) {
    if (targetPage !== commentCurrentPage.value) {
      commentCurrentPage.value = targetPage
      fetchUserComments()
    }
  } else {
    commentPageInput.value = commentCurrentPage.value.toString()
  }
}

// 清除评论筛选条件
const clearCommentFilters = () => {
  commentKeyword.value = ''
  commentType.value = 'all'
  contentTypeFilter.value = '0'
  commentCurrentPage.value = 1
  fetchUserComments()
}


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