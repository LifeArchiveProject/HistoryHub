<!-- 视频下载弹窗 -->
<template>
  <Teleport to="body">
    <!-- 通知容器 -->
    <div class="notification-container fixed top-0 left-0 right-0 z-[100000]"></div>

    <div v-if="show" class="fixed inset-0 z-[9999] flex items-center justify-center">
      <!-- 遮罩层 -->
      <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="handleClose"></div>

      <!-- 弹窗内容 -->
      <div class="relative bg-white rounded-lg shadow-xl w-[1000px] max-h-[90vh] z-10">
        <!-- 关闭按钮 -->
        <button
          @click="handleClose"
          class="absolute right-4 top-4 text-gray-400 hover:text-gray-500 z-20"
        >
          <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <!-- Yutto 项目致谢 -->
        <div class="py-3 px-4 flex items-center justify-center space-x-4 bg-gray-50 border-b border-gray-100 rounded-t-lg">
          <img src="https://yutto.nyakku.moe/logo-mini.svg" alt="Yutto Logo" class="w-8 h-8">
          <div class="flex flex-col">
            <p class="text-sm text-gray-600">下载功能通过 <a href="https://yutto.nyakku.moe/" target="_blank" class="text-[#fb7299] hover:text-[#fb7299]/80 font-medium">Yutto</a> 实现</p>
            <p class="text-xs text-gray-400">感谢 Yutto 开发团队的开源贡献</p>
          </div>
        </div>

        <!-- 标题 -->
        <div class="px-6 pt-4 pb-0">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-lg font-medium text-gray-900">下载视频</h3>
              <p v-if="downloadStarted" class="mt-1 text-sm text-gray-500">
                {{ isDownloading ? '正在下载：' : (downloadError ? '下载出错：' : '下载完成：') }} {{ videoInfo.title }}
              </p>
              <p v-else class="mt-1 text-sm text-gray-500">
                {{ videoInfo.title }}
              </p>
            </div>

            <!-- FFmpeg 状态 -->
            <div v-if="ffmpegStatus" class="flex-shrink-0 ml-4">
              <div v-if="ffmpegStatus.installed" class="flex items-center space-x-2 p-2 bg-green-50 text-green-700 rounded-lg text-sm">
                <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <div>
                  <p class="font-medium">FFmpeg 已安装</p>
                  <p class="text-xs">{{ ffmpegStatus.version }}</p>
                </div>
              </div>
              <div v-else class="group relative">
                <div class="flex flex-col space-y-2">
                  <div class="flex items-center space-x-2 p-2 bg-red-50 text-red-700 rounded-lg text-sm">
                    <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <p class="font-medium">FFmpeg 未安装</p>
                  </div>
                  <div class="text-sm text-gray-600">
                    <p class="mt-1">
                      <a href="https://yutto.nyakku.moe/guide/quick-start#ffmpeg-%E4%B8%8B%E8%BD%BD%E4%B8%8E%E9%85%8D%E7%BD%AE"
                         target="_blank"
                         class="text-[#fb7299] hover:text-[#fb7299]/80">
                        点击查看Yutto说明 →
                      </a>
                    </p>
                  </div>
                </div>
                <!-- 添加间隙区域 -->
                <div class="hidden group-hover:block hover:block absolute right-0 top-full h-2 w-full"></div>
                <!-- 悬浮提示 -->
                <div class="hidden group-hover:block hover:block absolute right-0 top-[calc(100%+0.5rem)] w-[500px] p-4 bg-white rounded-lg shadow-lg border border-gray-200 z-30 text-sm">
                  <p class="font-medium text-gray-900 mb-3">安装指南：</p>
                  <!-- 使用接口返回的安装指南 -->
                  <div v-if="ffmpegStatus?.install_guide" class="space-y-2 whitespace-pre-wrap">
                    <div v-for="(line, index) in installGuideLines" :key="index" class="flex items-start space-x-2">
                      <template v-if="isCommand(line)">
                        <div class="flex-1 bg-gray-50 p-2 rounded break-all">
                          <code class="text-gray-700">{{ getCommandContent(line) }}</code>
                        </div>
                        <button @click="copyToClipboard(getCommandContent(line))"
                                class="text-[#fb7299] hover:text-[#fb7299]/80 p-1 rounded-md hover:bg-[#fb7299]/10 flex-shrink-0"
                                title="点击复制命令">
                          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                          </svg>
                        </button>
                      </template>
                      <template v-else>
                        <p class="text-gray-600 break-all">{{ line }}</p>
                      </template>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 视频信息 -->
        <div class="p-6 pt-4 flex flex-col items-center space-y-3">
          <!-- 封面图 -->
          <div class="relative w-full">
            <div class="flex space-x-6">
              <div class="w-44 h-28 flex-shrink-0">
                <img :src="videoInfo.cover" :alt="videoInfo.title" class="w-full h-full object-cover rounded-lg">
              </div>
              <div class="flex-1 min-w-0 space-y-2">
                <h4 class="text-base font-medium text-gray-900 truncate whitespace-nowrap overflow-hidden">{{ videoInfo.title }}</h4>
                <p class="text-sm text-gray-500">UP主：{{ videoInfo.author }}</p>
                <p class="text-sm text-gray-500">BV号：{{ videoInfo.bvid }}</p>
                <!-- 下载选项 -->
                <div class="flex gap-8 items-start text-sm text-gray-600">
                  <div class="space-y-1">
                    <label class="flex items-center space-x-2 cursor-pointer select-none">
                      <input
                        type="checkbox"
                        v-model="downloadCover"
                        class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                      >
                      <span>下载并合成视频封面</span>
                    </label>
                    <div class="text-xs text-gray-500">
                      提示：FFmpeg版本过低时可能导致封面合成失败
                    </div>
                  </div>
                  <label class="flex items-center space-x-2 cursor-pointer select-none">
                    <input
                      type="checkbox"
                      v-model="onlyAudio"
                      class="w-4 h-4 text-[#fb7299] border-gray-300 rounded focus:ring-[#fb7299]"
                    >
                    <span>仅下载音频</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- 下载日志 -->
          <div class="w-full h-[260px] bg-gray-50 rounded-lg p-4 font-mono text-sm overflow-y-auto" ref="logContainer">
            <div v-if="!downloadStarted" class="text-gray-500">
              点击下方按钮开始下载...
            </div>
            <div v-else>
              <div v-for="(log, index) in downloadLogs" :key="index" class="whitespace-pre break-all leading-6" :class="{
                'text-gray-600': !log.includes('ERROR'),
                'text-red-500': log.includes('ERROR'),
                'text-green-500': log.includes('下载完成'),
                'text-yellow-500': log.includes('WARN'),
              }">{{ log }}</div>
            </div>
          </div>

          <!-- 状态和按钮 -->
          <div class="w-full flex items-center justify-between">
            <div class="text-sm" :class="{
              'text-gray-500': !downloadStarted,
              'text-red-500': downloadError,
              'text-green-500': !isDownloading && downloadStarted && !downloadError,
              'text-[#fb7299]': isDownloading
            }">
              {{ downloadStatus }}
            </div>
            <div class="flex space-x-4">
              <button
                @click="handleClose"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
                :disabled="isDownloading"
              >
                {{ isDownloading ? '下载中...' : '关闭' }}
              </button>
              <button
                v-if="!downloadStarted || downloadError"
                @click="startDownload"
                class="px-4 py-2 text-sm font-medium text-white bg-[#fb7299] rounded-md hover:bg-[#fb7299]/90 disabled:opacity-50"
                :disabled="isDownloading"
              >
                {{ downloadError ? '重试' : '开始下载' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, onUnmounted, nextTick } from 'vue'
import { downloadVideo, checkFFmpeg } from '../../api/api'

defineOptions({
  name: 'DownloadDialog'
})

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  videoInfo: {
    type: Object,
    required: true,
    default: () => ({
      title: '',
      author: '',
      bvid: '',
      cover: '',
      cid: 0
    })
  }
})

