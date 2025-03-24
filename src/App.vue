<script setup>
import { ref, onMounted } from 'vue'
import { tryConnectServers, setBaseUrl } from './api/api'
import { showNotify, showDialog } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'

const isLoading = ref(true)
const serverConnected = ref(false)
const connectionChecked = ref(false)

// 检查服务器连接
const checkServerConnection = async () => {
  isLoading.value = true
  try {
    const result = await tryConnectServers()
    serverConnected.value = result.success
    
    if (result.success) {
      showNotify({
        type: 'success',
        message: `服务器连接成功: ${result.url}`,
        duration: 3000
      })
    } else {
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
  } catch (error) {
    console.error('服务器连接检查失败:', error)
    serverConnected.value = false
  } finally {
    isLoading.value = false
    connectionChecked.value = true
  }
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
