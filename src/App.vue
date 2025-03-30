<script setup>
import { ref, onMounted, provide } from 'vue'
import { useRouter } from 'vue-router'
import { tryConnectServers, setBaseUrl, updateInstanceBaseUrl } from './api/api'
import { showDialog } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'

const isLoading = ref(true)
const serverConnected = ref(false)
const connectionChecked = ref(false)
const baseUrl = ref('')
const router = useRouter()

provide('baseUrl', baseUrl)

// 检查服务器连接
const checkServerConnection = async () => {
  try {
    isLoading.value = true
    const result = await tryConnectServers()

    if (result.success) {
      // 确保数据同步API也使用相同的baseUrl
      updateInstanceBaseUrl(result.url)
      serverConnected.value = true
    } else {
      // 显示服务器连接失败提示
      showServerConnectionError()
      serverConnected.value = false
    }
  } catch (error) {
    console.error('连接服务器出错:', error)
    showServerConnectionError()
    serverConnected.value = false
  } finally {
    isLoading.value = false
    connectionChecked.value = true
  }
}

// 显示服务器连接失败提示
const showServerConnectionError = () => {
  showDialog({
    title: '服务器连接失败',
    message: '无法连接到服务器，请检查服务器是否已启动，或手动设置服务器地址',
    showCancelButton: true,
    confirmButtonText: '设置服务器地址',
    cancelButtonText: '继续尝试',
    confirmButtonColor: '#fb7299'
  }).then(() => {
    // 用户点击设置服务器地址
    const url = window.prompt('请输入服务器地址', 'http://localhost:8899')
    if (url) {
      setBaseUrl(url)
    }
  }).catch(() => {
    // 用户点击继续尝试，重新检查连接
    checkServerConnection()
  })
}

onMounted(() => {
  checkServerConnection()
})
</script>

<template>
  <div>
    <!-- 服务器连接检查提示 -->
    <div v-if="isLoading && !connectionChecked" class="server-check-overlay">
      <div class="server-check-container">
        <div class="server-check-spinner"></div>
        <div class="server-check-text">连接服务器中...</div>
      </div>
    </div>

    <!-- 主应用内容 -->
    <router-view></router-view>
  </div>
</template>

<style scoped>
.server-check-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.server-check-container {
  text-align: center;
  padding: 20px;
  border-radius: 8px;
  background-color: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.server-check-spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 16px;
  border: 4px solid rgba(251, 114, 153, 0.2);
  border-top: 4px solid #fb7299;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.server-check-text {
  font-size: 16px;
  color: #333;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
