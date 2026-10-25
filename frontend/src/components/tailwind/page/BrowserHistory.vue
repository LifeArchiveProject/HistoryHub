<template>
  <div ref="scrollContainer" class="h-full overflow-y-auto" @scroll.passive="handleScroll">
    <div class="mx-auto max-w-4xl px-4 py-5 sm:px-6">
      <header class="mb-5 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-semibold text-[#fb7299] sm:hidden">HistoryHub</p>
          <h1 class="text-xl font-bold text-gray-900 dark:text-gray-100">网页历史</h1>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">查看浏览器同步的访问记录，无需 B 站登录。</p>
        </div>
        <div class="flex items-center gap-4 text-sm">
          <router-link to="/" class="text-[#fb7299] sm:hidden">B站历史</router-link>
          <router-link to="/settings" class="text-gray-600 hover:text-[#fb7299] dark:text-gray-300">设置</router-link>
          <button type="button" class="text-gray-600 hover:text-[#fb7299] dark:text-gray-300" @click="togglePrivacyMode">
            {{ isPrivacyMode ? '关闭隐私' : '隐私模式' }}
          </button>
        </div>
      </header>

      <form class="mb-4 rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800" @submit.prevent="connect">
        <div class="mb-2 flex items-center justify-between gap-3 text-sm">
          <label for="browser-history-token" class="font-medium text-gray-800 dark:text-gray-100">连接密钥</label>
          <a href="https://github.com/LifeArchiveProject/HistoryHub#网页历史" target="_blank" rel="noopener noreferrer" class="text-[#fb7299] hover:underline">连接说明</a>
        </div>
        <div class="flex flex-wrap gap-2">
          <input
            id="browser-history-token"
            v-model="tokenInput"
            type="password"
            autocomplete="off"
            placeholder="与浏览器扩展使用相同的密钥"
            class="min-w-0 flex-1 rounded-lg border-gray-300 bg-transparent text-sm text-gray-900 focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-600 dark:text-gray-100"
          />
          <button type="submit" :disabled="loading" class="rounded-lg bg-[#fb7299] px-4 py-2 text-sm font-medium text-white hover:bg-[#fb7299]/90 disabled:opacity-60">{{ loading ? '连接中…' : '保存并连接' }}</button>
        </div>
      </form>

      <label for="browser-history-search" class="sr-only">搜索网页历史</label>
      <input
        id="browser-history-search"
        v-model="query"
        type="search"
        placeholder="搜索标题或网址"
        class="mb-4 w-full rounded-lg border-gray-300 bg-white text-sm text-gray-900 focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-700 dark:bg-gray-800 dark:text-gray-100"
      />

      <ul v-if="records.length" class="divide-y divide-gray-200 rounded-lg border border-gray-200 bg-white dark:divide-gray-700 dark:border-gray-700 dark:bg-gray-800">
        <li v-for="record in records" :key="record.id" class="px-4 py-4">
          <a
            :href="isPrivacyMode ? undefined : record.url"
            target="_blank"
            rel="noopener noreferrer"
            class="break-words font-medium text-gray-900 hover:text-[#fb7299] dark:text-gray-100"
            :class="{ 'blur-sm': isPrivacyMode }"
          >{{ isPrivacyMode ? '******' : (record.title || record.url) }}</a>
          <div class="mt-2 flex flex-wrap gap-x-3 gap-y-1 text-xs text-gray-500 dark:text-gray-400" :class="{ 'blur-sm': isPrivacyMode }">
            <span>{{ isPrivacyMode ? '******' : record.domain }}</span>
            <time>{{ isPrivacyMode ? '******' : formatTime(record.visited_at) }}</time>
          </div>
        </li>
      </ul>

      <div class="py-6 text-center text-sm text-gray-500 dark:text-gray-400" role="status" aria-live="polite">
        <p v-if="loading">正在加载…</p>
        <template v-else-if="errorMessage">
          <p>{{ errorMessage }}</p>
          <button type="button" class="mt-2 text-[#fb7299] hover:underline" @click="loadRecords(!records.length)">重试</button>
        </template>
        <p v-else-if="!connectionToken">请在后端配置 HISTORYHUB_SYNC_TOKEN，并在扩展和此处使用同一密钥。</p>
        <p v-else-if="!records.length">暂无匹配的网页历史。</p>
        <button v-else-if="nextCursor" type="button" class="text-[#fb7299] hover:underline" @click="loadRecords()">向下滚动或点击加载更多</button>
        <p v-else>已显示全部匹配记录。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
