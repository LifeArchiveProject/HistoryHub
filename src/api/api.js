import axios from 'axios'

// 你的服务器地址
const getBaseUrl = () => {
  return localStorage.getItem('baseUrl') || 'http://localhost:8899'
}

const BASE_URL = getBaseUrl()

// 服务器地址列表
const SERVER_URLS = [
  'http://127.0.0.1:8899',
  'http://localhost:8899',
  'http://0.0.0.0:8899'
]

// 尝试连接多个服务器地址，返回第一个可用的
export const tryConnectServers = async () => {
  // 如果已经存储了服务器地址，先尝试这个地址
  const savedUrl = localStorage.getItem('baseUrl')
  if (savedUrl) {
    try {
      const response = await axios.get(`${savedUrl}/health`, { timeout: 3000 })
      if (response.data && response.data.status === 'running') {
        // 更新 axios 实例的 baseURL
        updateInstanceBaseUrl(savedUrl)
        return { success: true, url: savedUrl }
      }
    } catch (error) {
      console.warn(`尝试连接已保存的服务器 ${savedUrl} 失败:`, error.message)
    }
  }

  // 尝试所有预定义服务器
  for (const url of SERVER_URLS) {
    try {
      console.log(`尝试连接服务器: ${url}`)
      const response = await axios.get(`${url}/health`, { timeout: 3000 })
      if (response.data && response.data.status === 'running') {
        // 保存可用的服务器地址
        localStorage.setItem('baseUrl', url)
        // 更新 axios 实例的 baseURL
        updateInstanceBaseUrl(url)
        return { success: true, url }
      }
    } catch (error) {
      console.warn(`尝试连接服务器 ${url} 失败:`, error.message)
    }
  }

  return { success: false, url: null }
}

// 设置服务器地址
export const setBaseUrl = (url) => {
  localStorage.setItem('baseUrl', url)
  // 更新 axios 实例的 baseURL
  updateInstanceBaseUrl(url)
  // 触发API BASE URL更新事件，供其他API模块使用
  try {
    const event = new CustomEvent('api-baseurl-updated', { detail: { url } })
    window.dispatchEvent(event)
    console.log('已触发API BaseURL更新事件:', url)
  } catch (error) {
    console.error('触发API BaseURL更新事件失败:', error)
  }
  window.location.reload() // 刷新页面以应用新的baseUrl
}

// 获取当前服务器地址
export const getCurrentBaseUrl = () => {
  return getBaseUrl()
}

// 创建一个 axios 实例
const instance = axios.create({
  baseURL: BASE_URL,
})

// 更新 axios 实例的 baseURL
export const updateInstanceBaseUrl = (newBaseUrl) => {
  instance.defaults.baseURL = newBaseUrl
}

// 历史记录相关接口
export const getBiliHistory2024 = (page, size, sortOrder, tagName, mainCategory, dateRange, useLocalImages = false, business = '') => {
  return instance.get(`/history/all`, {
    params: {
      page,
      size,
      sort_order: sortOrder,
      tag_name: tagName,
      main_category: mainCategory,
      date_range: dateRange,
      use_local_images: useLocalImages,
      business: business,
    },
  })
}

export const searchBiliHistory2024 = (search, searchType = 'all', page = 1, size = 30, sortOrder = 0, sortBy = 'relevance') => {
  return instance.get(`/history/search`, {
    params: {
      page,
      size,
      search,
      search_type: searchType,
      sort_order: sortOrder,
      sort_by: sortBy
    },
  })
}

// 获取可用年份列表
export const getAvailableYears = () => {
  return instance.get(`/history/available-years`)
}

// 分类相关接口
export const getVideoCategories = () => {
  return instance.get(`/categories/categories`) // 使用新的分类接口
}

export const getMainCategories = () => {
  return instance.get(`/categories/main-categories`)
}

