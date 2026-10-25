import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import MainLayout from '../components/tailwind/layout/MainLayout.vue'
import History from '../components/tailwind/page/History.vue'
import BrowserHistory from '../components/tailwind/page/BrowserHistory.vue'
import Settings from '../components/tailwind/Settings.vue'

export const createMyRouter = (mode = 'hash') => createRouter({
  history: mode === 'hash' ? createWebHashHistory() : createWebHistory(),
  routes: [{
    path: '/',
    component: MainLayout,
    children: [
      { path: '', component: History },
      { path: 'browser-history', component: BrowserHistory },
      { path: 'settings', component: Settings },
    ],
  }],
})
