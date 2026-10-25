<template>
  <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="close">
    <div role="dialog" aria-modal="true" aria-labelledby="login-title" class="relative max-h-full w-full max-w-sm overflow-y-auto rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800">
      <div class="flex items-center justify-between gap-3">
        <h2 id="login-title" class="text-lg font-semibold">B站扫码登录</h2>
        <button type="button" class="text-sm text-gray-500 dark:text-gray-400" @click="close">关闭</button>
      </div>
      <div class="mt-5 flex flex-col items-center gap-4">
        <img v-if="qrcodeImageUrl" :src="qrcodeImageUrl" alt="B站登录二维码" class="h-48 w-48 rounded-lg" />
        <p class="text-center text-sm text-gray-600 dark:text-gray-300" role="status">{{ errorMessage || statusText }}</p>
        <button type="button" :disabled="loading" class="rounded-lg bg-[#fb7299] px-4 py-2 text-sm text-white disabled:opacity-60" @click="getQRCode">
          {{ loading ? '获取中…' : (qrcodeImageUrl ? '刷新二维码' : '获取二维码') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onUnmounted, ref, watch } from 'vue'
import { generateLoginQRCode, getQRCodeImageBlob, pollQRCodeStatus } from '../../api/api'

const props = defineProps({ show: { type: Boolean, default: false } })
const emit = defineEmits(['update:show', 'login-success'])
const qrcodeKey = ref('')
const qrcodeImageUrl = ref('')
const loginStatus = ref(86101)
const loading = ref(false)
const errorMessage = ref('')
let pollingInterval
let generation = 0

const statusText = computed(() => {
  if (loading.value) return '正在获取二维码…'
  if (loginStatus.value === 86038) return '二维码已失效，请刷新。'
  if (loginStatus.value === 86090) return '已扫码，请在手机上确认。'
  return '请使用 B站 App 扫码登录。'
})

const stopPolling = () => {
  clearInterval(pollingInterval)
  pollingInterval = undefined
}

const releaseImage = () => {
  if (qrcodeImageUrl.value) URL.revokeObjectURL(qrcodeImageUrl.value)
  qrcodeImageUrl.value = ''
}

const cleanup = () => {
  generation++
  stopPolling()
  releaseImage()
  qrcodeKey.value = ''
  loading.value = false
}

const close = () => {
  cleanup()
  emit('update:show', false)
}

const poll = async (request) => {
  try {
    const response = await pollQRCodeStatus(qrcodeKey.value)
    if (request !== generation || !props.show) return
    if (response.data.status !== 'success') throw new Error(response.data.message || '无法查询登录状态。')
    loginStatus.value = response.data.data.code
    if (loginStatus.value === 0) {
      emit('login-success')
      close()
    } else if (loginStatus.value === 86038) {
      stopPolling()
    }
  } catch (error) {
    if (request !== generation || !props.show) return
    stopPolling()
    errorMessage.value = error.response?.data?.detail || error.message || '无法查询登录状态，请刷新二维码。'
  }
}

const getQRCode = async () => {
  cleanup()
  const request = generation
  loading.value = true
  errorMessage.value = ''
  loginStatus.value = 86101
  try {
    const response = await generateLoginQRCode()
    if (request !== generation || !props.show) return
    if (response.data.status !== 'success' || !response.data.data?.qrcode_key) {
      throw new Error(response.data.message || '获取二维码失败。')
    }
    qrcodeKey.value = response.data.data.qrcode_key
    const imageUrl = await getQRCodeImageBlob()
    if (request !== generation || !props.show) {
      URL.revokeObjectURL(imageUrl)
      return
    }
    qrcodeImageUrl.value = imageUrl
    pollingInterval = setInterval(() => poll(request), 2000)
  } catch (error) {
    if (request === generation) {
      errorMessage.value = error.response?.data?.detail || error.message || '获取二维码失败。'
    }
  } finally {
    if (request === generation) loading.value = false
  }
}

watch(() => props.show, (show) => {
  if (show) getQRCode()
  else cleanup()
})
onUnmounted(cleanup)
</script>
