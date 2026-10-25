import axios from 'axios'

const DEFAULT_BACKEND_URL = import.meta.env.VITE_DEFAULT_BACKEND_URL || 'http://localhost:8899'

export const getCurrentBaseUrl = () => localStorage.getItem('baseUrl') || DEFAULT_BACKEND_URL

const instance = axios.create({ baseURL: getCurrentBaseUrl() })

export const setBaseUrl = (url) => {
  localStorage.setItem('baseUrl', url)
  instance.defaults.baseURL = url
  window.dispatchEvent(new CustomEvent('api-baseurl-updated', { detail: { url } }))
  window.location.reload()
}

export const getBrowserHistoryRecords = ({ token, cursor = null, query = '' }) => {
  return instance.get('/browser-history/records', {
    headers: { Authorization: `Bearer ${token}` },
    params: { cursor, size: 50, query },
  })
}

export const getBiliHistoryRecords = (page = 1) => {
  return instance.get('/history/all', { params: { page, size: 30, sort_order: 0 } })
}

export const searchBiliHistoryRecords = (search, page = 1) => {
  return instance.get('/history/search', {
    params: { page, size: 30, sortOrder: 0, search, search_type: 'all' },
  })
}

export const syncBiliHistory = () => instance.get('/fetch/bili-history')

export const getLoginStatus = () => instance.get('/login/check')

export const generateLoginQRCode = () => instance.get('/login/qrcode/generate')

export const getQRCodeImageBlob = async () => {
  const response = await instance.get('/login/qrcode/image', { responseType: 'blob' })
  return URL.createObjectURL(response.data)
}

export const pollQRCodeStatus = (qrcodeKey) => {
  return instance.get('/login/qrcode/poll', { params: { qrcode_key: qrcodeKey } })
}

export const logout = () => instance.post('/login/logout')
