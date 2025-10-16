<template>
  <div class="space-y-4">
    <!-- 输入与操作 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex items-center space-x-3">
        <div class="flex-1">
          <SimpleSearchBar
            v-model="inputMid"
            placeholder="输入用户 MID"
            @search="triggerQueryNow"
            class="w-full"
          />
        </div>
        <button
          class="px-4 py-2 bg-green-600 text-white rounded-md hover:opacity-90 disabled:opacity-50"
          :disabled="!canStartDownload"
          @click="handleStartDownload"
        >下载</button>
        <button
          class="px-4 py-2 bg-gray-700 text-white rounded-md hover:opacity-90 disabled:opacity-50"
          :disabled="!downloading"
          @click="handleStop"
        >停止</button>
      </div>
    </div>

    <!-- 用户信息卡片 -->
    <div v-if="hostInfo" class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 flex items-center space-x-4">
      <img :src="hostFaceUrl" alt="face" class="w-14 h-14 rounded-full object-cover border" />
      <div class="flex-1 min-w-0">
        <div class="text-base font-medium truncate">{{ hostInfo.up_name || `UID ${hostInfo.host_mid}` }}</div>
        <div class="text-xs text-gray-500 dark:text-gray-400">动态数：{{ hostInfo.item_count }} · 核心数：{{ hostInfo.core_count }}</div>
        <div class="text-xs text-gray-400 dark:text-gray-500">最近发布时间：{{ formatTs(hostInfo.last_publish_ts) }} · 最近抓取：{{ formatTs(hostInfo.last_fetch_time) }}</div>
      </div>
      <button
        class="px-3 py-1.5 bg-green-600 text-white rounded-md hover:opacity-90 disabled:opacity-50"
        :disabled="!canStartDownload"
        @click="handleStartDownload"
      >下载</button>
      <button
        class="ml-2 px-3 py-1.5 bg-red-600 text-white rounded-md hover:opacity-90 disabled:opacity-50"
        :disabled="!hostMid || downloading || deleting"
        @click="handleDeleteHost"
      >删除</button>
    </div>

    <!-- 已抓取的UP列表 -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex items-center justify-between mb-3">
        <div class="text-sm font-medium">已抓取的UP</div>
        <button class="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300" @click="loadHosts">刷新</button>
      </div>
      <div v-if="hostsLoading" class="text-xs text-gray-400">加载中...</div>
      <div v-else>
        <div v-if="hosts.length" class="grid gap-4 grid-cols-1 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
          <div v-for="h in hosts" :key="h.host_mid" class="group border rounded-md p-2 flex items-center space-x-2 hover:border-[#fb7299] cursor-pointer dark:border-gray-700"
               @click="selectHost(h.host_mid)">
            <img :src="h.face_path ? toStaticUrl(h.face_path) : ''" class="w-9 h-9 rounded-full object-cover border" alt="face" />
            <div class="min-w-0 flex-1">
              <div class="text-xs font-medium truncate">{{ h.up_name || h.host_mid }}</div>
              <div class="text-[11px] text-gray-500 truncate">动态：{{ h.item_count }} · 抓取：{{ formatTs(h.last_fetch_time) }}</div>
            </div>
          </div>
        </div>
        <div v-else class="text-xs text-gray-400">暂无数据</div>
      </div>
    </div>

    <!-- SSE 实时日志：下载中或有历史日志时显示 -->
    <div v-if="downloading || logs.length" class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
      <div class="flex items-center justify-between">
        <div class="text-sm font-medium">实时日志</div>
        <button class="text-xs text-gray-500 hover:text-gray-700" @click="logs=[]">清空</button>
      </div>
      <div ref="logsContainer" class="mt-2 h-40 overflow-auto bg-gray-50 dark:bg-gray-900 border dark:border-gray-700 rounded p-2 text-xs whitespace-pre-wrap">
        <template v-if="logs.length">
          <div v-for="(line, idx) in logs" :key="idx" class="text-gray-700 dark:text-gray-300">{{ line }}</div>
        </template>
        <div v-else class="text-gray-400 dark:text-gray-500">暂无日志</div>
      </div>
    </div>

    <!-- 已下载动态（数据库读取） -->
    <div v-if="hostMid && items.length" class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
      <div class="text-sm font-medium mb-3">已下载动态</div>
      <div class="space-y-3">
        <div v-for="it in items" :key="it.id_str">
          <component
            :is="isVideoDynamic(it) ? DynamicCardVideo : DynamicCardNormal"
            :item="it"
            :face-url="hostFaceUrl"
          />
        </div>
      </div>
      <div class="mt-3 flex justify-center">
        <button class="px-3 py-1.5 text-sm bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50" :disabled="loadingMore || noMore" @click="loadMore">
          {{ noMore ? '没有更多了' : (loadingMore ? '加载中...' : '加载更多') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, watch, nextTick } from 'vue'
import { showDialog } from 'vant'
import 'vant/es/dialog/style'
import { toStaticUrl } from '@/utils/imageUrl'
import DynamicCardVideo from '@/components/tailwind/dynamic/DynamicCardVideo.vue'
import DynamicCardNormal from '@/components/tailwind/dynamic/DynamicCardNormal.vue'
import SimpleSearchBar from '@/components/tailwind/SimpleSearchBar.vue'
import {
  getDynamicDbHosts,
  getDynamicDbSpace,
  startDynamicAutoFetch,
  createDynamicProgressSSE,
  stopDynamicAutoFetch,
  deleteDynamicSpace
} from '@/api/api'

// 输入 mid
const inputMid = ref('')
const hostMid = ref('')

// 主机信息与头像
const hostInfo = ref(null)
const hostFaceUrl = computed(() => hostInfo.value?.face_path ? toStaticUrl(hostInfo.value.face_path) : '')

// UP 列表
const hosts = ref([])
const hostsLoading = ref(false)

// 列表 & 分页
const items = ref([])
const limit = ref(20)
const offset = ref(0)
const total = ref(0)
const loadingMore = ref(false)
const noMore = ref(false)

// 下载状态与 SSE
const downloading = ref(false)
const deleting = ref(false)
let sse = null
const logs = ref([])
let queryTimer = null
const logsContainer = ref(null)

const canStartDownload = computed(() => !!hostMid.value && !downloading.value)

const formatTs = (ts) => {
  if (!ts) return '-'
  try {
    const d = new Date(ts * 1000)
    return [d.getFullYear(), d.getMonth() + 1, d.getDate()].join('-') + ' ' + [d.getHours(), d.getMinutes(), d.getSeconds()].map(n => String(n).padStart(2, '0')).join(':')
  } catch {
    return String(ts)
  }
}

// 从 hosts 里尝试读取基本信息（face/up_name）
const fetchHostInfo = async (mid) => {
  const res = await getDynamicDbHosts(200, 0)
  const list = res?.data?.data || []
  const found = list.find(x => String(x.host_mid) === String(mid))
  hostInfo.value = found || { host_mid: String(mid) }
}

const loadHosts = async () => {
  try {
    hostsLoading.value = true
    const res = await getDynamicDbHosts(50, 0)
    hosts.value = res?.data?.data || []
  } catch (e) {
    // 忽略错误
  } finally {
    hostsLoading.value = false
  }
}

const selectHost = async (mid) => {
  inputMid.value = String(mid)
  await triggerQueryNow()
}

const refreshList = async (reset = true) => {
  if (!hostMid.value) return
  if (reset) {
    items.value = []
    offset.value = 0
    noMore.value = false
  }
  const res = await getDynamicDbSpace(hostMid.value, limit.value, offset.value)
  total.value = res?.data?.total || 0
  const rows = res?.data?.items || []
  items.value = reset ? rows : items.value.concat(rows)
  offset.value += rows.length
  if (!rows.length || items.value.length >= total.value) noMore.value = true
}

// 手动查询入口已移除，改为输入 1 秒后自动触发

// 去重追加日志：仅当与上一条不同才加入
const addLog = (line) => {
  const msg = String(line || '').trim()
  if (!msg) return
  const last = logs.value[logs.value.length - 1]
  if (last !== msg) {
    logs.value.push(msg)
    // 追加后自动滚动到底部
    nextTick(() => {
      if (logsContainer.value) {
        logsContainer.value.scrollTop = logsContainer.value.scrollHeight
      }
    })
  }
}

const openSSE = (mid) => {
  closeSSE()
  try {
    sse = createDynamicProgressSSE(mid)
    sse.onopen = () => {
      addLog(`[SSE] connected for ${mid}`)
    }
    // 仅识别最终完成格式："抓取完成！共获取 xx 条动态，总计 xx 页"
    const FINAL_DONE_RE = /\[全部抓取完毕\]\s*抓取完成！共获取\s+\d+\s*条动态，\s*总计\s+\d+\s*页/
    // 显式监听 progress 事件名（后端事件名: progress）
    sse.addEventListener('progress', (evt) => {
      try {
        const data = JSON.parse(evt.data)
        const msg = data?.message || evt.data
        addLog(String(msg))
        // 仅在最终完成消息出现时自动停止
        if (FINAL_DONE_RE.test(String(msg))) {
          if (downloading.value) handleStop()
        }
      } catch {
        addLog(String(evt.data))
      }
    })
    // 兜底接收未命名事件
    sse.onmessage = (evt) => {
      try {
        const data = JSON.parse(evt.data)
        const msg = data?.message || evt.data
        addLog(String(msg))
        if (FINAL_DONE_RE.test(String(msg))) {
          if (downloading.value) handleStop()
        }
      } catch {
        addLog(String(evt.data))
      }
    }
    sse.onerror = (evt) => {
      addLog('[SSE] error, will close')
      closeSSE()
    }
  } catch (e) {
    addLog(`[SSE] create failed: ${e?.message || e}`)
  }
}

const closeSSE = () => {
  if (sse) {
    try { sse.close() } catch {}
    sse = null
  }
}

const handleStartDownload = async () => {
  if (!hostMid.value || downloading.value) return
  downloading.value = true
  logs.value.push(`Start auto fetch for MID ${hostMid.value}`)
  openSSE(hostMid.value)
  try {
    await startDynamicAutoFetch(hostMid.value, {
      need_top: false,
      save_to_db: true,
      save_media: true
    })
  } catch (e) {
    logs.value.push(`start error: ${e?.message || e}`)
  }
}

const handleStop = async () => {
  if (!hostMid.value) return
  try {
    await stopDynamicAutoFetch(hostMid.value)
    addLog('Stop requested')
  } catch (e) {
    addLog(`stop error: ${e?.message || e}`)
  } finally {
    downloading.value = false
    closeSSE()
    // 停止后刷新一次列表
    await refreshList(true)
    // 停止后刷新头像（可能在抓取期间生成了face）
    await fetchHostInfo(hostMid.value)
  }
}

const confirmDelete = (mid, name) => {
  return new Promise((resolve) => {
    showDialog({
      title: '⚠️ 危险操作',
      message: `即将删除 ${name} (UID: ${mid}) 的所有动态媒体与数据库记录。\n\n此操作不可恢复，请谨慎确认！`,
      showCancelButton: true,
      confirmButtonText: '确认删除',
      cancelButtonText: '取消'
    }).then(() => {
      // 第二次确认
      showDialog({
        title: '🚨 最终确认',
        message: `请再次确认删除 ${name} (UID: ${mid}) 的所有数据。\n\n点击确认后将立即执行删除操作！`,
        showCancelButton: true,
        confirmButtonText: '立即删除',
        cancelButtonText: '取消'
      }).then(() => resolve(true)).catch(() => resolve(false))
    }).catch(() => resolve(false))
  })
}

const handleDeleteHost = async () => {
  if (!hostMid.value || downloading.value || deleting.value) return
  const mid = String(hostMid.value)
  const name = hostInfo.value?.up_name || `UID ${mid}`
  const confirmed = await confirmDelete(mid, name)
  if (!confirmed) return
  await executeDelete(mid, name, true)
}

const executeDelete = async (mid, name, clearSelection) => {
  try {
    deleting.value = true
    addLog(`Delete requested for ${name} (MID: ${mid})`)
    await deleteDynamicSpace(mid)
    addLog(`Delete success for ${name} (MID: ${mid})`)
    
    if (clearSelection) {
      // 清空本地列表、选择状态并刷新
      items.value = []
      offset.value = 0
      total.value = 0
      noMore.value = true
      hostInfo.value = null
      hostMid.value = ''
      inputMid.value = ''
    }
    
    await loadHosts()
  } catch (e) {
    const errorMsg = e?.message || e
    addLog(`delete error: ${errorMsg}`)
    showDialog({
      title: '删除失败',
      message: `删除 ${name} 失败：\n${errorMsg}`,
      confirmButtonText: '确定'
    })
  } finally {
    deleting.value = false
  }
}

const isVideoDynamic = (it) => {
  // 有 bvid 即视为视频动态；或 type 包含 VIDEO
  if (it?.bvid) return true
  const t = String(it?.type || '')
  return t.includes('VIDEO') || t.includes('AV')
}

const loadMore = async () => {
  if (loadingMore.value || noMore.value) return
  loadingMore.value = true
  try {
    await refreshList(false)
  } finally {
    loadingMore.value = false
  }
}

onUnmounted(() => {
  closeSSE()
  if (queryTimer) clearTimeout(queryTimer)
})

// 监听输入，1秒后自动查询
watch(() => inputMid.value, (val) => {
  const mid = String(val || '').trim()
  if (!mid) return
  if (queryTimer) clearTimeout(queryTimer)
  queryTimer = setTimeout(async () => {
    if (hostMid.value !== mid) {
      hostMid.value = mid
      await fetchHostInfo(mid)
      await refreshList(true)
    }
  }, 1000)
})

// 立即触发查询（供按回车使用）
const triggerQueryNow = async () => {
  const mid = String(inputMid.value || '').trim()
  if (!mid) return
  if (queryTimer) clearTimeout(queryTimer)
  if (hostMid.value !== mid) {
    hostMid.value = mid
    await fetchHostInfo(mid)
    await refreshList(true)
  }
}

// 初始化加载UP列表
loadHosts()
</script>

<style scoped>
</style>


