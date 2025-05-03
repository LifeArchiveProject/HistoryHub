import { pixelateImageToDataURL, proxyLoadImage } from './pixelate';

/**
 * 全局图片像素化处理工具
 */
class GlobalPixelateManager {
  constructor() {
    this.enabled = false;
    this.quality = 50;
    this.processedImages = new Map(); // 存储已处理的图片映射
    this.observer = null; // MutationObserver实例
    this.processingQueue = []; // 正在处理的图片队列
    this.isProcessing = false; // 是否正在处理图片
  }

  /**
   * 启用全局图片像素化
   * @param {Object} options 配置项
   */
  enable(options = {}) {
    this.enabled = true;
    this.quality = options.quality || 50;
    this.processExistingImages();
    this.startObserving();
  }

  /**
   * 禁用全局图片像素化
   */
  disable() {
    this.enabled = false;
    this.stopObserving();
    this.restoreImages();
  }

  /**
   * 更新像素化质量
   * @param {Number} quality 新的质量值
   */
  updateQuality(quality) {
    if (this.quality === quality) return;
    
    const oldQuality = this.quality;
    this.quality = quality;
    
    if (this.enabled) {
      // 如果质量降低超过10%或者低于30%，才重新处理所有图片
      const significantDecrease = oldQuality - quality > 10 || quality < 30;
      
      if (significantDecrease) {
        // 重新处理所有图片
        this.restoreImages();
        this.processExistingImages();
      } else {
        // 只处理新图片，已处理的保持不变
        const newImages = document.querySelectorAll('img:not(.no-pixelate):not([data-pixelated="true"])');
        this.queueImagesForProcessing(newImages);
      }
    }
  }

  /**
   * 处理现有的所有图片
   */
  processExistingImages() {
    if (!this.enabled) return;
    
    const images = document.querySelectorAll('img:not(.no-pixelate)');
    this.queueImagesForProcessing(images);
  }

  /**
   * 将图片加入处理队列
   * @param {NodeList} images 图片元素集合
   */
  queueImagesForProcessing(images) {
    for (const img of images) {
      // 跳过已处理的图片
      if (this.processedImages.has(img) || img.classList.contains('no-pixelate')) continue;
      
      // 处理未加载完成的图片
      if (!img.complete) {
        img.addEventListener('load', () => this.processImage(img), { once: true });
        continue;
      }
      
      // 加入处理队列
      this.processingQueue.push(img);
    }
    
    // 开始处理队列
    if (!this.isProcessing) {
      this.processQueue();
    }
  }

  /**
   * 处理图片队列
   */
  async processQueue() {
    if (this.processingQueue.length === 0) {
      this.isProcessing = false;
      return;
    }
    
    this.isProcessing = true;
    
    // 每次处理5张图片，避免阻塞UI
    const batch = this.processingQueue.splice(0, 5);
    
    // 并行处理图片
    await Promise.all(batch.map(img => this.processImage(img)));
    
    // 使用requestAnimationFrame继续处理队列
    requestAnimationFrame(() => this.processQueue());
  }

  /**
   * 处理单张图片
   * @param {HTMLImageElement} img 图片元素
   */
  async processImage(img) {
    // 跳过无效图片
    if (!img.src || img.classList.contains('no-pixelate') || 
        this.processedImages.has(img) || !this.enabled) {
      return;
    }
    
    try {
      // 保存原始图片
      if (!img.dataset.originalSrc) {
        img.dataset.originalSrc = img.src;
      }
      
      // 使用proxyLoadImage函数加载图片，处理所有网络图片和跨域问题
      const proxyImg = await proxyLoadImage(img.dataset.originalSrc);
      
      // 分析图片尺寸，小图片应用更强的像素化效果
      const isSmallImage = Math.min(proxyImg.width, proxyImg.height) < 200;
      const isTinyImage = Math.min(proxyImg.width, proxyImg.height) < 100;
      
      // 根据图片大小计算质量参数
      let enhancedQuality = this.quality;
      
      // 存储尺寸信息，以便CSS效果应用
      let sizeCategory = 'normal';
      
      if (isTinyImage) {
        // 非常小的图片(如头像)使用更强的像素化
        enhancedQuality = Math.max(5, this.quality * 0.4);
        sizeCategory = 'tiny';
      } else if (isSmallImage) {
        // 小图片使用更强的像素化
        enhancedQuality = Math.max(5, this.quality * 0.6);
        sizeCategory = 'small';
      } else if (this.quality <= 20) {
        // 低质量值时强化效果
        enhancedQuality = this.quality * 0.75;
      }
      
      // 应用像素化处理
      const pixelatedDataUrl = await pixelateImageToDataURL(proxyImg, {
        quality: enhancedQuality
      });
      
      // 更新图片
      img.src = pixelatedDataUrl;
      
      // 标记为已处理
      img.dataset.pixelated = "true";
      img.dataset.pixelSize = sizeCategory;
      
      // 记录已处理
      this.processedImages.set(img, {
        originalSrc: img.dataset.originalSrc,
        sizeCategory
      });
    } catch (error) {
      console.error('处理图片失败:', error, '图片URL:', img.dataset.originalSrc);
      
      // 错误处理 - 继续显示原始图片，并标记为跳过处理
      img.classList.add('pixelate-error');
      
      // 如果图片已经被修改，恢复原始图片
      if (img.dataset.originalSrc && img.src !== img.dataset.originalSrc) {
        img.src = img.dataset.originalSrc;
      }
    }
  }

  /**
   * 恢复所有处理过的图片
   */
  restoreImages() {
    for (const [img, data] of this.processedImages.entries()) {
      if (img && data.originalSrc) {
        img.src = data.originalSrc;
        img.removeAttribute('data-pixelated');
        img.removeAttribute('data-pixel-size');
        img.classList.remove('pixelate-error');
      }
    }
    
    this.processedImages.clear();
  }

  /**
   * 开始监测DOM变化
   */
  startObserving() {
    if (this.observer) return;
    
    this.observer = new MutationObserver(mutations => {
      const newImages = [];
      
      for (const mutation of mutations) {
        // 处理新添加的节点
        if (mutation.type === 'childList') {
          for (const node of mutation.addedNodes) {
            if (node.nodeName === 'IMG') {
              newImages.push(node);
            } else if (node.nodeType === Node.ELEMENT_NODE) {
              // 检查子元素中的图片
              const childImages = node.querySelectorAll('img:not(.no-pixelate)');
              newImages.push(...childImages);
            }
          }
          
          // 处理被移除的节点
          for (const node of mutation.removedNodes) {
            if (node.nodeType === Node.ELEMENT_NODE) {
              const removedImages = node.querySelectorAll('img');
              for (const img of removedImages) {
                this.processedImages.delete(img);
              }
            }
          }
        }
        // 处理图片src属性变化
        else if (mutation.type === 'attributes' && 
                 mutation.attributeName === 'src' && 
                 mutation.target.nodeName === 'IMG') {
          // 如果图片src变了，重新处理
          if (!mutation.target.classList.contains('no-pixelate') && 
              !mutation.target.src.startsWith('data:')) {
            newImages.push(mutation.target);
          }
        }
      }
      
      if (newImages.length > 0) {
        this.queueImagesForProcessing(newImages);
      }
    });
    
    // 开始监测
    this.observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['src']
    });
  }

  /**
   * 停止监测DOM变化
   */
  stopObserving() {
    if (this.observer) {
      this.observer.disconnect();
      this.observer = null;
    }
  }
}

// 创建单例
export const globalPixelate = new GlobalPixelateManager(); 