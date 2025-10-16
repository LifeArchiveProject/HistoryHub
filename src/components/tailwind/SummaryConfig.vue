<template>
  <div class="p-4">
    <div class="flex items-center space-x-2 text-gray-900 dark:text-gray-100 mb-2">
      <div class="p-1.5 bg-[#fb7299]/5 rounded-lg">
        <svg class="w-5 h-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h2 class="text-lg font-medium">摘要配置</h2>
    </div>
    <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">配置AI摘要的缓存策略，优化请求效率和存储空间</p>

    <div v-if="loading" class="flex justify-center py-4">
      <div class="animate-spin h-5 w-5 border-2 border-[#fb7299] border-t-transparent rounded-full"></div>
    </div>

    <div v-else-if="error" class="text-red-500 text-sm py-2">
      {{ error }}
      <button
        @click="fetchConfig"
        class="ml-2 text-xs bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 rounded px-2 py-1 border border-gray-200 dark:border-gray-700"
      >
        重试
      </button>
    </div>

    <div v-else>
      <div class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
        <span class="text-sm font-medium text-gray-700 dark:text-gray-300">缓存空摘要</span>
        <label class="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            v-model="config.cache_empty_summary"
            class="sr-only peer"
            @change="updateConfig"
          >
          <div
            class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[#fb7299]/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#fb7299]"></div>
        </label>
      </div>

      <div class="text-xs text-gray-500 dark:text-gray-400 mt-3">
        <p class="mb-1"><strong>提示：</strong></p>
        <ul class="list-disc pl-5 space-y-1">
          <li>开启缓存空摘要可减少API请求次数，但会增加数据库存储空间</li>
          <li>关闭缓存空摘要可减少数据库存储空间，但会增加API请求次数</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getSummaryConfig, updateSummaryConfig } from '../../api/api'
import { showNotify } from 'vant'
import 'vant/es/notify/style'

const loading = ref(false)
const error = ref(null)
const config = reactive({
  cache_empty_summary: true,
})

// 获取当前配置
const fetchConfig = async () => {
  loading.value = true
  error.value = null

  try {
    const response = await getSummaryConfig()
    if (response.data) {
      config.cache_empty_summary = response.data.cache_empty_summary
    }
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || '获取配置失败'
    console.error('获取摘要配置失败:', err)
  } finally {
    loading.value = false
  }
}

// 更新配置
const updateConfig = async () => {
  loading.value = true

  try {
    const response = await updateSummaryConfig({
      cache_empty_summary: config.cache_empty_summary,
    })

    if (response.data) {
      showNotify({
        type: 'success',
        message: '配置已更新',
      })
    }
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || '更新配置失败'
    console.error('更新摘要配置失败:', err)

    // 恢复原值
    fetchConfig()
  } finally {
    loading.value = false
  }
}

// 组件挂载时获取配置
onMounted(() => {
  fetchConfig()
})
</script>
