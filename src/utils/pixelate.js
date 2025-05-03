/**
 * 图片像素化处理工具
 */

import { getImageProxyUrl } from './imageProxy';

/**
 * 计算图片的有效像素化强度
 * @param {Number} originalWidth - 原始图片宽度
 * @param {Number} originalHeight - 原始图片高度
 * @param {Number} quality - 设置的质量值(1-100)
 * @returns {Number} 调整后的质量值
 */
const calculateEffectiveQuality = (originalWidth, originalHeight, quality) => {
  // 基准尺寸（示例图片的近似尺寸）
  const REFERENCE_SIZE = 400;
  
  // 获取图片的短边
  const minDimension = Math.min(originalWidth, originalHeight);
  
  // 根据图片尺寸计算调整系数
  // 对于小图片，要比大图片使用更低的质量值才能获得类似的像素效果
  const sizeFactor = Math.min(1, minDimension / REFERENCE_SIZE);
  
  // 对小图片的质量值进行额外缩减
  // 图片越小，质量值缩减越多
  const sizeAdjustment = sizeFactor * 0.6 + 0.2; // 减少最小系数到0.2倍
  
  // 计算调整后的质量值，并额外降低30%以增强像素效果
  let adjustedQuality = quality * sizeAdjustment * 0.7;
  
  // 对于非常小的图片(如头像)，质量值设得更低以强化像素效果
  if (minDimension < 100) {
    adjustedQuality = adjustedQuality * 0.5; // 更强的降低比例
  } else if (minDimension < 200) {
    adjustedQuality = adjustedQuality * 0.7; // 中等图片也强化像素效果
  }
  
  // 确保质量值在合理范围内，最低到3
  return Math.max(3, Math.min(adjustedQuality, quality));
};

/**
 * 通过代理加载图片
 * @param {string} url 图片URL
 * @returns {Promise<HTMLImageElement>} 加载好的图片元素
 */
export const proxyLoadImage = async (url) => {
  try {
    // 规范化URL (处理 // 开头的协议相对URL)
    const normalizedUrl = url.startsWith('//') ? `https:${url}` : url;
    
    // 检查是否是数据URL，如果是则直接加载
    if (normalizedUrl.startsWith('data:')) {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = normalizedUrl;
      });
      return img;
    }
    
    // 检查是否需要代理
    const needsProxy = normalizedUrl.startsWith('http');
    
    if (needsProxy) {
      try {
        // 先尝试直接使用fetch代理请求
        const response = await fetch(normalizedUrl, {
          mode: 'cors',
          cache: 'no-cache',
          headers: {
            'Cache-Control': 'no-cache'
          }
        });
        
        if (!response.ok) {
          throw new Error(`HTTP错误: ${response.status}`);
        }
        
        const blob = await response.blob();
        const blobUrl = URL.createObjectURL(blob);
        
        const img = new Image();
        img.crossOrigin = 'anonymous';
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = reject;
          img.src = blobUrl;
        });
        
        return img;
      } catch (directError) {
        console.warn('直接加载图片失败，尝试使用代理:', directError);
        
        // 直接获取失败，使用代理
        const proxyUrl = getImageProxyUrl(normalizedUrl);
        
        const img = new Image();
        img.crossOrigin = 'anonymous';
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = (e) => reject(new Error(`代理加载失败: ${e.message || proxyUrl}`));
          img.src = proxyUrl;
        });
        
        return img;
      }
    } else {
      // 本地图片直接加载
      const img = new Image();
      img.crossOrigin = 'anonymous';
      await new Promise((resolve, reject) => {
        img.onload = resolve;
        img.onerror = reject;
        img.src = normalizedUrl;
      });
      
      return img;
    }
  } catch (error) {
    console.error('所有尝试加载图片的方法都失败:', error);
    throw error;
  }
};

/**
 * 将图片像素化处理
 * @param {HTMLImageElement|String} image - 图片元素或图片URL
 * @param {Object} options - 配置选项
 * @param {Number} options.pixelSize - 像素大小，默认为10
 * @param {Number} options.quality - 质量级别（1-100），默认为50
 * @param {Boolean} options.usePixelFont - 是否使用像素字体，默认为false
 * @returns {Promise<HTMLCanvasElement>} 处理后的canvas元素
 */
