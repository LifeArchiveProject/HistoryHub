<!-- 侧边栏组件 -->
<template>
  <div class="flex h-screen">
    <!-- 左侧导航栏 -->
    <div :class="[
      'transition-all duration-300 ease-in-out bg-white/10 backdrop-blur-lg border-r border-gray-200/50 hidden sm:block',
      isCollapsed ? 'w-10' : 'w-40'
    ]">
      <!-- 侧边栏内容 -->
      <div class="h-full flex flex-col">
        <!-- 顶部 Logo -->
        <div class="p-3 border-b border-gray-200/50">
          <router-link to="/" class="flex items-center space-x-2" :class="{ 'justify-center': isCollapsed }">
            <svg class="h-6 w-6 text-gray-900 flex-shrink-0" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
              <path fill="currentColor" d="M306.005333 117.632L444.330667 256h135.296l138.368-138.325333a42.666667 42.666667 0 0 1 60.373333 60.373333L700.330667 256H789.333333A149.333333 149.333333 0 0 1 938.666667 405.333333v341.333334a149.333333 149.333333 0 0 1-149.333334 149.333333h-554.666666A149.333333 149.333333 0 0 1 85.333333 746.666667v-341.333334A149.333333 149.333333 0 0 1 234.666667 256h88.96L245.632 177.962667a42.666667 42.666667 0 0 1 60.373333-60.373334zM789.333333 341.333333h-554.666666a64 64 0 0 0-63.701334 57.856L170.666667 405.333333v341.333334a64 64 0 0 0 57.856 63.701333L234.666667 810.666667h554.666666a64 64 0 0 0 63.701334-57.856L853.333333 746.666667v-341.333334A64 64 0 0 0 789.333333 341.333333zM341.333333 469.333333a42.666667 42.666667 0 0 1 42.666667 42.666667v85.333333a42.666667 42.666667 0 0 1-85.333333 0v-85.333333a42.666667 42.666667 0 0 1 42.666666-42.666667z m341.333334 0a42.666667 42.666667 0 0 1 42.666666 42.666667v85.333333a42.666667 42.666667 0 0 1-85.333333 0v-85.333333a42.666667 42.666667 0 0 1 42.666667-42.666667z" />
            </svg>
            <span v-show="!isCollapsed" class="text-base font-semibold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent whitespace-nowrap">B站历史记录</span>
          </router-link>
        </div>

        <!-- 导航菜单 -->
        <nav class="flex-1 overflow-y-auto py-4 space-y-2" :class="{ 'px-4': !isCollapsed }">
          <!-- 历史记录 -->
          <button
            @click="changeContent('history')"
            :title="isCollapsed ? '历史记录' : ''"
            class="w-full flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'history' && !showRemarks },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">历史记录</span>
          </button>

          <!-- 我的备注 -->
          <button
            @click="changeContent('remarks')"
            :title="isCollapsed ? '我的备注' : ''"
            class="w-full flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'remarks' || (currentContent === 'history' && showRemarks) },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">我的备注</span>
          </button>

          <!-- 我的评论 -->
          <router-link
            to="/comments"
            :title="isCollapsed ? '我的评论' : ''"
            class="flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'comments' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
            @click="currentContent = 'comments'"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">我的评论</span>
          </router-link>

          <!-- 年度总结 -->
          <router-link
            to="/analytics"
            :title="isCollapsed ? '年度总结' : ''"
            class="flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'analytics' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
            @click="currentContent = 'analytics'"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">年度总结</span>
          </router-link>

          <!-- 媒体管理（整合图片管理和视频下载） -->
          <router-link
            to="/media"
            :title="isCollapsed ? '媒体管理' : ''"
            class="flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'media' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
            @click="currentContent = 'media'"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">媒体管理</span>
          </router-link>

          <!-- 计划任务 -->
          <router-link
            to="/scheduler"
            :title="isCollapsed ? '计划任务' : ''"
            class="flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'scheduler' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
            @click="currentContent = 'scheduler'"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">计划任务</span>
          </router-link>

          <!-- 关于页面 -->
          <router-link
            to="/about"
            :title="isCollapsed ? '关于' : ''"
            class="flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'about' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
            @click="currentContent = 'about'"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">关于</span>
          </router-link>

          <!-- 设置 -->
          <button
            @click="changeContent('settings')"
            :title="isCollapsed ? '设置' : ''"
            class="w-full flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'settings' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">设置</span>
          </button>

          <!-- 登录状态显示 -->
          <div
            @click="handleLoginClick"
            class="w-full flex items-center py-1.5 text-gray-700 transition-all duration-300 ease-in-out cursor-pointer hover:text-[#fb7299] text-sm"
            :class="[
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg
              class="w-5 h-5 flex-shrink-0"
              :class="{ 'mr-3': !isCollapsed }"
              fill="none"
              viewBox="0 0 24 24"
              :stroke="isLoggedIn ? '#10b981' : 'currentColor'"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span
              v-show="!isCollapsed"
              class="truncate"
              :class="{ 'text-green-500': isLoggedIn }"
            >
              <template v-if="isLoggedIn">
                {{ isPrivacyMode ? '已登录' : (userInfo?.uname || '已登录') }} (退出)
              </template>
              <template v-else>
                未登录
              </template>
            </span>
          </div>
        </nav>

        <!-- 底部设置区域 -->
        <div class="p-3 border-t border-gray-200/50">
          <!-- 服务器状态和数据完整性放在一个容器中，与SQLite版本信息保持一致的边距 -->
          <div v-if="!isCollapsed" class="mt-1 text-[11px] space-y-1 px-2">
            <!-- 服务器状态显示 -->
            <div class="flex items-center text-gray-500">
              <div class="mr-1">服务器状态:</div>
              <div class="flex items-center">
                <span
                  class="w-1.5 h-1.5 rounded-full mr-1"
                  :class="serverStatus.isRunning ? 'bg-green-500' : 'bg-red-500'"
                ></span>
                <span :class="serverStatus.isRunning ? 'text-green-600' : 'text-red-600'">
                  {{ serverStatus.isRunning ? '运行中' : '未连接' }}
                </span>
              </div>
            </div>
            
            <!-- 数据完整性状态 -->
            <div class="flex items-center text-gray-500">
              <div class="mr-1">数据完整性:</div>
              <div class="flex items-center">
                <span 
                  class="w-1.5 h-1.5 rounded-full mr-1" 
                  :class="integrityStatus.status === 'consistent' ? 'bg-green-500' : 
                        integrityStatus.status === 'inconsistent' ? 'bg-yellow-500' : 'bg-gray-400'"
                ></span>
                <span 
                  class="cursor-pointer hover:underline" 
                  :class="integrityStatus.status === 'consistent' ? 'text-green-600' : 
                        integrityStatus.status === 'inconsistent' ? 'text-yellow-600' : 'text-gray-400'"
                  @click="openDataSyncManager('integrity')"
                >
                  {{ integrityStatus.status === 'consistent' ? '一致' : 
                    integrityStatus.status === 'inconsistent' ? '不一致' : '未检查' }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- SQLite版本显示 -->
          <div v-if="!isCollapsed" class="mt-3 text-xs space-y-1 px-2 text-[11px]">
            <div class="text-gray-500">
              SQLite版本: {{ sqliteVersion?.sqlite_version || '加载中...' }}
            </div>
            <div class="text-gray-500">
              数据库大小: {{ sqliteVersion?.database_file?.size_mb?.toFixed(2) || '0' }} MB
            </div>
          </div>

          <!-- 收缩按钮 -->
          <button
            @click="toggleCollapse"
            :title="isCollapsed ? '展开侧边栏' : '收起侧边栏'"
            class="mt-3 w-full flex items-center justify-center px-2 py-1.5 text-gray-700 hover:text-[#fb7299] transition-colors duration-200 text-sm"
          >
            <svg
              class="w-5 h-5 flex-shrink-0 transform transition-transform duration-300"
              :class="{ 'rotate-180': isCollapsed }"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
            <span v-show="!isCollapsed" class="ml-2 truncate">收起侧边栏</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 右侧内容区域 -->
    <div class="flex-1 border-l border-gray-200/50 transition-all duration-300">
      <slot></slot>
    </div>
  </div>

  <!-- 登录弹窗组件 -->
  <LoginDialog
    v-model:show="showLoginDialog"
    @login-success="checkLoginStatus"
  />
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { usePrivacyStore } from '../../store/privacy'
import { importSqliteData, getLoginStatus, logout, getSqliteVersion, checkServerHealth, checkDataIntegrity } from '../../api/api'
import { showNotify } from 'vant'
import { showDialog } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'
import LoginDialog from './LoginDialog.vue'

const route = useRoute()
const router = useRouter()
const currentRoute = computed(() => route.path)

// 当前内容 - 根据路由初始化
const currentContent = ref((() => {
  const path = route.path
  if (path === '/settings') {
    return 'settings'
  } else if (path === '/remarks') {
    return 'remarks'
  } else if (path === '/media') {
    return 'media'
  } else if (path === '/analytics') {
    return 'analytics'
  } else if (path === '/scheduler') {
    return 'scheduler'
  } else if (path === '/comments') {
    return 'comments'
  } else if (path === '/about') {
    return 'about'
  } else if (path === '/' || path.startsWith('/page/')) {
    return 'history'
  }
  return 'history'
})())
const props = defineProps({
  showRemarks: {
    type: Boolean,
    default: false
  }
})
const emit = defineEmits(['change-content', 'update:showRemarks'])

// 监听路由变化
watch(
  () => route.path,
  (path) => {
    if (path === '/settings') {
      currentContent.value = 'settings'
    } else if (path === '/remarks') {
      currentContent.value = 'remarks'
    } else if (path === '/media') {
      currentContent.value = 'media'
    } else if (path === '/analytics') {
      currentContent.value = 'analytics'
    } else if (path === '/scheduler') {
      currentContent.value = 'scheduler'
    } else if (path === '/comments') {
      currentContent.value = 'comments'
    } else if (path === '/about') {
      currentContent.value = 'about'
    } else if (path === '/' || path.startsWith('/page/')) {
      currentContent.value = 'history'
    }
  }
)

// 切换内容
const changeContent = (content) => {
  if (content === 'remarks') {
    emit('change-content', 'history')
    emit('update:showRemarks', true)
    router.push('/remarks')
  } else {
    emit('change-content', content)
    emit('update:showRemarks', false)

    // 更新路由
    if (content === 'history') {
      if (route.path !== '/' && !route.path.startsWith('/page/')) {
        router.push('/')
      }
    } else if (content === 'settings') {
      router.push('/settings')
    }
  }
}

// 判断是否在历史记录页面（包括分页）
computed(() => {
  return currentRoute.value === '/' || currentRoute.value.startsWith('/page/')
})
// 隐私模式状态
const { isPrivacyMode } = usePrivacyStore()

// 侧边栏收缩状态
const isCollapsed = ref(false)
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

// SQLite版本信息
const sqliteVersion = ref({
  sqlite_version: '',
  user_version: 0,
  database_settings: {
    journal_mode: '',
    synchronous: 0,
    legacy_format: null
  },
  database_file: {
    exists: false,
    size_bytes: 0,
    size_mb: 0,
    path: ''
  }
})

// 登录相关状态
const isLoggedIn = ref(false)
const userInfo = ref(null)
const showLoginDialog = ref(false)

// 检查登录状态
const checkLoginStatus = async () => {
  try {
    const response = await getLoginStatus()
    if (response.data.status === 'success') {
      isLoggedIn.value = response.data.data.is_logged_in
      if (isLoggedIn.value) {
        userInfo.value = response.data.data.user_info
      }
    }
  } catch (error) {
    console.error('获取登录状态失败:', error)
    isLoggedIn.value = false
    userInfo.value = null
  }
}

// 点击登录状态处理
const handleLoginClick = () => {
  if (!isLoggedIn.value) {
    showLoginDialog.value = true
  } else {
    showDialog({
      title: '确认退出',
      message: '确定要退出登录吗？',
      showCancelButton: true,
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      confirmButtonColor: '#fb7299'
    }).then(() => {
      // 点击确认按钮
      handleLogout()
    }).catch(() => {
      // 点击取消按钮，不做任何操作
    })
  }
}

// 处理退出登录
const handleLogout = async () => {
  try {
    const response = await logout()
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: '已成功退出登录'
      })
      isLoggedIn.value = false
      userInfo.value = null
      // 1秒后刷新页面
      setTimeout(() => {
        window.location.reload()
      }, 1000)
    } else {
      throw new Error(response.data.message || '退出登录失败')
    }
  } catch (error) {
    console.error('退出登录失败:', error)
    showNotify({
      type: 'danger',
      message: error.response?.status === 500 ?
        '服务器错误,请稍后重试' :
        `退出登录失败: ${error.message}`
    })
  }
}

