import { applyPixelEffect, removePixelEffect } from './pixelate';

/**
 * Vue自定义指令: v-pixelate
 *
 * 用法:
 *   v-pixelate="true" - 启用像素化
 *   v-pixelate="false" - 禁用像素化
 *   v-pixelate="{ quality: 30 }" - 自定义配置
 */
export const pixelateDirective = {
  mounted(el, binding) {
    // 确保元素是图片
    if (el.tagName !== 'IMG') {
      console.warn('v-pixelate 仅支持作用于 <img> 元素');
      return;
    }

    // 存储原始src
    el._originalSrc = el.src;

    // 初始化配置
    el._pixelateOptions = {
      quality: 50,
      ...(typeof binding.value === 'object' ? binding.value : {})
    };

    // 如果指令值为true或对象，则应用像素化
    if (binding.value === true || typeof binding.value === 'object') {
      // 如果图片已加载，则直接应用
      if (el.complete) {
        applyPixelEffect(el, el._pixelateOptions);
      } else {
        // 否则等待图片加载完成
        el.addEventListener('load', function onLoad() {
          applyPixelEffect(el, el._pixelateOptions);
          el.removeEventListener('load', onLoad);
        });
      }
    }
  },

  updated(el, binding) {
    // 判断值是否改变
    const newValue = binding.value;
    const oldValue = binding.oldValue;

    // 如果值未改变，则不执行操作
    if (newValue === oldValue) return;

    // 更新配置
    if (typeof newValue === 'object') {
      el._pixelateOptions = {
        quality: 50,
        ...newValue
      };
    }

    // 应用或移除像素化
    if (newValue === true || typeof newValue === 'object') {
      applyPixelEffect(el, el._pixelateOptions);
    } else if (newValue === false) {
      removePixelEffect(el);
    }
  },

  unmounted(el) {
    // 重置为原始图片
    if (el._originalSrc) {
      el.src = el._originalSrc;
      el.style.imageRendering = '';
    }
  }
};

// 用于全局注册
export const pixelatePlugin = {
  install(app) {
    app.directive('pixelate', pixelateDirective);
  }
};
