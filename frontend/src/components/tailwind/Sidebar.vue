<!-- 侧边栏组件 -->
<template>
  <div class="flex h-screen">
    <!-- 左侧导航栏 -->
    <div :class="[
      'transition-all duration-300 ease-in-out bg-white/10 dark:bg-gray-800/10 backdrop-blur-lg border-r border-gray-200/50 dark:border-gray-700/50 hidden sm:block',
      isCollapsed ? 'w-10' : 'w-40'
    ]">
      <!-- 侧边栏内容 -->
      <div class="h-full flex flex-col">
        <!-- 顶部 Logo -->
        <div class="p-1 border-b border-gray-200/50 dark:border-gray-700/50">
          <router-link to="/" class="w-full flex justify-center items-center">
            <img v-if="isCollapsed" src="/logo.svg" class="w-full object-contain" alt="Logo" />
            <img v-else src="/logo.png" class="w-full object-contain" alt="Logo" />
          </router-link>
        </div>

        <!-- 导航菜单 -->
        <nav class="flex-1 overflow-y-auto py-4 space-y-2" :class="{ 'px-4': !isCollapsed }">
          <!-- 历史记录 -->
          <button
            @click="changeContent('history')"
            :title="isCollapsed ? '历史记录' : ''"
            class="w-full flex items-center py-1.5 text-gray-700 dark:text-gray-300 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299] dark:bg-[#fb7299]/20': currentContent === 'history' && !showRemarks },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">历史记录</span>
          </button>

          <!-- 我的收藏 -->
          <router-link
            to="/favorites"
            :title="isCollapsed ? '我的收藏' : ''"
            class="flex items-center py-1.5 text-gray-700 dark:text-gray-300 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299] dark:bg-[#fb7299]/20': currentContent === 'favorites' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">我的收藏</span>
          </router-link>

          <!-- 年度总结 -->
          <router-link
            to="/analytics"
            :title="isCollapsed ? '年度总结' : ''"
            class="flex items-center py-1.5 text-gray-700 dark:text-gray-300 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299] dark:bg-[#fb7299]/20': currentContent === 'analytics' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
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
            class="flex items-center py-1.5 text-gray-700 dark:text-gray-300 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299] dark:bg-[#fb7299]/20': currentContent === 'media' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">媒体管理</span>
          </router-link>

          <!-- B站助手 -->
          <router-link
            to="/bili-tools"
            :title="isCollapsed ? 'B站助手' : ''"
            class="flex items-center py-1.5 text-gray-700 dark:text-gray-300 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299] dark:bg-[#fb7299]/20': currentContent === 'bili-tools' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">B站助手</span>
          </router-link>

          <!-- 计划任务 -->
          <router-link
            to="/scheduler"
            :title="isCollapsed ? '计划任务' : ''"
            class="flex items-center py-1.5 text-gray-700 dark:text-gray-300 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299] dark:bg-[#fb7299]/20': currentContent === 'scheduler' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-5 h-5 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">计划任务</span>
          </router-link>

          <!-- 设置 -->
          <button
            @click="changeContent('settings')"
            :title="isCollapsed ? '设置' : ''"
            class="w-full flex items-center py-1.5 text-gray-700 dark:text-gray-300 transition-all duration-300 ease-in-out text-sm"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299] dark:bg-[#fb7299]/20': currentContent === 'settings' },
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
            class="w-full flex items-center py-1.5 text-gray-700 dark:text-gray-300 transition-all duration-300 ease-in-out cursor-pointer hover:text-[#fb7299] text-sm"
            :class="[
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <!-- 未登录时显示默认图标 -->
            <svg
              v-if="!isLoggedIn"
              class="w-5 h-5 flex-shrink-0"
              :class="{ 'mr-3': !isCollapsed }"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>

            <!-- 已登录时显示用户头像 -->
            <div
              v-else
              class="w-5 h-5 flex-shrink-0 rounded-full overflow-hidden"
              :class="{ 'mr-3': !isCollapsed }"
            >
              <img
                :src="userInfo?.face"
                alt="用户头像"
                class="w-full h-full object-cover"
                :class="{ 'blur-md': isPrivacyMode }"
                onerror="this.src='/defaultAvatar.png'"
              />
            </div>

            <span
              v-show="!isCollapsed"
              class="truncate relative"
              :class="{ 'text-green-500': isLoggedIn }"
            >
              <template v-if="isLoggedIn">
                {{ isPrivacyMode ? '已登录' : (userInfo?.uname || '已登录') }}
              </template>
              <template v-else>
                未登录
              </template>
            </span>
          </div>
        </nav>

        <!-- 底部设置区域 -->
        <div class="p-3 border-t border-gray-200/50 dark:border-gray-700/50">
          <!-- 服务器状态和数据完整性放在一个容器中，与SQLite版本信息保持一致的边距 -->
          <div v-if="!isCollapsed" class="mt-1 text-[11px] space-y-1 px-2">
            <!-- 服务器状态显示 -->
            <div class="flex items-center text-gray-500 dark:text-gray-400">
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
            <div class="flex items-center text-gray-500 dark:text-gray-400">
              <div class="mr-1">数据完整性:</div>
              <div class="flex items-center">
                <span
                  class="w-1.5 h-1.5 rounded-full mr-1"
                  :class="integrityStatus.status === 'consistent' ? 'bg-green-500' :
                        integrityStatus.status === 'inconsistent' ? 'bg-yellow-500' :
                        integrityStatus.status === 'disabled' ? 'bg-gray-500' : 'bg-gray-400'"
                ></span>
                <span
                  class="cursor-pointer hover:underline"
                  :class="integrityStatus.status === 'consistent' ? 'text-green-600' :
                        integrityStatus.status === 'inconsistent' ? 'text-yellow-600' :
                        integrityStatus.status === 'disabled' ? 'text-gray-500' : 'text-gray-400'"
                  @click="openDataSyncManager('integrity')"
                >
                  {{ integrityStatus.status === 'consistent' ? '一致' :
                    integrityStatus.status === 'inconsistent' ? '不一致' :
                    integrityStatus.status === 'disabled' ? '未开启' : '未检查' }}
                </span>
              </div>
            </div>
          </div>

          <!-- SQLite版本显示 -->
          <div v-if="!isCollapsed" class="mt-3 text-xs space-y-1 px-2 text-[11px]">
            <div class="text-gray-500 dark:text-gray-400">
              SQLite版本: {{ sqliteVersion?.sqlite_version || '加载中...' }}
            </div>
            <div class="text-gray-500 dark:text-gray-400">
              数据库大小: {{ sqliteVersion?.database_file?.size_mb?.toFixed(2) || '0' }} MB
            </div>
          </div>

          <!-- 收缩按钮 -->
          <button
            @click="toggleCollapse"
            :title="isCollapsed ? '展开侧边栏' : '收起侧边栏'"
            class="mt-3 w-full flex items-center justify-center px-2 py-1.5 text-gray-700 dark:text-gray-300 hover:text-[#fb7299] transition-colors duration-200 text-sm"
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
    <div class="flex-1 border-l border-gray-200/50 dark:border-gray-700/50 transition-all duration-300">
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
import { usePrivacyStore } from '@/store/privacy.js'
import { useDarkMode } from '@/store/darkMode.js'
import { getLoginStatus, logout, getSqliteVersion, checkServerHealth, checkDataIntegrity, getIntegrityCheckConfig } from '../../api/api'
import { showNotify } from 'vant'
import { showDialog } from 'vant'
import 'vant/es/notify/style'
import 'vant/es/dialog/style'
import LoginDialog from './LoginDialog.vue'

const { isDarkMode } = useDarkMode()

const route = useRoute()
const router = useRouter()
const currentRoute = computed(() => route.path)

// 根据当前路由路径计算当前内容
const currentContent = computed(() => {
  const path = route.path
  if (path.startsWith('/search')) return 'search'
  if (path.startsWith('/analytics')) return 'analytics'
  if (path.startsWith('/settings')) return 'settings'
  if (path.startsWith('/images')) return 'images'
  if (path.startsWith('/scheduler')) return 'scheduler'
  if (path.startsWith('/downloads')) return 'downloads'
  if (path.startsWith('/media')) return 'media'
  if (path.startsWith('/favorites')) return 'favorites'
  if (path.startsWith('/bili-tools')) return 'bili-tools'
  return 'history' // 默认返回历史记录
})
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
    } else if (path === '/media') {
      currentContent.value = 'media'
    } else if (path === '/analytics') {
      currentContent.value = 'analytics'
    } else if (path === '/scheduler') {
      currentContent.value = 'scheduler'
    } else if (path === '/favorites' || path.startsWith('/favorites/')) {
      currentContent.value = 'favorites'
    } else if (path === '/bili-tools') {
      currentContent.value = 'bili-tools'
    } else if (path === '/' || path.startsWith('/page/')) {
      currentContent.value = 'history'
    }
  }
)

