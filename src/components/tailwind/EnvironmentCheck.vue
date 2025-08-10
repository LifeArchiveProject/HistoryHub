<template>
  <!-- 系统资源状态显示 -->
  <div :class="[inline ? 'flex flex-row items-center space-x-2' : 'flex flex-col space-y-2']">
    <!-- 加载状态 -->
    <div v-if="loading" class="flex items-center space-x-2 bg-gray-50 text-gray-500 rounded-lg" :class="[compact ? 'p-1 text-xs' : 'p-2 text-sm']">
      <div class="animate-spin h-4 w-4 border-2 border-gray-300 border-t-transparent rounded-full"></div>
      <span>检查系统环境...</span>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="flex items-center space-x-2 bg-red-50 text-red-700 rounded-lg" :class="[compact ? 'p-1 text-xs' : 'p-2 text-sm']">
      <svg :class="[compact ? 'w-4 h-4 flex-shrink-0' : 'w-5 h-5 flex-shrink-0']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <span>{{ error }}</span>
    </div>

    <!-- 系统资源检查结果 -->
    <template v-else>
      <!-- 系统资源状态 -->
      <div class="group relative">
        <div v-if="systemResources?.can_run_speech_to_text" 
             class="flex items-center space-x-2 bg-green-50 text-green-700 rounded-lg cursor-help" :class="[compact ? 'p-1 text-xs' : 'p-2 text-sm']">
          <svg :class="[compact ? 'w-4 h-4 flex-shrink-0' : 'w-5 h-5 flex-shrink-0']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span class="font-medium">系统资源满足要求</span>
          
          <!-- 悬浮详情 -->
          <div class="hidden group-hover:block absolute right-0 top-full mt-2 w-64 p-3 bg-white rounded-lg shadow-lg border border-gray-200 z-30 text-sm">
            <h4 class="font-medium text-gray-900 mb-2">系统资源详情</h4>
            <div class="space-y-2 text-gray-600">
              <p>内存: {{ systemResources.memory.available_gb.toFixed(1) }}GB / {{ systemResources.memory.total_gb.toFixed(1) }}GB</p>
              <p>CPU: {{ systemResources.cpu.physical_cores }} 核心 ({{ systemResources.cpu.logical_cores }} 线程)</p>
              <p>磁盘可用: {{ systemResources.disk.free_gb.toFixed(1) }}GB</p>
            </div>
          </div>
        </div>
        <div v-else class="flex items-center space-x-2 bg-red-50 text-red-700 rounded-lg" :class="[compact ? 'p-1 text-xs' : 'p-2 text-sm']">
          <svg :class="[compact ? 'w-4 h-4 flex-shrink-0' : 'w-5 h-5 flex-shrink-0']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div class="flex flex-col">
            <span class="font-medium">无法使用本地摘要功能</span>
            <span class="text-xs">{{ systemResources?.limitation_reason }}</span>
          </div>
        </div>
      </div>

      <!-- CUDA状态 -->
      <template v-if="systemResources?.can_run_speech_to_text">
        <div v-if="cudaLoading" class="flex items-center space-x-2 bg-gray-50 text-gray-500 rounded-lg" :class="[compact ? 'p-1 text-xs' : 'p-2 text-sm']">
          <div class="animate-spin h-4 w-4 border-2 border-gray-300 border-t-transparent rounded-full"></div>
          <span>检查CUDA支持...</span>
        </div>
        
        <div v-else class="group relative">
          <div v-if="envInfo?.system_info.cuda_available" 
               class="flex items-center space-x-2 bg-green-50 text-green-700 rounded-lg" :class="[compact ? 'p-1 text-xs' : 'p-2 text-sm']">
            <svg :class="[compact ? 'w-4 h-4 flex-shrink-0' : 'w-5 h-5 flex-shrink-0']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span class="font-medium">CUDA 可用 ({{ envInfo.system_info.cuda_version }})</span>
          </div>
          <div v-else class="flex items-center space-x-2 bg-yellow-50 text-yellow-700 rounded-lg" :class="[compact ? 'p-1 text-xs' : 'p-2 text-sm']">
            <svg :class="[compact ? 'w-4 h-4 flex-shrink-0' : 'w-5 h-5 flex-shrink-0']" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="flex flex-col">
              <span class="font-medium">CUDA 不可用</span>
              <span class="text-xs">将使用 CPU 进行处理（速度较慢）</span>
            </div>
          </div>
        </div>
      </template>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { checkAudioToTextEnvironment, checkSystemResources } from '../../api/api'
import { showNotify } from 'vant'
import 'vant/es/notify/style'

const { inline = false, compact = false } = defineProps({
  inline: { type: Boolean, default: false },
  compact: { type: Boolean, default: false }
})

const loading = ref(true)
const cudaLoading = ref(false)
const error = ref(null)
const envInfo = ref(null)
const systemResources = ref(null)

const emit = defineEmits(['environment-checked'])

const checkEnvironment = async () => {
  try {
    loading.value = true
    error.value = null

    // 1. 首先检查系统资源
    const resourceResponse = await checkSystemResources()
    systemResources.value = resourceResponse.data

    // 发送检查结果到父组件
    emit('environment-checked', {
      canRun: systemResources.value.can_run_speech_to_text,
      limitationReason: systemResources.value.limitation_reason
    })

    // 2. 如果系统资源满足要求，再检查CUDA
    if (systemResources.value.can_run_speech_to_text) {
      cudaLoading.value = true
      const cudaResponse = await checkAudioToTextEnvironment()
      envInfo.value = cudaResponse.data
    }
  } catch (err) {
    error.value = '获取环境信息失败：' + (err.message || '未知错误')
    showNotify({
      type: 'danger',
      message: error.value
    })
    // 发送错误状态到父组件
    emit('environment-checked', {
      canRun: false,
      limitationReason: error.value
    })
  } finally {
    loading.value = false
    cudaLoading.value = false
  }
}

onMounted(() => {
  checkEnvironment()
})
</script> 