<template>
  <div class="transition-all duration-300 ease-in-out">
    <!-- 年度总结横幅 -->
    <div class="mt-1 mb-3 sm:hidden">
      <router-link
        to="/analytics"
        class="flex h-10 items-center justify-between px-2 bg-gradient-to-r from-[#fb7299] to-[#FF9966] text-white"
      >
        <div class="flex items-center space-x-2">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span class="text-sm">点击查看年度总结</span>
        </div>
        <svg class="w-4 h-4 animate-bounce-x" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </router-link>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="flex flex-col items-center justify-center py-16 bg-white rounded-lg">
      <div class="w-16 h-16 border-4 border-[#fb7299] border-t-transparent rounded-full animate-spin mb-4"></div>
      <h3 class="text-xl font-medium text-gray-600 mb-2">加载中</h3>
      <p class="text-gray-500">正在获取历史记录数据...</p>
    </div>

    <!-- 登录状态空状态 -->
    <div v-else-if="!isLoggedIn" class="flex flex-col items-center justify-center py-16 bg-white rounded-lg shadow-sm">
      <svg class="w-24 h-24 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
      </svg>
      <h3 class="text-xl font-medium text-gray-600 mb-2">请先登录</h3>
      <p class="text-gray-500 mb-6">登录B站账号后才能查看您的历史记录</p>
      <button
        class="px-4 py-2 bg-[#fb7299] text-white rounded-md hover:bg-[#fb7299]/90 transition-colors duration-200 flex items-center space-x-2"
        @click="openLoginDialog">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
        </svg>
        <span>点击登录</span>
      </button>
    </div>

    <!-- 数据为空状态 -->
    <div v-else-if="isLoggedIn && records.length === 0"
         class="flex flex-col items-center justify-center py-16 bg-white rounded-lg">
      <svg class="w-24 h-24 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="text-xl font-medium text-gray-600 mb-2">暂无历史记录</h3>
      <p class="text-gray-500 mb-6">点击下方按钮从B站获取您的历史记录</p>
      <button
        class="px-4 py-2 bg-[#fb7299] text-white rounded-md hover:bg-[#fb7299]/90 transition-colors duration-200 flex items-center space-x-2"
        @click="refreshData">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span>获取历史记录</span>
      </button>
    </div>

    <!-- 视频记录列表 -->
    <div v-else class="overflow-hidden">
      <transition name="float" mode="out-in">
        <!-- 网格布局（仅PC端） -->
        <div v-if="layout === 'grid'"
             class="hidden sm:grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 px-4 mx-auto transition-all duration-300 ease-in-out transform-gpu"
             style="max-width: 1152px;" key="grid-layout">
          <template v-for="(record, index) in records" :key="`grid-${record.id}-${record.view_at}`">
            <!-- 日期分割线和视频数量 -->
            <div v-if="shouldShowDivider(index)" class="col-span-full relative py-1">
              <div>
                <div class="relative">
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="w-full border-t border-gray-300" />
                  </div>
                  <div class="relative flex items-center justify-between">
                    <div class="bg-white pr-3 flex items-center space-x-2">
                      <!-- 添加当天记录的勾选框 -->
                      <div v-if="isBatchMode"
                           class="flex items-center justify-center cursor-pointer"
                           @click.stop="toggleDaySelection(record.view_at)">
                        <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                             :class="isDaySelected(record.view_at) ? 'bg-[#fb7299] border-[#fb7299]' : 'border-gray-300 bg-white'">
                          <svg v-if="isDaySelected(record.view_at)" class="w-3 h-3 text-white" fill="none"
                               viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                      </div>
                      <span class="lm:text-xs">
 {{ formatDividerDate(record.view_at) }}
 </span>
                    </div>
                    <div class="bg-white pl-3">
 <span class="lm:text-xs text-[#FF6699]">
 {{ getDailyStatsForDate(record.view_at) }}条数据 · 总时长 {{ formatDailyWatchTime(record.view_at) }}
 </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 网格布局的视频卡片 -->
            <div
              class="bg-white/50 backdrop-blur-sm rounded-lg overflow-hidden border border-gray-200/50 hover:border-[#FF6699] hover:shadow-md transition-all duration-200 relative group"
              :class="{ 'ring-2 ring-[#fb7299]': selectedRecords.has(`${record.bvid}_${record.view_at}`), 'cursor-pointer': isBatchMode }"
              @click="isBatchMode ? toggleRecordSelection(record) : null">
              <!-- 多选框 -->
              <div v-if="isBatchMode"
                   class="absolute top-2 left-2 z-10">
                <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                     :class="selectedRecords.has(`${record.bvid}_${record.view_at}`) ? 'bg-[#fb7299] border-[#fb7299]' : 'border-white bg-black/20'">
                  <svg v-if="selectedRecords.has(`${record.bvid}_${record.view_at}`)" class="w-3 h-3 text-white"
                       fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </div>

              <!-- 封面图片 -->
              <div class="relative aspect-video" :class="{ 'cursor-pointer': !isBatchMode }"
                   @click="!isBatchMode ? handleVideoClick(record) : null">
                <!-- 下载状态标识 -->
                <div v-if="isVideoDownloaded(record.cid) && record.business === 'archive'"
                     class="absolute left-0 top-0 z-20">
                  <div
                    class="bg-gradient-to-r from-green-500 to-green-400 text-white font-semibold px-2 py-0.5 text-xs flex items-center space-x-1.5 rounded-br-md shadow-md">
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    <span>已下载</span>
                  </div>
                </div>

                <!-- 收藏状态标识 - 不对直播类型显示 -->
                <div
                  v-if="isVideoFavorited(parseInt(record.aid || record.avid || (record.business === 'archive' ? record.oid : 0), 10)) && record.business !== 'live'"
                  class="absolute right-0 top-0 z-20">
                  <div
                    class="bg-gradient-to-r from-amber-500 to-yellow-400 text-white font-semibold px-2 py-0.5 text-xs flex items-center space-x-1.5 rounded-bl-md shadow-md">
                    <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                    </svg>
                    <span>已收藏</span>
                  </div>
                </div>

                <!-- 按钮组 -->
                <div v-if="!isBatchMode"
                     class="absolute right-2 top-2 z-20 hidden group-hover:flex flex-row items-center space-x-2">
                  <!-- 收藏按钮 - 不对直播类型显示 -->
                  <div v-if="record.business !== 'live'"
                       class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                       @click.stop.prevent="handleFavoriteGrid(record)">
                    <svg class="w-4 h-4"
                         :class="isVideoFavorited(parseInt(record.aid || record.avid || (record.business === 'archive' ? record.oid : 0), 10)) ? 'text-yellow-400' : 'text-white'"
                         :fill="isVideoFavorited(parseInt(record.aid || record.avid || (record.business === 'archive' ? record.oid : 0), 10)) ? 'currentColor' : 'none'"
                         viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                    </svg>
                  </div>
                  <!-- 下载按钮 - 只对视频类型显示 -->
                  <div v-if="record.business === 'archive'"
                       class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                       @click.stop.prevent="handleDownloadGrid(record)">
                    <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                  </div>
                  <!-- 详情按钮 - 只对普通视频类型显示 -->
                  <div v-if="record.business === 'archive'"
                       class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                       @click.stop="openVideoDetail(record)">
                    <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <!-- 删除按钮 -->
                  <div
                    class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                    @click.stop="handleDelete(record)">
                    <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </div>
                </div>
                <img
                  :src="normalizeImageUrl(record.cover || record.covers?.[0])"
                  class="w-full h-full object-cover transition-all duration-300"
                  :class="{ 'blur-md': isPrivacyMode }"
                  alt=""
                />
                <!-- 视频进度条 -->
                <div
                  v-if="record.business !== 'article-list' && record.business !== 'article' && record.business !== 'live'"
                  class="absolute bottom-0 left-0 w-full">
                  <div
                    class="absolute bottom-1 right-1 rounded bg-black/50 px-1 py-1 text-[10px] font-semibold text-white">
                    <span>{{ formatDuration(record.progress) }}</span>
                    <span>/</span>
                    <span>{{ formatDuration(record.duration) }}</span>
                  </div>
                  <div class="absolute bottom-0 left-0 h-0.5 w-full bg-black">
                    <div class="h-full bg-[#FF6699]"
                         :style="{ width: getProgressWidth(record.progress, record.duration) }">
                    </div>
                  </div>
                </div>
                <!-- 右上角的类型角标 -->
                <div
                  v-if="record.badge"
                  class="absolute right-1 top-1 rounded bg-[#FF6699] px-1 py-0.5 text-[10px] text-white"
                >
                  {{ record.badge }}
                </div>
              </div>
              <!-- 视频信息 -->
              <div class="p-3 flex flex-col space-y-1">
                <!-- 标题 - 单行显示 -->
                <div class="line-clamp-1 text-sm text-gray-900"
                     v-html="isPrivacyMode ? '******' : highlightText(record.title)"
                     :class="{ 'blur-sm': isPrivacyMode, 'cursor-pointer': !isBatchMode }"
                     @click="!isBatchMode ? handleVideoClick(record) : null">
                </div>
                <!-- 分区标签 - 单行显示 -->
                <div class="text-xs text-gray-500 truncate flex items-center space-x-1">
 <span class="inline-flex items-center rounded-md bg-[#f1f2f3] px-2 py-1 text-xs text-[#71767d]">
 {{ record.business === 'archive' ? record.tag_name : getBusinessType(record.business) }}
 </span>
                  <span v-if="record.business === 'archive'" class="text-gray-400">·</span>
                  <span v-if="record.business === 'archive' && record.name" class="text-[#71767d]">{{ record.name
                    }}</span>
                </div>
                <!-- UP主和时间信息 - 单行显示 -->
                <div class="flex items-center justify-between text-xs text-gray-600">
                  <div class="flex items-center space-x-2 min-w-0 flex-1">
                    <img v-if="record.business !== 'cheese' && record.business !== 'pgc'"
                         :src="normalizeImageUrl(record.author_face)"
                         :class="{ 'blur-md': isPrivacyMode, 'cursor-pointer': !isBatchMode }"
                         class="w-4 h-4 rounded-full flex-shrink-0"
                         @click="!isBatchMode ? handleAuthorClick(record) : null"
                         :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
                    />
                    <span v-html="isPrivacyMode ? '******' : highlightText(record.author_name)"
                          :class="{ 'blur-sm': isPrivacyMode, 'cursor-pointer': !isBatchMode }"
                          class="hover:text-[#fb7299] transition-colors duration-200 truncate"
                          @click="!isBatchMode ? handleAuthorClick(record) : null">
 </span>
                  </div>
                  <div class="flex items-center space-x-2 flex-shrink-0">
                    <img v-if="record.dt === 1 || record.dt === 3 || record.dt === 5 || record.dt === 7"
                         src="/Mobile.svg"
                         alt="Mobile"
                         class="h-4 w-4"
                    />
                    <img v-else-if="record.dt === 2 || record.dt === 33"
                         src="/PC.svg"
                         alt="PC"
                         class="h-4 w-4"
                    />
                    <img v-else-if="record.dt === 4 || record.dt === 6"
                         src="/Pad.svg"
                         alt="Pad"
                         class="h-4 w-4"
                    />
                    <span>{{ formatTimestamp(record.view_at) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>

        <!-- 列表布局（移动端始终显示，PC端在list模式下显示） -->
        <div v-else :class="{'sm:hidden': layout === 'grid'}"
             class="transition-all duration-300 ease-in-out transform-gpu" key="list-layout">
          <template v-for="(record, index) in records" :key="`list-${record.id}-${record.view_at}`">
            <!-- 日期分割线和视频数量 -->
            <div v-if="shouldShowDivider(index)" class="relative py-1 max-w-4xl mx-auto">
              <div class="px-2">
                <div class="relative">
                  <div class="absolute inset-0 flex items-center" aria-hidden="true">
                    <div class="w-full border-t border-gray-300" />
                  </div>
                  <div class="relative flex items-center justify-between">
                    <div class="bg-white pr-3 flex items-center space-x-2">
                      <!-- 添加当天记录的勾选框 -->
                      <div v-if="isBatchMode"
                           class="flex items-center justify-center cursor-pointer"
                           @click.stop="toggleDaySelection(record.view_at)">
                        <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                             :class="isDaySelected(record.view_at) ? 'bg-[#fb7299] border-[#fb7299]' : 'border-gray-300 bg-white'">
                          <svg v-if="isDaySelected(record.view_at)" class="w-3 h-3 text-white" fill="none"
                               viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                      </div>
                      <span class="lm:text-xs">
 {{ formatDividerDate(record.view_at) }}
 </span>
                    </div>
                    <div class="bg-white pl-3">
 <span class="lm:text-xs text-[#FF6699]">
 {{ getDailyStatsForDate(record.view_at) }}条数据 · 总时长 {{ formatDailyWatchTime(record.view_at) }}
 </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <VideoRecord
              :record="record"
              :is-batch-mode="isBatchMode"
              :is-selected="selectedRecords.has(`${record.bvid}_${record.view_at}`)"
              :remark-data="remarkData"
              :is-downloaded="isVideoDownloaded(record.cid)"
              :is-video-favorited="isVideoFavorited(parseInt(record.aid || record.avid || (record.business === 'archive' ? record.oid : 0), 10))"
              @toggle-selection="toggleRecordSelection"
              @refresh-data="fetchHistoryByDateRange"
              @remark-updated="handleRemarkUpdate"
              @favorite="handleFavorite"
            />
          </template>
        </div>
      </transition>
    </div>

    <!-- 日期选择日历 -->
    <van-calendar
      :show-confirm="false"
      title="选择日期区间"
      switch-mode="year-month"
      :show="show"
      :style="{ height: '65%' }"
      type="range"
      @confirm="onConfirm"
      @update:show="(val) => emit('update:show', val)"
    />

    <!-- 批量操作按钮区域 -->
    <div v-if="isBatchMode && selectedRecords.size > 0"
         class="fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50 w-[90vw] max-w-[1200px]">
      <div class="flex flex-col space-y-2 w-full">
        <!-- 删除模式切换按钮 -->
        <div class="flex justify-center mb-1">
          <!-- 已移除本地/远程收藏模式切换 -->
        </div>

        <div class="flex flex-wrap gap-3 justify-center w-full mt-2">
          <!-- 批量删除按钮 -->
          <button
            @click="handleBatchDelete"
            class="w-28 py-2 bg-red-500 text-white rounded-lg shadow-md hover:bg-red-600 transition-all duration-200 flex items-center justify-center space-x-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-opacity-50"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            <span>删除({{ selectedRecords.size }})</span>
          </button>

          <!-- 批量下载按钮 - 始终显示 -->
          <button
            @click="handleBatchDownload"
            class="w-28 py-2 bg-green-500 text-white rounded-lg shadow-md hover:bg-green-600 transition-all duration-200 flex items-center justify-center space-x-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-50"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>下载({{ selectedRecords.size }})</span>
          </button>

          <!-- 批量收藏按钮 - 仅在有未收藏的视频时显示 -->
          <button
            v-if="!isAllFavorited && unfavoritedCount > 0"
            @click="handleBatchFavorite"
            class="w-28 py-2 bg-[#fb7299] text-white rounded-lg shadow-md hover:bg-[#fb7299]/90 transition-all duration-200 flex items-center justify-center space-x-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-pink-400 focus:ring-opacity-50"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            <span>收藏({{ unfavoritedCount }})</span>
          </button>

          <!-- 批量取消收藏按钮 - 仅在有已收藏的视频时显示 -->
          <button
            v-if="hasFavoritedVideos"
            @click="handleBatchUnfavorite"
            class="w-28 py-2 bg-orange-500 text-white rounded-lg shadow-md hover:bg-orange-600 transition-all duration-200 flex items-center justify-center space-x-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-orange-400 focus:ring-opacity-50"
          >
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            <span>取消收藏({{ favoritedCount }})</span>
          </button>

          <!-- 复制链接按钮 - 始终显示 -->
          <button
            @click="handleCopyLinks"
            class="w-28 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition-all duration-200 flex items-center justify-center space-x-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-opacity-50"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
            </svg>
            <span>复制链接({{ selectedRecords.size }})</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 视频详情对话框 -->
  <Teleport to="body">
    <VideoDetailDialog
      :modelValue="showDetailDialog"
      @update:modelValue="showDetailDialog = $event"
      :video="selectedRecord"
      :remarkData="remarkData"
      @remark-updated="handleRemarkUpdate"
    />
  </Teleport>

  <!-- 下载弹窗 -->
  <Teleport to="body">
    <DownloadDialog
      v-model:show="showDownloadDialog"
      :video-info="{
 title: selectedRecord?.title || '',
 author: selectedRecord?.author_name || '',
 bvid: selectedRecord?.bvid || '',
 cover: selectedRecord?.cover || selectedRecord?.covers?.[0] || '',
 cid: selectedRecord?.cid || ''
 }"
      :is-batch-download="isBatchDownload"
      :batch-videos="batchVideos"
      v-model:currentVideoIndex="currentVideoIndex"
      @download-complete="handleDownloadComplete"
    />
  </Teleport>

  <!-- 收藏夹选择对话框 -->
  <Teleport to="body">
    <FavoriteDialog
      v-model="showFavoriteDialog"
      :video-info="favoriteVideoInfo"
      @favorite-done="handleFavoriteDone"
    />
  </Teleport>

  <!-- 登录对话框 -->
  <Teleport to="body">
    <LoginDialog
      v-model:show="showLoginDialog"
      @login-success="handleLoginSuccess"
    />
  </Teleport>
</template>

<style scoped>
@keyframes bounce-x {
  0%, 100% {
    transform: translateX(0);
  }
  50% {
    transform: translateX(25%);
  }
}

.animate-bounce-x {
  animation: bounce-x 1s infinite;
}

.float-enter-active,
.float-leave-active {
  transition: all 0.3s ease;
}

.float-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.float-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import {
  getBiliHistory2024,
  getMainCategories,
  getDailyStats,
  batchDeleteHistory,
  batchGetRemarks,
  getLoginStatus,
  updateBiliHistoryRealtime,
  checkVideoDownload,
  batchCheckFavoriteStatus,
  favoriteResource,
  localBatchFavoriteResource,
  batchDeleteBilibiliHistory,
  deleteBilibiliHistory,
} from '@/api/api.js'
import { showNotify, showDialog } from 'vant'
import 'vant/es/dialog/style'
import VideoRecord from './VideoRecord.vue'
import { usePrivacyStore } from '@/store/privacy.js'
import VideoDetailDialog from './VideoDetailDialog.vue'
import LoginDialog from './LoginDialog.vue'
import DownloadDialog from './DownloadDialog.vue'
import FavoriteDialog from './FavoriteDialog.vue'
import { openInBrowser } from '@/utils/openUrl.js'
import { normalizeImageUrl } from '@/utils/imageUrl.js'

const { isPrivacyMode } = usePrivacyStore()

const props = defineProps({
  selectedYear: {
    type: Number,
    default: new Date().getFullYear(),
  },
  page: {
    type: Number,
    default: 1,
  },
  show: {
    type: Boolean,
    default: false,
  },
  showBottom: {
    type: Boolean,
    default: false,
  },
  layout: {
    type: String,
    default: 'list',
  },
  searchKeyword: {
    type: String,
    default: '',
  },
  date: {
    type: String,
    default: '',
  },
  category: {
    type: String,
    default: '',
  },
  business: {
    type: String,
    default: '',
  },
  isBatchMode: {
    type: Boolean,
    default: false,
  },
  pageSize: {
    type: Number,
    default: 30,
  },
})

const emit = defineEmits([
  'update:total-pages',
  'update:total',
  'update:date',
  'update:category',
  'update:show',
  'update:showBottom',
  'update:pageSize',
])

// 状态变量
const records = ref([])
const total = ref(0)
const sortOrder = ref(0)
const size = ref(props.pageSize)
const remarkData = ref({}) // 存储备注数据
const downloadedVideos = ref(new Set()) // 存储已下载视频的CID集合
const favoriteStatus = ref({}) // 存储视频收藏状态信息

const date = ref('')
const dateRange = ref('')

const tagName = ref('')
const mainCategory = ref('')
const mainCategories = ref([])

// 每日统计数据
const dailyStats = ref({})

// 批量删除相关
const selectedRecords = ref(new Set())

// 在data区域添加
const selectedRecord = ref(null)
const showDetailDialog = ref(false)
const showDownloadDialog = ref(false)
const showFavoriteDialog = ref(false)
const favoriteVideoInfo = ref(null) // 用于存储收藏相关的视频信息

// 登录相关
const isLoggedIn = ref(false)
const isLoading = ref(false)
const showLoginDialog = ref(false)

// 选择/取消选择记录
const toggleRecordSelection = (record) => {
  const key = `${record.bvid}_${record.view_at}`
  if (selectedRecords.value.has(key)) {
    selectedRecords.value.delete(key)
  } else {
    selectedRecords.value.add(key)
  }
}

// 批量删除选中的记录
const handleBatchDelete = async () => {
  if (selectedRecords.value.size === 0) {
    showNotify({
      type: 'warning',
      message: '请先选择要删除的记录',
    })
    return
  }

  try {
    // 检查是否需要同步删除B站历史记录
    const syncDeleteToBilibili = localStorage.getItem('syncDeleteToBilibili') === 'true'

    // 根据是否同步删除B站历史记录，显示不同的确认信息
    await showDialog({
      title: '确认删除',
      message: syncDeleteToBilibili
        ? `确定要删除选中的 ${selectedRecords.value.size} 条记录吗？此操作将同时删除B站服务器上的历史记录，不可恢复。`
        : `确定要删除选中的 ${selectedRecords.value.size} 条记录吗？此操作不可恢复。`,
      showCancelButton: true,
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      confirmButtonColor: '#fb7299',
    })

    // 从记录中找到对应的完整信息
    const items = Array.from(selectedRecords.value).map(key => {
      const [bvid, view_at] = key.split('_')
      return {
        bvid,
        view_at: parseInt(view_at),
      }
    })

    if (syncDeleteToBilibili) {
      // 构建B站历史记录删除请求的items
      const biliItems = items.map(item => {
        // 查找对应的完整记录以获取业务类型
        const record = records.value.find(r => r.bvid === item.bvid && r.view_at === item.view_at)
        if (!record) return null

        // 根据业务类型构建kid
        const business = record.business || 'archive'
        let kid

        switch (business) {
          case 'archive':
            // 使用oid而不是bvid
            kid = `${business}_${record.oid}`
            break
          case 'live':
            kid = `${business}_${record.oid}`
            break
          case 'article':
            kid = `${business}_${record.oid}`
            break
          case 'pgc':
            kid = `${business}_${record.oid || record.ssid}`
            break
          case 'article-list':
            kid = `${business}_${record.oid || record.rlid}`
            break
          default:
            kid = `${business}_${record.oid || record.bvid}`
            break
        }

        if (!kid) {
          return null
        }

        return {
          kid,
          sync_to_bilibili: true,
        }
      }).filter(item => item !== null)

      if (biliItems.length > 0) {
        try {
          // 调用B站历史记录删除API
          const biliResponse = await batchDeleteBilibiliHistory(biliItems)
          if (biliResponse.data.status === 'success' || biliResponse.data.status === 'partial_success') {
            console.log('B站历史记录删除成功或部分成功:', biliResponse.data)
          } else {
            console.error('B站历史记录删除失败:', biliResponse.data)
            throw new Error(biliResponse.data.message || '删除B站历史记录失败')
          }
        } catch (error) {
          console.error('B站历史记录删除失败:', error)
          // 即使B站删除失败，也继续删除本地记录
        }
      }
    }

    // 删除本地记录
    const response = await batchDeleteHistory(items)
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message + (syncDeleteToBilibili ? '，并已同步删除B站历史记录' : ''),
      })
      selectedRecords.value.clear()
      await fetchHistoryByDateRange()
    } else {
      throw new Error(response.data.message || '删除失败')
    }
  } catch (error) {
    if (error.toString().includes('cancel')) return

    showNotify({
      type: 'danger',
      message: error.response?.data?.detail || error.message || '删除失败',
    })
  }
}

