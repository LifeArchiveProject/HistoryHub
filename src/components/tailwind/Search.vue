<template>
  <div class="mt-2 mx-auto max-w-7xl sm:px-2 lg:px-8">
    <!-- 搜索框和总数显示容器 -->
    <div class="fixed top-0 left-0 right-0 bg-white z-50 p-1.5">
      <div class="relative mx-auto max-w-4xl p-1">
        <!-- 输入框 -->
        <input
            v-model="searchQuery"
            @keyup.enter="onSearch"
            type="text"
            placeholder="视频标题/oid"
            class="w-full p-3 pr-14 rounded-lg border border-gray-300 bg-[#edf2fa] hover:bg-[#e1e6ed] focus:outline-none focus:ring-1 focus:ring-[#00A1D6] text-gray-900 lm:text-xs lg:text-lg"
        />
        <!-- 搜索按钮 -->
        <button
            @click="onSearch"
            class="lm:text-xs absolute top-1/2 right-2 transform -translate-y-1/2 bg-[#00A1D6] text-white rounded-lg transition-all duration-300 hover:bg-[#008ec1] p-2"
        >
          搜索
        </button>
      </div>

      <!-- 显示总条数，和输入框左端对齐 -->
      <div class="max-w-4xl mx-auto">
        <p class="text-gray-700 p-1.5 text-lg lm:text-sm">
          共 <span class="text-[#FF6699]">{{ totalResults }}</span> 条数据和
          <span class="text-[#FF6699]">{{ keyword }}</span> 相关
        </p>
      </div>
    </div>

    <!-- 使用 VideoRecord 组件展示每个记录 -->
    <div class="lm:pt-20 pt-[105px]"> <!-- 增加顶部填充，避免被固定元素遮盖 -->
      <VideoRecord
          v-for="record in records"
          :key="record.id"
          :record="record"
      />
    </div>

    <!-- 分页功能 -->
    <div class="mx-auto max-w-4xl mt-8 mb-5 lm:text-xs">
      <div class="flex justify-between space-x-4 lm:m-5">
        <!-- 上一页按钮 -->
        <button
            @click="prevPage"
            :disabled="page === 1"
            class="bg-[#00A1D6] text-white p-1 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
        >
          上一页
        </button>

        <!-- 跳转页码 -->
        <div class="flex items-center space-x-2">
          <input type="number" v-model="jumpPage" min="1" :max="totalPages" class="border border-gray-300 rounded-lg p-1 w-20" placeholder="页码" />
          <button @click="jumpToPage" class="bg-[#00A1D6] text-white p-1 rounded-md">跳转</button>
        </div>

        <!-- 页码显示 -->
        <p class="text-gray-700 pt-1.5">第 {{ page }} 页 / 共 {{ totalPages }} 页</p>

        <!-- 下一页按钮 -->
        <button
            @click="nextPage"
            :disabled="page === totalPages"
            class="bg-[#00A1D6] text-white p-1 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { searchBiliHistory2024 } from "../../api/api.js";
import VideoRecord from "./VideoRecord.vue";

// 获取路由参数
const route = useRoute();
const router = useRouter();
const keyword = ref(route.params.keyword);

// 状态变量
const records = ref([]);
const page = ref(1);
const size = ref(30);
const sortOrder = ref(0);
const totalPages = ref(0);
const totalResults = ref(0); // 保存总条数
const jumpPage = ref('');

// 获取搜索数据的函数
const fetchSearchResults = async () => {
  try {
    const response = await searchBiliHistory2024(page.value, size.value, sortOrder.value, keyword.value);
    records.value = response.data.data.records;
    totalPages.value = response.data.data.pages;
    totalResults.value = response.data.data.total; // 保存总条数
  } catch (error) {
    console.error('数据获取失败: ', error);
  }
};

// 翻页功能
const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++;
    fetchSearchResults();
  }
};

const prevPage = () => {
  if (page.value > 1) {
    page.value--;
    fetchSearchResults();
  }
};

// 跳转到指定页码的函数
const jumpToPage = () => {
  const targetPage = parseInt(jumpPage.value);
  if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= totalPages.value) {
    page.value = targetPage;
    fetchSearchResults();
  } else {
    alert(`请输入有效的页码（1-${totalPages.value}）`);
  }
};

// 监听 keyword 变化，重新获取搜索数据
watch(() => route.params.keyword, (newKeyword) => {
  keyword.value = newKeyword;
  page.value = 1; // 重置到第一页
  fetchSearchResults();
});

// 组件挂载时获取数据
onMounted(() => {
  fetchSearchResults();
});

// 搜索框绑定的搜索关键词
const searchQuery = ref('');

// 跳转到搜索页面的逻辑
const onSearch = () => {
  if (searchQuery.value.trim()) {
    // 构造新的 URL 地址
    const newUrl = router.resolve({
      name: 'Search',
      params: { keyword: searchQuery.value.trim() }
    }).href;

    // 在新标签页打开搜索结果
    window.open(newUrl, '_blank');
  } else {
    alert('请输入有效的搜索关键词');
  }
};
</script>
