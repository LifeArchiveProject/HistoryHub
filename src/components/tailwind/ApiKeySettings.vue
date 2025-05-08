<template>
  <div class="bg-white rounded-lg border border-gray-200 divide-y divide-gray-200">
    <!-- 修改API密钥 -->
    <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
      <div class="flex items-center justify-between mb-3">
        <div>
          <h3 class="text-base font-medium text-gray-900">修改API密钥</h3>
          <p class="text-sm text-gray-500">验证当前密钥后更新为新密钥</p>
        </div>
      </div>

      <div class="space-y-4">
        <div class="flex items-center space-x-2">
          <input
            v-model="currentApiKey"
            type="password"
            class="flex-1 block rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
            placeholder="请输入当前API密钥"
          />
        </div>

        <div class="flex items-center space-x-2">
          <input
            v-model="newApiKey"
            type="password"
            class="flex-1 block rounded-md border-gray-300 shadow-sm focus:border-[#fb7299] focus:ring-[#fb7299] sm:text-sm"
            placeholder="请输入新API密钥"
          />
        </div>

        <div class="flex space-x-2">
          <button
            @click="verifyAndUpdate"
            :disabled="updating"
            class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md shadow-sm text-white bg-[#fb7299] hover:bg-[#e66a8a] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#fb7299]"
          >
            <svg v-if="updating" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            验证并更新
          </button>
          <button
            @click="testApiKey"
            :disabled="testing"
            class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#fb7299]"
          >
            <svg v-if="testing" class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m-8 6H4m0 0l4 4m-4-4l4-4" />
            </svg>
            测试连接
          </button>
        </div>
      </div>
    </div>

    <!-- 安全提示 -->
    <div class="p-4 transition-colors duration-200 hover:bg-gray-50">
      <div class="flex items-center justify-between mb-2">
        <div>
          <h3 class="text-base font-medium text-gray-900">安全提示</h3>
        </div>
      </div>
      <div class="text-sm text-gray-500 space-y-2">
        <p>• API密钥用于验证API请求，防止未授权访问</p>
        <p>• 请使用复杂的随机字符串作为API密钥</p>
        <p>• 为了安全，API密钥不会在前端显示，请妥善保存</p>
        <p>• 如需查看当前API密钥，请查看配置文件 config/config.yaml</p>
        <p>• 定期更换API密钥以提高安全性</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { showNotify, showDialog } from 'vant'
import { checkApiKey, updateApiKey, verifyAndUpdateApiKey } from '@/api/api'

export default {
  name: 'ApiKeySettings',
  emits: ['api-key-updated'],
  setup(props, { emit }) {
    const apiKey = ref(localStorage.getItem('apiKey') || '')
    const loading = ref(false)
    const testing = ref(false)
    const DEFAULT_API_KEY = 'your-secret-api-key-change-this'

    // 验证并更新API密钥相关状态
    const currentApiKey = ref('')
    const newApiKey = ref('')
    const updating = ref(false)

    // 检查是否使用默认API密钥
    const checkDefaultApiKey = async () => {
      try {
        // 检查API密钥
        const response = await checkApiKey()

        // 如果API安全验证未启用，不需要进一步处理
        if (response.data && response.data.message === "API安全验证未启用") {
          return
        }

        // 获取后端配置的API密钥状态
        const isBackendKeyDefault = response.data && response.data.message &&
                                   response.data.message.includes(DEFAULT_API_KEY)

        // 如果后端使用默认API密钥，提示用户修改
        // 注意：在App.vue中已经处理了默认密钥的弹窗显示，这里不再重复显示
        // 只在设置页面中主动点击测试API密钥时才显示弹窗
        if ((isBackendKeyDefault || apiKey.value === DEFAULT_API_KEY) &&
            document.activeElement && document.activeElement.textContent &&
            document.activeElement.textContent.includes('测试连接')) {
          showDialog({
            title: '安全警告',
            message: '检测到默认的API密钥，这可能会导致安全风险。请设置自定义的复杂密钥。',
            confirmButtonText: '立即设置',
            confirmButtonColor: '#fb7299',
            showCancelButton: false
          }).then(action => {
            // 由于没有取消按钮，action始终为confirm
            // 弹出输入框让用户输入新密钥
            showDialog({
              title: '设置API密钥',
              message: '请输入新的API密钥，建议使用复杂的随机字符串。\n注意：为了安全，此密钥将不会在前端显示，请妥善保存。后续只能在配置文件中查看。',
              showCancelButton: false,
              confirmButtonText: '确认',
              confirmButtonColor: '#fb7299',
              showInput: true,
              inputType: 'password',
              inputPlaceholder: '请输入新的API密钥'
            }).then(({ value, action }) => {
              if (value) { // 由于没有取消按钮，action始终为confirm
                // 使用用户输入的密钥
                apiKey.value = value
                saveApiKey()
              }
            })
          })
        }
        // 如果前端API密钥与后端不一致
        else if (response.data && !response.data.is_valid) {
          showDialog({
            title: 'API密钥不匹配',
            message: '前端API密钥与后端不一致。请使用正确的API密钥。',
            confirmButtonText: '确定',
            confirmButtonColor: '#fb7299'
          })
        }
      } catch (error) {
        console.error('检查API密钥状态失败:', error)

        // 如果是401错误，说明API密钥无效
        if (error.response && error.response.status === 401) {
          showDialog({
            title: 'API密钥无效',
            message: '您的API密钥无效。请输入正确的API密钥。',
            confirmButtonText: '确定',
            confirmButtonColor: '#fb7299'
          })
        }
      }
    }

    // 生成随机API密钥
    const generateRandomApiKey = () => {
      const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:,.<>?'
      let result = ''
      for (let i = 0; i < 32; i++) {
        result += chars.charAt(Math.floor(Math.random() * chars.length))
      }
      return result
    }

    // 更新后端配置文件中的API密钥
    const updateBackendApiKey = async (newApiKey) => {
      try {
        // 发送请求更新API密钥
        const response = await updateApiKey(newApiKey)

        if (response.data && response.data.success) {
          showNotify({
            type: 'success',
            message: '后端API密钥已更新',
            duration: 2000
          })
          return true
        } else {
          showNotify({
            type: 'warning',
            message: '后端API密钥更新失败: ' + (response.data?.message || '未知错误'),
            duration: 3000
          })
          return false
        }
      } catch (error) {
        console.error('更新后端API密钥失败:', error)
        showNotify({
          type: 'danger',
          message: '更新后端API密钥失败: ' + (error.response?.data?.message || error.message),
          duration: 3000
        })
        return false
      }
    }

    const saveApiKey = async () => {
      loading.value = true

      try {
        // 检查API密钥是否为空
        if (!apiKey.value.trim()) {
          showNotify({
            type: 'danger',
            message: 'API密钥不能为空',
            duration: 2000
          })
          return
        }

        // 尝试更新后端配置
        const backendUpdated = await updateBackendApiKey(apiKey.value)

        if (backendUpdated) {
          // 保存API密钥到本地存储
          localStorage.setItem('apiKey', apiKey.value)

          // 触发API密钥更新事件
          emit('api-key-updated', apiKey.value)

          // 显示成功通知
          showNotify({
            type: 'success',
            message: 'API密钥已保存',
            duration: 2000
          })

          // 刷新页面以应用新的API密钥
          setTimeout(() => {
            window.location.reload()
          }, 1000)
        } else {
          showNotify({
            type: 'danger',
            message: '更新API密钥失败',
            duration: 2000
          })
        }
      } catch (error) {
        console.error('保存API密钥失败:', error)
        showNotify({
          type: 'danger',
          message: '保存API密钥失败: ' + (error.response?.data?.message || error.message),
          duration: 2000
        })
      } finally {
        loading.value = false
      }
    }

    const testApiKey = async () => {
      testing.value = true

      try {
        // 检查API密钥是否为空
        if (!apiKey.value.trim()) {
          showNotify({
            type: 'danger',
            message: 'API密钥不能为空',
            duration: 2000
          })
          testing.value = false
          return
        }

        // 临时设置API密钥
        const originalApiKey = localStorage.getItem('apiKey')
        localStorage.setItem('apiKey', apiKey.value)

        // 测试API密钥
        const response = await checkApiKey()

        // 检查是否是默认API密钥
        const isDefaultKey = response.data && response.data.message &&
                            response.data.message.includes(DEFAULT_API_KEY)

        if (isDefaultKey) {
          // 在测试连接时显示安全警告弹窗
          showDialog({
            title: '安全警告',
            message: '检测到服务器正在使用默认的API密钥，这可能会导致安全风险。请立即设置自定义的复杂密钥。',
            confirmButtonText: '立即设置',
            confirmButtonColor: '#fb7299',
            showCancelButton: false
          }).then(async (action) => {
            // 由于没有取消按钮，action始终为confirm
            // 弹出输入框让用户输入新密钥
            showDialog({
              title: '设置API密钥',
              message: '请输入新的API密钥，建议使用复杂的随机字符串。\n注意：为了安全，此密钥将不会在前端显示，请妥善保存。后续只能在配置文件中查看。',
              showCancelButton: false,
              confirmButtonText: '确认',
              confirmButtonColor: '#fb7299',
              showInput: true,
              inputType: 'password',
              inputPlaceholder: '请输入新的API密钥'
            }).then(({ value, action }) => {
              if (value) { // 由于没有取消按钮，action始终为confirm
                // 使用用户输入的密钥
                apiKey.value = value
                saveApiKey()
              }
            })
          })
        }
        else if (response && response.data && response.data.is_valid) {
          showNotify({
            type: 'success',
            message: 'API密钥验证成功: ' + response.data.message,
            duration: 2000
          })
        } else {
          // 恢复原始API密钥
          localStorage.setItem('apiKey', originalApiKey || '')

          showNotify({
            type: 'warning',
            message: 'API密钥验证失败: ' + (response.data?.message || '未知错误'),
            duration: 2000
          })
        }
      } catch (error) {
        console.error('测试API密钥失败:', error)

        // 检查是否是401错误（未授权）
        if (error.response && error.response.status === 401) {
          showNotify({
            type: 'danger',
            message: 'API密钥无效',
            duration: 3000
          })
        } else {
          showNotify({
            type: 'danger',
            message: '测试API密钥失败: ' + (error.response?.data?.message || error.message),
            duration: 3000
          })
        }
      } finally {
        testing.value = false
      }
    }

    // 组件挂载时不再自动检查默认API密钥，避免与App.vue中的检查重复
    // 用户可以通过点击"测试连接"按钮主动触发检查
    onMounted(() => {
      // 不再自动检查，避免重复弹窗
      // 注释掉原有代码，保留以便理解
      // setTimeout(() => {
      //   checkDefaultApiKey()
      // }, 500)
    })

    // 验证当前密钥并更新为新密钥
    const verifyAndUpdate = async () => {
      // 检查输入是否为空
      if (!currentApiKey.value.trim()) {
        showNotify({
          type: 'warning',
          message: '当前API密钥不能为空',
          duration: 2000
        })
        return
      }

      if (!newApiKey.value.trim()) {
        showNotify({
          type: 'warning',
          message: '新API密钥不能为空',
          duration: 2000
        })
        return
      }

      // 如果当前密钥和新密钥相同，提示用户
      if (currentApiKey.value === newApiKey.value) {
        showNotify({
          type: 'warning',
          message: '新API密钥不能与当前API密钥相同',
          duration: 2000
        })
        return
      }

      updating.value = true

      try {
        // 调用验证并更新API密钥的接口
        const response = await verifyAndUpdateApiKey(currentApiKey.value, newApiKey.value)

        if (response.data && response.data.success) {
          // 更新本地存储的API密钥
          localStorage.setItem('apiKey', newApiKey.value)

          // 触发API密钥更新事件
          emit('api-key-updated', newApiKey.value)

          // 显示成功通知
          showNotify({
            type: 'success',
            message: '密钥验证成功并已更新',
            duration: 2000
          })

          // 清空输入框
          currentApiKey.value = ''
          newApiKey.value = ''

          // 刷新页面以应用新的API密钥
          setTimeout(() => {
            window.location.reload()
          }, 1000)
        } else {
          showNotify({
            type: 'danger',
            message: response.data?.message || '验证并更新API密钥失败',
            duration: 3000
          })
        }
      } catch (error) {
        console.error('验证并更新API密钥失败:', error)

        // 显示错误通知
        showNotify({
          type: 'danger',
          message: error.response?.data?.message || error.message || '验证并更新API密钥失败',
          duration: 3000
        })
      } finally {
        updating.value = false
      }
    }

    // 不再需要生成随机密钥的函数

    return {
      apiKey,
      loading,
      testing,
      saveApiKey,
      testApiKey,
      checkDefaultApiKey,
      // 验证并更新API密钥相关
      currentApiKey,
      newApiKey,
      updating,
      verifyAndUpdate
    }
  }
}
</script>