// 标题分析相关接口
export const getTitleAnalytics = (year, useCache = true) => {
  return instance.get(`/title/`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取观看时间分布分析
export const getViewingAnalytics = async (year, useCache = true) => {
  return instance.get(`/viewing/`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取观看行为数据分析
export const getViewingBehavior = async (year, useCache = false) => {
  return instance.get(`/viewing/viewing/`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取每年每天的观看数合集
export const getYearlyAnalysis = async (year) => {
  return instance.post(`/analysis/analyze`, null, {
    params: {
      year
    }
  })
}

// 实时更新历史记录
export const updateBiliHistoryRealtime = () => {
  return instance.get(`/fetch/bili-history-realtime`).then(response => {
    // 检查响应格式
    if (!response.data) {
      throw new Error('响应数据格式错误')
    }

    // 如果返回未找到本地历史记录错误，则调用完整获取接口
    if (response.data.status === 'error' && response.data.message === '未找到本地历史记录') {
      return getBiliHistory()
    }

    return response
  }).catch(error => {
    console.error('API 请求错误:', error)
    // 重新抛出错误，让调用者处理
    throw error
  })
}

// 获取完整历史记录
export const getBiliHistory = () => {
  return instance.get('/fetch/bili-history').then(async response => {
    // 检查响应格式
    if (!response.data) {
      throw new Error('响应数据格式错误')
    }

    // 如果获取历史记录成功，调用导入SQLite接口
    if (response.data.status === 'success') {
      try {
        await importSqliteData()
        // 1秒后刷新页面，让用户看到成功提示
        setTimeout(() => {
          window.location.reload()
        }, 1000)
      } catch (error) {
        console.error('导入SQLite失败:', error)
        // 即使导入失败也返回历史记录的响应
      }
    }

    return response
  }).catch(error => {
    console.error('获取历史记录失败:', error)
    throw error
  })
}

// 获取每日视频统计
export const getDailyStats = async (date, year) => {
  return instance.get(`/daily/daily-count`, {
    params: {
      date,
      year
    }
  })
}

// 导入SQLite数据
export const importSqliteData = () => {
  return instance.post(`/importSqlite/import_data_sqlite`)
}

// 导出相关接口
// 导出历史记录到Excel
export const exportHistory = (year) => {
  return instance.post('/export/export_history', null, {
    params: {
      year
    }
  })
}

// 下载Excel文件
export const downloadExcelFile = (year) => {
  return instance.get(`/export/download_excel/${year}`, {
    responseType: 'blob',
    headers: {
      'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }
  }).then(response => {
    // 创建blob链接并下载
    const blob = new Blob([response.data], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `bilibili_history_${year}.xlsx`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    return response
  })
}

// 下载SQLite数据库
export const downloadDatabase = () => {
  return instance.get('/export/download_db', {
    responseType: 'blob',
    headers: {
      'Accept': 'application/x-sqlite3'
    }
  }).then(response => {
    // 创建blob链接并下载
    const blob = new Blob([response.data], {
      type: 'application/x-sqlite3'
    })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'bilibili_history.db')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    return response
  })
}

// 登录相关接口
// 生成登录二维码
export const generateLoginQRCode = () => {
  return instance.get('/login/qrcode/generate')
}

// 获取二维码图片URL
export const getQRCodeImageURL = () => {
  return `${BASE_URL}/login/qrcode/image`
}

// 轮询二维码状态
export const pollQRCodeStatus = (qrcodeKey) => {
  return instance.get('/login/qrcode/poll', {
    params: {
      qrcode_key: qrcodeKey
    }
  })
}

// 退出登录
export const logout = () => {
  return instance.post('/login/logout')
}

// 获取登录状态
export const getLoginStatus = () => {
  return instance.get('/login/check')
}

// 获取视频摘要
export const getVideoSummary = (bvid, cid, upMid, forceRefresh = false) => {
  return instance.get('/summary/get_summary', {
    params: {
      bvid,
      cid,
      up_mid: upMid,
      force_refresh: forceRefresh
    }
  })
}

// 获取摘要配置
export const getSummaryConfig = () => {
  return instance.get('/summary/config')
}

// 更新摘要配置
export const updateSummaryConfig = (config) => {
  return instance.post('/summary/config', config)
}

// 批量删除历史记录
export const batchDeleteHistory = (items) => {
  return instance.delete('/delete/batch-delete', {
    data: items  // 直接发送数组，不要包装在 items 对象中
  })
}

// 数据库管理相关接口
// 重置数据库
export const resetDatabase = () => {
  return instance.post('/history/reset-database')
}

// 备注相关接口
// 更新视频备注
export const updateVideoRemark = (bvid, viewAt, remark) => {
  return instance.post('/history/update-remark', {
    bvid,
    view_at: viewAt,
    remark
  })
}

// 批量获取视频备注
export const batchGetRemarks = (records) => {
  return instance.post('/history/batch-remarks', {
    items: records
  })
}

// 获取所有备注记录
export const getAllRemarks = (page = 1, size = 10, sortOrder = 0) => {
  return instance.get('/history/remarks', {
    params: {
      page,
      size,
      sort_order: sortOrder
    }
  })
}

// 获取SQLite版本
export const getSqliteVersion = () => {
  return instance.get('/history/sqlite-version')
}

// 图片管理相关接口
// 获取图片下载状态
export const getImagesStatus = () => {
  return instance.get('/images/status')
}

// 开始下载图片
export const startImagesDownload = (year = null) => {
  return instance.post('/images/start', null, {
    params: {
      year
    }
  })
}

// 停止下载图片
export const stopImagesDownload = () => {
  return instance.post('/images/stop')
}

// 清空图片
export const clearImages = () => {
  return instance.post('/images/clear')
}

// 下载视频
export const downloadVideo = async (bvid, sessdata = null, onMessage, downloadCover = true, onlyAudio = false, cid = 0) => {
  console.log('调用下载API, bvid:', bvid)

  const response = await fetch(`${BASE_URL}/download/download_video`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: bvid,
      sessdata,
      download_cover: downloadCover,
      only_audio: onlyAudio,
      cid
    })
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || '下载请求失败')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { value, done } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })

    // 处理缓冲区中的完整行
    const lines = buffer.split('\n')
    buffer = lines.pop() // 保留最后一个不完整的行

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const content = line.substring(6).trim()
        if (content && content !== 'close') {
          onMessage(content)
        }
      }
    }
  }

  // 处理最后可能剩余的数据
  if (buffer) {
    if (buffer.startsWith('data: ')) {
      const content = buffer.substring(6).trim()
      if (content && content !== 'close') {
        onMessage(content)
      }
    }
  }
}