// 监听批量模式变化
watch(() => props.isBatchMode, (newVal) => {
  if (!newVal) {
    selectedRecords.value.clear()
  }
})

// 计算属性用于显示当前选中的分类
computed(() => {
  return mainCategory.value || tagName.value || '全部分区'
})
// 获取主分区列表
const fetchMainCategories = async () => {
  try {
    const response = await getMainCategories()
    if (response.data.status === 'success') {
      mainCategories.value = response.data.data.map((cat) => cat.name)
    }
  } catch (error) {
    console.error('Error fetching main categories:', error)
  }
}

// 辅助函数：格式化日期
const formatDate = (date) => `${date.getMonth() + 1}/${date.getDate()}`
const formatDateWithYear = (date) => `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
const formatDateForAPI = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}${month}${day}`
}

// 处理日期区间确认
const onConfirm = (values) => {
  const [start, end] = values
  emit('update:show', false)

  const startYear = start.getFullYear()
  const endYear = end.getFullYear()

  let dateText
  if (startYear === props.selectedYear && endYear === props.selectedYear) {
    dateText = `${formatDate(start)} - ${formatDate(end)}`
  } else {
    dateText = `${formatDateWithYear(start)} - ${formatDateWithYear(end)}`
  }

  emit('update:date', dateText)
  dateRange.value = `${formatDateForAPI(start)}-${formatDateForAPI(end)}`
  fetchHistoryByDateRange()
}

