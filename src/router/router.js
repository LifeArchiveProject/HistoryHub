import Main from "../components/tailwind/page/Main.vue";
import Search from "../components/tailwind/page/Search.vue";


const routes = [
    {
        path: '/',
        name: 'Home',
        component: Main // 使用 component 而非 components
    },
    {
        path: '/search/:keyword',
        name: 'Search',
        component: Search,
        props: {search: true}
    },
];

export default routes;
