<template>
  <div>
    <div class="mx-auto max-w-4xl px-1.5">
      <div class="flex justify-between text-lg text-gray-700 lm:text-sm">
        <div class="space-x-1" @click="show = true">
          <span>日期区间:</span>
          <span class="text-xs text-[#FF6699]">{{ date }}</span>
        </div>

        <!-- 总计视频数量显示 -->
        <div class="space-x-1">
          <span>总视频数:</span>
          <span class="text-xs text-[#FF6699]">{{ total }}</span>
        </div>

        <van-calendar
          :show-confirm="false"
          title="选择日期区间"
          switch-mode="year-month"
          v-model:show="show"
          :style="{ height: '65%' }"
          type="range"
          @confirm="onConfirm"
        />

        <div class="space-x-1" @click="showBottom = !showBottom">
          <span>视频分区:</span>
          <span class="text-xs text-[#FF6699]">{{ displayCategory || '全部分区' }}</span>
        </div>

        <!-- 通过 v-model 传递 showBottom 给子组件，并接收子分区选择 -->
        <VideoCategories
          v-model:showBottom="showBottom"
          @selectSubCategory="onSubCategorySelected"
        />
      </div>
    </div>

    <div>
      <VideoRecord v-for="record in records" :key="record.id" :record="record" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { getBiliHistory2024, getMainCategories } from '../../api/api.js'
import VideoRecord from './VideoRecord.vue'
import VideoCategories from './VideoCategories.vue'

const props = defineProps({
  selectedYear: {
    type: Number,
    required: true
  },
  page: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:total-pages', 'update:total'])

// 状态变量
const records = ref([])
const total = ref(0)
const sortOrder = ref(0)
const size = ref(30)

const date = ref('')
const dateRange = ref('')
const show = ref(false)

const showBottom = ref(false)
const tagName = ref('')
const mainCategory = ref('')
const mainCategories = ref([])

// 计算属性用于显示当前选中的分类
const displayCategory = computed(() => {
  return mainCategory.value || tagName.value || '全部分区'
})

// 获取主分区列表
const fetchMainCategories = async () => {
  try {
    const response = await getMainCategories()
    if (response.data.status === 'success') {
      mainCategories.value = response.data.data.map((cat) => cat.name)
    }
  } catch (error) {
    console.error('Error fetching main categories:', error)
  }
}

// 接收子组件传递的子分区并立即获取数据
const onSubCategorySelected = ({ name, type }) => {
  const isMainName = mainCategories.value.includes(name)

  if (type === 'main' || (type === 'sub' && isMainName)) {
    if (mainCategory.value === name) {
      mainCategory.value = ''
    } else {
      mainCategory.value = name
    }
    tagName.value = ''
  } else if (type === 'sub') {
    if (tagName.value === name) {
      tagName.value = ''
    } else {
      tagName.value = name
    }
    mainCategory.value = ''
  }

  fetchHistoryByDateRange()
}

// 辅助函数：格式化日期
const formatDate = (date) => `${date.getMonth() + 1}/${date.getDate()}`
const formatDateWithYear = (date) => `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
const formatDateForAPI = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}${month}${day}`
}

// 处理日期区间确认
const onConfirm = (values) => {
  const [start, end] = values
  show.value = false

  const startYear = start.getFullYear()
  const endYear = end.getFullYear()

  if (startYear === props.selectedYear && endYear === props.selectedYear) {
    date.value = `${formatDate(start)} - ${formatDate(end)}`
  } else {
    date.value = `${formatDateWithYear(start)} - ${formatDateWithYear(end)}`
  }

  dateRange.value = `${formatDateForAPI(start)}-${formatDateForAPI(end)}`
  fetchHistoryByDateRange()
}

// 数据获取函数
const fetchHistoryByDateRange = async () => {
  try {
    records.value = []
    const response = await getBiliHistory2024(
      props.page,
      size.value,
      sortOrder.value,
      tagName.value,
      mainCategory.value,
      dateRange.value
    )

    if (response.data && response.data.data) {
      total.value = response.data.data.total
      records.value = response.data.data.records
      emit('update:total-pages', Math.ceil(response.data.data.total / size.value))
      emit('update:total', response.data.data.total)
    }
  } catch (error) {
    console.error('数据获取失败:', error)
    records.value = []
    total.value = 0
    emit('update:total-pages', 0)
    emit('update:total', 0)
  }
}

// 监听年份和页码变化
watch(
  () => [props.selectedYear, props.page],
  () => {
    if (dateRange.value) {
      fetchHistoryByDateRange()
    }
  }
)

onMounted(async () => {
  await fetchMainCategories()
  const today = new Date()
  const startOfYear = new Date(props.selectedYear, 0, 1)
  onConfirm([startOfYear, today])
})
</script>
