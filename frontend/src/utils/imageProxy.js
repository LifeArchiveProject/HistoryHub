/**
 * 图片代理服务
 * 使用公共代理服务获取跨域图片
 */

/**
 * 从原始URL获取代理图片URL
 * @param {string} originalUrl 原始图片URL
 * @returns {string} 处理后的URL
 */
export const getImageProxyUrl = (originalUrl) => {
  // 检查是否需要代理
  if (!originalUrl) return originalUrl;
  
  // 数据URL和blob URL不需要代理
  if (originalUrl.startsWith('data:') || originalUrl.startsWith('blob:')) {
    return originalUrl;
  }
  
  // 相对URL不需要代理
  if (!/^https?:\/\/|^\/\//.test(originalUrl)) {
    return originalUrl;
  }
  
  // 使用images.weserv.nl (较稳定的公共代理)
  return `https://images.weserv.nl/?url=${encodeURIComponent(originalUrl)}`;
};

export default {
  getImageProxyUrl
}; 