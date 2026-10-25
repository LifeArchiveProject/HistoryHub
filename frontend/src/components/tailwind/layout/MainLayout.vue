<template>
  <Sidebar>
    <main class="min-h-0 min-w-0 flex-1 overflow-hidden">
      <router-view />
    </main>
  </Sidebar>
</template>

<script setup>
import Sidebar from '../Sidebar.vue'
</script>