// 获取SQLite版本
const fetchSqliteVersion = async () => {
  try {
    const response = await getSqliteVersion()
    if (response.data.status === 'success') {
      sqliteVersion.value = response.data.data
    }
  } catch (error) {
    console.error('获取SQLite版本失败:', error)
    sqliteVersion.value = null
  }
}

// 服务器状态相关
const serverStatus = ref({
  isRunning: false,
  timestamp: '',
  schedulerStatus: ''
})

// 数据完整性状态
const integrityStatus = ref({
  status: 'unknown', // 'consistent', 'inconsistent', 'unknown'
  difference: 0,
  lastCheck: null
})

// 开始服务器健康检查
const checkServerHealthStatus = async () => {
  try {
    const response = await checkServerHealth()
    if (response.data && response.data.status === 'running') {
      serverStatus.value = {
        isRunning: true,
        timestamp: response.data.timestamp,
        schedulerStatus: response.data.scheduler_status
      }
      return true
    } else {
      serverStatus.value.isRunning = false
      showNotify({
        type: 'danger',
        message: '服务器未运行，请检查后端服务'
      })
      return false
    }
  } catch (error) {
    console.error('服务器健康检查失败:', error)
    serverStatus.value.isRunning = false
    showNotify({
      type: 'danger',
      message: '无法连接到服务器，请检查网络或服务器状态'
    })
    return false
  }
}

