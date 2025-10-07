import axios from 'axios'
// 导入通知组件
import 'vant/es/notify/style'

// 你的服务器地址
const DEFAULT_FALLBACK_URL = 'http://localhost:8899';
const VITE_CONFIGURED_DEFAULT_URL = import.meta.env.VITE_DEFAULT_BACKEND_URL || DEFAULT_FALLBACK_URL;
const getBaseUrl = () => {
  return localStorage.getItem('baseUrl') || VITE_CONFIGURED_DEFAULT_URL
}

const BASE_URL = getBaseUrl()

// 服务器地址列表
const SERVER_URLS = [
  'http://127.0.0.1:8899',
  'http://localhost:8899',
  'http://0.0.0.0:8899'
]

if (!SERVER_URLS.includes(VITE_CONFIGURED_DEFAULT_URL)) {
  SERVER_URLS.unshift(VITE_CONFIGURED_DEFAULT_URL)
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

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    return Promise.reject(error)
  }
)

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

export const searchBiliHistory2024 = (search, searchType = 'all', page = 1, size = 30, useLocalImages = false, useSessdata = true) => {
  return instance.get(`/history/search`, {
    params: {
      page,
      size,
      search,
      search_type: searchType,
      use_local_images: useLocalImages,
      use_sessdata: useSessdata
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

// 标题分析相关接口已拆分为以下独立接口：
// - getTitleKeywordAnalysis: 关键词分析
// - getTitleLengthAnalysis: 长度分析
// - getTitleSentimentAnalysis: 情感分析
// - getTitleTrendAnalysis: 趋势分析
// - getTitleInteractionAnalysis: 互动分析

// 获取标题关键词分析
export const getTitleKeywordAnalysis = (year, useCache = true) => {
  return instance.get(`/title/keyword-analysis`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取标题长度分析
export const getTitleLengthAnalysis = (year, useCache = true) => {
  return instance.get(`/title/length-analysis`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取标题情感分析
export const getTitleSentimentAnalysis = (year, useCache = true) => {
  return instance.get(`/title/sentiment-analysis`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取标题趋势分析
export const getTitleTrendAnalysis = (year, useCache = true) => {
  return instance.get(`/title/trend-analysis`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取标题互动分析
export const getTitleInteractionAnalysis = (year, useCache = true) => {
  return instance.get(`/title/interaction-analysis`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 观看时间分析相关接口已拆分为以下独立接口：
// - getViewingMonthlyStats: 月度统计分析
// - getViewingWeeklyStats: 周度统计分析
// - getViewingTimeSlots: 时段分析
// - getViewingContinuity: 观看连续性分析
// 更多维度接口将逐步添加...

// 获取月度观看统计分析
export const getViewingMonthlyStats = (year, useCache = true) => {
  return instance.get(`/viewing/monthly-stats`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取周度观看统计分析
export const getViewingWeeklyStats = (year, useCache = true) => {
  return instance.get(`/viewing/weekly-stats`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取时段观看分析
export const getViewingTimeSlots = (year, useCache = true) => {
  return instance.get(`/viewing/time-slots`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取观看连续性分析
export const getViewingContinuity = (year, useCache = true) => {
  return instance.get(`/viewing/continuity`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取重复观看分析
export const getViewingWatchCounts = (year, useCache = true) => {
  return instance.get(`/viewing/watch-counts`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取视频完成率分析
export const getViewingCompletionRates = (year, useCache = true) => {
  return instance.get(`/viewing/completion-rates`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取UP主完成率分析
export const getViewingAuthorCompletion = (year, useCache = true) => {
  return instance.get(`/viewing/author-completion`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取标签分析
export const getViewingTagAnalysis = (year, useCache = true) => {
  return instance.get(`/viewing/tag-analysis`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取视频时长分析
export const getViewingDurationAnalysis = (year, useCache = true) => {
  return instance.get(`/viewing/duration-analysis`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 原始的观看时间分析接口已删除，现在使用拆分后的独立接口

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

// 获取热门视频命中率分析
export const getPopularHitRate = async (year, useCache = true) => {
  return instance.get(`/popular/popular-hit-rate`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取热门预测能力分析
export const getPopularPredictionAbility = async (year, useCache = true) => {
  return instance.get(`/popular/popular-prediction-ability`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取UP主热门关联分析
export const getAuthorPopularAssociation = async (year, useCache = true) => {
  return instance.get(`/popular/author-popular-association`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取热门视频分区分布分析
export const getCategoryPopularDistribution = async (year, useCache = true) => {
  return instance.get(`/popular/category-popular-distribution`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取热门视频时长分布分析
export const getDurationPopularDistribution = async (year, useCache = true) => {
  return instance.get(`/popular/duration-popular-distribution`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}



// 实时更新历史记录
export const updateBiliHistoryRealtime = (syncDeleted = false) => {
  return instance.get(`/fetch/bili-history-realtime`, {
    params: {
      sync_deleted: syncDeleted
    }
  }).then(response => {
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
export const exportHistory = (options = {}) => {
  // 只传递非空参数
  const params = {}

  // 年份参数
  if (options.year !== undefined && options.year !== null) {
    params.year = options.year
  }

  // 月份参数
  if (options.month !== undefined && options.month !== null) {
    params.month = options.month
  }

  // 开始日期参数
  if (options.start_date) {
    params.start_date = options.start_date
  }

  // 结束日期参数
  if (options.end_date) {
    params.end_date = options.end_date
  }

  console.log('导出参数:', params)

  return instance.post('/export/export_history', null, {
    params
  })
}

// 下载Excel文件
export const downloadExcelFile = (filename) => {
  return instance.get(`/export/download_excel/${encodeURIComponent(filename)}`, {
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
    link.setAttribute('download', filename)
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

// 获取二维码图片（返回blob URL）
export const getQRCodeImageBlob = async () => {
  try {
    const response = await instance.get('/login/qrcode/image', {
      responseType: 'blob'
    })

    // 创建blob URL
    const blob = new Blob([response.data], {
      type: response.headers['content-type'] || 'image/png'
    })
    return URL.createObjectURL(blob)
  } catch (error) {
    console.error('获取二维码图片失败:', error)
    throw error
  }
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

// 删除B站历史记录
export const deleteBilibiliHistory = (kid, syncToBilibili = true) => {
  return instance.delete(`/bilibili/history/single`, {
    params: {
      kid
    },
    data: {
      sync_to_bilibili: syncToBilibili
    }
  })
}

// 批量删除B站历史记录
export const batchDeleteBilibiliHistory = (items) => {
  return instance.delete('/bilibili/history/batch', {
    data: {
      items
    }
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
export const startImagesDownload = (year = null, useSessdata = true) => {
  return instance.post('/images/start', null, {
    params: {
      year,
      use_sessdata: useSessdata
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
export const downloadVideo = async (bvid, sessdata = null, onMessage, downloadCover = true, onlyAudio = false, cid = 0, options = {}) => {
  console.log('调用下载API, bvid:', bvid, '高级选项:', options)

  const requestBody = {
    url: bvid,
    sessdata,
    download_cover: downloadCover,
    only_audio: onlyAudio,
    cid,
    // 添加高级选项
    ...options
  }

  // 从本地存储获取API密钥
  const apiKey = localStorage.getItem('apiKey')

  // 准备请求头
  const headers = {
    'Content-Type': 'application/json',
  }

  // 如果存在API密钥，添加到请求头
  if (apiKey) {
    headers['X-API-Key'] = apiKey
  }

  const response = await fetch(`${BASE_URL}/download/download_video`, {
    method: 'POST',
    headers,
    body: JSON.stringify(requestBody)
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
  return instance.get('/scheduler/tasks', { params })
    .then(response => {
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


export const deleteSubTask = (taskId, subTaskId) => {
  return instance.delete(`/scheduler/tasks/${taskId}/subtasks/${subTaskId}`)
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

// API安全相关接口已移除

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

/**
 * 删除已下载的视频
 * @param {number|null} cid 视频的CID，若为null则必须指定directory
 * @param {boolean} deleteDirectory 是否删除整个目录，默认为false（只删除视频文件）
 * @param {string|null} directory 可选，指定要删除文件的目录路径
 *                               若提供则在该目录中查找和删除文件
 *                               对于从收藏夹下载的视频，由于没有CID，
 *                               可以设置cid为null并通过directory参数指定目录路径
 * @returns {Promise<object>} 包含删除结果信息的响应
 */
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

  // 构建基本URL
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

    return await instance.get(`/download/stream_danmaku`, {
      params,
      responseType: 'text' // 获取纯文本格式的弹幕文件
    });
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
 * @param {boolean} force_check - 是否强制执行检查，忽略配置设置
 * @returns {Promise} - API响应
 */
export const checkDataIntegrity = (db_path = 'output/bilibili_history.db', json_path = 'output/history_by_date', async_mode = false, force_check = false) => {
  return instance.post('/data_sync/check', {
    db_path,
    json_path,
    async_mode,
    force_check
  })
}

/**
 * 获取数据完整性校验配置API
 * @returns {Promise} - API响应
 */
export const getIntegrityCheckConfig = () => {
  return instance.get('/data_sync/config')
}

/**
 * 获取数据完整性报告API
 * @returns {Promise} - API响应
 */
export const getIntegrityReport = () => {
  return instance.get('/data_sync/report')
}

/**
 * 更新数据完整性校验配置API
 * @param {boolean} checkOnStartup - 是否在启动时进行数据完整性校验
 * @returns {Promise} - API响应
 */
export const updateIntegrityCheckConfig = (checkOnStartup) => {
  return instance.post('/data_sync/config', {
    check_on_startup: checkOnStartup
  })
}

/**
 * 获取指定用户创建的所有收藏夹信息
 * @param {Object} params 请求参数
 * @param {number} [params.up_mid] 目标用户mid，不提供则使用当前登录用户
 * @param {number} [params.type] 目标内容属性，0=全部(默认)，2=视频稿件
 * @param {number} [params.rid] 目标内容id，视频稿件为avid
 * @param {string} [params.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @returns {Promise<Object>} 收藏夹列表
 */
export const getCreatedFavoriteFolders = (params = {}) => {
  return instance.get('/favorite/folder/created/list-all', { params })
}

/**
 * 获取指定用户收藏的视频收藏夹列表
 * @param {Object} params 请求参数
 * @param {number} [params.up_mid] 目标用户mid，不提供则使用当前登录用户
 * @param {number} [params.pn] 页码，默认为1
 * @param {number} [params.ps] 每页项数，默认为20
 * @param {string} [params.keyword] 搜索关键词
 * @param {string} [params.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @returns {Promise<Object>} 收藏夹列表
 */
export const getCollectedFavoriteFolders = (params = {}) => {
  return instance.get('/favorite/folder/collected/list', { params })
}

/**
 * 获取收藏夹内容列表
 * @param {Object} params 请求参数
 * @param {number} params.media_id 目标收藏夹id（完整id）
 * @param {number} [params.pn] 页码，默认为1
 * @param {number} [params.ps] 每页项数，默认为20
 * @param {string} [params.keyword] 搜索关键词
 * @param {string} [params.order] 排序方式，mtime(收藏时间，默认)或view(播放量)
 * @param {number} [params.type] 筛选类型，0=全部(默认)，2=视频
 * @param {number} [params.tid] 分区ID，0=全部(默认)
 * @param {string} [params.platform] 平台标识，默认为web
 * @param {string} [params.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @returns {Promise<Object>} 收藏夹内容列表
 */
export const getFavoriteContents = (params = {}) => {
  return instance.get('/favorite/folder/resource/list', { params })
}

/**
 * 获取数据库中的收藏夹列表
 * @param {Object} params 请求参数
 * @param {number} [params.mid] 用户UID，不提供则返回所有收藏夹
 * @param {number} [params.page] 页码，默认为1
 * @param {number} [params.size] 每页数量，默认为20
 * @returns {Promise<Object>} 收藏夹列表
 */
export const getLocalFavoriteFolders = (params = {}) => {
  return instance.get('/favorite/list', { params })
}

/**
 * 获取数据库中的收藏内容列表
 * @param {Object} params 请求参数
 * @param {number} params.media_id 收藏夹ID
 * @param {number} [params.page] 页码，默认为1
 * @param {number} [params.size] 每页数量，默认为20
 * @returns {Promise<Object>} 内容列表
 */
export const getLocalFavoriteContents = (params = {}) => {
  return instance.get('/favorite/content/list', { params })
}
// #endregion

/**
 * 收藏或取消收藏视频
 * @param {Object} params 请求参数
 * @param {number} params.rid 稿件avid (不含av前缀)
 * @param {string} [params.add_media_ids] 需要加入的收藏夹ID，多个用逗号分隔
 * @param {string} [params.del_media_ids] 需要取消的收藏夹ID，多个用逗号分隔
 * @param {string} [params.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @returns {Promise<Object>} 操作结果
 */
export const favoriteResource = (params = {}) => {
  return instance.post('/favorite/resource/deal', params)
}

/**
 * 批量收藏或取消收藏视频
 * @param {Object} params 请求参数
 * @param {string} params.rids 稿件avid列表 (不含av前缀)，多个用逗号分隔
 * @param {string} [params.add_media_ids] 需要加入的收藏夹ID，多个用逗号分隔
 * @param {string} [params.del_media_ids] 需要取消的收藏夹ID，多个用逗号分隔
 * @param {string} [params.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @returns {Promise<Object>} 操作结果
 */
export const batchFavoriteResource = (params = {}) => {
  return instance.post('/favorite/resource/batch-deal', params)
}

/**
 * 本地批量收藏或取消收藏视频
 * @param {Object} params 请求参数
 * @param {string} params.rids 稿件avid列表 (不含av前缀)，多个用逗号分隔
 * @param {string} [params.add_media_ids] 需要加入的收藏夹ID，多个用逗号分隔
 * @param {string} [params.del_media_ids] 需要取消的收藏夹ID，多个用逗号分隔
 * @param {string} [params.operation_type] 操作类型，`sync`=同步到远程，`local`=仅本地操作，默认为`sync`
 * @param {string} [params.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @returns {Promise<Object>} 操作结果
 */
export const localBatchFavoriteResource = (params = {}) => {
  return instance.post('/favorite/resource/local-batch-deal', params)
}

/**
 * 批量检查视频收藏状态
 * @param {Object} params 请求参数
 * @param {Array<number>|string} params.oids 视频av号列表，可以是数组或逗号分隔的字符串
 * @param {string} [params.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @returns {Promise<Object>} 视频收藏状态
 */
export const batchCheckFavoriteStatus = (params = {}) => {
  const requestParams = { ...params };

  // 确保 oids 是数组格式
  if (typeof requestParams.oids === 'string') {
    requestParams.oids = requestParams.oids.split(',').map(id => parseInt(id.trim(), 10)).filter(id => !isNaN(id));
  } else if (!Array.isArray(requestParams.oids)) {
    console.error('批量检查收藏状态参数错误：oids必须是数组或逗号分隔的字符串');
    requestParams.oids = [];
  }

  return instance.post('/favorite/check/batch', requestParams);
}

/**
 * 下载用户收藏夹视频
 * @param {Object} options 下载选项
 * @param {string} options.user_id 用户UID
 * @param {string} [options.fid] 收藏夹ID，不提供则下载全部收藏夹
 * @param {string} [options.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @param {boolean} [options.download_cover] 是否下载封面，默认true
 * @param {boolean} [options.only_audio] 是否仅下载音频，默认false
 * @param {Function} onMessage 消息处理回调函数
 * @returns {Promise<void>}
 */
export const downloadFavorites = async (options, onMessage) => {
  console.log('调用收藏夹下载API, 参数:', options)

  // 提取基本选项和高级选项
  const { user_id, fid, sessdata, download_cover, only_audio, ...advancedOptions } = options

  const requestBody = {
    user_id,
    fid,
    sessdata,
    download_cover: download_cover ?? true,
    only_audio: only_audio ?? false,
    // 添加高级选项
    ...advancedOptions
  }

  // 准备请求头
  const headers = {
    'Content-Type': 'application/json',
  }

  const response = await fetch(`${BASE_URL}/download/download_favorites`, {
    method: 'POST',
    headers,
    body: JSON.stringify(requestBody)
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

/**
 * 批量下载多个视频
 * @param {Object} options 下载选项
 * @param {Array} options.videos 要下载的视频列表，每个视频包含bvid、cid、title、author、cover
 * @param {string} [options.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @param {boolean} [options.download_cover] 是否下载封面，默认true
 * @param {boolean} [options.only_audio] 是否仅下载音频，默认false
 * @param {Function} onMessage 消息处理回调函数
 * @returns {Promise<void>}
 */
export const batchDownloadVideos = async (options, onMessage) => {
  console.log('调用批量下载API, 参数:', options)

  // 提取基本选项和高级选项
  const { videos, sessdata, download_cover, only_audio, ...advancedOptions } = options

  const requestBody = {
    videos,
    sessdata,
    download_cover: download_cover ?? true,
    only_audio: only_audio ?? false,
    // 添加高级选项
    ...advancedOptions
  }

  // 准备请求头
  const headers = {
    'Content-Type': 'application/json',
  }

  const response = await fetch(`${BASE_URL}/download/batch_download`, {
    method: 'POST',
    headers,
    body: JSON.stringify(requestBody)
  })

  if (!response.ok) {
    const errorData = await response.json()
    throw new Error(errorData.detail || '批量下载请求失败')
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
}

/**
 * 下载用户全部投稿视频
 * @param {Object} options 下载选项
 * @param {string} options.user_id 用户UID
 * @param {string} [options.sessdata] 用户的SESSDATA，不提供则从配置文件读取
 * @param {boolean} [options.download_cover] 是否下载封面，默认true
 * @param {boolean} [options.only_audio] 是否仅下载音频，默认false
 * @param {Function} onMessage 消息处理回调函数
 * @returns {Promise<void>}
 */
export const downloadUserVideos = async (options, onMessage) => {
  console.log('调用用户视频下载API, 参数:', options)

  // 提取基本选项和高级选项
  const { user_id, sessdata, download_cover, only_audio, ...advancedOptions } = options

  const requestBody = {
    user_id,
    sessdata,
    download_cover: download_cover ?? true,
    only_audio: only_audio ?? false,
    // 添加高级选项
    ...advancedOptions
  }

  // 准备请求头
  const headers = {
    'Content-Type': 'application/json',
  }

  const response = await fetch(`${BASE_URL}/download/download_user_videos`, {
    method: 'POST',
    headers,
    body: JSON.stringify(requestBody)
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


/**
 * 获取B站视频详细信息
 * @param {Object} params 参数对象
 * @param {string} [params.aid] 视频的avid
 * @param {string} [params.bvid] 视频的bvid
 * @returns {Promise<object>} 包含视频详细信息的响应
 */
export const getVideoInfo = (params) => {
  return instance.get(`/download/video_info`, {
    params
  })
}

// 获取用户投稿视频列表
export const getUserVideos = (params) => {
  return instance.get('/download/user_videos', {
    params: {
      mid: params.mid,
      pn: params.pn || 1,
      ps: params.ps || 30,
      tid: params.tid || 0,
      keyword: params.keyword || '',
      order: params.order || 'pubdate',
      sessdata: params.sessdata || ''
    }
  })
}

/**
 * 批量获取视频详情（使用新的超详细接口）
 * @param {object} params - 请求参数
 * @param {number} params.max_videos - 最多处理的视频数量，0表示全部
 * @param {string} params.specific_videos - 要获取的特定视频ID列表，用逗号分隔（可选）
 * @param {boolean} params.use_sessdata - 是否使用SESSDATA获取详情，某些视频需要登录才能查看（可选，默认为true）
 * @returns {Promise<object>} - 包含获取结果的响应
 */
export const fetchVideoDetails = (params) => {
  let maxVideos = 100
  let specificVideos = ''
  let useSessdata = true

  // 兼容旧版调用方式，同时支持对象参数和独立参数
  if (typeof params === 'object') {
    maxVideos = params.max_videos !== undefined ? params.max_videos : 100
    specificVideos = params.specific_videos || ''
    useSessdata = params.use_sessdata !== undefined ? params.use_sessdata : true
  } else if (typeof params === 'number') {
    // 旧版调用方式: fetchVideoDetails(maxVideos, specificVideos)
    maxVideos = params
    specificVideos = arguments[1] || ''
  }

  // 使用新的超详细视频详情接口
  return instance.get('/video_details/batch_fetch_from_history', {
    params: {
      max_videos: maxVideos,
      specific_videos: specificVideos,
      use_sessdata: useSessdata
    }
  })
}

/**
 * 创建视频详情进度的SSE连接（使用新的超详细接口）
 * @param {object|number} params - 请求参数或更新间隔
 * @param {number} params.update_interval - 更新间隔，单位秒
 * @returns {EventSource} - SSE事件源对象
 */
export const createVideoDetailsProgressSSE = (params) => {
  let updateInterval = 0.1

  // 兼容旧版调用方式，同时支持对象参数和数字参数
  if (typeof params === 'object') {
    updateInterval = params.update_interval !== undefined ? params.update_interval : 0.1
  } else if (typeof params === 'number') {
    updateInterval = params
  }

  const baseUrl = instance.defaults.baseURL

  // 构建基本URL，使用新的超详细接口
  let url = `${baseUrl}/video_details/progress?update_interval=${updateInterval}`

  return new EventSource(url)
}

/**
 * 获取视频详情统计数据（使用新的超详细接口）
 * @returns {Promise<object>} - 包含视频详情统计的响应
 */
export const getVideoDetailsStats = () => {
  return instance.get('/video_details/stats')
}

/**
 * 停止视频详情获取任务
 * @returns {Promise<object>} - 包含停止结果的响应
 */
export const stopVideoDetailsFetch = () => {
  return instance.post('/video_details/stop')
}
/**
 * 获取视频观看时长信息（合集视频）
 * @param {Object} params 参数对象
 * @param {string} params.bvid 视频的bvid
 * @param {boolean} [params.use_sessdata=true] 是否使用登录状态查询
 * @returns {Promise<object>} 包含视频合集观看时长信息的响应
 */
export const getVideoSeasonInfo = (params) => {
  return instance.get('/download/video_season_info', {
    params
  })
}

/**
 * 检查视频是否为合集
 * @param {string} url 视频URL
 * @param {string} [sessdata] 可选的SESSDATA用于认证
 * @returns {Promise<object>} 包含合集信息的响应
 */
export const checkCollection = (url, sessdata = null) => {
  const params = { url }
  if (sessdata) {
    params.sessdata = sessdata
  }
  return instance.get('/collection/check_collection', {
    params
  })
}

/**
 * 下载整个合集
 * @param {Object} params 下载参数
 * @param {string} params.url 合集URL
 * @param {number} params.cid 视频的CID
 * @param {Function} onMessage 消息回调函数
 * @returns {Promise<void>}
 */
export const downloadCollection = async (params, onMessage) => {
  try {
    const response = await fetch(`${BASE_URL}/collection/download_collection`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(params)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value)
      const lines = chunk.split('\n')

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const message = line.slice(6)
          if (message && onMessage) {
            onMessage(message)
          }
        }
      }
    }
  } catch (error) {
    console.error('下载合集失败:', error)
    throw error
  }
}

// =============================
// 动态相关接口（/dynamic）
// =============================

/**
 * 列出数据库中已有动态的 UP 列表（含名称与头像）
 * GET /dynamic/db/hosts
 * @param {number} [limit=50] - 每页数量（1-200）
 * @param {number} [offset=0] - 偏移量（>=0）
 */
export const getDynamicDbHosts = (limit = 50, offset = 0) => {
  return instance.get('/dynamic/db/hosts', {
    params: { limit, offset }
  })
}

/**
 * 列出指定 UP 的动态（来自数据库）
 * GET /dynamic/db/space/{host_mid}
 * @param {string|number} hostMid - UP 的 mid
 * @param {number} [limit=20] - 每页数量（1-200）
 * @param {number} [offset=0] - 偏移量（>=0）
 */
export const getDynamicDbSpace = (hostMid, limit = 20, offset = 0) => {
  return instance.get(`/dynamic/db/space/${hostMid}`, {
    params: { limit, offset }
  })
}
/**
 * 自动从上次位置继续抓取（页级延迟 3-5 秒，支持“页级停止”）
 * GET /dynamic/space/auto/{host_mid}
 * @param {string|number} hostMid - UP 的 mid
 * @param {Object} params - 查询参数
 * @param {boolean} [params.need_top=false]
 * @param {boolean} [params.save_to_db=true]
 * @param {boolean} [params.save_media=true]
 */
export const startDynamicAutoFetch = (hostMid, params = {}) => {
  const {
    need_top = false,
    save_to_db = true,
    save_media = true
  } = params
  return instance.get(`/dynamic/space/auto/${hostMid}`, {
    params: { need_top, save_to_db, save_media }
  })
}

/**
 * 创建动态抓取进度的 SSE 连接
 * GET /dynamic/space/auto/{host_mid}/progress
 * @param {string|number} hostMid - UP 的 mid
 * @returns {EventSource}
 */
export const createDynamicProgressSSE = (hostMid) => {
  const baseUrl = instance.defaults.baseURL
  const url = `${baseUrl}/dynamic/space/auto/${hostMid}/progress`
  return new EventSource(url)
}

/**
 * 发送停止信号（当前页抓取完成后停止并记录 offset）
 * POST /dynamic/space/auto/{host_mid}/stop
 * @param {string|number} hostMid - UP 的 mid
 */
export const stopDynamicAutoFetch = (hostMid) => {
  return instance.post(`/dynamic/space/auto/${hostMid}/stop`)
}
// =============================
// 动态删除接口（/dynamic）
// =============================

/**
 * 清理指定 UP 的动态及媒体文件
 * DELETE /dynamic/space/{host_mid}
 * @param {string|number} hostMid - UP 的 mid
 * @returns {Promise<any>}
 */
export const deleteDynamicSpace = (hostMid) => {
  return instance.delete(`/dynamic/space/${hostMid}`)
}