// 检查 FFmpeg 安装状态
export const checkFFmpeg = () => {
  return instance.get('/download/check_ffmpeg')
}

// 计划任务管理相关接口
export const getAllSchedulerTasks = (params = {}) => {
  console.log('调用getAllSchedulerTasks API:', { params })
  return instance.get('/scheduler/tasks', { params })
    .then(response => {
      console.log('getAllSchedulerTasks API响应:', response)
      return response
    })
    .catch(error => {
      console.error('getAllSchedulerTasks API错误:', error)
      throw error
    })
}

export const getSchedulerTaskDetail = (taskId, params = {}) => {
  return instance.get(`/scheduler/tasks`, {
    params: {
      task_id: taskId,
      include_subtasks: true,  // 默认包含子任务
      ...params
    }
  }).then(response => {
    return response;
  }).catch(error => {
    console.error('API - 获取任务详情出错:', error);
    throw error;
  });
}

export const createSchedulerTask = (taskData) => {
  return instance.post('/scheduler/tasks', taskData)
}

export const updateSchedulerTask = (taskId, taskData) => {
  return instance.put(`/scheduler/tasks/${taskId}`, taskData)
}

export const deleteSchedulerTask = (taskId) => {
  return instance.delete(`/scheduler/tasks/${taskId}`)
}

export const executeSchedulerTask = (taskId, options = {}) => {
  return instance.post(`/scheduler/tasks/${taskId}/execute`, options)
}

// 子任务管理接口
export const addSubTask = (taskId, subTaskData) => {
  console.log('调用addSubTask API:', { taskId, subTaskData })
  return instance.post(`/scheduler/tasks/${taskId}/subtasks`, subTaskData)
    .then(response => {
      console.log('addSubTask API响应:', response)
      return response
    })
    .catch(error => {
      console.error('addSubTask API错误:', error)
      throw error
    })
}

