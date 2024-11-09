import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router';
import History from '../components/tailwind/History.vue';
import Search from '../components/tailwind/Search.vue';

const routes = [
    {
        path: '/',
        component: History
    },
    {
        path: '/page/:pageNumber',
        component: History
    },
    {
        path: '/search/:keyword',
        name: 'Search',
        component: Search
    }
];

// 创建路由实例的工厂函数
export const createMyRouter = (mode = 'hash') => {
    return createRouter({
        history: mode === 'hash' ? createWebHashHistory() : createWebHistory(),
        routes
    });
};

// 默认导出 hash 模式的路由（用于 Electron）
export default createMyRouter('hash');
