import axios from 'axios'

// 你的服务器地址
// const BASE_URL = 'http://localhost:8899'

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
    return response
  }).catch(error => {
    console.error('API 请求错误:', error)
    // 重新抛出错误，让调用者处理
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
