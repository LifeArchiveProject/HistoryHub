<template>
  <div class="mt-2 mx-auto max-w-7xl sm:px-2 lg:px-8">
    <!-- 搜索框和总数显示容器 -->
    <div class="fixed top-0 left-0 right-0 bg-white z-50 p-1.5">
      <div class="relative mx-auto max-w-4xl p-1">
        <!-- 输入框 -->
        <input
            v-model="searchQuery"
            @keyup.enter="onSearch"
            type="search"
            placeholder="视频标题/oid"
            class="w-full p-3 rounded-lg border border-gray-300 bg-[#edf2fa] hover:bg-[#e1e6ed] focus:outline-none focus:ring-1 focus:ring-[#00A1D6] text-gray-900 lm:text-xs lg:text-lg"
        />
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
    <Pagination
        v-model:current-page="page"
        :total-pages="totalPages"
        :use-routing="false"
        @update:current-page="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { searchBiliHistory2024 } from "../../api/api.js";
import VideoRecord from "./VideoRecord.vue";
import Pagination from "./page/Pagination.vue";

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
const totalResults = ref(0);
const searchQuery = ref('');

// 处理页码变化
const handlePageChange = async (newPage) => {
  if (newPage !== page.value) {  // 只在页码实际改变时才请求
    page.value = newPage;
    await fetchSearchResults();
  }
};

// 获取搜索数据的函数
const fetchSearchResults = async () => {
  try {
    const response = await searchBiliHistory2024(
        page.value,
        size.value,
        keyword.value,  // 修改参数顺序，确保搜索关键词正确传递
        sortOrder.value
    );
    
    // 更新数据前先清空当前记录
    records.value = [];
    // 设置新的记录
    records.value = response.data.data.records;
    totalResults.value = response.data.data.total;
    totalPages.value = Math.ceil(response.data.data.total / size.value);
  } catch (error) {
    console.error('数据获取失败: ', error);
  }
};

// 监听 keyword 变化时的处理
watch(() => route.params.keyword, (newKeyword) => {
  if (newKeyword !== keyword.value) {  // 只在关键词实际改变时才重置
    keyword.value = newKeyword;
    page.value = 1; // 重置到第一页
    records.value = []; // 清空当前记录
    fetchSearchResults();
  }
});

// 组件挂载时获取数据
onMounted(() => {
  fetchSearchResults();
});

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