// 批量检查视频下载状态
const batchCheckDownloadStatus = async () => {
  try {
    if (records.value.length === 0) return

    // 筛选出视频类型的记录
    const videoRecords = records.value.filter(record => record.business === 'archive')
    if (videoRecords.length === 0) return

    // 获取所有视频的CID
    const cids = videoRecords.map(record => record.cid).filter(cid => cid)
    if (cids.length === 0) return

    const response = await checkVideoDownload(cids)

    if (response.data && response.data.status === 'success') {
      // 清空已有集合
      downloadedVideos.value.clear()

      // 处理返回结果，将已下载视频的CID添加到集合中
      const results = response.data.results || {}

      // 遍历results对象的每个键值对
      Object.entries(results).forEach(([cid, info]) => {
        if (info.downloaded) {
          downloadedVideos.value.add(cid.toString())
        }
      })
    }
  } catch (error) {
    console.error('批量检查下载状态失败:', error)
  }
}

// 检查视频是否已下载
const isVideoDownloaded = (cid) => {
  return cid && downloadedVideos.value.has(cid.toString())
}

// 检查视频是否已收藏
const isVideoFavorited = (oid) => {
  if (!oid) return false

  // 确保oid是字符串类型，方便比较
  const oidStr = String(oid)

  // 检查是否在收藏状态中
  return Object.keys(favoriteStatus.value).some(key => {
    return String(key) === oidStr && favoriteStatus.value[key].is_favorited
  })
}

