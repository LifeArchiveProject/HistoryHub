/**
 * 隐私模式管理工具
 * 集中管理隐私模式状态，提供全局API
 */

// 隐私模式事件名称
const PRIVACY_MODE_EVENT = 'privacy-mode-changed'

/**
 * 检查隐私模式是否启用
 * @returns {boolean} 隐私模式是否启用
 */
export const isPrivacyModeEnabled = () => {
  return localStorage.getItem('privacyMode') === 'true'
}

/**
 * 启用隐私模式
 */
export const enablePrivacyMode = () => {
  localStorage.setItem('privacyMode', 'true')
  
  // 触发隐私模式变更事件
  dispatchPrivacyModeChanged(true)
  
  console.log('隐私模式已启用')
}

/**
 * 禁用隐私模式
 */
export const disablePrivacyMode = () => {
  localStorage.setItem('privacyMode', 'false')
  
  // 触发隐私模式变更事件
  dispatchPrivacyModeChanged(false)
  
  console.log('隐私模式已禁用')
}

/**
 * 切换隐私模式
 * @returns {boolean} 切换后的状态
 */
export const togglePrivacyMode = () => {
  const currentState = isPrivacyModeEnabled()
  const newState = !currentState
  
  if (newState) {
    enablePrivacyMode()
  } else {
    disablePrivacyMode()
  }
  
  return newState
}

/**
 * 分发隐私模式变更事件
 * @param {boolean} enabled 隐私模式是否启用
 */
export const dispatchPrivacyModeChanged = (enabled) => {
  window.dispatchEvent(new CustomEvent(PRIVACY_MODE_EVENT, {
    detail: { enabled }
  }))
}

/**
 * 添加隐私模式变更监听器
 * @param {Function} callback 回调函数
 */
export const addPrivacyModeListener = (callback) => {
  window.addEventListener(PRIVACY_MODE_EVENT, (event) => {
    if (event.detail && typeof event.detail.enabled === 'boolean') {
      callback(event.detail.enabled)
    }
  })
}

export default {
  isEnabled: isPrivacyModeEnabled,
  enable: enablePrivacyMode,
  disable: disablePrivacyMode,
  toggle: togglePrivacyMode,
  addListener: addPrivacyModeListener
} 