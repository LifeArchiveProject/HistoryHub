<template>
  <Sidebar @change-content="currentContent = $event" v-model:showRemarks="showRemarks">
    <!-- 主要内容区域 -->
    <div class="h-screen overflow-y-auto">
      <router-view></router-view>
    </div>
  </Sidebar>

  <!-- 数据同步管理模态框 - 全局层级 -->
  <DataSyncManager 
    v-model:showModal="showDataSyncModal"
    :initialTab="currentSyncTab"
    @sync-complete="handleSyncComplete"
    @check-complete="handleCheckComplete"
  />
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '../Sidebar.vue'
import DataSyncManager from '../DataSyncManager.vue'

const route = useRoute()

// 当前显示的内容
const currentContent = ref('history')
const showRemarks = ref(false)

// 数据同步弹窗状态
const showDataSyncModal = ref(false)
const currentSyncTab = ref('integrity')

// 监听路由变化
watch(
  () => route.path,
  (path) => {
    if (path === '/settings') {
      currentContent.value = 'settings'
      showRemarks.value = false
    } else if (path === '/media') {
      currentContent.value = 'media'
      
      // 如果是通过备注路由重定向过来的，需要显示备注
      if (route.query.tab === 'remarks') {
        showRemarks.value = true
      } else {
        showRemarks.value = false
      }
    } else if (path === '/' || path.startsWith('/page/')) {
      currentContent.value = 'history'
      showRemarks.value = false
    } else if (path === '/analytics') {
      currentContent.value = 'analytics'
      showRemarks.value = false
    } else if (path === '/images') {
      currentContent.value = 'images'
      showRemarks.value = false
    } else if (path === '/scheduler') {
      currentContent.value = 'scheduler'
      showRemarks.value = false
    } else if (path === '/video-downloader') {
      currentContent.value = 'video-downloader'
      showRemarks.value = false
    }
  },
  { immediate: true }
)

// 处理同步完成事件
const handleSyncComplete = (result) => {
  console.log('同步完成:', result)
}

// 处理检查完成事件
const handleCheckComplete = (result) => {
  console.log('完整性检查完成:', result)
}

// 监听自定义全局事件
onMounted(() => {
  window.addEventListener('open-data-sync-manager', handleOpenDataSyncManager)
})

onUnmounted(() => {
  window.removeEventListener('open-data-sync-manager', handleOpenDataSyncManager)
})

// 处理打开数据同步管理器事件
const handleOpenDataSyncManager = (event) => {
  if (event.detail && event.detail.tab) {
    currentSyncTab.value = event.detail.tab
  }
  showDataSyncModal.value = true
}
</script> 