const emit = defineEmits(['update:show', 'download-complete'])

// 下载相关状态
const downloadStarted = ref(false)
const isDownloading = ref(false)
const downloadError = ref(false)
const downloadLogs = ref([])

// 下载状态文本
const downloadStatus = computed(() => {
  if (!downloadStarted.value) return '准备就绪'
  if (downloadError.value) return '下载出错'
  if (isDownloading.value) return '下载中...'
  return '下载完成'
})

// 日志容器引用
const logContainer = ref(null)

// FFmpeg 状态
const ffmpegStatus = ref(null)

// 检查 FFmpeg 安装状态
const checkFFmpegStatus = async () => {
  try {
    const response = await checkFFmpeg()
    if (response.data) {
      ffmpegStatus.value = {
        installed: response.data.status === 'success',
        version: response.data.version,
        path: response.data.path,
        os_info: response.data.os_info,
        install_guide: response.data.install_guide
      }
    }
  } catch (error) {
    console.error('检查 FFmpeg 失败:', error)
  }
}

// 下载封面选项
const downloadCover = ref(true)
// 仅下载音频选项
const onlyAudio = ref(false)

// 开始下载
const startDownload = async () => {
  try {
    // 如果 FFmpeg 未安装，显示错误提示
    if (ffmpegStatus.value && !ffmpegStatus.value.installed) {
      downloadLogs.value.push('ERROR: FFmpeg 未安装，请先安装 FFmpeg')
      downloadError.value = true
      return
    }

    // 重置状态
    downloadStarted.value = true
    isDownloading.value = true
    downloadError.value = false
    downloadLogs.value = []

    // 发起下载请求并处理实时消息
    await downloadVideo(props.videoInfo.bvid, null, (content) => {
      console.log('收到消息:', content)
      downloadLogs.value.push(content)

      // 检查下载状态
      if (content.includes('下载完成')) {
        isDownloading.value = false
        emit('download-complete')
      } else if (content.includes('ERROR')) {
        downloadError.value = true
        isDownloading.value = false
      }

      // 自动滚动到底部
      nextTick(() => {
        scrollToBottom()
      })
    }, downloadCover.value, onlyAudio.value, props.videoInfo.cid)
  } catch (error) {
    console.error('下载失败:', error)
    downloadError.value = true
    isDownloading.value = false
    const errorLines = error.message.split('\n')
    for (const line of errorLines) {
      downloadLogs.value.push(`ERROR: ${line}`)
    }
  }
}

