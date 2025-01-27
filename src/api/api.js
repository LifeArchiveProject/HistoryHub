import axios from 'axios'

// 你的服务器地址
const BASE_URL = 'http://localhost:8899'

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

export const searchBiliHistory2024 = (page, size, search, sortOrder = 0, year) => {
  return instance.get(`/BiliHistory2024/search`, {
    params: {
      page,
      size,
      search,
      sort_order: sortOrder,
      year,
    },
  })
}

// 作者搜索接口
export const searchBiliHistoryAuthor = (page, size, author, sortOrder = 0, year) => {
  // 确保 author 是字符串类型
  const authorStr = Array.isArray(author) ? author[0] : String(author || '')

  return instance.get(`/BiliHistory2024/search_author`, {
    params: {
      page,
      size,
      author: authorStr,
      sort_order: sortOrder,
      year,
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
