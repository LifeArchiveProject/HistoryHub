<template>
  <div class="flex h-[100dvh] flex-col bg-gray-50 dark:bg-gray-900 sm:flex-row">
    <aside class="shrink-0 border-b border-gray-200 bg-white px-4 py-3 dark:border-gray-700 dark:bg-gray-800 sm:w-48 sm:border-b-0 sm:border-r sm:py-6">
      <router-link to="/" class="flex items-center gap-2 text-lg font-bold text-gray-900 dark:text-gray-100">
        <img src="/logo.svg" alt="" class="h-7 w-7" />
        HistoryHub
      </router-link>
      <nav aria-label="主要导航" class="mt-3 flex gap-2 text-sm sm:mt-6 sm:flex-col">
        <router-link
          v-for="item in navigation"
          :key="item.to"
          :to="item.to"
          class="rounded-lg px-3 py-2 text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-700"
          :class="{ 'bg-[#fb7299]/10 !text-[#fb7299]': route.path === item.to }"
          :aria-current="route.path === item.to ? 'page' : undefined"
        >{{ item.label }}</router-link>
      </nav>
    </aside>
    <slot />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
const navigation = [
  { to: '/', label: 'B站历史' },
  { to: '/browser-history', label: '网页历史' },
  { to: '/settings', label: '设置' },
]
</script>
