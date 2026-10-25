<template>
  <!-- Outer container: removes x-padding completely on mobile for edge-to-edge feel -->
  <div class="mx-auto max-w-4xl pb-safe md:px-4 md:py-4">
    <!-- Sticky Header for Mobile -->
    <div class="sticky top-0 z-20 flex items-center justify-between bg-white/90 px-3 py-2.5 backdrop-blur-md dark:bg-gray-900/90 md:static md:mb-4 md:bg-transparent md:px-0 md:py-0 md:backdrop-blur-none">
      <div class="flex items-center gap-3">
        <button
          class="flex h-8 w-8 items-center justify-center rounded-full bg-gray-100/80 text-gray-700 transition-colors active:bg-gray-200 dark:bg-gray-800/80 dark:text-gray-200 dark:active:bg-gray-700 md:h-10 md:w-10"
          @click="goBack"
        >
          <svg class="h-4 w-4 md:h-5 md:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <div class="text-sm font-bold text-gray-900 dark:text-gray-100 md:text-xl">视频操作</div>
      </div>
      <div class="hidden text-xs text-gray-500 dark:text-gray-400 md:block">移动端详情与操作页</div>
    </div>

    <div v-if="record" class="flex flex-col md:space-y-4">
      <!-- Media Card & Metadata Edge-to-Edge Container (Mobile) -->
      <div class="bg-white dark:bg-gray-900 md:overflow-hidden md:rounded-2xl md:border md:border-gray-200 md:shadow-sm md:dark:border-gray-700">
        <!-- Edge-to-edge Cover -->
        <div class="relative w-full overflow-hidden bg-black md:aspect-video">
          <!-- Mobile cover ratio wrapper -->
          <div class="h-0 pb-[56.25%] md:pb-0 md:h-full">
            <img
              :src="normalizeImageUrl(record.cover || record.covers?.[0])"
              class="absolute left-0 top-0 h-full w-full object-cover"
              :class="{ 'blur-md': isPrivacyMode }"
              alt=""
            />
          </div>
          <div
            v-if="record.business !== 'article-list' && record.business !== 'article' && record.business !== 'live'"
            class="absolute bottom-2 right-2 rounded bg-black/70 px-1.5 py-0.5 text-[10px] font-medium tracking-wide text-white md:px-2 md:py-1 md:text-xs"
          >
            {{ formatDuration(record.progress) }} / {{ formatDuration(record.duration) }}
          </div>
        </div>

        <!-- Compact Metadata Block -->
        <div class="p-3 pb-2 md:p-5">
          <div
            class="text-[15px] font-bold leading-snug text-gray-900 line-clamp-2 dark:text-gray-100 md:text-lg md:leading-6"
            v-html="isPrivacyMode ? '******' : record.title"
            :class="{ 'blur-sm': isPrivacyMode }"
          ></div>

          <!-- Denser single line for Avatar, Name, Time, and Type -->
          <div class="mt-2.5 flex items-center justify-between text-[11px] text-gray-500 dark:text-gray-400 md:text-sm">
            <div class="flex min-w-0 items-center gap-1.5 md:gap-2">
              <img
                v-if="record.business !== 'cheese' && record.business !== 'pgc'"
                :src="normalizeImageUrl(record.author_face)"
                class="h-4 w-4 rounded-full md:h-6 md:w-6"
                :class="{ 'blur-md': isPrivacyMode }"
                alt=""
              />
              <span class="truncate font-medium text-gray-700 dark:text-gray-300 md:font-normal" :class="{ 'blur-sm': isPrivacyMode }">
                {{ isPrivacyMode ? '******' : record.author_name }}
              </span>
              <span class="opacity-80">·</span>
              <span class="opacity-80">{{ formatTimestamp(record.view_at) }}</span>
            </div>
            
            <div class="flex flex-shrink-0 items-center justify-end gap-1.5">
               <span class="rounded bg-pink-50/80 px-1.5 py-0.5 text-[9px] font-medium text-pink-600 dark:bg-pink-900/40 dark:text-pink-400 md:rounded-full md:px-2 md:py-1 md:text-xs">
                {{ record.business === 'archive' ? record.tag_name : getBusinessType(record.business) }}
              </span>
              <span v-if="isDownloaded && record.business === 'archive'" class="rounded bg-green-50/80 px-1.5 py-0.5 text-[9px] font-medium text-green-600 dark:bg-green-900/40 dark:text-green-400 md:rounded-full md:px-2 md:py-1 md:text-xs">
                已下载
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons (Mobile: Icon Grid, Desktop: Button Grid) -->
      <div class="bg-white px-3 py-4 dark:bg-gray-900 md:bg-transparent md:px-0 md:py-0">
        <!-- Desktop Layout -->
        <div class="hidden md:grid md:grid-cols-2 md:gap-3">
          <button class="action-btn" @click="handleOpenContent">打开内容</button>
          <button
            v-if="record.business !== 'cheese' && record.business !== 'pgc'"
            class="action-btn"
            @click="handleAuthorClick"
          >
            UP主页
          </button>
          <button
            v-if="record.business === 'archive'"
            class="action-btn"
            @click="showDownloadDialog = true"
          >
            下载视频
          </button>
          <button
            v-if="record.business !== 'live'"
            class="action-btn"
            @click="handleFavoriteClick"
          >
            {{ isVideoFavorited ? '取消收藏' : '收藏视频' }}
          </button>
          <button class="action-btn danger-btn" @click="handleDelete">删除记录</button>
        </div>

        <!-- App-like Minimalist Mobile Action Bar -->
        <div class="flex justify-between items-center bg-transparent border-t border-gray-100 dark:border-gray-800 px-1 py-1 md:hidden">
          <button class="flex flex-1 flex-col items-center justify-center gap-1 py-2 active:bg-gray-100 dark:active:bg-gray-800 transition-colors rounded-lg" @click="handleOpenContent">
            <svg class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span class="text-[10px] font-medium text-gray-500 dark:text-gray-400">播放</span>
          </button>

          <button
            v-if="record.business !== 'cheese' && record.business !== 'pgc'"
            class="flex flex-1 flex-col items-center justify-center gap-1 py-2 active:bg-gray-100 dark:active:bg-gray-800 transition-colors rounded-lg"
            @click="handleAuthorClick"
          >
            <svg class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span class="text-[10px] font-medium text-gray-500 dark:text-gray-400">UP主页</span>
          </button>

          <button
            v-if="record.business === 'archive'"
            class="flex flex-1 flex-col items-center justify-center gap-1 py-2 active:bg-gray-100 dark:active:bg-gray-800 transition-colors rounded-lg"
            @click="showDownloadDialog = true"
          >
             <svg class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span class="text-[10px] font-medium text-gray-500 dark:text-gray-400">下载</span>
          </button>

          <button
            v-if="record.business !== 'live'"
            class="flex flex-1 flex-col items-center justify-center gap-1 py-2 active:bg-gray-100 dark:active:bg-gray-800 transition-colors rounded-lg"
            @click="handleFavoriteClick"
          >
            <svg class="h-5 w-5" :class="isVideoFavorited ? 'text-[#fb7299] fill-current' : 'text-gray-600 dark:text-gray-400'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            <span class="text-[10px] font-medium" :class="isVideoFavorited ? 'text-[#fb7299]' : 'text-gray-500 dark:text-gray-400'">
              {{ isVideoFavorited ? '已收藏' : '收藏' }}
            </span>
          </button>

          <button class="flex flex-1 flex-col items-center justify-center gap-1 py-2 active:bg-gray-100 dark:active:bg-gray-800 transition-colors rounded-lg" @click="handleDelete">
            <svg class="h-5 w-5 text-gray-600 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            <span class="text-[10px] font-medium text-gray-500 dark:text-gray-400">删除</span>
          </button>
        </div>
      </div>

      <!-- App-Like Remark Section (Mobile V2) -->
      <div class="bg-gray-50 px-3 py-4 dark:bg-gray-900 md:rounded-2xl md:border md:border-gray-200 md:bg-white md:p-4 md:shadow-sm md:dark:border-gray-700 md:dark:bg-gray-900">
        <div class="mb-3 flex items-center gap-2">
           <svg class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
           </svg>
           <span class="text-xs font-bold text-gray-700 dark:text-gray-200 md:text-sm">我的备注日志</span>
        </div>
        <div class="relative rounded-xl bg-white p-3 shadow-sm ring-1 ring-inset ring-gray-200 dark:bg-gray-800 dark:ring-gray-700 md:bg-gray-50">
          <textarea
            v-model="remarkContent"
            @blur="handleRemarkBlur"
            :disabled="isPrivacyMode"
            rows="4"
            placeholder="写点属于你自己的学习记录或吐槽吧..."
            class="w-full resize-none border-none bg-transparent p-0 text-[13px] leading-relaxed text-gray-800 outline-none focus:ring-0 dark:text-gray-100 md:text-sm"
            :class="{ 'blur-sm': isPrivacyMode }"
          ></textarea>
        </div>
        <div v-if="remarkTime" class="mt-2 text-right text-[10px] text-gray-400 md:text-xs">
          最后修改于 {{ formatRemarkTime(remarkTime) }}
        </div>
      </div>
    </div>

    <div
      v-else
      class="rounded-2xl border border-dashed border-gray-300 px-4 py-10 text-center text-sm text-gray-500 dark:border-gray-700 dark:text-gray-400"
    >
      未找到这条记录，请从列表重新进入。
    </div>

    <Teleport to="body">
      <DownloadDialog
        v-if="record"
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

    <Teleport to="body">
      <FavoriteDialog
        v-if="record"
        v-model="showFavoriteDialog"
        :video-info="record"
        @favoriteDone="handleFavoriteDone"
      />
    </Teleport>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showDialog, showNotify } from 'vant'
