<template>
  <div ref="scrollContainer" class="h-full overflow-y-auto" @scroll.passive="handleScroll">
    <div class="mx-auto max-w-4xl px-4 py-5 sm:px-6">
      <header class="mb-5 flex flex-wrap items-center justify-between gap-3">
        <h1 class="text-xl font-bold text-gray-900 dark:text-gray-100">B站历史</h1>
        <button type="button" :disabled="syncing" class="rounded-lg bg-[#fb7299] px-4 py-2 text-sm font-medium text-white hover:bg-[#fb7299]/90 disabled:opacity-60" @click="syncHistory">
          {{ syncing ? '同步中…' : '同步历史' }}
        </button>
      </header>

      <p v-if="syncMessage" class="mb-4 text-sm" :class="syncFailed ? 'text-red-600 dark:text-red-400' : 'text-gray-600 dark:text-gray-300'" role="status">{{ syncMessage }}</p>

      <label for="bili-history-search" class="sr-only">搜索 B站历史</label>
      <input
        id="bili-history-search"
        v-model="query"
        type="search"
        placeholder="搜索标题、作者或分区"
        class="mb-4 w-full rounded-lg border-gray-300 bg-white text-sm text-gray-900 focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100"
      />

      <ul v-if="records.length" class="divide-y divide-gray-200 rounded-lg border border-gray-200 bg-white dark:divide-gray-700 dark:border-gray-700 dark:bg-gray-800">
        <li v-for="record in records" :key="`${record.id}-${record.view_at}`" class="px-4 py-4">
          <a
            v-if="record.original_url"
            :href="isPrivacyMode ? undefined : record.original_url"
            target="_blank"
            rel="noopener noreferrer"
            class="break-words font-medium text-gray-900 hover:text-[#fb7299] dark:text-gray-100"
            :class="{ 'blur-sm': isPrivacyMode }"
            @click.prevent="openRecord(record)"
          >{{ isPrivacyMode ? '******' : record.title }}</a>
          <span v-else class="break-words font-medium" :class="{ 'blur-sm': isPrivacyMode }">{{ isPrivacyMode ? '******' : record.title }}</span>
          <div class="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs text-gray-500 dark:text-gray-400" :class="{ 'blur-sm': isPrivacyMode }">
            <span v-if="record.author_name">{{ isPrivacyMode ? '******' : record.author_name }}</span>
            <time>{{ isPrivacyMode ? '******' : formatTime(record.view_at) }}</time>
          </div>
        </li>
      </ul>

      <div class="py-6 text-center text-sm text-gray-500 dark:text-gray-400" role="status" aria-live="polite">
        <p v-if="loading">正在加载…</p>
        <template v-else-if="errorMessage">
          <p>{{ errorMessage }}</p>
          <button type="button" class="mt-2 text-[#fb7299] hover:underline" @click="loadRecords(!records.length)">重试</button>
        </template>
        <p v-else-if="!records.length">{{ query.trim() ? '暂无匹配的历史记录。' : '暂无历史记录，请在设置中登录 B站后同步。' }}</p>
        <button v-else-if="hasMore" type="button" class="text-[#fb7299] hover:underline" @click="loadRecords()">向下滚动或点击加载更多</button>
        <p v-else>已显示全部匹配记录。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { getBiliHistoryRecords, getLoginStatus, searchBiliHistoryRecords, syncBiliHistory } from '../../../api/api'
import { usePrivacyStore } from '../../../store/privacy'
import { openInBrowser } from '../../../utils/openUrl'

const query = ref('')
const records = ref([])
const page = ref(0)
const total = ref(0)
const loading = ref(false)
const errorMessage = ref('')
const scrollContainer = ref(null)
const syncing = ref(false)
const syncMessage = ref('')
const syncFailed = ref(false)
const { isPrivacyMode } = usePrivacyStore()
const hasMore = computed(() => records.value.length < total.value)
let latestRequest = 0

const formatTime = (timestamp) => new Date(timestamp * 1000).toLocaleString()

const openRecord = (record) => {
  if (!isPrivacyMode.value) openInBrowser(record.original_url)
}

const loadRecords = async (reset = false) => {
  if (!reset && (loading.value || !hasMore.value)) return
  const request = ++latestRequest
  if (reset) {
    records.value = []
    page.value = 0
    total.value = 0
    scrollContainer.value?.scrollTo({ top: 0 })
  }
  loading.value = true
  errorMessage.value = ''

  try {
    const nextPage = page.value + 1
    const search = query.value.trim()
    const response = search
      ? await searchBiliHistoryRecords(search, nextPage)
      : await getBiliHistoryRecords(nextPage)
    if (request !== latestRequest) return
    if (response.data.status !== 'success') throw new Error(response.data.message || '无法加载历史记录。')
    const data = response.data.data
    records.value = reset ? data.records : [...records.value, ...data.records]
    page.value = data.current
    total.value = data.total
  } catch (error) {
    if (request === latestRequest) {
      errorMessage.value = error.response?.data?.detail || error.message || '无法加载历史记录，请检查后端连接。'
    }
  } finally {
    if (request === latestRequest) loading.value = false
  }
}

const syncHistory = async () => {
  syncing.value = true
  syncMessage.value = ''
  syncFailed.value = false
  try {
    const login = await getLoginStatus()
    if (login.data.code !== 0 || !login.data.data?.isLogin) {
      throw new Error('请先在设置中登录 B站，再同步历史记录。')
    }
    const response = await syncBiliHistory()
    if (response.data.status !== 'success') throw new Error(response.data.message || '同步失败。')
    syncMessage.value = response.data.message || '同步完成。'
    await loadRecords(true)
  } catch (error) {
    syncFailed.value = true
    syncMessage.value = error.response?.data?.detail || error.message || '同步失败，请检查后端连接。'
  } finally {
    syncing.value = false
  }
}

const handleScroll = (event) => {
  const { scrollTop, clientHeight, scrollHeight } = event.currentTarget
  if (scrollTop + clientHeight >= scrollHeight - 80 && !errorMessage.value) loadRecords()
}

watch(query, () => loadRecords(true))
onMounted(() => loadRecords(true))
</script>
