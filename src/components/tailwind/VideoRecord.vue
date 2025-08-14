<template>
  <!-- 每条记录的容器 -->
  <div
    class="mx-auto max-w-2xl cursor-pointer border-b border-gray-200 transition-all duration-200 ease-in-out sm:px-4 lg:max-w-4xl lg:px-0 relative"
    :class="{
      'group': !showDownloadDialog,
      'border-[#fb7299] bg-[#fff9fb] ring-1 ring-[#fb7299]/20': isBatchMode && isSelected,
      'hover:border-[#fb7299] hover:bg-[#f5f5f5] hover:shadow-md': !isBatchMode || !isSelected
    }"
    @click="handleClick"
  >
    <!-- 内层容器 -->
    <div class="p-2">
      <!-- 当类型为文章或文集时，图片铺满整行，标题在上方 -->
      <div v-if="record.business === 'article-list' || record.business === 'article'">
        <!-- 标题在封面图片上方 -->
        <div class="mb-2">
          <div
            class="line-clamp-2 text-gray-900 lm:text-sm lg:font-semibold"
            v-html="isPrivacyMode ? '******' : highlightedTitle"
            :class="{ 'blur-sm': isPrivacyMode }"
          ></div>
        </div>
        <!-- 封面图片，铺满整行 -->
        <div class="relative h-28 w-full overflow-hidden rounded-lg">
          <!-- 删除按钮 -->
          <div v-if="!isBatchMode"
               class="absolute right-0 top-0 z-20 hidden group-hover:flex flex-row items-center justify-end pt-1 pr-1">
            <div class="flex items-center justify-end space-x-2">
              <!-- 下载按钮 - 只对视频类型显示 -->
              <div v-if="record.business === 'archive'"
                   class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop.prevent="handleDownload"
                   title="下载视频">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
              </div>
              <!-- 收藏按钮 - 不对直播类型显示 -->
              <div v-if="record.business !== 'live'"
                   class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop.prevent="handleFavorite"
                   title="收藏视频">
                <svg class="w-4 h-4" :class="isVideoFavorited ? 'text-yellow-400' : 'text-white'" :fill="isVideoFavorited ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
              </div>
              <!-- 删除按钮 -->
              <div class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop="handleDelete"
                   title="删除记录">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <!-- 详情按钮 - 只对普通视频类型显示 -->
              <div v-if="record.business === 'archive'"
                   class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop="showDetailDialog = true"
                   title="查看详情">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>
          <!-- 多选框 -->
          <div v-if="isBatchMode"
               class="absolute left-2 top-2 z-10"
               @click.stop="$emit('toggle-selection', record)">
            <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                 :class="isSelected ? 'bg-[#fb7299] border-[#fb7299]' : 'border-white bg-black/20'">
              <svg v-if="isSelected" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
          <!-- 批量模式下的收藏状态图标 - 不对直播类型显示 -->
          <div v-if="isBatchMode && record.business !== 'live'"
               class="absolute right-2 top-2 z-10">
            <div class="flex items-center justify-center w-6 h-6 rounded-full bg-black/40 backdrop-blur-sm">
              <svg class="w-4 h-4" :class="isVideoFavorited ? 'text-yellow-400' : 'text-white'" :fill="isVideoFavorited ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
            </div>
          </div>
          <!-- 已下载标识 -->
          <div v-if="isDownloaded && record.business === 'archive'"
               class="absolute left-0 top-0 z-10">
            <div class="bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] text-white font-semibold px-2 py-0.5 text-xs flex items-center space-x-1.5 rounded-br-md shadow-md">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>已下载</span>
            </div>
          </div>

          <!-- 收藏状态标识 - 不对直播类型显示 -->
          <div v-if="isVideoFavorited && record.business !== 'live'"
               class="absolute right-0 top-0 z-10">
            <div class="bg-gradient-to-r from-amber-500 to-yellow-400 text-white font-semibold px-2 py-0.5 text-xs flex items-center space-x-1.5 rounded-bl-md shadow-md">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              <span>已收藏</span>
            </div>
          </div>

          <img
            :src="normalizeImageUrl(record.cover || record.covers[0])"
            class="h-full w-full object-cover transition-all duration-300"
            :class="{ 'blur-md': isPrivacyMode }"
            alt=""
          />
          <!-- 右上角的类型角标 -->
          <div
            v-if="record.badge"
            class="absolute right-1 top-1 rounded bg-[#FF6699] px-1 py-0.5 text-[10px] font-semibold text-white"
          >
            {{ record.badge }}
          </div>
        </div>
        <!-- 文章类型：作者信息、观看设备、时间放在封面图片下方 -->
        <div class="mt-2 flex items-center justify-between text-sm text-[#99a2aa] lm:text-xs">
          <!-- 左侧：仅当类型不是剧集或课程时，显示作者头像和名字 -->
          <div
            v-if="record.business !== 'cheese' && record.business !== 'pgc'"
            class="flex items-center space-x-2"
            @click.stop
          >
            <img
              :src="normalizeImageUrl(record.author_face)"
              alt="author"
              class="h-4 w-4 cursor-pointer rounded-full transition-all duration-300 hover:scale-110 lg:h-8 lg:w-8"
              :class="{ 'blur-md': isPrivacyMode }"
              @click="handleAuthorClick"
              :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
            />
            <p
              class="cursor-pointer transition-colors hover:text-[#FF6699]"
              @click="handleAuthorClick"
              :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
              v-html="isPrivacyMode ? '******' : highlightedAuthorName"
            ></p>
          </div>
          <!-- 右侧：设备和时间信息 -->
          <div class="flex items-center space-x-2">
            <img
              v-if="record.dt === 1 || record.dt === 3 || record.dt === 5 || record.dt === 7"
              src="/Mobile.svg"
              alt="Mobile"
              class="h-4 w-4 lg:h-8 lg:w-8"
            />
            <img
              v-else-if="record.dt === 2 || record.dt === 33"
              src="/PC.svg"
              alt="PC"
              class="h-4 w-4 lg:h-8 lg:w-8"
            />
            <img
              v-else-if="record.dt === 4 || record.dt === 6"
              src="/Pad.svg"
              alt="Pad"
              class="h-4 w-4 lg:h-8 lg:w-8"
            />
            <p v-else>未知设备</p>
            <!-- 显示时间 -->
            <span>{{ formatTimestamp(record.view_at) }}</span>
          </div>
        </div>
      </div>

      <!-- 其他类型的展示方式 -->
      <div v-else class="flex space-x-2">
        <!-- 封面图片区域 -->
        <div class="relative h-20 w-32 overflow-hidden rounded-lg sm:h-28 sm:w-40">
          <!-- 多选框 -->
          <div v-if="isBatchMode"
               class="absolute left-2 top-2 z-10"
               @click.stop="$emit('toggle-selection', record)">
            <div class="w-5 h-5 rounded border-2 flex items-center justify-center"
                 :class="isSelected ? 'bg-[#fb7299] border-[#fb7299]' : 'border-white bg-black/20'">
              <svg v-if="isSelected" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          </div>
          <!-- 批量模式下的收藏状态图标 - 不对直播类型显示 -->
          <div v-if="isBatchMode && record.business !== 'live'"
               class="absolute right-2 top-2 z-10">
            <div class="flex items-center justify-center w-6 h-6 rounded-full bg-black/40 backdrop-blur-sm">
              <svg class="w-4 h-4" :class="isVideoFavorited ? 'text-yellow-400' : 'text-white'" :fill="isVideoFavorited ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
            </div>
          </div>
          <!-- 已下载标识 -->
          <div v-if="isDownloaded && record.business === 'archive'"
               class="absolute left-0 top-0 z-10">
            <div class="bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] text-white font-semibold px-2 py-0.5 text-xs flex items-center space-x-1.5 rounded-br-md shadow-md">
              <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
              </svg>
              <span>已下载</span>
            </div>
          </div>

          <!-- 收藏状态标识 - 不对直播类型显示 -->
          <div v-if="isVideoFavorited && record.business !== 'live'"
               class="absolute right-0 top-0 z-10">
            <div class="bg-gradient-to-r from-amber-500 to-yellow-400 text-white font-semibold px-2 py-0.5 text-xs flex items-center space-x-1.5 rounded-bl-md shadow-md">
              <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
              </svg>
              <span>已收藏</span>
            </div>
          </div>

          <img
            v-if="record.cover"
            :src="normalizeImageUrl(record.cover)"
            class="h-full w-full object-cover transition-all duration-300"
            :class="{ 'blur-md': isPrivacyMode }"
            alt=""
          />
          <div v-else>
            <div v-for="(cover, index) in record.covers" :key="index" class="mb-1">
              <img
                :src="normalizeImageUrl(cover)"
                class="h-full w-full object-cover transition-all duration-300"
                :class="{ 'blur-md': isPrivacyMode }"
                alt=""
              />
            </div>
          </div>
          <!-- 右上角的类型角标 -->
          <div
            v-if="record.badge"
            class="absolute right-1 top-1 rounded bg-[#FF6699] px-1 py-0.5 text-[10px] font-semibold text-white"
          >
            {{ record.badge }}
          </div>
          <!-- 右下角的时间进度角标和进度条，仅当不是文章时显示 -->
          <div
            v-if="
              record.business !== 'article-list' &&
              record.business !== 'article' &&
              record.business !== 'live'
            "
          >
            <div
              class="absolute bottom-1 right-1 rounded bg-black/50 px-1 py-1 text-[10px] font-semibold text-white"
            >
              <span>{{ formatDuration(record.progress) }}</span>
              <span>/</span>
              <span>{{ formatDuration(record.duration) }}</span>
            </div>
            <div class="absolute bottom-0 left-0 h-0.5 w-full bg-black">
              <div
                class="h-full bg-[#FF6699]"
                :style="{ width: getProgressWidth(record.progress, record.duration) }"
              ></div>
            </div>
          </div>
        </div>

        <!-- 右侧内容区域 -->
        <div class="ml-2 flex flex-1 flex-col justify-between lm:text-sm lg:font-semibold relative">
          <!-- 删除按钮 -->
          <div v-if="!isBatchMode"
               class="absolute right-0 top-0 z-20 hidden group-hover:flex flex-row items-center justify-end pt-1 pr-1">
            <div class="flex items-center justify-end space-x-2">
              <!-- 下载按钮 - 只对视频类型显示 -->
              <div v-if="record.business === 'archive'"
                   class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop.prevent="handleDownload"
                   title="下载视频">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
              </div>
              <!-- 收藏按钮 - 不对直播类型显示 -->
              <div v-if="record.business !== 'live'"
                   class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop.prevent="handleFavorite"
                   title="收藏视频">
                <svg class="w-4 h-4" :class="isVideoFavorited ? 'text-yellow-400' : 'text-white'" :fill="isVideoFavorited ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
              </div>
              <!-- 删除按钮 -->
              <div class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop="handleDelete"
                   title="删除记录">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </div>
              <!-- 详情按钮 - 只对普通视频类型显示 -->
              <div v-if="record.business === 'archive'"
                   class="flex items-center justify-center w-7 h-7 bg-[#7d7c75]/60 backdrop-blur-sm hover:bg-[#7d7c75]/80 rounded-md cursor-pointer transition-all duration-200"
                   @click.stop="showDetailDialog = true"
                   title="查看详情">
                <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
            </div>
          </div>
          <div class="items-center justify-between lg:flex">
            <div
              class="line-clamp-2 text-gray-900 lm:text-sm lg:font-semibold"
              v-html="isPrivacyMode ? '******' : highlightedTitle"
              :class="{ 'blur-sm': isPrivacyMode }"
            ></div>
          </div>
          <div class="flex items-center space-x-2">
            <span
              v-if="record.business !== 'pgc'"
              class="inline-flex items-center rounded-md bg-[#f1f2f3] px-2 py-1 text-xs text-[#71767d]"
            >
              {{ record.tag_name }}
            </span>

            <!-- 备注输入框 -->
            <div class="flex-1 relative group" @click.stop>
              <div class="flex items-center space-x-1">
                <span class="text-xs text-[#fb7299]">备注:</span>
                <input
                  type="text"
                  v-model="remarkContent"
                  @focus="handleRemarkFocus"
                  @blur="handleRemarkBlur"
                  placeholder="添加备注..."
                  :disabled="isPrivacyMode"
                  class="flex-1 px-2 py-1 text-xs text-[#fb7299] bg-[#f8f8f8] rounded border-0 border-b border-transparent hover:border-gray-200 focus:border-[#fb7299] focus:ring-0 transition-colors duration-200 placeholder-[#fb7299]/50"
                  :class="{ 'blur-sm': isPrivacyMode }"
                />
                <span v-if="remarkTime" class="text-xs text-gray-400">{{ formatRemarkTime(remarkTime) }}</span>
              </div>
              <div v-if="!remarkContent && !isPrivacyMode" class="absolute right-2 top-1/2 -translate-y-1/2 hidden group-hover:block">
                <svg class="w-3 h-3 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </div>
            </div>
          </div>

          <div class="flex items-end justify-between text-sm text-[#99a2aa] lm:text-xs">
            <!-- PGC内容显示long_title -->
            <div v-if="record.business === 'pgc'" class="flex items-center space-x-2">
              <p class="text-[#99a2aa]">{{ record.long_title }}</p>
            </div>
            <!-- 非PGC内容显示UP主信息 -->
            <div v-else class="flex items-center space-x-2" @click.stop>
              <img
                :src="normalizeImageUrl(record.author_face)"
                alt="author"
                class="h-5 w-5 cursor-pointer rounded-full transition-all duration-300 hover:scale-110 lg:h-8 lg:w-8"
                :class="{ 'blur-md': isPrivacyMode }"
                @click="handleAuthorClick"
                :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
              />
              <p
                class="cursor-pointer transition-colors hover:text-[#FF6699]"
                @click="handleAuthorClick"
                :title="isPrivacyMode ? '隐私模式已开启' : `访问 ${record.author_name} 的个人空间`"
                v-html="isPrivacyMode ? '******' : highlightedAuthorName"
              ></p>
            </div>

            <div class="flex items-center space-x-2">
              <img
                v-if="record.dt === 1 || record.dt === 3 || record.dt === 5 || record.dt === 7"
                src="/Mobile.svg"
                alt="Mobile"
                class="h-4 w-4 lg:h-8 lg:w-8"
              />
              <img
                v-else-if="record.dt === 2 || record.dt === 33"
                src="/PC.svg"
                alt="PC"
                class="h-4 w-4 lg:h-8 lg:w-8"
              />
              <img
                v-else-if="record.dt === 4 || record.dt === 6"
                src="/Pad.svg"
                alt="Pad"
                class="h-4 w-4 lg:h-8 lg:w-8"
              />
              <p v-else>未知设备</p>

              <!-- 显示时间 -->
              <span>{{ formatTimestamp(record.view_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 下载弹窗 -->
    <Teleport to="body">
      <DownloadDialog
        v-model:show="showDownloadDialog"
        :video-info="{
          title: record.title,
          author: record.author_name,
          bvid: record.bvid,
          cover: record.cover || record.covers?.[0],
          cid: record.cid
        }"
        :is-batch-download="false"
      />
    </Teleport>

    <!-- 视频详情对话框 -->
    <Teleport to="body">
      <VideoDetailDialog
        :modelValue="showDetailDialog"
        @update:modelValue="showDetailDialog = $event"
        :video="record"
        :remarkData="remarkData"
        @remark-updated="$emit('remark-updated', $event)"
      />
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { usePrivacyStore } from '../../store/privacy'
import { showDialog, showNotify } from 'vant'
import { batchDeleteHistory, updateVideoRemark, deleteBilibiliHistory } from '../../api/api'
import 'vant/es/dialog/style'
import 'vant/es/popup/style'
import 'vant/es/field/style'
import DownloadDialog from './DownloadDialog.vue'
import VideoDetailDialog from './VideoDetailDialog.vue'
import { openInBrowser } from '@/utils/openUrl.js'
import { normalizeImageUrl } from '@/utils/imageUrl.js'

const { isPrivacyMode } = usePrivacyStore()

const props = defineProps({
  record: {
    type: Object,
    required: true
  },
  searchKeyword: {
    type: String,
    default: ''
  },
  searchType: {
    type: String,
    default: 'title'
  },
  isBatchMode: {
    type: Boolean,
    default: false
  },
  isSelected: {
    type: Boolean,
    default: false
  },
  remarkData: {
    type: Object,
    default: () => ({})
  },
  isDownloaded: {
    type: Boolean,
    default: false
  },
  isVideoFavorited: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'toggle-selection',
  'refresh-data',
  'remark-updated',
  'favorite'
])

const remarkContent = ref('')
const originalRemark = ref('') // 用于存储原始备注内容
const remarkTime = ref(null)
const showDetailDialog = ref(false)

// 高亮显示匹配的文本
const highlightText = (text) => {
  if (!props.searchKeyword || !text) return text

  // 将搜索关键词按空格分割成数组
  const keywords = props.searchKeyword.split(/\s+/).filter(k => k)
  let highlightedText = text

  // 对每个关键词进行高亮处理
  keywords.forEach(keyword => {
    const regex = new RegExp(keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')
    highlightedText = highlightedText.replace(regex, match => `<span class="text-[#FF6699]">${match}</span>`)
  })

  return highlightedText
}

// 获取高亮后的标题
const highlightedTitle = computed(() => {
  if (!props.searchKeyword) return props.record.title
  if (props.searchType === 'all' || props.searchType === 'title') {
    return highlightText(props.record.title)
  }
  return props.record.title
})

// 获取高亮后的作者名称
const highlightedAuthorName = computed(() => {
  if (!props.searchKeyword) return props.record.author_name
  if (props.searchType === 'all' || props.searchType === 'author') {
    return highlightText(props.record.author_name)
  }
  return props.record.author_name
})

// 处理点击事件
const handleClick = () => {
  if (props.isBatchMode) {
    emit('toggle-selection', props.record)
  } else {
    handleContentClick()
  }
}

// 处理内容点击事件
const handleContentClick = async () => {
  let url = ''

  switch (props.record.business) {
    case 'archive':
      url = `https://www.bilibili.com/video/${props.record.bvid}`
      break
    case 'article':
      url = `https://www.bilibili.com/read/cv${props.record.oid}`
      break
    case 'article-list':
      url = `https://www.bilibili.com/read/readlist/rl${props.record.oid}`
      break
    case 'live':
      url = `https://live.bilibili.com/${props.record.oid}`
      break
    case 'pgc':
      url = props.record.uri || `https://www.bilibili.com/bangumi/play/ep${props.record.epid}`
      break
    case 'cheese':
      url = props.record.uri || `https://www.bilibili.com/cheese/play/ep${props.record.epid}`
      break
    default:
      console.warn('未知的业务类型:', props.record.business)
      return
  }

  if (url) {
    await openInBrowser(url)
  }
}

// 处理UP主点击事件
const handleAuthorClick = async () => {
  const url = `https://space.bilibili.com/${props.record.author_mid}`
  await openInBrowser(url)
}

// 修改时间戳显示相关的代码
const formatTimestamp = (timestamp) => {
  // 检查 timestamp 是否有效
  if (!timestamp) {
    console.warn('Invalid timestamp:', timestamp)
    return '时间未知'
  }

  try {
    // 将秒级时间戳转换为毫秒级
    const date = new Date(timestamp * 1000)
    const now = new Date()

    // 检查日期是否有效
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

const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完'
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0')
  const secs = String(seconds % 60).padStart(2, '0')
  return `${minutes}:${secs}`
}

const getProgressWidth = (progress, duration) => {
  if (progress === -1) return '100%'
  if (duration === 0) return '0%'
  return `${(progress / duration) * 100}%`
}

// 处理删除事件
const handleDelete = async () => {
  try {
    // 检查是否需要同步删除B站历史记录
    const syncDeleteToBilibili = localStorage.getItem('syncDeleteToBilibili') === 'true'

    // 根据是否同步删除B站历史记录，显示不同的确认信息
    await showDialog({
      title: '确认删除',
      message: syncDeleteToBilibili
        ? '确定要删除这条记录吗？此操作将同时删除B站服务器上的历史记录，不可恢复。'
        : '确定要删除这条记录吗？此操作不可恢复。',
      showCancelButton: true,
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      confirmButtonColor: '#fb7299'
    })

    if (syncDeleteToBilibili) {
      try {
        // 构建kid
        let kid = ''
        const business = props.record.business || 'archive'

        // 根据业务类型构建kid
        switch (business) {
          case 'archive':
            // 使用oid而不是bvid
            kid = `${business}_${props.record.oid}`
            break
          case 'live':
            kid = `${business}_${props.record.oid}`
            break
          case 'article':
            kid = `${business}_${props.record.oid}`
            break
          case 'pgc':
            kid = `${business}_${props.record.oid || props.record.ssid}`
            break
          case 'article-list':
            kid = `${business}_${props.record.oid || props.record.rlid}`
            break
          default:
            kid = `${business}_${props.record.oid || props.record.bvid}`
            break
        }

        if (kid) {
          // 调用B站历史记录删除API
          const biliResponse = await deleteBilibiliHistory(kid, true)
          if (biliResponse.data.status === 'success') {
            console.log('B站历史记录删除成功:', biliResponse.data)
          } else {
            console.error('B站历史记录删除失败:', biliResponse.data)
            throw new Error(biliResponse.data.message || '删除B站历史记录失败')
          }
        }
      } catch (error) {
        console.error('B站历史记录删除失败:', error)
        // 即使B站删除失败，也继续删除本地记录
      }
    }

    // 删除本地记录
    const response = await batchDeleteHistory([{
      bvid: props.record.bvid,
      view_at: props.record.view_at
    }])
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message + (syncDeleteToBilibili ? '，并已同步删除B站历史记录' : '')
      })
      emit('refresh-data')
    } else {
      throw new Error(response.data.message || '删除失败')
    }
  } catch (error) {
    if (error.toString().includes('cancel')) return

    showNotify({
      type: 'danger',
      message: error.response?.data?.detail || error.message || '删除失败'
    })
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
    minute: '2-digit'
  })
}