export const pixelateImage = async (image, options = {}) => {
  // 默认配置
  const config = {
    pixelSize: 10,
    quality: 50,
    usePixelFont: false,
    ...options
  };

  // 创建临时canvas
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  // 加载图片
  let imgElement;
  if (typeof image === 'string') {
    // 如果是URL，使用增强的代理加载
    try {
      imgElement = await proxyLoadImage(image);
    } catch (error) {
      console.error('加载图片失败:', error);
      throw error;
    }
  } else {
    // 如果已经是图片元素
    imgElement = image;
  }

  // 根据图片尺寸动态调整质量值
  const effectiveQuality = calculateEffectiveQuality(
    imgElement.width, 
    imgElement.height, 
    config.quality
  );
  
  // 计算像素化后的尺寸
  const width = Math.floor(imgElement.width / 100 * effectiveQuality);
  const height = Math.floor(imgElement.height / 100 * effectiveQuality);

  // 对于极低的质量值，确保有最小的尺寸限制，避免图片消失
  const minDimension = Math.max(5, Math.min(width, height));
  
  // 进一步调整尺寸以增强像素效果
  // 当图片较小或质量值较低时，更强化像素效果
  let scaleFactor = 1;
  if (effectiveQuality <= 15) {
    scaleFactor = 0.4;  // 质量非常低时，更大幅度减小尺寸
  } else if (effectiveQuality <= 30) {
    scaleFactor = 0.5;  // 质量低时，大幅减小尺寸
  } else if (effectiveQuality <= 50) {
    scaleFactor = 0.6;  // 中等质量时，中等减小尺寸
  } else if (Math.min(imgElement.width, imgElement.height) < 200) {
    scaleFactor = 0.7;  // 小图片时，轻微减小尺寸
  }
  
  const finalWidth = Math.max(minDimension, Math.floor(width * scaleFactor));
  const finalHeight = Math.max(minDimension, Math.floor(height * scaleFactor));

  // 设置canvas尺寸
  canvas.width = imgElement.width;
  canvas.height = imgElement.height;

  // 绘制低分辨率图像
  const tempCanvas = document.createElement('canvas');
  const tempCtx = tempCanvas.getContext('2d');
  tempCanvas.width = finalWidth;
  tempCanvas.height = finalHeight;
  
  try {
    // 尝试绘制图像
    tempCtx.drawImage(imgElement, 0, 0, finalWidth, finalHeight);
    
    // 禁用平滑处理，确保像素边界清晰
    ctx.imageSmoothingEnabled = false;
    
    // 放大到原始尺寸，产生像素化效果
    ctx.drawImage(tempCanvas, 0, 0, finalWidth, finalHeight, 0, 0, canvas.width, canvas.height);
  } catch (error) {
    console.error('绘制图像失败:', error);
    throw error;
  }

  return canvas;
};

/**
 * 将图片转换为Data URL
 * @param {HTMLCanvasElement} canvas - Canvas元素
 * @param {String} type - 图片类型，默认为image/png
 * @param {Number} quality - 图片质量（0-1），默认为0.8
 * @returns {String} 图片的Data URL
 */
export const canvasToDataURL = (canvas, type = 'image/png', quality = 0.8) => {
  try {
    return canvas.toDataURL(type, quality);
  } catch (error) {
    console.error('Canvas导出失败:', error);
    throw error;
  }
};

/**
 * 像素化图片并返回Data URL
 * @param {HTMLImageElement|String} image - 图片元素或图片URL
 * @param {Object} options - 配置选项
 * @returns {Promise<String>} 处理后图片的Data URL
 */
export const pixelateImageToDataURL = async (image, options = {}) => {
  try {
    const canvas = await pixelateImage(image, options);
    return canvasToDataURL(canvas);
  } catch (error) {
    console.error('像素化图片失败:', error);
    throw error;
  }
};

/**
 * 应用像素化效果到图片元素
 * @param {HTMLImageElement} imgElement - 图片元素
 * @param {Object} options - 配置选项
 * @returns {Promise<void>}
 */
export const applyPixelEffect = async (imgElement, options = {}) => {
  try {
    // 保存原始src以便可以恢复
    if (!imgElement.dataset.originalSrc) {
      imgElement.dataset.originalSrc = imgElement.src;
    }
    
    // 使用增强的代理加载图片，处理各种网络图片URL和跨域问题
    const proxyImg = await proxyLoadImage(imgElement.dataset.originalSrc);
    
    // 应用像素化处理
    const dataUrl = await pixelateImageToDataURL(proxyImg, options);
    
    // 应用像素化图片
    imgElement.src = dataUrl;
    imgElement.dataset.pixelated = "true";
    
    // 添加像素化渲染样式
    imgElement.style.imageRendering = 'pixelated';
  } catch (error) {
    console.error('应用像素化效果失败:', error, '图片URL:', imgElement.dataset.originalSrc);
    
    // 错误恢复 - 确保图片仍然可见
    if (imgElement.dataset.originalSrc) {
      imgElement.classList.add('pixelate-error');
    }
    
    throw error;
  }
};

/**
 * 恢复图片到原始状态
 * @param {HTMLImageElement} imgElement - 图片元素
 */
export const removePixelEffect = (imgElement) => {
  if (imgElement.dataset.originalSrc) {
    imgElement.src = imgElement.dataset.originalSrc;
    imgElement.style.imageRendering = '';
    imgElement.removeAttribute('data-pixelated');
  }
}; 