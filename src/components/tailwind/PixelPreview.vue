<template>
  <div class="p-4 bg-white rounded-lg border border-gray-200">
    <h3 class="text-base font-medium text-gray-900 mb-3">图片像素化效果预览</h3>
    
    <div class="grid grid-cols-2 gap-4">
      <div class="border border-gray-200 rounded-lg p-2">
        <h4 class="text-sm font-medium text-gray-700 mb-2">原始图片</h4>
        <img 
          :src="demoImage" 
          alt="原始图片" 
          class="w-full h-auto rounded no-pixelate" 
        />
      </div>
      
      <div class="border border-gray-200 rounded-lg p-2">
        <h4 class="text-sm font-medium text-gray-700 mb-2">像素化效果</h4>
        <img 
          :src="pixelatedImage || demoImage" 
          alt="像素化效果" 
          class="w-full h-auto rounded pixelated" 
          :style="{ 
            imageRendering: usePixelImage ? 'pixelated' : 'auto' 
          }"
        />
      </div>
    </div>
    
    <div class="mt-4">
      <p class="text-sm text-gray-500">
        图片像素化可以为界面增添复古游戏风格，与像素字体搭配效果更佳。
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed, onUnmounted } from 'vue';
import { pixelateImageToDataURL } from '../../utils/pixelate';

// 演示用图片地址
const demoImage = '/demo-image.jpg'; // 使用一个项目中的图片
const pixelatedImage = ref(null);
const usePixelImage = ref(localStorage.getItem('usePixelImage') === 'true');
const pixelQuality = ref(parseInt(localStorage.getItem('pixelQuality') || '20'));

// 处理像素化
const applyPixelEffect = async () => {
  if (usePixelImage.value) {
    try {
      // 创建一个临时图片加载原图
      const img = new Image();
      img.crossOrigin = 'Anonymous';
      img.src = demoImage;
      
      // 等待图片加载完成
      await new Promise((resolve) => {
        img.onload = resolve;
      });
      
      // 应用像素化效果
      const dataUrl = await pixelateImageToDataURL(img, {
        quality: pixelQuality.value
      });
      
      pixelatedImage.value = dataUrl;
    } catch (error) {
      console.error('生成像素化图片预览失败:', error);
    }
  } else {
    pixelatedImage.value = null;
  }
};

// 监听像素化设置变更
watch([usePixelImage, pixelQuality], () => {
  applyPixelEffect();
});

// 监听全局设置变更事件
const handlePixelImageChanged = (event) => {
  if (event.detail) {
    usePixelImage.value = event.detail.usePixelImage;
    pixelQuality.value = event.detail.pixelQuality;
  }
};

onMounted(() => {
  // 应用初始像素化效果
  applyPixelEffect();
  
  // 监听全局设置变更事件
  window.addEventListener('pixel-image-changed', handlePixelImageChanged);
});

// 组件卸载时移除事件监听
onUnmounted(() => {
  window.removeEventListener('pixel-image-changed', handlePixelImageChanged);
});
</script>

<style scoped>
.pixelated {
  transition: filter 0.3s ease;
}
</style> 