// 获取数据完整性状态
const fetchIntegrityStatus = async () => {
  try {
    const response = await checkDataIntegrity('output/bilibili_history.db', 'output/history_by_date', false)
    if (response.data && response.data.success) {
      integrityStatus.value = {
        status: response.data.difference === 0 ? 'consistent' : 'inconsistent',
        difference: response.data.difference || 0,
        lastCheck: response.data.timestamp
      }
      console.log('完整性状态:', integrityStatus.value)
    }
  } catch (error) {
    console.error('获取完整性状态失败:', error)
  }
}

// 打开数据同步管理器
const openDataSyncManager = (tab = null) => {
  // 使用自定义事件触发全局弹窗
  const event = new CustomEvent('open-data-sync-manager', {
    detail: { tab: tab || 'integrity' }
  })
  window.dispatchEvent(event)
}

// 定时器引用
const healthCheckTimer = ref(null)

// 设置定期健康检查
const setupPeriodicHealthCheck = () => {
  // 先清除可能存在的定时器
  if (healthCheckTimer.value) {
    clearInterval(healthCheckTimer.value)
  }

  // 每30秒检查一次服务器状态
  healthCheckTimer.value = setInterval(async () => {
    await checkServerHealthStatus()
  }, 30000) // 30秒
}

onMounted(async () => {
  // 初始时检查登录状态
  checkLoginStatus()
  await fetchSqliteVersion()
  
  // 设置定期健康检查
  setupPeriodicHealthCheck()
  checkServerHealthStatus()
  
  // 添加获取数据完整性状态
  await fetchIntegrityStatus()
  
  // 添加全局事件监听器，当登录状态变化时更新侧边栏的登录状态
  window.addEventListener('login-status-changed', handleLoginStatusChange)
})

// 处理登录状态变化事件
const handleLoginStatusChange = (event) => {
  console.log('侧边栏收到登录状态变化事件，正在更新登录状态...', event.detail)

  // 如果事件中包含用户信息，直接使用
  if (event.detail && event.detail.isLoggedIn) {
    isLoggedIn.value = true
    if (event.detail.userInfo) {
      userInfo.value = event.detail.userInfo
      console.log('从事件中获取到用户信息:', userInfo.value)
    } else {
      // 如果没有用户信息，则调用API获取
      checkLoginStatus()
    }
  } else {
    // 如果事件中没有登录状态信息，则调用API获取
    checkLoginStatus()
  }
}

// 组件卸载时移除事件监听器和清除定时器
onUnmounted(() => {
  window.removeEventListener('login-status-changed', handleLoginStatusChange)
  
  // 清除定时器
  if (healthCheckTimer.value) {
    clearInterval(healthCheckTimer.value)
    healthCheckTimer.value = null
  }
})
</script>