// 滚动到底部的优化实现
const scrollToBottom = () => {
  if (logContainer.value) {
    logContainer.value.scrollTop = logContainer.value.scrollHeight
  }
}

// 监听日志变化
watch(() => downloadLogs.value.length, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

// 处理关闭弹窗
const handleClose = () => {
  if (isDownloading.value) {
    if (!confirm('下载正在进行中，确定要关闭吗？')) {
      return
    }
  }
  
  // 如果下载已完成且没有错误，触发下载完成事件
  if (downloadStarted.value && !isDownloading.value && !downloadError.value) {
    emit('download-complete')
  }
  
  emit('update:show', false)
  // 重置状态
  downloadStarted.value = false
  isDownloading.value = false
  downloadError.value = false
  downloadLogs.value = []
}

// 监听show变化
watch(() => props.show, (newVal) => {
  if (!newVal) {
    handleClose()
  } else {
    // 在弹窗打开时检查 FFmpeg
    checkFFmpegStatus()
  }
})

// 组件卸载时清理
onUnmounted(() => {
  // 重置状态
  downloadStarted.value = false
  isDownloading.value = false
  downloadError.value = false
  downloadLogs.value = []
})

// 复制到剪贴板函数
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showNotify({
      type: 'success',
      message: '命令已复制到剪贴板',
      position: 'top',
      duration: 2000,
      teleport: '.notification-container'
    })
  } catch (err) {
    console.error('复制失败:', err)
    showNotify({
      type: 'danger',
      message: '复制失败，请手动复制',
      position: 'top',
      duration: 2000,
      teleport: '.notification-container'
    })
  }
}

// 处理安装指南的行
const installGuideLines = computed(() => {
  if (!ffmpegStatus.value?.install_guide) return []
  return ffmpegStatus.value.install_guide.split('\n').filter(line => line.trim())
})

// 判断是否为命令行
const isCommand = (line) => {
  return line.trim().startsWith('yum') ||
         line.trim().startsWith('sudo') ||
         line.trim().startsWith('apt') ||
         line.trim().startsWith('brew')
}

// 获取命令内容
const getCommandContent = (line) => {
  return line.trim()
}

// 导入通知组件
import { showNotify } from 'vant'
import 'vant/es/notify/style'
</script>

<style scoped>
/* 当弹窗显示时禁用页面滚动 */
:global(body) {
  overflow: hidden;
}
</style>
