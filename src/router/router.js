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
    },
    {
        path: '/search/:keyword/page/:pageNumber',
        name: 'SearchPage',
        component: Search
    }
];

// 创建路由实例的工厂函数
export const createMyRouter = (mode = 'hash') => {
    console.log('创建路由实例，模式:', mode);

    const history = mode === 'hash' ? createWebHashHistory() : createWebHistory();
    console.log('使用的 history 类型:', history);

    return createRouter({
        history,
        routes
    });
};
