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

    <!-- 将固定定位的分页组件改为正常流式布局 -->
    <div class="mx-auto max-w-4xl mt-8 mb-5">
      <Pagination
          :current-page="page"
          :total-pages="totalPages"
          :use-routing="true"
      />
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, watch, computed} from 'vue';
import {getBiliHistory2024, getMainCategories} from "../../api/api.js"; // 确保导入正确的 API 函数
import {useRouter, useRoute} from 'vue-router';
import VideoRecord from "./VideoRecord.vue";
import VideoCategories from "./VideoCategories.vue";
import Pagination from "./page/Pagination.vue";

// 将 currentPageInput 的声明移到最前面
const currentPageInput = ref('1');

// 其他状态变量
const records = ref([]);
const page = ref(1);
const size = ref(30);
const totalPages = ref(0);
const total = ref(0);
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
    // 使用新的主分类接口
    const response = await getMainCategories();
    if (response.data.status === 'success') {
      // 提取主分区名称
      mainCategories.value = response.data.data.map(cat => cat.name);
    }
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
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}${month}${day}`;
};

// 处理日期区间确认
const onConfirm = (values) => {
  const [start, end] = values;
  show.value = false;

  const startYear = start.getFullYear();
  const endYear = end.getFullYear();

  if (startYear === currentYear && endYear === currentYear) {
    date.value = `${formatDate(start)} - ${formatDate(end)}`;
  } else {
    date.value = `${formatDateWithYear(start)} - ${formatDateWithYear(end)}`;
  }

  dateRange.value = `${formatDateForAPI(start)}-${formatDateForAPI(end)}`;

  console.log('日期范围:', dateRange.value);

  if (page.value !== 1) {
    router.push('/');
  } else {
    fetchHistoryByDateRange();
  }
};

// 数据获取函数：基于日期区间和分类
const fetchHistoryByDateRange = async () => {
  try {
    records.value = [];
    const response = await getBiliHistory2024(
        page.value,
        size.value,
        sortOrder.value,
        tagName.value,
        mainCategory.value,
        dateRange.value
    );

    if (response.data && response.data.data) {
        total.value = response.data.data.total;
        records.value = response.data.data.records;
        totalPages.value = Math.ceil(response.data.data.total / size.value);

        if (response.data.data.current !== page.value) {
            page.value = response.data.data.current;
        }
    }
  } catch (error) {
    console.error('数据获取失败:', error);
    records.value = [];
    total.value = 0;
    totalPages.value = 0;
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
const route = useRoute();

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

// 修改路由参数监听部分
watch(
    [() => route.params.pageNumber, () => route.path],
    ([newPage, path], [oldPage, oldPath]) => {
        if (newPage === oldPage && path === oldPath) return;

        if (path === '/') {
            if (page.value !== 1) {
                page.value = 1;
                currentPageInput.value = '1';
                fetchHistoryByDateRange();
            }
        } else if (newPage) {
            const pageNum = parseInt(newPage);
            if (page.value !== pageNum) {
                page.value = pageNum;
                currentPageInput.value = newPage;
                fetchHistoryByDateRange();
            }
        }
    },
    { immediate: true }
);
</script>

<style scoped>
button {
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #008ec1;
}
</style>
