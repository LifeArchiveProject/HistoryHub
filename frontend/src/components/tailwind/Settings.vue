<template>
  <div class="h-full overflow-y-auto">
    <div class="mx-auto max-w-3xl space-y-6 px-4 py-5 sm:px-6">
      <h1 class="text-xl font-bold text-gray-900 dark:text-gray-100">设置</h1>

      <section class="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
        <h2 class="mb-4 font-semibold">后端连接</h2>
        <form class="flex flex-wrap gap-2" @submit.prevent="saveServerUrl">
          <label for="server-url" class="sr-only">后端地址</label>
          <input id="server-url" v-model="serverUrl" type="url" required class="min-w-0 flex-1 rounded-lg border-gray-300 bg-transparent text-sm focus:border-[#fb7299] focus:ring-[#fb7299] dark:border-gray-600" placeholder="http://localhost:8899" />
          <button type="submit" class="rounded-lg bg-[#fb7299] px-4 py-2 text-sm font-medium text-white">保存地址</button>
        </form>
        <p v-if="serverError" class="mt-2 text-sm text-red-600 dark:text-red-400" role="status">{{ serverError }}</p>
      </section>

      <section class="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
        <div class="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 class="font-semibold">B站登录</h2>
            <p class="mt-2 text-sm text-gray-600 dark:text-gray-300">{{ checkingLogin ? '正在检查登录状态…' : (isLoggedIn ? username + ' 已登录' : '未登录') }}</p>
          </div>
          <button type="button" :disabled="checkingLogin || authPending" class="rounded-lg bg-[#fb7299] px-4 py-2 text-sm font-medium text-white disabled:opacity-60" @click="handleLogin">
            {{ authPending ? '处理中…' : (isLoggedIn ? '退出登录' : '扫码登录') }}
          </button>
        </div>
        <p class="mt-3 text-sm text-gray-500 dark:text-gray-400">扫码登录后可同步 B站历史，也可在后端 config/config.yaml 中配置 SESSDATA。</p>
        <p v-if="authMessage" class="mt-2 text-sm text-red-600 dark:text-red-400" role="status">{{ authMessage }}</p>
      </section>

      <section class="divide-y divide-gray-200 rounded-lg border border-gray-200 bg-white px-4 dark:divide-gray-700 dark:border-gray-700 dark:bg-gray-800">
        <div class="flex items-center justify-between gap-3 py-4">
          <h2 class="font-semibold">深色模式</h2>
          <button type="button" :aria-pressed="isDarkMode" class="rounded-lg border border-gray-300 px-4 py-2 text-sm dark:border-gray-600" @click="toggleDarkMode">{{ isDarkMode ? '关闭深色模式' : '开启深色模式' }}</button>
        </div>
        <div class="flex items-center justify-between gap-3 py-4">
          <h2 class="font-semibold">隐私模式</h2>
          <button type="button" :aria-pressed="isPrivacyMode" class="rounded-lg border border-gray-300 px-4 py-2 text-sm dark:border-gray-600" @click="togglePrivacyMode">{{ isPrivacyMode ? '关闭隐私模式' : '开启隐私模式' }}</button>
        </div>
      </section>
    </div>
    <LoginDialog v-model:show="showLoginDialog" @login-success="checkLogin" />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getCurrentBaseUrl, getLoginStatus, logout, setBaseUrl } from '../../api/api'
import { useDarkMode } from '../../store/darkMode'
import { usePrivacyStore } from '../../store/privacy'
import LoginDialog from './LoginDialog.vue'

const serverUrl = ref(getCurrentBaseUrl())
const serverError = ref('')
const checkingLogin = ref(false)
const isLoggedIn = ref(false)
const username = ref('')
const authPending = ref(false)
const authMessage = ref('')
const showLoginDialog = ref(false)
const { isDarkMode, toggleDarkMode } = useDarkMode()
const { isPrivacyMode, togglePrivacyMode } = usePrivacyStore()

const saveServerUrl = () => {
  serverError.value = ''
  try {
    const url = new URL(serverUrl.value.trim())
    if (!['http:', 'https:'].includes(url.protocol)) throw new Error('invalid_protocol')
    setBaseUrl(url.toString().replace(/\/$/, ''))
  } catch {
    serverError.value = '请输入有效的 HTTP 或 HTTPS 后端地址。'
  }
}

const checkLogin = async () => {
  checkingLogin.value = true
  authMessage.value = ''
  try {
    const response = await getLoginStatus()
    isLoggedIn.value = response.data.code === 0 && Boolean(response.data.data?.isLogin)
    username.value = isLoggedIn.value ? response.data.data.uname : ''
  } catch {
    isLoggedIn.value = false
    username.value = ''
    authMessage.value = '无法检查 B站登录状态，请检查后端连接。'
  } finally {
    checkingLogin.value = false
  }
}

const handleLogin = async () => {
  if (!isLoggedIn.value) {
    showLoginDialog.value = true
    return
  }
  if (!window.confirm('确定退出 B站登录？')) return
  authPending.value = true
  authMessage.value = ''
  try {
    const response = await logout()
    if (response.data.status !== 'success') throw new Error(response.data.message || '退出登录失败。')
    isLoggedIn.value = false
    username.value = ''
  } catch (error) {
    authMessage.value = error.response?.data?.detail || error.message || '退出登录失败。'
  } finally {
    authPending.value = false
  }
}

onMounted(checkLogin)
</script>
