import { createApp } from 'vue';
import './style.css';
// Vant的库，会在桌面端自动将 mouse 事件转换成对应的 touch 事件，使得组件能够在桌面端使用
import '@vant/touch-emulator';
import App from './App.vue';
import { createMyRouter } from './router/router';
import Vant from 'vant';
// 引入Vant组件样式
import 'vant/lib/index.css';

// 判断是否在 Electron 环境中
const isElectron = window && window.process && window.process.type;

// 根据环境创建适当的路由实例
const router = createMyRouter(isElectron ? 'hash' : 'history');

const app = createApp(App);
app.use(router);
app.use(Vant);
app.mount('#app');