// 获取视频被收藏到的收藏夹
const getVideoFavoriteFolders = (oid) => {
  if (!oid) return []

  // 确保oid是字符串类型，方便比较
  const oidStr = String(oid)

  // 查找匹配的收藏状态
  for (const key in favoriteStatus.value) {
    if (String(key) === oidStr) {
      return favoriteStatus.value[key].favorite_folders || []
    }
  }

  return []
}

// 批量检查视频收藏状态
const batchCheckFavorites = async () => {
  try {
    if (records.value.length === 0) return

    // 筛选出视频类型的记录
    const videoRecords = records.value.filter(record => record.business === 'archive')
    if (videoRecords.length === 0) return

    // 获取所有视频的avid
    const oids = videoRecords.map(record => {
      // 使用 aid 或 avid 或 (oid 如果 business 是 archive)
      const id = record.aid || record.avid || (record.business === 'archive' ? record.oid : null)
      // 确保ID是数字类型
      return id ? parseInt(id, 10) : null
    }).filter(oid => oid !== null && !isNaN(oid))

    if (oids.length === 0) return

    console.log('批量检查视频收藏状态:', oids)
    const response = await batchCheckFavoriteStatus({ oids }) // 直接传递数组

    if (response.data && response.data.status === 'success') {
      // 清空已有状态
      favoriteStatus.value = {}

      // 处理返回结果
      const results = response.data.data.results || []
      results.forEach(item => {
        favoriteStatus.value[item.oid] = {
          is_favorited: item.is_favorited,
          favorite_folders: item.favorite_folders || [],
        }
      })

      console.log('收藏状态数据:', favoriteStatus.value)
    }
  } catch (error) {
    console.error('批量检查收藏状态失败:', error)
  }
}

// 数据获取函数
const fetchHistoryByDateRange = async () => {

  try {
    isLoading.value = true
    records.value = []
    const response = await getBiliHistory2024(
      props.page,
      size.value,
      sortOrder.value,
      tagName.value,
      mainCategory.value,
      dateRange.value || '',
      localStorage.getItem('useLocalImages') === 'true',
      props.business,
    )

    if (response.data && response.data.data) {
      total.value = response.data.data.total
      records.value = response.data.data.records
      emit('update:total-pages', Math.ceil(response.data.data.total / size.value))
      emit('update:total', response.data.data.total)

      // 批量获取备注
      if (records.value.length > 0) {
        const batchRecords = records.value.map(record => ({
          bvid: record.bvid,
          view_at: record.view_at,
        }))
        const remarksResponse = await batchGetRemarks(batchRecords)
        if (remarksResponse.data.status === 'success') {
          remarkData.value = remarksResponse.data.data
        }

        // 批量检查下载状态
        await batchCheckDownloadStatus()

        // 批量检查收藏状态
        await batchCheckFavorites()
      }
    }
  } catch (error) {
    console.error('数据获取失败:', error)
    records.value = []
    total.value = 0
    emit('update:total-pages', 0)
    emit('update:total', 0)
  } finally {
    isLoading.value = false
  }
}

