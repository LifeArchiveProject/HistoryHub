<template>
  <nav class="fixed left-0 right-0 top-0 z-50 bg-white dark:bg-gray-800 shadow-sm">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="flex h-16 justify-between items-center">
        <!-- Logo -->
        <div class="flex-shrink-0 flex items-center">
          <router-link to="/" class="flex items-center space-x-2">
            <svg class="h-8 w-8 text-gray-900 dark:text-white" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg">
              <path fill="currentColor" d="M306.005333 117.632L444.330667 256h135.296l138.368-138.325333a42.666667 42.666667 0 0 1 60.373333 60.373333L700.330667 256H789.333333A149.333333 149.333333 0 0 1 938.666667 405.333333v341.333334a149.333333 149.333333 0 0 1-149.333334 149.333333h-554.666666A149.333333 149.333333 0 0 1 85.333333 746.666667v-341.333334A149.333333 149.333333 0 0 1 234.666667 256h88.96L245.632 177.962667a42.666667 42.666667 0 0 1 60.373333-60.373334zM789.333333 341.333333h-554.666666a64 64 0 0 0-63.701334 57.856L170.666667 405.333333v341.333334a64 64 0 0 0 57.856 63.701333L234.666667 810.666667h554.666666a64 64 0 0 0 63.701334-57.856L853.333333 746.666667v-341.333334A64 64 0 0 0 789.333333 341.333333zM341.333333 469.333333a42.666667 42.666667 0 0 1 42.666667 42.666667v85.333333a42.666667 42.666667 0 0 1-85.333333 0v-85.333333a42.666667 42.666667 0 0 1 42.666666-42.666667z m341.333334 0a42.666667 42.666667 0 0 1 42.666666 42.666667v85.333333a42.666667 42.666667 0 0 1-85.333333 0v-85.333333a42.666667 42.666667 0 0 1 42.666667-42.666667z"></path>
            </svg>
            <span class="text-lg font-semibold text-gray-900 dark:text-white hidden sm:block">B站历史记录</span>
          </router-link>
        </div>

        <!-- 搜索框 -->
        <div class="flex-1 max-w-2xl mx-4">
          <SearchBar />
        </div>

        <!-- 年度总结入口 -->
        <div class="flex-shrink-0">
          <router-link 
            to="/analytics" 
            class="inline-flex items-center rounded-lg border border-transparent p-2 text-white lm:text-xs lg:text-lg bg-gradient-to-r from-[#FF6699] to-[#FF9966] hover:from-[#FF5588] hover:to-[#FF8855] transition-all duration-300"
          >
            <svg class="w-4 h-4 lg:w-5 lg:h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <span>年度总结</span>
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import SearchBar from './SearchBar.vue'
</script>

<style scoped>
/* 如果需要添加特定样式可以在这里添加 */
</style> 