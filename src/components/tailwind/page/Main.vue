<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

onMounted(() => {
  // 确保从根路径访问时重定向到第一页
  if (window.location.pathname === '/') {
    router.push('/page/1');
  }
});
</script>

<template>
  <router-view></router-view>
</template>

<style scoped>

</style>