// 监听年份和页码变化
watch(
  () => [props.selectedYear, props.page],
  () => {
    fetchHistoryByDateRange()
  },
)

// 监听 pageSize 变化
watch(
  () => props.pageSize,
  (newSize) => {
    size.value = newSize
    // 保存到 localStorage
    localStorage.setItem('pageSize', newSize.toString())
    fetchHistoryByDateRange()
  },
)

// 监听父组件的 date 变化
watch(
  () => props.date,
  (newDate) => {
    if (!newDate) {
      dateRange.value = ''
      fetchHistoryByDateRange()
    } else {
      // 解析日期区间格式 "YYYY/MM/DD 至 YYYY/MM/DD"
      const dates = newDate.split(' 至 ')
      if (dates.length === 2) {
        const startParts = dates[0].split('/')
        const endParts = dates[1].split('/')

        if (startParts.length === 3 && endParts.length === 3) {
          const startDate = `${startParts[0]}${startParts[1].padStart(2, '0')}${startParts[2].padStart(2, '0')}`
          const endDate = `${endParts[0]}${endParts[1].padStart(2, '0')}${endParts[2].padStart(2, '0')}`
          dateRange.value = `${startDate}-${endDate}`
          fetchHistoryByDateRange()
        }
      }
    }
  },
)

// 监听父组件的 category 变化
watch(
  () => props.category,
  (newCategory) => {
    if (!newCategory) {
      tagName.value = ''
      mainCategory.value = ''
    } else {
      // 根据分区名称判断是主分区还是子分区
      // 由于我们无法确定是主分区还是子分区，所以统一赋值给mainCategory
      mainCategory.value = newCategory
      tagName.value = ''
    }
    // 这里会触发数据获取
    fetchHistoryByDateRange()
  },
)

// 监听父组件的 business 变化
watch(
  () => props.business,
  () => {
    fetchHistoryByDateRange()
  },
)

// 获取每日统计数据
const fetchDailyStats = async (timestamp) => {
  if (!timestamp) return

  try {
    const date = new Date(timestamp * 1000)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    const dateStr = `${month}${day}`

    // 如果已经有这个日期的数据，就不重复获取
    const dateKey = `${year}-${month}-${day}`
    if (dailyStats.value[dateKey]) return

    const response = await getDailyStats(dateStr, year)
    if (response.data.status === 'success') {
      dailyStats.value[dateKey] = response.data.data
    }
  } catch (error) {
    console.error('获取每日统计数据失败:', error)
  }
}

// 监听记录变化，获取所有不同日期的统计数据
watch(() => records.value, (newRecords) => {
  if (newRecords && newRecords.length > 0) {
    // 获取所有不同日期的时间戳
    const uniqueDates = new Set()
    newRecords.forEach(record => {
      const date = new Date(record.view_at * 1000)
      const dateKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
      if (!uniqueDates.has(dateKey)) {
        uniqueDates.add(dateKey)
        fetchDailyStats(record.view_at)
      }
    })
  } else {
    dailyStats.value = {}
  }
}, { deep: true })

// 获取指定日期的统计数据
const getDailyStatsForDate = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const dateKey = `${date.getFullYear()}-${month}-${day}`
  return dailyStats.value[dateKey]?.total_count || 0
}

// 获取指定日期的总观看时长（秒）
const getDailyWatchSecondsForDate = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const dateKey = `${date.getFullYear()}-${month}-${day}`
  return dailyStats.value[dateKey]?.total_watch_seconds || 0
}

// 将秒格式化为中文时长（如 1小时23分45秒）
const formatHMS = (seconds) => {
  const total = Math.max(0, Math.floor(seconds || 0))
  const h = Math.floor(total / 3600)
  const m = Math.floor((total % 3600) / 60)
  const s = total % 60
  if (h > 0) {
    return `${h}小时${String(m).padStart(2, '0')}分${String(s).padStart(2, '0')}秒`
  }
  if (m > 0) {
    return `${m}分${String(s).padStart(2, '0')}秒`
  }
  return `${s}秒`
}

// 获取指定日期的总时长（格式化）
const formatDailyWatchTime = (timestamp) => {
  return formatHMS(getDailyWatchSecondsForDate(timestamp))
}

// 打开登录对话框
const openLoginDialog = () => {
  showLoginDialog.value = true
}

// 处理登录成功
const handleLoginSuccess = async (userData) => {
  try {
    // 如果登录对话框传递了用户数据，直接使用
    if (userData && userData.isLogin) {
      isLoggedIn.value = userData.isLogin

      // 触发全局事件，通知侧边栏更新登录状态，并传递用户信息
      window.dispatchEvent(new CustomEvent('login-status-changed', {
        detail: {
          isLoggedIn: true,
          userInfo: userData,
        },
      }))
    } else {
      // 如果没有传递用户数据，则调用API获取
      const response = await getLoginStatus()
      if (response.data && response.data.code === 0) {
        isLoggedIn.value = response.data.data.isLogin

        // 触发全局事件，通知侧边栏更新登录状态，并传递用户信息
        window.dispatchEvent(new CustomEvent('login-status-changed', {
          detail: {
            isLoggedIn: true,
            userInfo: response.data.data,
          },
        }))
      }
    }

    // 刷新历史记录数据
    if (isLoggedIn.value) {
      fetchHistoryByDateRange()
    }
  } catch (error) {
    console.error('登录成功后获取状态失败:', error)
  }
}

// 检查登录状态
const checkLoginStatus = async () => {
  try {
    const response = await getLoginStatus()
    isLoggedIn.value = response.data && response.data.code === 0 && response.data.data.isLogin
  } catch (error) {
    console.error('获取登录状态失败:', error)
    isLoggedIn.value = false
  }
}

// 刷新数据
const refreshData = async () => {
  try {
    isLoading.value = true
    showNotify({ type: 'success', message: '正在从B站获取历史记录...' })

    const syncDeleted = localStorage.getItem('syncDeleted') === 'true'
    const response = await updateBiliHistoryRealtime(syncDeleted)
    if (response.data.status === 'success') {
      showNotify({ type: 'success', message: response.data.message || '数据获取成功' })
      fetchHistoryByDateRange()
    } else {
      throw new Error(response.data.message || '获取失败')
    }
  } catch (error) {
    console.error('刷新数据失败:', error)
    showNotify({
      type: 'danger',
      message: error.response?.data?.message || error.message || '获取历史记录失败',
    })
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  isLoading.value = true
  try {
    await checkLoginStatus()
    await fetchMainCategories()
    if (isLoggedIn.value) {
      await fetchHistoryByDateRange()
    } else {
      isLoading.value = false
    }
  } catch (error) {
    console.error('初始化失败:', error)
    isLoading.value = false
  }
})

// 暴露方法给父组件
defineExpose({
  fetchHistoryByDateRange,
  refreshData,
  checkLoginStatus,
})

// 格式化分割线日期
const formatDividerDate = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const currentYear = new Date().getFullYear()
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()

  if (year === currentYear) {
    return `${month}月${day}日`
  } else {
    return `${year}年${month}月${day}日`
  }
}

// 判断是否需要显示分割线
const shouldShowDivider = (index) => {
  if (index === 0) return true

  const currentDate = new Date(records.value[index].view_at * 1000)
  const prevDate = new Date(records.value[index - 1].view_at * 1000)

  return currentDate.getDate() !== prevDate.getDate() ||
    currentDate.getMonth() !== prevDate.getMonth() ||
    currentDate.getFullYear() !== prevDate.getFullYear()
}

