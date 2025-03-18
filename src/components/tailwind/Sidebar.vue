<!-- 侧边栏组件 -->
<template>
  <div class="flex h-screen">
    <!-- 左侧导航栏 -->
    <div :class="[
      'transition-all duration-300 ease-in-out bg-white/10 backdrop-blur-lg border-r border-gray-200/50 hidden sm:block',
      isCollapsed ? 'w-12' : 'w-48'
    ]">
      <!-- 侧边栏内容 -->
      <div class="h-full flex flex-col">
        <!-- 顶部 Logo -->
        <div class="p-4 border-b border-gray-200/50">
          <router-link to="/" class="flex items-center space-x-3" :class="{ 'justify-center': isCollapsed }">
            <svg class="h-8 w-8 text-gray-900 flex-shrink-0" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
              <path fill="currentColor" d="M306.005333 117.632L444.330667 256h135.296l138.368-138.325333a42.666667 42.666667 0 0 1 60.373333 60.373333L700.330667 256H789.333333A149.333333 149.333333 0 0 1 938.666667 405.333333v341.333334a149.333333 149.333333 0 0 1-149.333334 149.333333h-554.666666A149.333333 149.333333 0 0 1 85.333333 746.666667v-341.333334A149.333333 149.333333 0 0 1 234.666667 256h88.96L245.632 177.962667a42.666667 42.666667 0 0 1 60.373333-60.373334zM789.333333 341.333333h-554.666666a64 64 0 0 0-63.701334 57.856L170.666667 405.333333v341.333334a64 64 0 0 0 57.856 63.701333L234.666667 810.666667h554.666666a64 64 0 0 0 63.701334-57.856L853.333333 746.666667v-341.333334A64 64 0 0 0 789.333333 341.333333zM341.333333 469.333333a42.666667 42.666667 0 0 1 42.666667 42.666667v85.333333a42.666667 42.666667 0 0 1-85.333333 0v-85.333333a42.666667 42.666667 0 0 1 42.666666-42.666667z m341.333334 0a42.666667 42.666667 0 0 1 42.666666 42.666667v85.333333a42.666667 42.666667 0 0 1-85.333333 0v-85.333333a42.666667 42.666667 0 0 1 42.666667-42.666667z" />
            </svg>
            <span v-show="!isCollapsed" class="text-lg font-semibold bg-gradient-to-r from-[#fb7299] to-[#fc9b7a] bg-clip-text text-transparent whitespace-nowrap">B站历史记录</span>
          </router-link>
        </div>

        <!-- 导航菜单 -->
        <nav class="flex-1 overflow-y-auto py-4 space-y-2" :class="{ 'px-4': !isCollapsed }">
          <!-- 历史记录 -->
          <button
            @click="changeContent('history')"
            :title="isCollapsed ? '历史记录' : ''"
            class="w-full flex items-center py-2 text-gray-700 transition-all duration-300 ease-in-out"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'history' && !showRemarks },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-6 h-6 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">历史记录</span>
          </button>

          <!-- 我的备注 -->
          <button
            @click="changeContent('remarks')"
            :title="isCollapsed ? '我的备注' : ''"
            class="w-full flex items-center py-2 text-gray-700 transition-all duration-300 ease-in-out"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'remarks' || (currentContent === 'history' && showRemarks) },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-6 h-6 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">我的备注</span>
          </button>

          <!-- 年度总结 -->
          <router-link
            to="/analytics"
            :title="isCollapsed ? '年度总结' : ''"
            class="flex items-center py-2 text-gray-700 transition-all duration-300 ease-in-out"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'analytics' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-6 h-6 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">年度总结</span>
          </router-link>

          <!-- 图片管理 -->
          <router-link
            to="/images"
            :title="isCollapsed ? '图片管理' : ''"
            class="flex items-center py-2 text-gray-700 transition-all duration-300 ease-in-out"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'images' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-6 h-6 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">图片管理</span>
          </router-link>

          <!-- 计划任务 -->
          <router-link
            to="/scheduler"
            :title="isCollapsed ? '计划任务' : ''"
            class="flex items-center py-2 text-gray-700 transition-all duration-300 ease-in-out"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'scheduler' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
            @click="currentContent = 'scheduler'"
          >
            <svg class="w-6 h-6 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">计划任务</span>
          </router-link>

          <!-- 视频下载 -->
          <router-link
            to="/downloads"
            :title="isCollapsed ? '视频下载' : ''"
            class="flex items-center py-2 text-gray-700 transition-all duration-300 ease-in-out"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'downloads' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
            @click="currentContent = 'downloads'"
          >
            <svg class="w-6 h-6 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">视频下载</span>
          </router-link>

          <!-- 设置 -->
          <button
            @click="changeContent('settings')"
            :title="isCollapsed ? '设置' : ''"
            class="w-full flex items-center py-2 text-gray-700 transition-all duration-300 ease-in-out"
            :class="[
              { 'bg-[#fb7299]/10 text-[#fb7299]': currentContent === 'settings' },
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg class="w-6 h-6 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">设置</span>
          </button>


          <!-- 登录状态显示 -->
          <div
            @click="handleLoginClick"
            class="w-full flex items-center py-2 text-gray-700 transition-all duration-300 ease-in-out cursor-pointer hover:text-[#fb7299]"
            :class="[
              { 'justify-center': isCollapsed },
              isCollapsed ? 'px-2' : 'px-3 rounded-lg'
            ]"
          >
            <svg
              class="w-6 h-6 flex-shrink-0"
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
        <div class="p-4 border-t border-gray-200/50">
          <!-- 导入SQLite数据 -->
          <button
            @click="importToSqlite"
            :disabled="isImporting"
            :title="isCollapsed ? (isImporting ? '导入中...' : '导入SQLite') : ''"
            class="w-full flex items-center px-2 py-2 text-gray-700 hover:text-[#fb7299] rounded-lg transition-colors duration-200"
            :class="[
              { 'justify-center': isCollapsed },
              { 'opacity-50 cursor-not-allowed': isImporting }
            ]"
          >
            <svg class="w-6 h-6 flex-shrink-0" :class="{ 'mr-3': !isCollapsed }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            <span v-show="!isCollapsed" class="truncate">{{ isImporting ? '导入中...' : '导入SQLite' }}</span>
          </button>

          <!-- SQLite版本显示 -->
          <div v-if="!isCollapsed" class="mt-2 text-xs space-y-1 px-2">
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
            class="mt-4 w-full flex items-center justify-center px-2 py-2 text-gray-700 hover:text-[#fb7299] transition-colors duration-200"
          >
            <svg
              class="w-6 h-6 flex-shrink-0 transform transition-transform duration-300"
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
import { importSqliteData, getLoginStatus, logout, getSqliteVersion } from '../../api/api'
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
  } else if (path === '/images') {
    return 'images'
  } else if (path === '/analytics') {
    return 'analytics'
  } else if (path === '/scheduler') {
    return 'scheduler'
  } else if (path === '/downloads') {
    return 'downloads'
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
    } else if (path === '/images') {
      currentContent.value = 'images'
    } else if (path === '/analytics') {
      currentContent.value = 'analytics'
    } else if (path === '/scheduler') {
      currentContent.value = 'scheduler'
    } else if (path === '/downloads') {
      currentContent.value = 'downloads'
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

// 导入SQLite数据
const isImporting = ref(false)
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
const importToSqlite = async () => {
  if (isImporting.value) return

  try {
    isImporting.value = true
    const response = await importSqliteData()
    if (response.data.status === 'success') {
      showNotify({
        type: 'success',
        message: response.data.message
      })
      // 导入成功后等待1秒再刷新页面，让用户看到成功提示
      setTimeout(() => {
        window.location.reload()
      }, 1000)
    } else {
      throw new Error(response.data.message)
    }
  } catch (error) {
    showNotify({
      type: 'danger',
      message: `导入失败：${error.message}`
    })
  } finally {
    isImporting.value = false
  }
}

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

onMounted(async () => {
  checkLoginStatus()
  await fetchSqliteVersion()
  
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

// 组件卸载时移除事件监听器
onUnmounted(() => {
  window.removeEventListener('login-status-changed', handleLoginStatusChange)
})
</script>
