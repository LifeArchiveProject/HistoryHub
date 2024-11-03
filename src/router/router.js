import {createRouter, createWebHistory, createWebHashHistory} from 'vue-router';
import Search from "../components/tailwind/page/Search.vue";
import History from "../components/tailwind/History.vue";

const routes = [
    {
        path: '/',
        name: 'History',
        component: History
    },
    {
        path: '/page/:pageNumber',
        name: 'HistoryPage',
        component: History,
        props: true
    },
    {
        path: '/search/:keyword',
        name: 'Search',
        component: Search,
        props: true
    },
];

const isElectron = () => {
    return navigator.userAgent.toLowerCase().indexOf(' electron/') > -1;
};

const router = createRouter({
    history: isElectron() ? createWebHashHistory() : createWebHistory(),
    routes,
});

export default router;
