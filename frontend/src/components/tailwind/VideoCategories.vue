<template>
  <!-- 圆角弹窗（底部） -->
  <van-popup v-model:show="localShowBottom" round position="bottom" :style="{ height: '80%' }">
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
import { computed, onMounted, ref } from 'vue'
import { getVideoCategories } from '../../api/api.js'

const emit = defineEmits(['update:category', 'update:showBottom', 'selectSubCategory'])

const props = defineProps({
  category: {
    type: String,
    default: ''
  },
  showBottom: {
    type: Boolean,
    default: false,
  },
})

// 定义状态
const activeId = ref(null)
const activeIndex = ref(0)
const items = ref([]) // 用于存放转换后的items结构

// 计算属性，用于实现双向绑定
const localShowBottom = computed({
  get() {
    return props.showBottom
  },
  set(value) {
    emit('update:showBottom', value)
  },
})

// 获取视频分类并转换数据结构
const fetchCategories = async () => {
  try {
    const response = await getVideoCategories()
    if (response.data.status === 'success') {
      // 转换数据结构以适应组件
      items.value = response.data.data.map((category) => ({
        text: category.name,
        type: 'main',
        children: category.sub_categories.map((sub) => ({
          text: sub.name,
          id: sub.tid,
          type: 'sub',
        })),
      }))
    }
  } catch (error) {
    console.error('Error fetching categories:', error)
  }
}

// 当选中分类时，发出事件并传递 name 和 type
const onSelectItem = (item) => {
  emit('selectSubCategory', { name: item.text, type: item.type })
}

// 页面加载时获取数据
onMounted(() => {
  fetchCategories()
})
</script>

<style scoped></style>
