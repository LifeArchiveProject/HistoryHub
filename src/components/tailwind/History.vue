<template>
  <div class="mt-2 mx-auto max-w-7xl sm:px-2 lg:px-8">
    <!-- 搜索框 -->
    <div class="fixed top-0 left-0 right-0 bg-white z-50 px-1.5">
      <div class="relative mx-auto max-w-4xl p-1">
        <!-- 输入框，设置默认背景和悬停背景颜色 -->
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

      <div class="max-w-4xl mx-auto">
        <div class="lm:text-sm text-gray-700 text-lg">
          <div class="flex justify-between px-1.5" @click="show = true">
            <p>选择历史记录的日期区间</p>
            <span class="text-[#FF6699]">{{ date }}</span>
          </div>
          <van-calendar :show-confirm="false" title="选择日期区间" color="#FF6699" switch-mode="year-month" v-model:show="show" type="range" @confirm="onConfirm"/>
        </div>
      </div>
    </div>


    <div class="pt-20 lm:pt-14">
      <VideoRecord
          v-for="record in records"
          :key="record.id"
          :record="record"
      />
    </div>

    <!-- 修改分页按钮容器的最大宽度 -->
    <div class="mx-auto max-w-4xl mt-8 mb-5 lm:text-xs">
      <div class="flex justify-between space-x-4 lm:m-5">
        <!-- 上一页按钮 -->
        <button @click="prevPage" :disabled="page === 1"
                class="bg-[#00A1D6] text-white p-1 rounded-md disabled:opacity-50 disabled:cursor-not-allowed">上一页
        </button>

        <!-- 跳转框 -->
        <div class="flex items-center space-x-2 h-8">
          <input type="number" v-model="jumpPage" min="1" :max="totalPages"
                 class="h-7 border border-gray-300 rounded-lg p-1 w-20" placeholder="页码"/>
          <button @click="jumpToPage" class="bg-[#00A1D6] h-7 text-white px-1 rounded-md">跳转</button>
        </div>

        <!-- 页码显示 -->
        <p class="text-gray-700 pt-1.5">第 {{ page }} 页 / 共 {{ totalPages }} 页</p>

        <!-- 下一页按钮 -->
        <button @click="nextPage" :disabled="page === totalPages"
                class="bg-[#00A1D6] text-white p-1 rounded-md disabled:opacity-50 disabled:cursor-not-allowed">下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue';
import {getHistoryByDay} from "../../api/api.js"; // 确保导入正确的 API 函数
import {useRouter} from 'vue-router';
import VideoRecord from "./VideoRecord.vue";

// 状态变量
const records = ref([]);
const page = ref(1);
const size = ref(30); // 每页数据
const totalPages = ref(0);
const jumpPage = ref(''); // 跳转页码输入框的值

const date = ref('');
const dateRange = ref('');
const show = ref(false);

const currentYear = new Date().getFullYear();

// 辅助函数：格式化日期为 'MM/DD'（不含年份）
const formatDate = (date) => `${date.getMonth() + 1}/${date.getDate()}`;

// 辅助函数：格式化日期为 'YYYY/MM/DD'（含年份）
const formatDateWithYear = (date) => `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`;

// 辅助函数：格式化日期为 'yyyyMMdd' 用于 API
const formatDateForAPI = (date) => {
  const year = date.getFullYear();
  const month = (`0${date.getMonth() + 1}`).slice(-2);
  const day = (`0${date.getDate()}`).slice(-2);
  return `${year}${month}${day}`;
};

const onConfirm = (values) => {
  const [start, end] = values;
  show.value = false;

  const startYear = start.getFullYear();
  const endYear = end.getFullYear();

  // 判断日期区间是否在当前年份内
  if (startYear === currentYear && endYear === currentYear) {
    date.value = `${formatDate(start)} - ${formatDate(end)}`;
  } else {
    // 显示年份
    date.value = `${formatDateWithYear(start)} - ${formatDateWithYear(end)}`;
  }

  // 设置 dateRange 为 'yyyyMMdd-yyyyMMdd' 格式
  dateRange.value = `${formatDateForAPI(start)}-${formatDateForAPI(end)}`;

  // 重置页码为1
  page.value = 1;

  // 重新获取数据
  fetchHistoryByDateRange();
};

// 数据获取函数：基于日期区间
const fetchHistoryByDateRange = async () => {
  try {
    const response = await getHistoryByDay(page.value, size.value, dateRange.value);
    records.value = response.data.data.records;
    totalPages.value = response.data.data.pages;
  } catch (error) {
    console.error('数据获取失败: ', error);
  }
};

// 跳转到指定页码的函数
const jumpToPage = () => {
  const targetPage = parseInt(jumpPage.value);
  if (!isNaN(targetPage) && targetPage >= 1 && targetPage <= totalPages.value) {
    page.value = targetPage;
    fetchHistoryByDateRange(); // 重新获取数据
  } else {
    alert(`请输入有效的页码（1-${totalPages.value}）`);
  }
};

// 翻页功能
const nextPage = () => {
  if (page.value < totalPages.value) {
    page.value++;
    fetchHistoryByDateRange();
  }
};

const prevPage = () => {
  if (page.value > 1) {
    page.value--;
    fetchHistoryByDateRange();
  }
};

// 组件挂载时获取数据
onMounted(() => {
  // 默认日期范围为当前年份的起始到当前日期
  const today = new Date();
  const startOfYear = new Date(currentYear, 0, 1);
  onConfirm([startOfYear, today]);
});

// 路由对象
const router = useRouter();

// 搜索框绑定的搜索关键词
const searchQuery = ref('');

// 跳转到搜索页面的逻辑
const onSearch = () => {
  if (searchQuery.value.trim()) {
    // 构造新的 URL 地址
    const newUrl = router.resolve({
      name: 'Search',
      params: {keyword: searchQuery.value.trim()}
    }).href;

    // 在新标签页打开搜索结果
    window.open(newUrl, '_blank');
  } else {
    alert('请输入有效的搜索关键词');
  }
};
</script>

<style scoped>
button {
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #008ec1;
}
</style>
