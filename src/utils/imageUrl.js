// 规范化图片 URL：
// - data:/blob: 保持不变
// - // 开头的协议相对地址 -> https:
// - http/https 绝对地址 -> 保持不变
// - 以 / 开头或相对路径 -> 拼接当前 API BaseURL
import { getCurrentBaseUrl } from '@/api/api'

export const normalizeImageUrl = (url) => {
	if (!url) return ''
	if (typeof url !== 'string') return url

	// 数据或 blob URL
	if (url.startsWith('data:') || url.startsWith('blob:')) return url

	// 协议相对 URL
	if (url.startsWith('//')) return `https:${url}`

	// 已是绝对 URL
	if (/^https?:\/\//i.test(url)) return url

	// 其余按相对路径处理，拼接当前 API BaseURL
	const base = getCurrentBaseUrl && getCurrentBaseUrl()
	if (!base) return url
	const baseNormalized = String(base).replace(/\/$/, '')
	const pathNormalized = url.startsWith('/') ? url : `/${url}`
	return `${baseNormalized}${pathNormalized}`
}

/**
 * 将相对 output 路径转换为可访问的静态 URL（自动拼接 /static/ 前缀，并处理反斜杠）
 * 例如："dynamic\\341376543\\face.jpg" -> "<BASE>/static/dynamic/341376543/face.jpg"
 * 若已是 http(s)/data/blob，则保持不变
 * 若已以 /static/ 开头，则直接规范化为完整 URL
 */
export const toStaticUrl = (relativePath) => {
  if (!relativePath) return ''
  if (typeof relativePath !== 'string') return relativePath

  // 已是绝对/数据/Blob URL
  if (relativePath.startsWith('data:') || relativePath.startsWith('blob:') || /^https?:\/\//i.test(relativePath)) {
    return relativePath
  }

  // 统一分隔符
  const normalized = relativePath.replace(/\\/g, '/').replace(/^\/+/, '')

  // 已包含 /static/ 前缀
  const staticPath = normalized.startsWith('static/') || normalized.startsWith('/static/')
    ? (normalized.startsWith('/') ? normalized : `/${normalized}`)
    : `/static/${normalized}`

  // 拼接域名
  return normalizeImageUrl(staticPath)
}

export default {
	normalizeImageUrl,
	toStaticUrl,
}