export const getSubTasks = (taskId) => {
  console.log('调用getSubTasks API:', { taskId })
  return instance.get(`/scheduler/tasks/${taskId}/subtasks`)
    .then(response => {
      console.log('getSubTasks API响应:', response)
      return response
    })
    .catch(error => {
      console.error('getSubTasks API错误:', error)
      throw error
    })
}

export const deleteSubTask = (taskId, subTaskId) => {
  return instance.delete(`/scheduler/tasks/${taskId}/subtasks/${subTaskId}`)
}

export const updateSubTaskSequence = (taskId, subTaskId, sequence) => {
  return instance.put(`/scheduler/tasks/${taskId}/subtasks/${subTaskId}/sequence`, { sequence })
}

// 获取任务历史记录
export const getTaskHistory = ({
  task_id = null,
  include_subtasks = true,
  status = null,
  start_date = null,
  end_date = null,
  page = 1,
  page_size = 20
}) => {
  return instance.get(`/scheduler/tasks/history`, {
    params: {
      task_id,
      include_subtasks,
      status,
      start_date,
      end_date,
      page,
      page_size
    }
  })
}

// 系统接口
export const getAvailableEndpoints = () => {
  return instance.get('/scheduler/available-endpoints')
}

// 启用/禁用任务
export const setTaskEnabled = (taskId, enabled) => {
  return instance.post(`/scheduler/tasks/${taskId}/enable`, {
    enabled
  })
}

// 邮件配置相关接口
// 获取邮件配置
export const getEmailConfig = () => {
  return instance.get('/config/email-config')
    .then(response => {
      console.log('邮件配置API响应成功:', response)
      return response
    })
    .catch(error => {
      console.error('邮件配置API错误:', error)
      throw error
    })
}

// 更新邮件配置
export const updateEmailConfig = (config) => {
  return instance.post('/config/email-config', config)
    .then(response => {
      console.log('更新邮件配置API响应成功:', response)
      return response
    })
    .catch(error => {
      console.error('更新邮件配置API错误:', error)
      throw error
    })
}

// 测试邮件配置
export const testEmailConfig = (testData) => {
  return instance.post('/config/test-email', testData)
    .then(response => {
      console.log('测试邮件API响应成功:', response)
      return response
    })
    .catch(error => {
      console.error('测试邮件API错误:', error)
      throw error
    })
}

// 音频转文字相关接口
export const checkAudioToTextEnvironment = () => {
  return instance.get('/audio_to_text/check_environment')
}

// 检查系统资源
export const checkSystemResources = () => {
  return instance.get('/audio_to_text/resource_check')
}

// 获取可用的 Whisper 模型列表
export const getWhisperModels = () => {
  return instance.get('/audio_to_text/models')
}

// 查找音频文件路径
export const findAudioPath = (cid) => {
  return instance.get('/audio_to_text/find_audio', {
    params: { cid }
  })
}

// 检查语音转文字文件是否存在
export const checkSttFile = (cid) => {
  return instance.get('/audio_to_text/check_stt_file', {
    params: { cid }
  })
}

// 转录音频文件
export const transcribeAudio = (params) => {
  return instance.post('/audio_to_text/transcribe', params)
}

// 根据CID生成视频摘要
export const summarizeByCid = (cid) => {
  return instance.post('/summary/summarize_by_cid', {
    cid
  })
}

// 检查本地摘要文件
export const checkLocalSummary = (cid, includeContent = true) => {
  return instance.get(`/summary/check_local_summary/${cid}`, {
    params: {
      include_content: includeContent
    }
  })
}

// 下载指定的Whisper模型
export const downloadWhisperModel = (modelSize) => {
  return instance.post('/audio_to_text/download_model', null, {
    params: {
      model_size: modelSize
    }
  })
}

// 删除指定的Whisper模型
export const deleteWhisperModel = (modelSize) => {
  return instance.delete('/audio_to_text/models', {
    data: {
      model_size: modelSize
    }
  })
}

// DeepSeek相关接口
export const checkDeepSeekApiKey = () => {
  return instance.get('/deepseek/check_api_key')
}