// 修改初始化备注内容的方法
const initRemark = () => {
  const key = `${props.record.bvid}_${props.record.view_at}`
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

// 修改备注更新方法
const handleRemarkBlur = async () => {
  // 如果内容没有变化，不发送请求
  if (remarkContent.value === originalRemark.value) {
    return
  }

  try {
    const response = await updateVideoRemark(
      props.record.bvid,
      props.record.view_at,
      remarkContent.value
    )
    if (response.data.status === 'success') {
      if (remarkContent.value) { // 只在有内容时显示提示
        showNotify({
          type: 'success',
          message: '备注已保存'
        })
      }
      originalRemark.value = remarkContent.value // 更新原始值
      remarkTime.value = response.data.data.remark_time // 更新备注时间
      // 通知父组件备注已更新
      emit('remark-updated', {
        bvid: props.record.bvid,
        view_at: props.record.view_at,
        remark: remarkContent.value,
        remark_time: response.data.data.remark_time
      })
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `保存备注失败：${error.message}`
    })
    remarkContent.value = originalRemark.value // 恢复原始值
  }
}

// 组件挂载时初始化备注
onMounted(() => {
  initRemark()
})

// 监听 remarkData 的变化
watch(() => props.remarkData, () => {
  initRemark()
}, { deep: true })

// 下载弹窗状态
const showDownloadDialog = ref(false)

// 处理下载按钮点击
const handleDownload = () => {
  showDownloadDialog.value = true
}

// 处理收藏按钮点击
const handleFavorite = () => {
  // 触发父组件的favorite事件
  emit('favorite', props.record)
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 可以添加一些额外的悬停效果样式 */
.hover\:scale-110:hover {
  transform: scale(1.1);
}

.hover\:text-\[\#FF6699\]:hover {
  color: #ff6699;
}

/* 添加 group-hover 相关样式 */
.group:hover .group-hover\:flex {
  display: flex;
}
</style>