import 'vant/es/dialog/style'
import DownloadDialog from '../DownloadDialog.vue'
import FavoriteDialog from '../FavoriteDialog.vue'
import {
  batchCheckFavoriteStatus,
  batchDeleteHistory,
  batchGetRemarks,
  checkVideoDownload,
  deleteBilibiliHistory,
  favoriteResource,
  localBatchFavoriteResource,
  updateVideoRemark,
} from '@/api/api.js'
import { normalizeImageUrl } from '@/utils/imageUrl.js'
import { openInBrowser } from '@/utils/openUrl.js'
import { getHistoryRecord } from '@/utils/historyRecordStore.js'
import { usePrivacyStore } from '@/store/privacy.js'

const route = useRoute()
const router = useRouter()
const { isPrivacyMode } = usePrivacyStore()

const record = ref(null)
const remarkContent = ref('')
const originalRemark = ref('')
const remarkTime = ref(null)
const isDownloaded = ref(false)
const favoriteStatus = ref({})
const showDownloadDialog = ref(false)
const showFavoriteDialog = ref(false)

const isVideoFavorited = computed(() => {
  if (!record.value) return false
  const videoId = getVideoId(record.value)
  return !!(videoId && favoriteStatus.value[String(videoId)]?.is_favorited)
})

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}