export const setDeepSeekApiKey = (apiKey) => {
  return instance.post('/deepseek/set_api_key', {
    api_key: apiKey
  })
}

export const getDeepSeekBalance = () => {
  return instance.get('/deepseek/balance')
}

// 检查视频是否已下载
export const checkVideoDownload = (cids) => {
  return instance.get(`/download/check_video_download`, {
    params: {
      cids: Array.isArray(cids) ? cids.join(',') : cids
    }
  })
}

// 获取已下载视频列表
export const getDownloadedVideos = (searchTerm = '', page = 1, limit = 20) => {
  return instance.get(`/download/list_downloaded_videos`, {
    params: {
      search_term: searchTerm,
      page,
      limit
    }
  })
}

// 删除已下载的视频
export const deleteDownloadedVideo = (cid, deleteDirectory = false, directory = null) => {
  return instance.delete(`/download/delete_downloaded_video`, {
    params: {
      cid,
      delete_directory: deleteDirectory,
      directory: directory
    }
  })
}

// 获取评论列表
export const getComments = (uid, page = 1, pageSize = 20, commentType = 'all', keyword = '', typeFilter = '') => {
  // 确保 typeFilter 为有效整数或不传递
  const params = {
    page,
    page_size: pageSize,
    comment_type: commentType,
    keyword
  }
  
  // 只有当 typeFilter 有值且不为 '0' 时才添加到参数中
  if (typeFilter && typeFilter !== '0') {
    params.type_filter = parseInt(typeFilter)
  }
  
  return instance.get(`/comment/query/${uid}`, { params })
}

// 导入通知组件
import 'vant/es/notify/style'

// 服务器健康检查
export const checkServerHealth = () => {
  return instance.get('/health')
}

/**
 * 获取视频流地址
 * @param {string} file_path 视频文件路径
 * @returns {string} 视频流URL
 */
export const getVideoStream = (file_path) => {
  if (!file_path) return ''
  const baseUrl = instance.defaults.baseURL
  return `${baseUrl}/download/stream_video?file_path=${encodeURIComponent(file_path)}&t=${Date.now()}`
}

/**
 * 获取弹幕文件内容
 * @param {string} cid 弹幕ID
 * @param {string} file_path 弹幕文件路径
 * @returns {Promise<Object>} 响应对象
 */
export const getDanmakuFile = async (cid = '', file_path = '') => {
  try {
    const params = {};
    if (cid) params.cid = cid;
    if (file_path) params.file_path = file_path;
    
    const response = await instance.get(`/download/stream_danmaku`, { 
      params,
      responseType: 'text' // 获取纯文本格式的弹幕文件
    });
    return response;
  } catch (error) {
    console.error('获取弹幕文件失败:', error);
    throw error;
  }
}

// 数据同步相关接口
/**
 * 数据同步API
 * @param {string} db_path - 数据库文件路径
 * @param {string} json_path - JSON文件根目录
 * @param {boolean} async_mode - 是否异步执行
 * @returns {Promise} - API响应
 */
export const syncData = (db_path = 'output/bilibili_history.db', json_path = 'output/history_by_date', async_mode = false) => {
  return instance.post('/data_sync/sync', {
    db_path,
    json_path,
    async_mode
  })
}

/**
 * 获取最新同步结果API
 * @returns {Promise} - API响应
 */
export const getSyncResult = () => {
  return instance.get('/data_sync/sync/result')
}

/**
 * 检查数据完整性API
 * @param {string} db_path - 数据库文件路径
 * @param {string} json_path - JSON文件根目录
 * @param {boolean} async_mode - 是否异步执行
 * @returns {Promise} - API响应
 */
export const checkDataIntegrity = (db_path = 'output/bilibili_history.db', json_path = 'output/history_by_date', async_mode = false) => {
  return instance.post('/data_sync/check', {
    db_path,
    json_path,
    async_mode
  })
}

/**
 * 获取数据完整性报告API
 * @returns {Promise} - API响应
 */
export const getIntegrityReport = () => {
  return instance.get('/data_sync/report')
}
