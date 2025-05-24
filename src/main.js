import { createApp } from 'vue'
import './style.css'
// Vant的库，会在桌面端自动将 mouse 事件转换成对应的 touch 事件，使得组件能够在桌面端使用
import '@vant/touch-emulator'
import App from './App.vue'
import { createMyRouter } from './router/router' // 使用命名导入
import Vant from 'vant'
// 引入Vant组件样式
import 'vant/lib/index.css'
// 引入像素化插件
import { pixelatePlugin } from './utils/pixelDirective'

// 初始化custom event用于API模块间通信
window.addEventListener('api-baseurl-updated', (event) => {
  console.log('API BaseURL 已更新:', event.detail?.url)
})

// 初始化Tauri API
let isTauri = false
async function initTauri() {
  try {
    // 尝试导入Tauri core API
    const { invoke } = await import('@tauri-apps/api/core')
    if (typeof invoke === 'function') {
      // 设置全局标识
      window.__TAURI_INVOKE__ = invoke
      window.__TAURI__ = true
      isTauri = true
      console.log('Tauri API 初始化成功')
    }
  } catch (error) {
    isTauri = false
  }
}

// 立即初始化Tauri
await initTauri()


// 在 Tauri 环境中设置所有链接在当前窗口打开
if (isTauri) {
  // 重写默认的链接打开行为
  document.addEventListener('click', function(e) {
    // 查找点击事件中是否包含链接元素
    let target = e.target;
    while (target && target !== document) {
      if (target.tagName === 'A' && target.getAttribute('href')) {
        // 获取链接地址
        const href = target.getAttribute('href');

        // 如果是外部链接或绝对路径，则在当前窗口打开
        if (href.startsWith('http') || href.startsWith('//') || href.startsWith('/')) {
          e.preventDefault();
          window.location.href = href;
        }
        break;
      }
      target = target.parentNode;
    }
  }, true);
}

// 根据环境创建适当的路由实例
const router = createMyRouter(isTauri ? 'hash' : 'history')

const app = createApp(App)
app.use(router)
app.use(Vant)
// 注册像素化插件
app.use(pixelatePlugin)
app.mount('#app')
