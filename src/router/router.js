import {createRouter, createWebHistory, createWebHashHistory} from 'vue-router';
import Main from "../components/tailwind/page/Main.vue";
import Search from "../components/tailwind/page/Search.vue";
import History from "../components/tailwind/History.vue";

const routes = [
    {
        path: '/',
        redirect: '/page/1'
    },
    {
        path: '/page/:pageNumber',
        name: 'History',
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