// 切换内容
const changeContent = (content) => {
  if (content === 'history') {
    emit('change-content', content)
    emit('update:showRemarks', false)

    // 更新路由
      if (route.path !== '/' && !route.path.startsWith('/page/')) {
        router.push('/')
      }
    } else if (content === 'settings') {
    emit('change-content', content)
    emit('update:showRemarks', false)
      router.push('/settings')
  }
}

// 判断是否在历史记录页面（包括分页）
const isHistoryPage = computed(() => {
  return currentRoute.value === '/' || currentRoute.value.startsWith('/page/')
})
// 隐私模式状态
const { isPrivacyMode } = usePrivacyStore()

// 侧边栏收缩状态
const isCollapsed = ref(false)
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
  // 保存当前侧边栏状态
  localStorage.setItem('sidebarCollapsed', isCollapsed.value.toString())

  // 如果用户手动收起侧边栏，将showSidebar设置为false
  if (isCollapsed.value) {
    localStorage.setItem('showSidebar', 'false')
    // 触发全局事件，通知设置组件更新
    try {
      const event = new CustomEvent('sidebar-toggle-changed', {
        detail: { showSidebar: false }
      })
      window.dispatchEvent(event)
    } catch (error) {
      console.error('触发侧边栏切换事件失败:', error)
    }
  } else {
    // 如果用户展开侧边栏，将showSidebar设置为true
    localStorage.setItem('showSidebar', 'true')
    // 触发全局事件，通知设置组件更新
    try {
      const event = new CustomEvent('sidebar-toggle-changed', {
        detail: { showSidebar: true }
      })
      window.dispatchEvent(event)
    } catch (error) {
      console.error('触发侧边栏切换事件失败:', error)
    }
  }
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
    // 新的API响应格式是 {code: 0, message: "0", ttl: 1, data: {...}}
    // code为0表示请求成功
    if (response.data && response.data.code === 0) {
      isLoggedIn.value = response.data.data.isLogin
      if (isLoggedIn.value) {
        userInfo.value = response.data.data
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
      console.error('服务器健康检查失败: 服务器未运行')
      return false
    }
  } catch (error) {
    console.error('服务器健康检查失败:', error)
    serverStatus.value.isRunning = false
    return false
  }
}

