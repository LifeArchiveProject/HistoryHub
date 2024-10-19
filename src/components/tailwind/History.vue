<template>
  <div class="mt-2 mx-auto max-w-7xl sm:px-2 lg:px-8">
    <!-- 搜索框 -->
    <div class="fixed top-0 left-0 right-0 bg-white z-50 px-1.5">
      <div class="relative mx-auto max-w-4xl p-1">
        <!-- 输入框 -->
        <input
            v-model="searchQuery"
            @keyup.enter="onSearch"
            type="search"
            placeholder="视频标题/oid"
            class="w-full p-2 rounded-lg border border-gray-300 bg-[#edf2fa] hover:bg-[#e1e6ed] focus:outline-none focus:ring-1 focus:ring-[#00A1D6] text-gray-900 lm:text-xs lg:text-lg"
        />
      </div>

      <div class="max-w-4xl mx-auto px-1.5">
        <div class="flex justify-between lm:text-sm text-gray-700 text-lg">
          <div class="space-x-1" @click="show = true">
            <span>日期区间:</span>
            <span class="text-[#FF6699] text-xs">{{ date }}</span>
          </div>

          <!-- 总计视频数量显示 -->
          <div class="space-x-1">
            <span>总视频数:</span>
            <span class="text-[#FF6699] text-xs">{{ total }}</span>
          </div>

          <van-calendar :show-confirm="false" title="选择日期区间" switch-mode="year-month"
                        v-model:show="show" :style="{ height: '65%' }" type="range" @confirm="onConfirm"/>

          <div class="space-x-1" @click="showBottom = !showBottom">
            <span>视频分区:</span>
            <span class="text-[#FF6699] text-xs">{{ displayCategory || '全部分区' }}</span>
          </div>

          <!-- 通过 v-model 传递 showBottom 给子组件，并接收子分区选择 -->
          <VideoCategories
              v-model:showBottom="showBottom"
              @selectSubCategory="onSubCategorySelected"
          />
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
        <button @click="prevPage" :disabled="page === 1"
                class="bg-[#00A1D6] text-white p-1 rounded-md disabled:opacity-50 disabled:cursor-not-allowed">上一页
        </button>

        <!-- 跳转框 -->
        <div class="flex items-center space-x-2 h-8">
          <input type="number" v-model="jumpPage" min="1" :max="totalPages"
                 class="h-7 border border-gray-300 rounded-lg p-1 w-20" placeholder="页码"/>
          <button @click="jumpToPage" class="bg-[#00A1D6] h-7 text-white px-1 rounded-md">跳转</button>
        </div>

        <p class="text-gray-700 pt-1.5">第 {{ page }} 页 / 共 {{ totalPages }} 页</p>

        <button @click="nextPage" :disabled="page === totalPages"
                class="bg-[#00A1D6] text-white p-1 rounded-md disabled:opacity-50 disabled:cursor-not-allowed">下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, computed} from 'vue';
import {getBiliHistory2024, getVideoCategories} from "../../api/api.js"; // 确保导入正确的 API 函数
import {useRouter} from 'vue-router';
import VideoRecord from "./VideoRecord.vue";
import VideoCategories from "./VideoCategories.vue";

// 状态变量
const records = ref([]);
const page = ref(1);
const size = ref(30); // 每页数据
const totalPages = ref(0);
const total = ref(0); // 视频总数
const jumpPage = ref(''); // 跳转页码输入框的值
const sortOrder = ref(0);

const date = ref('');
const dateRange = ref('');
const show = ref(false);

const currentYear = new Date().getFullYear();

const showBottom = ref(false); // 控制子组件显示的状态
const tagName = ref(''); // 选中的子分区
const mainCategory = ref(''); // 选中的主分区

// 计算属性用于显示当前选中的分类
const displayCategory = computed(() => {
  return mainCategory.value || tagName.value || '全部分区';
});

// 主分区列表
const mainCategories = ref([]);

// 获取主分区列表
const fetchMainCategories = async () => {
  try {
    const response = await getVideoCategories();
    // 假设返回的数据格式为 [{ mainCategory: '动画', subCategory: '动画' }, ...]
    // 提取主分区名称
    mainCategories.value = Array.from(new Set(response.data.data.map(cat => cat.mainCategory)));
  } catch (error) {
    console.error("Error fetching main categories:", error);
  }
};

// 接收子组件传递的子分区并立即获取数据
const onSubCategorySelected = ({name, type}) => {
  // 检查选中的名称是否在主分区列表中
  const isMainName = mainCategories.value.includes(name);

  if (type === 'main' || (type === 'sub' && isMainName)) {
    // 将其视为主分区
    if (mainCategory.value === name) {
      mainCategory.value = ''; // 取消选中
    } else {
      mainCategory.value = name; // 选择新的主分区
    }
    tagName.value = ''; // 确保 tagName 为空
  } else if (type === 'sub') {
    // 将其视为子分区
    if (tagName.value === name) {
      tagName.value = ''; // 取消选中
    } else {
      tagName.value = name; // 选择新的子分区
    }
    mainCategory.value = ''; // 确保 mainCategory 为空
  }

  // 重置页码并重新获取数据
  page.value = 1;
  fetchHistoryByDateRange();
};

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

// 处理日期区间确认
const onConfirm = (values) => {
  const [start, end] = values;
  show.value = false;

  const startYear = start.getFullYear();
  const endYear = end.getFullYear();

  // 判断日期区间是否在当前年份内
  if (startYear === currentYear && endYear === currentYear) {
    date.value = `${formatDate(start)} - ${formatDate(end)}`;
  } else {
    date.value = `${formatDateWithYear(start)} - ${formatDateWithYear(end)}`;
  }

  // 设置 dateRange 为 'yyyyMMdd-yyyyMMdd' 格式
  dateRange.value = `${formatDateForAPI(start)}-${formatDateForAPI(end)}`;

  // 重置页码为1
  page.value = 1;

  // 重新获取数据
  fetchHistoryByDateRange();
};

// 数据获取函数：基于日期区间和分类
const fetchHistoryByDateRange = async () => {
  try {
    const response = await getBiliHistory2024(
        page.value,
        size.value,
        sortOrder.value,
        tagName.value,
        mainCategory.value, // 传递 mainCategory
        dateRange.value
    );
    total.value = response.data.data.total;
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
  // 获取主分区列表
  fetchMainCategories();

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
