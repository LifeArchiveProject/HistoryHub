<template>
  <!-- 圆角弹窗（底部） -->
  <van-popup
      v-model:show="localShowBottom"
      round
      position="bottom"
      :style="{ height: '80%' }"
  >
    <van-tree-select
        class="m-2"
        height="95%"
        v-model:active-id="activeId"
        v-model:main-active-index="activeIndex"
        :items="items"
        @click-item="onSelectItem"
    />
  </van-popup>
</template>

<script setup>
import { defineProps, defineEmits, computed, onMounted, ref } from 'vue';
import { getVideoCategories } from "../../api/api.js";

// 定义 props 接受父组件传递的 showBottom
const props = defineProps({
  showBottom: {
    type: Boolean,
    default: false
  }
});

// 定义 emits 用于向父组件发送事件
const emit = defineEmits(['update:showBottom', 'selectSubCategory']);

// 定义状态
const activeId = ref(null);
const activeIndex = ref(0);
const items = ref([]); // 用于存放转换后的items结构

// 计算属性，用于实现双向绑定
const localShowBottom = computed({
  get() {
    return props.showBottom;
  },
  set(value) {
    emit('update:showBottom', value);
  }
});

// 定义数据转换函数，添加 type 字段
const transformDataToItems = (data) => {
  const transformedItems = [];

  data.forEach((category) => {
    let existingMainCategory = transformedItems.find(item => item.text === category.mainCategory);

    if (existingMainCategory) {
      existingMainCategory.children.push({ text: category.subCategory, id: category.id, type: 'sub' });
    } else {
      transformedItems.push({
        text: category.mainCategory,
        type: 'main',
        children: [{ text: category.subCategory, id: category.id, type: 'sub' }],
      });
    }
  });

  return transformedItems;
};

// 获取视频分类并转换数据结构
const fetchCategories = async () => {
  try {
    const response = await getVideoCategories();
    items.value = transformDataToItems(response.data.data); // 更新items为转换后的数据
  } catch (error) {
    console.error("Error fetching video categories:", error);
  }
};

// 当选中分类时，发出事件并传递 name 和 type
const onSelectItem = (item) => {
  emit('selectSubCategory', { name: item.text, type: item.type });
};

// 页面加载时获取数据
onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
</style>