// 获取数据完整性状态
const fetchIntegrityStatus = async () => {
  try {
    // 首先获取数据完整性校验配置
    const configResponse = await getIntegrityCheckConfig()

    // 检查是否启用了数据完整性校验
    if (configResponse.data && configResponse.data.success) {
      const checkEnabled = configResponse.data.check_on_startup

      if (!checkEnabled) {
        // 如果未启用数据完整性校验，显示"未开启"状态
        integrityStatus.value = {
          status: 'disabled',
          difference: 0,
          lastCheck: new Date().toISOString()
        }
        return
      }
    }

    // 如果启用了数据完整性校验，获取校验结果
    const response = await checkDataIntegrity('output/bilibili_history.db', 'output/history_by_date', false)

    if (response.data && response.data.success) {
      // 检查是否有消息提示（可能是配置禁用了校验）
      if (response.data.message && response.data.message.includes('数据完整性校验已在配置中禁用')) {
        integrityStatus.value = {
          status: 'disabled',
          difference: 0,
          lastCheck: response.data.timestamp
        }
      } else {
        integrityStatus.value = {
          status: response.data.difference === 0 ? 'consistent' : 'inconsistent',
          difference: response.data.difference || 0,
          lastCheck: response.data.timestamp
        }
      }
    }
  } catch (error) {
    console.error('获取完整性状态失败:', error)
    // 出错时保持当前状态不变
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
  // 读取侧边栏设置，默认显示
  const showSidebar = localStorage.getItem('showSidebar') !== 'false'
  // 如果设置为不显示侧边栏，则自动收起
  if (!showSidebar) {
    isCollapsed.value = true
  } else {
    // 否则使用上次保存的状态
    isCollapsed.value = localStorage.getItem('sidebarCollapsed') === 'true'
  }

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

  // 添加侧边栏设置变更事件监听
  window.addEventListener('sidebar-setting-changed', handleSidebarSettingChange)
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

// 处理侧边栏设置变更事件
const handleSidebarSettingChange = (event) => {
  console.log('侧边栏收到设置变更事件', event.detail)
  if (event.detail && typeof event.detail.showSidebar === 'boolean') {
    // 如果设置为不显示侧边栏，则自动收起
    if (!event.detail.showSidebar) {
      isCollapsed.value = true
    }
  }
}

// 组件卸载时移除事件监听器和清除定时器
onUnmounted(() => {
  window.removeEventListener('login-status-changed', handleLoginStatusChange)
  window.removeEventListener('sidebar-setting-changed', handleSidebarSettingChange)

  // 清除定时器
  if (healthCheckTimer.value) {
    clearInterval(healthCheckTimer.value)
    healthCheckTimer.value = null
  }
})
</script>
