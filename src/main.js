import { createApp } from 'vue';
import './style.css';
// Vant的库，会在桌面端自动将 mouse 事件转换成对应的 touch 事件，使得组件能够在桌面端使用
import '@vant/touch-emulator';
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router';
import routes from './router/router.js'; // 确保正确导入路由配置文件
import Vant from 'vant';
// 引入Vant组件样式
import 'vant/lib/index.css';

const router = createRouter({
    history: createWebHistory(),
    routes,
});

const app = createApp(App);
app.use(router);
app.use(Vant);
app.mount('#app');
