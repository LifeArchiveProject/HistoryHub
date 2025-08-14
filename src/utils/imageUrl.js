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

export default {
	normalizeImageUrl,
}