// 处理视频点击
const handleVideoClick = async (record) => {
  let url = ''

  switch (record.business) {
    case 'archive':
      url = `https://www.bilibili.com/video/${record.bvid}`
      break
    case 'article':
      url = `https://www.bilibili.com/read/cv${record.oid}`
      break
    case 'article-list':
      url = `https://www.bilibili.com/read/readlist/rl${record.oid}`
      break
    case 'live':
      url = `https://live.bilibili.com/${record.oid}`
      break
    case 'pgc':
      url = record.uri || `https://www.bilibili.com/bangumi/play/ep${record.epid}`
      break
    case 'cheese':
      url = record.uri || `https://www.bilibili.com/cheese/play/ep${record.epid}`
      break
    default:
      console.warn('未知的业务类型:', record.business)
      return
  }

  if (url) {
    await openInBrowser(url)
  }
}

// 处理UP主点击
const handleAuthorClick = async (record) => {
  const url = `https://space.bilibili.com/${record.author_mid}`
  await openInBrowser(url)
}

// 格式化时长
const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完'
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0')
  const secs = String(seconds % 60).padStart(2, '0')
  return `${minutes}:${secs}`
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

// 获取进度条宽度
const getProgressWidth = (progress, duration) => {
  if (progress === -1) return '100%'
  if (duration === 0) return '0%'
  return `${(progress / duration) * 100}%`
}

