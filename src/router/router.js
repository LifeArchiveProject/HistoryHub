import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
import History from '../components/tailwind/page/History.vue'
import Search from '../components/tailwind/page/Search.vue'
import AnimatedAnalytics from '../components/tailwind/page/AnimatedAnalytics.vue'
import Settings from '../components/tailwind/Settings.vue'
import MainLayout from '../components/tailwind/layout/MainLayout.vue'
import Images from '../components/tailwind/page/Images.vue'
import SchedulerTasks from '../components/tailwind/page/SchedulerTasks.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        component: History,
      },
      {
        path: 'page/:pageNumber',
        component: History,
      },
      {
        path: 'search/:keyword',
        name: 'Search',
        component: Search,
      },
      {
        path: 'search/:keyword/page/:pageNumber',
        name: 'SearchPage',
        component: Search,
      },
      {
        path: 'analytics',
        name: 'AnimatedAnalytics',
        component: AnimatedAnalytics,
      },
      {
        path: 'settings',
        name: 'Settings',
        component: Settings,
      },
      {
        path: 'remarks',
        name: 'Remarks',
        component: History,
        props: { defaultShowRemarks: true }
      },
      {
        path: 'images',
        name: 'Images',
        component: Images
      },
      {
        path: 'scheduler',
        name: 'SchedulerTasks',
        component: SchedulerTasks
      }
    ]
  }
]

// 创建路由实例的工厂函数
export const createMyRouter = (mode = 'hash') => {
  console.log('创建路由实例，模式:', mode)

  const history = mode === 'hash' ? createWebHashHistory() : createWebHistory()
  console.log('使用的 history 类型:', history)

  return createRouter({
    history,
    routes,
  })
}
