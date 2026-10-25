<script setup>
import { useDarkMode } from './store/darkMode'

const { initDarkMode } = useDarkMode()
initDarkMode()
</script>

<template>
  <router-view />
</template>