// 格式化时间戳
const formatTimestamp = (timestamp) => {
  if (!timestamp) {
    console.warn('Invalid timestamp:', timestamp)
    return '时间未知'
  }

  try {
    const date = new Date(timestamp * 1000)
    const now = new Date()

    if (isNaN(date.getTime())) {
      console.warn('Invalid date from timestamp:', timestamp)
      return '时间未知'
    }

    const isToday = now.toDateString() === date.toDateString()
    const isYesterday =
      new Date(now.setDate(now.getDate() - 1)).toDateString() === date.toDateString()
    const timeString = date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })

    if (isToday) {
      return timeString
    } else if (isYesterday) {
      return `昨天 ${timeString}`
    } else if (now.getFullYear() === date.getFullYear()) {
      return `${date.getMonth() + 1}-${date.getDate()} ${timeString}`
    } else {
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${timeString}`
    }
  } catch (error) {
    console.error('Error formatting timestamp:', error)
    return '时间未知'
  }
}

// 高亮显示匹配的文本
const highlightText = (text) => {
  if (!props.searchKeyword || !text) return text

  const regex = new RegExp(props.searchKeyword, 'gi')
  return text.replace(regex, match => `<span class="text-[#FF6699]">${match}</span>`)
}

// 处理删除记录
const handleDelete = async (record) => {
  try {
    // 检查是否需要同步删除B站历史记录
    const syncDeleteToBilibili = localStorage.getItem('syncDeleteToBilibili') === 'true'

    await showDialog({
      title: '确认删除',
      message: syncDeleteToBilibili
        ? '确定要删除这条记录吗？此操作将同时删除B站服务器上的历史记录，不可恢复。'
        : '确定要删除这条记录吗？此操作不可恢复。',
      showCancelButton: true,
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      confirmButtonColor: '#fb7299',
    })

    // 如果需要同步删除B站历史记录
    if (syncDeleteToBilibili) {
      // 构建B站历史记录删除请求
      const business = record.business || 'archive'
      let kid = ''

      switch (business) {
        case 'archive':
          // 使用oid而不是bvid
          kid = `${business}_${record.oid}`
          break
        case 'live':
          kid = `${business}_${record.oid}`
          break
        case 'article':
          kid = `${business}_${record.oid}`
          break
        case 'pgc':
          kid = `${business}_${record.oid || record.ssid}`
          break
        case 'article-list':
          kid = `${business}_${record.oid || record.rlid}`
          break
        default:
          kid = `${business}_${record.oid || record.bvid}`
          break
      }

      if (kid) {
        try {
          // 调用B站历史记录删除API
          const biliResponse = await deleteBilibiliHistory(kid, true)
          if (biliResponse.data.status === 'success') {
            console.log('B站历史记录删除成功:', biliResponse.data)
          } else {
            console.error('B站历史记录删除失败:', biliResponse.data)
            // 即使B站删除失败，也继续删除本地记录
          }
        } catch (error) {
          console.error('B站历史记录删除失败:', error)
          // 即使B站删除失败，也继续删除本地记录
        }
      }
    }

    const response = await batchDeleteHistory([{
      bvid: record.bvid,
      view_at: record.view_at,
    }])
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message + (syncDeleteToBilibili ? '，并已同步删除B站历史记录' : ''),
      })
      fetchHistoryByDateRange()
    } else {
      throw new Error(response.data.message || '删除失败')
    }
  } catch (error) {
    if (error.toString().includes('cancel')) return

    showNotify({
      type: 'danger',
      message: error.response?.data?.detail || error.message || '删除失败',
    })
  }
}

// 判断某一天是否被全部选中
const isDaySelected = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const dayStart = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime() / 1000
  const dayEnd = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1).getTime() / 1000 - 1

  const dayRecords = records.value.filter(record =>
    record.view_at >= dayStart && record.view_at <= dayEnd,
  )

  return dayRecords.every(record =>
    selectedRecords.value.has(`${record.bvid}_${record.view_at}`),
  )
}

// 切换某一天的所有记录的选中状态
const toggleDaySelection = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const dayStart = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime() / 1000
  const dayEnd = new Date(date.getFullYear(), date.getMonth(), date.getDate() + 1).getTime() / 1000 - 1

  const dayRecords = records.value.filter(record =>
    record.view_at >= dayStart && record.view_at <= dayEnd,
  )

  const allSelected = isDaySelected(timestamp)

  dayRecords.forEach(record => {
    const key = `${record.bvid}_${record.view_at}`
    if (allSelected) {
      selectedRecords.value.delete(key)
    } else {
      selectedRecords.value.add(key)
    }
  })
}

// 处理备注更新
const handleRemarkUpdate = (data) => {
  const key = `${data.bvid}_${data.view_at}`
  remarkData.value[key] = {
    bvid: data.bvid,
    view_at: data.view_at,
    remark: data.remark,
    remark_time: data.remark_time,
  }
}

// 添加打开详情对话框的方法
const openVideoDetail = (record) => {
  selectedRecord.value = record
  showDetailDialog.value = true
}

// 处理网格视图下载按钮点击
const handleDownloadGrid = (record) => {
  console.log('handleDownloadGrid - 处理网格视图下载按钮点击')
  selectedRecord.value = record
  // 确保设置为单个视频下载模式，而非批量下载
  isBatchDownload.value = false
  showDownloadDialog.value = true
}

// 批量下载视频列表
const batchVideos = ref([])
const isBatchDownload = ref(false)
const currentVideoIndex = ref(0)

// 批量下载处理函数
const handleBatchDownload = async () => {
  if (selectedRecords.value.size === 0) {
    showNotify({
      type: 'warning',
      message: '请先选择要下载的记录',
    })
    return
  }

  try {
    // 从选中的记录中提取视频信息
    const videoRecords = [...selectedRecords.value].map(key => {
      const [bvid, timestamp] = key.split('_')
      return records.value.find(r => r.bvid === bvid && String(r.view_at) === timestamp)
    }).filter(record => record && record.business === 'archive') // 过滤掉未找到的记录和非视频记录

    if (videoRecords.length === 0) {
      showNotify({
        type: 'warning',
        message: '选中的记录中没有有效的视频',
      })
      return
    }

    // 准备批量下载的视频列表
    batchVideos.value = videoRecords.map(record => ({
      bvid: record.bvid,
      cid: record.cid,
      title: record.title,
      author: record.author_name,
      cover: record.cover,
    }))

    // 设置批量下载模式
    isBatchDownload.value = true
    currentVideoIndex.value = 0

    // 显示下载对话框
    if (batchVideos.value.length > 0) {
      // 设置第一个视频作为当前下载视频
      const firstVideo = batchVideos.value[0]
      selectedRecord.value = {
        title: firstVideo.title,
        author_name: firstVideo.author,
        bvid: firstVideo.bvid,
        cover: firstVideo.cover,
        cid: firstVideo.cid,
      }
      showDownloadDialog.value = true
    }
  } catch (error) {
    console.error('批量下载准备失败:', error)
    showNotify({
      type: 'danger',
      message: '批量下载准备失败: ' + (error.message || '未知错误'),
    })
  }
}

// 处理下载完成
const handleDownloadComplete = async () => {
  // 下载完成后重新检查下载状态
  await batchCheckDownloadStatus()
}

// 调试函数，在控制台显示所有视频的CID和下载状态
// 处理收藏按钮点击（网格布局）
const handleFavoriteGrid = (record) => {
  // 获取视频ID，适配不同的属性名（aid或avid）
  let videoId = record.aid || record.avid || (record.business === 'archive' ? record.oid : null)
  if (videoId) {
    videoId = parseInt(videoId, 10)
  }
  if (!videoId || isNaN(videoId)) {
    showNotify({ type: 'warning', message: '无法识别视频ID' })
    return
  }

  // 检查是否已收藏
  if (isVideoFavorited(videoId)) {
    // 如果已收藏，提示是否取消收藏
    showDialog({
      title: '取消收藏',
      message: '确定要取消收藏该视频吗？',
      showCancelButton: true,
    }).then(async () => {
      // 获取视频的收藏夹列表
      const folders = getVideoFavoriteFolders(videoId)
      if (folders.length > 0) {
        // 获取收藏夹ID
        const folderIds = folders.map(folder => folder.media_id)
        try {
          // 发送取消收藏请求
          const response = await favoriteResource({
            rid: videoId,
            del_media_ids: folderIds.join(','),
          })

          // 如果远程操作成功，同步本地数据库（不提示用户）
          if (response.data.status === 'success') {
            try {
              await localBatchFavoriteResource({
                rids: videoId.toString(),
                del_media_ids: folderIds.join(','),
                operation_type: 'local', // 只在本地操作
              })
            } catch (syncError) {
              console.error('本地同步取消收藏失败，但不影响用户体验:', syncError)
            }

            // 更新收藏状态
            favoriteStatus.value[videoId] = {
              is_favorited: false,
              favorite_folders: [],
            }

            showNotify({ type: 'success', message: '已取消收藏' })

            // 刷新收藏状态
            await batchCheckFavorites()
          } else {
            throw new Error(response.data.message || '取消收藏失败')
          }
        } catch (error) {
          console.error('取消收藏失败:', error)
          showNotify({ type: 'danger', message: '取消收藏失败: ' + (error.message || '未知错误') })
        }
      }
    }).catch(() => {
      // 取消操作，不做任何处理
    })
  } else {
    // 如果未收藏，打开收藏夹选择对话框
    showFavoriteDialog.value = true
    favoriteVideoInfo.value = record
  }
}

// 处理收藏夹选择对话框
const handleFavoriteDone = async (result) => {
  console.log('handleFavoriteDone - 处理收藏完成', result)
  if (result && result.success) {
    if (result.isBatch) {
      // 批量收藏完成
      showNotify({ type: 'success', message: `批量收藏完成，已添加${result.videoInfo.selectedCount}个视频到收藏夹` })

      // 更新收藏状态
      if (result.videoInfo.batchIds) {
        const videoIds = result.videoInfo.batchIds.split(',').map(id => parseInt(id.trim(), 10)).filter(id => !isNaN(id))

        // 为每个视频ID更新收藏状态
        videoIds.forEach(videoId => {
          favoriteStatus.value[videoId] = {
            is_favorited: true,
            favorite_folders: result.folders.map(folderId => ({
              media_id: folderId,
              title: '收藏夹',
            })),
          }
        })

        // 取消批量模式并清空选择
        selectedRecords.value.clear()

        // 刷新收藏状态
        await batchCheckFavorites()
      }
    } else {
      // 单个视频收藏完成
      showNotify({ type: 'success', message: '收藏成功' })

      // 更新收藏状态
      let videoId = result.videoInfo.aid || result.videoInfo.avid ||
        (result.videoInfo.business === 'archive' ? result.videoInfo.oid : null)

      if (videoId) {
        // 确保ID是整数
        videoId = parseInt(videoId, 10)

        if (!isNaN(videoId)) {
          // 设置为已收藏状态
          favoriteStatus.value[videoId] = {
            is_favorited: true,
            favorite_folders: result.folders.map(folderId => ({
              media_id: folderId,
              title: '收藏夹', // 由于API返回的是ID列表，我们不知道具体名称，所以用通用名称
            })),
          }

          // 重新获取精确的收藏夹信息
          await batchCheckFavorites()
        }
      }
    }
  }
}

// 批量收藏选中的记录
const handleBatchFavorite = async () => {
  if (selectedRecords.value.size === 0) {
    showNotify({
      type: 'warning',
      message: '请先选择要收藏的记录',
    })
    return
  }

  // 从选中的记录中提取视频ID
  const videoRecords = [...selectedRecords.value].map(key => {
    const [bvid, timestamp] = key.split('_')
    return records.value.find(r => r.bvid === bvid && String(r.view_at) === timestamp)
  }).filter(record => record) // 过滤掉未找到的记录

  // 提取视频ID
  const oids = videoRecords.map(record => {
    const id = record.aid || record.avid || (record.business === 'archive' ? record.oid : null)
    return id ? parseInt(id, 10) : null
  }).filter(oid => oid !== null && !isNaN(oid))

  if (oids.length === 0) {
    showNotify({
      type: 'warning',
      message: '选中的记录中没有有效的视频ID',
    })
    return
  }

  // 打开收藏夹选择对话框
  showFavoriteDialog.value = true
  favoriteVideoInfo.value = {
    isBatch: true,
    batchIds: oids.join(','),
    selectedCount: oids.length,
  }
}

// 计算选中记录中已收藏的数量
const hasFavoritedVideos = computed(() => {
  return favoritedCount.value > 0
})

const favoritedCount = computed(() => {
  if (selectedRecords.value.size === 0) return 0

  let count = 0
  selectedRecords.value.forEach(key => {
    const [bvid, timestamp] = key.split('_')
    const record = records.value.find(r => r.bvid === bvid && String(r.view_at) === timestamp)
    if (record) {
      const videoId = record.aid || record.avid || (record.business === 'archive' ? record.oid : null)
      if (videoId && isVideoFavorited(parseInt(videoId, 10))) {
        count++
      }
    }
  })

  return count
})

// 计算选中记录中未收藏的数量
const unfavoritedCount = computed(() => {
  if (selectedRecords.value.size === 0) return 0
  return selectedRecords.value.size - favoritedCount.value
})

// 检查是否所有选中的记录都已收藏
const isAllFavorited = computed(() => {
  return selectedRecords.value.size > 0 && favoritedCount.value === selectedRecords.value.size
})

// 检查是否所有选中的记录都未收藏
computed(() => {
  return selectedRecords.value.size > 0 && unfavoritedCount.value === selectedRecords.value.size
})
// 复制选中视频的链接到剪贴板
const handleCopyLinks = async () => {
  if (selectedRecords.value.size === 0) {
    showNotify({
      type: 'warning',
      message: '请先选择要复制链接的记录',
    })
    return
  }

  try {
    // 从选中的记录中提取视频信息
    const videoRecords = [...selectedRecords.value].map(key => {
      const [bvid, timestamp] = key.split('_')
      return records.value.find(r => r.bvid === bvid && String(r.view_at) === timestamp)
    }).filter(record => record) // 过滤掉未找到的记录

    // 生成链接列表
    const links = videoRecords.map(record => {
      let url = ''
      switch (record.business) {
        case 'archive':
          url = `https://www.bilibili.com/video/${record.bvid}`
          break
        case 'article':
          url = `https://www.bilibili.com/read/cv${record.oid}`
          break
        case 'article-list':
          url = `https://www.bilibili.com/read/readlist/rl${record.oid}`
          break
        case 'live':
          url = `https://live.bilibili.com/${record.oid}`
          break
        case 'pgc':
          url = record.uri || `https://www.bilibili.com/bangumi/play/ep${record.epid}`
          break
        case 'cheese':
          url = record.uri || `https://www.bilibili.com/cheese/play/ep${record.epid}`
          break
        default:
          console.warn('未知的业务类型:', record.business)
          return null
      }
      return url
    }).filter(url => url) // 过滤掉无效的URL

    // 复制到剪贴板
    if (links.length > 0) {
      await copyToClipboard(links.join('\n'))
      showNotify({
        type: 'success',
        message: `已复制 ${links.length} 个链接到剪贴板`,
      })
    } else {
      showNotify({
        type: 'warning',
        message: '没有找到有效的链接',
      })
    }
  } catch (error) {
    console.error('复制链接失败:', error)
    showNotify({
      type: 'danger',
      message: '复制链接失败: ' + (error.message || '未知错误'),
    })
  }
}

