const STORAGE_PREFIX = 'history-record:'

export const buildHistoryRecordKey = (bvid, viewAt) => `${STORAGE_PREFIX}${bvid}_${viewAt}`

export const saveHistoryRecord = (record) => {
  if (!record?.bvid || !record?.view_at) return null

  const key = buildHistoryRecordKey(record.bvid, record.view_at)
  sessionStorage.setItem(key, JSON.stringify(record))
  return key
}

export const getHistoryRecord = (bvid, viewAt) => {
  const key = buildHistoryRecordKey(bvid, viewAt)
  const rawValue = sessionStorage.getItem(key)

  if (!rawValue) return null

  try {
    return JSON.parse(rawValue)
  } catch (error) {
    console.error('解析历史记录缓存失败:', error)
    return null
  }
}