const getVideoId = (videoRecord) => {
  const id = videoRecord?.aid || videoRecord?.avid || (videoRecord?.business === 'archive' ? videoRecord?.oid : null)
  return id ? parseInt(id, 10) : null
}

const getFavoriteFolders = () => {
  const videoId = getVideoId(record.value)
  if (!videoId) return []
  return favoriteStatus.value[String(videoId)]?.favorite_folders || []
}

const loadRecord = () => {
  const { bvid, viewAt } = route.params
  record.value = getHistoryRecord(bvid, viewAt)
}

const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完'
  const minutes = String(Math.floor((seconds || 0) / 60)).padStart(2, '0')
  const secs = String((seconds || 0) % 60).padStart(2, '0')
  return `${minutes}:${secs}`
}

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
    console.error('时间格式化失败:', error)
    return '时间未知'
  }
}

const formatRemarkTime = (timestamp) => {
  if (!timestamp) return ''
  return new Date(timestamp * 1000).toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getBusinessType = (business) => {
  const businessMap = {
    archive: '视频',
    article: '专栏',
    'article-list': '文集',
    live: '直播',
    pgc: '番剧',
    cheese: '课程',
  }
  return businessMap[business] || '其他'
}

const initRemark = async () => {
  if (!record.value) return

  try {
    const response = await batchGetRemarks([{ bvid: record.value.bvid, view_at: record.value.view_at }])
    const data = response.data?.data?.[`${record.value.bvid}_${record.value.view_at}`]
    remarkContent.value = data?.remark || ''
    remarkTime.value = data?.remark_time || null
    originalRemark.value = remarkContent.value
  } catch (error) {
    console.error('获取备注失败:', error)
  }
}

const handleRemarkBlur = async () => {
  if (!record.value || remarkContent.value === originalRemark.value) return

  try {
    const response = await updateVideoRemark(record.value.bvid, record.value.view_at, remarkContent.value)
    if (response.data.status === 'success') {
      originalRemark.value = remarkContent.value
      remarkTime.value = response.data.data.remark_time
      showNotify({ type: 'success', message: '备注已保存' })
    }
  } catch (error) {
    remarkContent.value = originalRemark.value
    showNotify({ type: 'danger', message: `保存备注失败：${error.message}` })
  }
}

const refreshDownloadedState = async () => {
  if (!record.value?.cid || record.value.business !== 'archive') return

  try {
    const response = await checkVideoDownload(record.value.cid)
    isDownloaded.value = !!response.data?.downloaded
  } catch (error) {
    console.error('检查下载状态失败:', error)
  }
}

const refreshFavoriteState = async () => {
  if (!record.value) return

  const videoId = getVideoId(record.value)
  if (!videoId) return

  try {
    const response = await batchCheckFavoriteStatus({ oids: [videoId] })
    const result = response.data?.data?.results?.[0]
    if (result) {
      favoriteStatus.value[String(videoId)] = {
        is_favorited: result.is_favorited,
        favorite_folders: result.favorite_folders || [],
      }
    }
  } catch (error) {
    console.error('检查收藏状态失败:', error)
  }
}

const handleOpenContent = async () => {
  if (!record.value) return

  let url = ''
  switch (record.value.business) {
    case 'archive':
      url = `https://www.bilibili.com/video/${record.value.bvid}`
      break
    case 'article':
      url = `https://www.bilibili.com/read/cv${record.value.oid}`
      break
    case 'article-list':
      url = `https://www.bilibili.com/read/readlist/rl${record.value.oid}`
      break
    case 'live':
      url = `https://live.bilibili.com/${record.value.oid}`
      break
    case 'pgc':
      url = record.value.uri || `https://www.bilibili.com/bangumi/play/ep${record.value.epid}`
      break
    case 'cheese':
      url = record.value.uri || `https://www.bilibili.com/cheese/play/ep${record.value.epid}`
      break
    default:
      break
  }

  if (url) {
    await openInBrowser(url)
  }
}

const handleAuthorClick = async () => {
  if (!record.value?.author_mid) return
  await openInBrowser(`https://space.bilibili.com/${record.value.author_mid}`)
}

const handleFavoriteDone = async () => {
  await refreshFavoriteState()
}

const handleFavoriteClick = async () => {
  if (!record.value) return

  const videoId = getVideoId(record.value)
  if (!videoId) {
    showNotify({ type: 'warning', message: '无法识别视频ID' })
    return
  }

  if (isVideoFavorited.value) {
    try {
      await showDialog({
        title: '取消收藏',
        message: '确定要取消收藏该视频吗？',
        showCancelButton: true,
      })

      const folderIds = getFavoriteFolders().map(folder => folder.media_id)
      const response = await favoriteResource({
        rid: videoId,
        del_media_ids: folderIds.join(','),
      })

      if (response.data.status === 'success') {
        try {
          await localBatchFavoriteResource({
            rids: videoId.toString(),
            del_media_ids: folderIds.join(','),
            operation_type: 'local',
          })
        } catch (syncError) {
          console.error('取消收藏本地同步失败:', syncError)
        }

        showNotify({ type: 'success', message: '已取消收藏' })
        await refreshFavoriteState()
      }
    } catch (error) {
      if (String(error).includes('cancel')) return
      showNotify({ type: 'danger', message: '取消收藏失败' })
    }
  } else {
    showFavoriteDialog.value = true
  }
}

const handleDelete = async () => {
  if (!record.value) return

  try {
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

    if (syncDeleteToBilibili) {
      let kid = ''
      switch (record.value.business || 'archive') {
        case 'archive':
        case 'live':
        case 'article':
          kid = `${record.value.business}_${record.value.oid}`
          break
        case 'pgc':
          kid = `${record.value.business}_${record.value.oid || record.value.ssid}`
          break
        case 'article-list':
          kid = `${record.value.business}_${record.value.oid || record.value.rlid}`
          break
        default:
          kid = `${record.value.business}_${record.value.oid || record.value.bvid}`
          break
      }

      if (kid) {
        try {
          await deleteBilibiliHistory(kid, true)
        } catch (error) {
          console.error('删除B站记录失败:', error)
        }
      }
    }

    const response = await batchDeleteHistory([{ bvid: record.value.bvid, view_at: record.value.view_at }])
    if (response.data.status === 'success') {
      showNotify({ type: 'success', message: '删除成功' })
      goBack()
    }
  } catch (error) {
    if (String(error).includes('cancel')) return
    showNotify({ type: 'danger', message: error.response?.data?.detail || error.message || '删除失败' })
  }
}

onMounted(async () => {
  loadRecord()
  await initRemark()
  await refreshDownloadedState()
  await refreshFavoriteState()
})
</script>

<style scoped>
.action-btn {
  border: 1px solid rgb(229 231 235);
  border-radius: 1rem;
  background: rgb(255 255 255);
  color: rgb(55 65 81);
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.action-btn:active {
  background: rgb(249 250 251);
  border: 1px solid rgb(229 231 235);
}

.dark .action-btn {
  border-color: rgb(55 65 81);
  background: rgb(17 24 39);
  color: rgb(229 231 235);
}

.dark .action-btn:active {
  background: rgb(31 41 55);
}

.danger-btn {
  color: rgb(220 38 38);
  background: rgb(254 242 242);
  border-color: rgb(254 202 202);
}

.dark .danger-btn {
  color: rgb(252 165 165);
  background: rgba(127, 29, 29, 0.25);
  border-color: rgba(127, 29, 29, 0.45);
}
</style>