// 复制到剪贴板函数
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch (err) {
    console.error('复制失败:', err)
    throw new Error('复制到剪贴板失败，请检查浏览器权限')
  }
}

// 批量取消收藏选中的记录
const handleBatchUnfavorite = async () => {
  if (selectedRecords.value.size === 0) {
    showNotify({
      type: 'warning',
      message: '请先选择要取消收藏的记录',
    })
    return
  }

  try {
    // 确认取消收藏
    await showDialog({
      title: '确认取消收藏',
      message: `确定要取消${favoritedCount.value}个视频的收藏吗？`,
      showCancelButton: true,
    })

    // 从选中的记录中提取视频ID
    const videoRecords = [...selectedRecords.value].map(key => {
      const [bvid, timestamp] = key.split('_')
      return records.value.find(r => r.bvid === bvid && String(r.view_at) === timestamp)
    }).filter(record => record) // 过滤掉未找到的记录

    // 过滤出已收藏的视频
    const favoritedRecords = videoRecords.filter(record => {
      const videoId = record.aid || record.avid || (record.business === 'archive' ? record.oid : null)
      return videoId && isVideoFavorited(parseInt(videoId, 10))
    })

    if (favoritedRecords.length === 0) {
      showNotify({
        type: 'warning',
        message: '选中的记录中不包含已收藏的视频',
      })
      return
    }

    // 提取视频ID
    const videoIds = favoritedRecords.map(record => {
      const id = record.aid || record.avid || (record.business === 'archive' ? record.oid : null)
      return id ? parseInt(id, 10) : null
    }).filter(id => id !== null && !isNaN(id))

    if (videoIds.length === 0) {
      showNotify({
        type: 'warning',
        message: '无法获取有效的视频ID',
      })
      return
    }

    // 获取每个视频的收藏夹列表和执行取消收藏操作
    let results

    // 获取每个视频的收藏夹列表
    const unfavoritePromises = videoIds.map(async videoId => {
      const folders = getVideoFavoriteFolders(videoId)
      if (folders.length > 0) {
        // 获取收藏夹ID
        const folderIds = folders.map(folder => folder.media_id)

        // 发送取消收藏请求
        const response = await favoriteResource({
          rid: videoId,
          del_media_ids: folderIds.join(','),
        })

        // 如果远程操作成功，同步本地数据库（不提示用户）
        if (response.data.status === 'success') {
          try {
            await localBatchFavoriteResource({
              rids: videoId.toString(),
              del_media_ids: folderIds.join(','),
              operation_type: 'local', // 只在本地操作
            })
          } catch (syncError) {
            console.error('本地同步取消收藏失败，但不影响用户体验:', syncError)
          }
        }

        return { videoId, success: response.data.status === 'success' }
      }
      return { videoId, success: false, reason: '没有找到收藏夹' }
    })

    results = await Promise.all(unfavoritePromises)
    const successCount = results.filter(r => r.success).length

    if (successCount > 0) {
      showNotify({
        type: 'success',
        message: `成功取消${successCount}个视频的收藏`,
      })

      // 更新收藏状态
      results.forEach(result => {
        if (result.success) {
          favoriteStatus.value[result.videoId] = {
            is_favorited: false,
            favorite_folders: [],
          }
        }
      })

      // 刷新收藏状态
      await batchCheckFavorites()

      // 取消选择
      selectedRecords.value.clear()
    } else {
      showNotify({
        type: 'danger',
        message: '取消收藏失败',
      })
    }
  } catch (error) {
    if (error.toString().includes('cancel')) return

    console.error('批量取消收藏失败:', error)
    showNotify({
      type: 'danger',
      message: '批量取消收藏失败: ' + (error.message || '未知错误'),
    })
  }
}

// 处理收藏按钮点击（列表布局）
const handleFavorite = (record) => {
  // 获取视频ID，适配不同的属性名（aid或avid）
  const videoId = record.aid || record.avid || (record.business === 'archive' ? record.oid : null)

  if (!videoId) {
    showNotify({ type: 'warning', message: '无法识别视频ID' })
    return
  }

  // 检查是否已收藏
  const parsedVideoId = parseInt(videoId, 10)
  if (isVideoFavorited(parsedVideoId)) {
    // 如果已收藏，提示是否取消收藏
    showDialog({
      title: '取消收藏',
      message: '确定要取消收藏该视频吗？',
      showCancelButton: true,
    }).then(async () => {
      // 获取视频的收藏夹列表
      const folders = getVideoFavoriteFolders(parsedVideoId)
      if (folders.length > 0) {
        // 获取收藏夹ID
        const folderIds = folders.map(folder => folder.media_id)
        try {
          // 发送取消收藏请求
          const response = await favoriteResource({
            rid: parsedVideoId,
            del_media_ids: folderIds.join(','),
          })

          // 如果远程操作成功，同步本地数据库（不提示用户）
          if (response.data.status === 'success') {
            try {
              await localBatchFavoriteResource({
                rids: parsedVideoId.toString(),
                del_media_ids: folderIds.join(','),
                operation_type: 'local', // 只在本地操作
              })
            } catch (syncError) {
              console.error('本地同步取消收藏失败，但不影响用户体验:', syncError)
            }

            // 更新收藏状态
            favoriteStatus.value[parsedVideoId] = {
              is_favorited: false,
              favorite_folders: [],
            }

            showNotify({ type: 'success', message: '已取消收藏' })

            // 刷新收藏状态
            await batchCheckFavorites()
          } else {
            throw new Error(response.data.message || '取消收藏失败')
          }
        } catch (error) {
          console.error('取消收藏失败:', error)
          showNotify({ type: 'danger', message: '取消收藏失败: ' + (error.message || '未知错误') })
        }
      }
    }).catch(() => {
      // 取消操作，不做任何处理
    })
  } else {
    // 如果未收藏，打开收藏夹选择对话框
    showFavoriteDialog.value = true
    favoriteVideoInfo.value = record
  }
}
</script>
