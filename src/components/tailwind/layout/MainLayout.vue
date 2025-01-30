<template>
  <Sidebar @change-content="currentContent = $event" v-model:showRemarks="showRemarks">
    <!-- 主要内容区域 -->
    <div class="h-screen overflow-y-auto">
      <router-view></router-view>
    </div>
  </Sidebar>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import Sidebar from '../Sidebar.vue'

const route = useRoute()

// 当前显示的内容
const currentContent = ref('history')
const showRemarks = ref(false)

// 监听路由变化
watch(
  () => route.path,
  (path) => {
    if (path === '/settings') {
      currentContent.value = 'settings'
      showRemarks.value = false
    } else if (path === '/remarks') {
      currentContent.value = 'remarks'
      showRemarks.value = true
    } else if (path === '/' || path.startsWith('/page/')) {
      currentContent.value = 'history'
      showRemarks.value = false
    }
  },
  { immediate: true }
)
</script> 