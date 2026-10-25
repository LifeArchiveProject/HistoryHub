<template>
  <div class="relative">
    <div class="flex h-9 items-center rounded-md border border-gray-300 dark:border-gray-600 bg-transparent focus-within:border-[#fb7299] transition-colors duration-200">
      <!-- 搜索图标 -->
      <div class="pl-3 text-gray-400 dark:text-gray-500">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      
      <!-- 输入框 -->
      <input
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        type="search"
        :placeholder="placeholder"
        class="h-full w-full border-none bg-transparent px-2 pr-3 text-gray-700 dark:text-gray-200 focus:outline-none focus:ring-0 text-xs leading-none"
        @keyup.enter="$emit('search')"
        @search="$emit('search')"
      />
    </div>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '输入关键词搜索...'
  }
})

defineEmits(['update:modelValue', 'search'])
</script>

<style scoped>
/* 移除搜索框的默认样式 */
input[type="search"]::-webkit-search-decoration,
input[type="search"]::-webkit-search-cancel-button,
input[type="search"]::-webkit-search-results-button,
input[type="search"]::-webkit-search-results-decoration {
  display: none;
}

/* 移除输入框的默认focus样式 */
input:focus {
  box-shadow: none !important;
  outline: none !important;
}
</style> 