import { getBrowserHistoryRecords, getCurrentBaseUrl } from '../../../api/api'
import { usePrivacyStore } from '../../../store/privacy'

const TOKEN_KEY = 'historyhub_sync_token'
let backendUrl = getCurrentBaseUrl()
const getTokenKey = () => `${TOKEN_KEY}:${backendUrl}`
const tokenInput = ref(localStorage.getItem(getTokenKey()) || '')
const connectionToken = ref(tokenInput.value)
const query = ref('')
const records = ref([])
const nextCursor = ref(null)
const loading = ref(false)
const errorMessage = ref('')
const scrollContainer = ref(null)
const { isPrivacyMode, togglePrivacyMode } = usePrivacyStore()
let latestRequest = 0

const formatTime = (timestamp) => new Date(timestamp).toLocaleString()

const loadRecords = async (reset = false) => {
  if (!connectionToken.value || (!reset && (loading.value || !nextCursor.value))) return

  const request = ++latestRequest
  if (reset) {
    records.value = []
    nextCursor.value = null
    scrollContainer.value?.scrollTo({ top: 0 })
  }
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await getBrowserHistoryRecords({
      token: connectionToken.value,
      cursor: reset ? null : nextCursor.value,
      query: query.value.trim(),
    })
    if (request !== latestRequest) return
    if (response.data.status !== 'success') throw new Error('request_failed')
    records.value = reset ? response.data.records : [...records.value, ...response.data.records]
    nextCursor.value = response.data.next_cursor
  } catch (error) {
    if (request !== latestRequest) return
    const status = error.response?.status
    if (status === 401) {
      errorMessage.value = '连接密钥不正确，请与后端和扩展使用同一密钥。'
    } else if (status === 503) {
      errorMessage.value = '请在后端配置 HISTORYHUB_SYNC_TOKEN，并在扩展和此处使用同一密钥。'
    } else if (status === 404) {
      errorMessage.value = '当前后端未提供网页历史，请更新 HistoryHub 后端。'
    } else {
      errorMessage.value = '无法加载网页历史，请检查设置中的服务器地址和后端状态。'
    }
  } finally {
    if (request === latestRequest) loading.value = false
  }
}

const connect = () => {
  if (loading.value) return
  connectionToken.value = tokenInput.value.trim()
  if (connectionToken.value) {
    localStorage.setItem(getTokenKey(), connectionToken.value)
    loadRecords(true)
  } else {
    localStorage.removeItem(getTokenKey())
    latestRequest++
    records.value = []
    nextCursor.value = null
    loading.value = false
    errorMessage.value = ''
  }
}

const handleBackendChange = () => {
  backendUrl = getCurrentBaseUrl()
  latestRequest++
  tokenInput.value = ''
  connectionToken.value = ''
  records.value = []
  nextCursor.value = null
  loading.value = false
  errorMessage.value = ''
}

const handleScroll = (event) => {
  const { scrollTop, clientHeight, scrollHeight } = event.currentTarget
  if (scrollTop + clientHeight >= scrollHeight - 80 && !errorMessage.value) loadRecords()
}

watch(query, () => loadRecords(true))
onMounted(() => {
  window.addEventListener('api-baseurl-updated', handleBackendChange)
  loadRecords(true)
})
onUnmounted(() => window.removeEventListener('api-baseurl-updated', handleBackendChange))
</script>
