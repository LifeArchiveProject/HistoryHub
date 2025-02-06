import axios from 'axios'

// 你的服务器地址
const getBaseUrl = () => {
  return localStorage.getItem('baseUrl') || 'http://localhost:8899'
}

const BASE_URL = getBaseUrl()

// 设置服务器地址
export const setBaseUrl = (url) => {
  localStorage.setItem('baseUrl', url)
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

// 历史记录相关接口
export const getBiliHistory2024 = (page, size, sortOrder, tagName, mainCategory, dateRange) => {
  return instance.get(`/BiliHistory2024/all`, {
    params: {
      page,
      size,
      sort_order: sortOrder,
      tag_name: tagName,
      main_category: mainCategory,
      date_range: dateRange,
    },
  })
}

export const searchBiliHistory2024 = (page, size, search, searchType = 'all', sortOrder = 0, sortBy = 'relevance') => {
  return instance.get(`/BiliHistory2024/search`, {
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
  return instance.get(`/BiliHistory2024/available-years`)
}

// 分类相关接口
export const getVideoCategories = () => {
  return instance.get(`/BiliHistory2024/categories`) // 使用新的分类接口
}

export const getMainCategories = () => {
  return instance.get(`/BiliHistory2024/main-categories`)
}

// 标题分析相关接口
export const getTitleAnalytics = (year, useCache = true) => {
  return instance.get(`/title-analytics/`, {
    params: {
      year,
      use_cache: useCache
    }
  })
}

// 获取观看时间分布分析
export const getViewingAnalytics = async (year, useCache = true) => {
  return instance.get(`/viewing-analytics/`, {
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
  return instance.get(`/stats/daily-count`, {
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

// 批量删除历史记录
export const batchDeleteHistory = (items) => {
  return instance.delete('/history/batch-delete', {
    data: items  // 直接发送数组，不要包装在 items 对象中
  })
}

// 数据库管理相关接口
// 重置数据库
export const resetDatabase = () => {
  return instance.post('/BiliHistory2024/reset-database')
}

// 备注相关接口
// 更新视频备注
export const updateVideoRemark = (bvid, viewAt, remark) => {
  return instance.post('/BiliHistory2024/update-remark', {
    bvid,
    view_at: viewAt,
    remark
  })
}

// 获取视频备注
export const getVideoRemark = (bvid, viewAt) => {
  return instance.get('/BiliHistory2024/remark', {
    params: {
      bvid,
      view_at: viewAt
    }
  })
}

// 获取所有备注记录
export const getAllRemarks = (page = 1, size = 10, sortOrder = 0) => {
  return instance.get('/BiliHistory2024/remarks', {
    params: {
      page,
      size,
      sort_order: sortOrder
    }
  })
}

// 获取SQLite版本
export const getSqliteVersion = () => {
  return instance.get('/BiliHistory2024/sqlite-version')
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

// 清空图片
export const clearImages = () => {
  return instance.post('/images/clear')
}

// 下载视频
export const downloadVideo = async (bvid, sessdata = null, onMessage) => {
  console.log('调用下载API, bvid:', bvid)
  
  const response = await fetch(`${BASE_URL}/download/download_video`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url: bvid,
      sessdata
    })
  })

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`)
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

// 获取下载进度事件流 URL
export const getDownloadProgressUrl = (bvid) => {
  return `${BASE_URL}/download/download_video/stream?bvid=${bvid}`
}
