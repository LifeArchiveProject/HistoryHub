/**
 * 在系统默认浏览器中打开URL
 * 在Tauri环境中使用shell API，在浏览器环境中使用window.open
 * @param {string} url - 要打开的URL
 */
export async function openInBrowser(url) {
  // 检测Tauri环境
  const hasTauriInvoke = window && typeof window.__TAURI_INVOKE__ === 'function'
  const hasTauriGlobal = window && window.__TAURI__
  const userAgent = navigator.userAgent
  const isTauriUserAgent = userAgent.includes('Tauri')
  const isLocalhost = window.location.hostname === 'localhost'
  const isTauriPort = window.location.port === '1420' // Tauri默认端口
  const hasFileProtocol = window.location.protocol === 'tauri:'

  // 检测是否应该尝试Tauri API
  const shouldTryTauri = hasTauriInvoke || hasTauriGlobal || isTauriUserAgent || isTauriPort || hasFileProtocol

  if (shouldTryTauri) {
    // 方法1: 直接使用__TAURI_INVOKE__
    if (hasTauriInvoke) {
      try {
        await window.__TAURI_INVOKE__('plugin:shell|open', { path: url })
        return
      } catch (error) {
        console.warn('Tauri __TAURI_INVOKE__ 失败:', error.message)
      }
    }

    // 方法2: 尝试导入@tauri-apps/api/core
    try {
      const { invoke } = await import('@tauri-apps/api/core')
      if (typeof invoke === 'function') {
        await invoke('plugin:shell|open', { path: url })
        return
      }
    } catch (error) {
      console.warn('Tauri core API 失败:', error.message)
    }

    // 方法3: 尝试导入@tauri-apps/plugin-shell
    try {
      const { open } = await import('@tauri-apps/plugin-shell')
      if (typeof open === 'function') {
        await open(url)
        return
      }
    } catch (error) {
      console.warn('Tauri shell plugin 失败:', error.message)
    }
  }

  // 回退到window.open
  window.open(url, '_blank')
}
