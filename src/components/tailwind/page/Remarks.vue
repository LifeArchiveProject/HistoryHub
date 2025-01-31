<template>
  <div class="min-h-screen bg-gray-50/30">
    <div class="py-6">
      <div class="max-w-7xl mx-auto px-4">
        <!-- 页面标题 -->
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center space-x-3 text-gray-900">
            <svg class="w-7 h-7 text-[#fb7299]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            <h1 class="text-2xl font-medium">我的备注</h1>
          </div>
          <div class="text-sm text-gray-500">
            共 {{ total }} 条备注
          </div>
        </div>

        <!-- 备注列表 -->
        <div class="grid grid-cols-1 gap-6">
          <div v-for="record in remarkRecords"
               :key="record.bvid + record.view_at"
               class="bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-300">
            <div class="flex p-4 space-x-6">
              <!-- 左侧：视频信息 -->
              <div class="w-64 flex-shrink-0">
                <!-- 视频封面 -->
                <div class="relative w-full aspect-video overflow-hidden rounded-lg mb-3">
                  <img
                    :src="record.cover"
                    :class="{ 'blur-md': isPrivacyMode }"
                    class="w-full h-full object-cover"
                    alt=""
                  />
                  <!-- 视频时长 -->
                  <div class="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
                    {{ formatDuration(record.duration) }}
                  </div>
                  <!-- 观看进度条 -->
                  <div class="absolute bottom-0 left-0 w-full h-1 bg-gray-200">
                    <div
                      class="h-full bg-[#fb7299]"
                      :style="{ width: getProgressWidth(record.progress, record.duration) }"
                    ></div>
                  </div>
                </div>

                <!-- 视频标题 -->
                <h3 class="text-sm font-medium text-gray-900 mb-2 line-clamp-2 hover:line-clamp-none"
                    :class="{ 'blur-sm': isPrivacyMode }"
                    v-html="isPrivacyMode ? '******' : record.title">
                </h3>

                <!-- UP主信息和时间 -->
                <div class="flex items-center space-x-2 mb-2">
                  <img
                    :src="record.author_face"
                    :class="{ 'blur-md': isPrivacyMode }"
                    class="w-4 h-4 rounded-full"
                    alt=""
                  />
                  <span class="text-xs text-gray-600"
                        :class="{ 'blur-sm': isPrivacyMode }"
                        v-text="isPrivacyMode ? '******' : record.author_name">
                  </span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-400">
                  <span>{{ formatTimestamp(record.view_at) }}</span>
                  <button
                    @click="openVideo(record)"
                    class="inline-flex items-center space-x-1 text-[#fb7299] hover:text-[#fb7299]/80 transition-colors duration-200"
                  >
                    <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>查看视频</span>
                  </button>
                </div>
              </div>

              <!-- 右侧：备注内容 -->
              <div class="flex-1 min-w-0 relative">
                <van-field
                  v-model="record.remark"
                  :disabled="isPrivacyMode"
                  @blur="handleRemarkUpdate(record)"
                  type="textarea"
                  rows="8"
                  :autosize="{ minHeight: 160 }"
                  :placeholder="'添加备注...'"
                  class="remarks-field !bg-transparent"
                />
                <div v-if="record.remark_time" class="absolute bottom-1 right-2 text-xs text-gray-400">
                  最后更新: {{ formatRemarkTime(record.remark_time) }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 分页组件 -->
        <div class="mt-8">
          <Pagination
            :current-page="page"
            :total-pages="totalPages"
            :use-routing="false"
            @page-change="handlePageChange"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { usePrivacyStore } from '../../../store/privacy'
import { getAllRemarks, updateVideoRemark } from '../../../api/api'
import { showNotify } from 'vant'
import Pagination from '../Pagination.vue'

const { isPrivacyMode } = usePrivacyStore()

// 状态管理
const page = ref(1)
const totalPages = ref(1)
const total = ref(0)
const remarkRecords = ref([])

// 获取备注列表
const fetchRemarks = async () => {
  try {
    const response = await getAllRemarks(page.value, 12) // 每页显示12条
    if (response.data.status === 'success') {
      remarkRecords.value = response.data.data.records.map(record => ({
        ...record,
        originalRemark: record.remark // 保存原始备注内容
      }))
      totalPages.value = Math.ceil(response.data.data.total / response.data.data.size)
      total.value = response.data.data.total
    } else {
      throw new Error(response.data.message || '获取备注列表失败')
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: error.message
    })
  }
}

// 处理分页变化
const handlePageChange = (newPage) => {
  page.value = newPage
  fetchRemarks()
}

// 打开视频
const openVideo = (record) => {
  const url = `https://www.bilibili.com/video/${record.bvid}`
  window.open(url, '_blank')
}

// 格式化时间戳
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化时长
const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完'
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0')
  const secs = String(seconds % 60).padStart(2, '0')
  return `${minutes}:${secs}`
}

// 获取进度条宽度
const getProgressWidth = (progress, duration) => {
  if (progress === -1) return '100%'
  if (duration === 0) return '0%'
  return `${(progress / duration) * 100}%`
}

// 格式化备注时间
const formatRemarkTime = (timestamp) => {
  if (!timestamp) return ''
  const date = new Date(timestamp * 1000)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 处理备注更新
const handleRemarkUpdate = async (record) => {
  const newValue = record.remark
  if (newValue === record.originalRemark) return

  try {
    const response = await updateVideoRemark(
      record.bvid,
      record.view_at,
      newValue
    )
    if (response.data.status === 'success') {
      record.originalRemark = newValue
      record.remark_time = response.data.data.remark_time // 更新备注时间
      showNotify({
        type: 'success',
        message: '备注已更新'
      })
    } else {
      throw new Error(response.data.message)
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: error.message
    })
    // 恢复原值
    record.remark = record.originalRemark
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchRemarks()
})

// 默认导出
defineOptions({
  name: 'Remarks'
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

:deep(.remarks-field) {
  height: 100%;
}

:deep(.remarks-field .van-field__control) {
  padding: 12px 16px;
  background-color: rgba(251, 114, 153, 0.03);
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  color: #4b5563;
  transition: all 0.2s ease;
  resize: none;
  min-height: 160px !important;
  border: 1px solid transparent;
}

:deep(.remarks-field .van-field__control:hover) {
  background-color: rgba(251, 114, 153, 0.05);
}

:deep(.remarks-field .van-field__control:focus) {
  background-color: rgba(251, 114, 153, 0.05);
  border-color: #fb7299;
  box-shadow: 0 0 0 2px rgba(251, 114, 153, 0.1);
  outline: none;
}

:deep(.remarks-field .van-field__control::placeholder) {
  color: #9ca3af;
}

:deep(.remarks-field.van-field) {
  padding: 0;
  border: none;
}

:deep(.van-field__error-message) {
  display: none;
}
</style>
