<template>
  <van-popup
    :show="show"
    @update:show="$emit('update:show', $event)"
    position="bottom"
    :style="{ height: '35%' }"
    round
  >
    <div class="pt-6 px-3">
      <div class="grid grid-cols-2 gap-2">
        <!-- 全部 -->
        <div
          class="flex items-center p-2 rounded-lg cursor-pointer border"
          :class="selectedType === '' ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 hover:border-[#fb7299]/50'"
          @click="selectType('')"
        >
          <div class="flex-1">
            <div class="font-medium">全部</div>
            <div class="text-xs text-gray-500">显示所有类型</div>
          </div>
          <div v-if="selectedType === ''" class="text-[#fb7299]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
        
        <!-- 普通视频 -->
        <div
          class="flex items-center p-2 rounded-lg cursor-pointer border"
          :class="selectedType === 'archive' ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 hover:border-[#fb7299]/50'"
          @click="selectType('archive')"
        >
          <div class="flex-1">
            <div class="font-medium">普通视频</div>
            <div class="text-xs text-gray-500">B站普通投稿视频</div>
          </div>
          <div v-if="selectedType === 'archive'" class="text-[#fb7299]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
        
        <!-- 番剧 -->
        <div
          class="flex items-center p-2 rounded-lg cursor-pointer border"
          :class="selectedType === 'pgc' ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 hover:border-[#fb7299]/50'"
          @click="selectType('pgc')"
        >
          <div class="flex-1">
            <div class="font-medium">番剧</div>
            <div class="text-xs text-gray-500">番剧、电影、纪录片等</div>
          </div>
          <div v-if="selectedType === 'pgc'" class="text-[#fb7299]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
        
        <!-- 直播 -->
        <div
          class="flex items-center p-2 rounded-lg cursor-pointer border"
          :class="selectedType === 'live' ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 hover:border-[#fb7299]/50'"
          @click="selectType('live')"
        >
          <div class="flex-1">
            <div class="font-medium">直播</div>
            <div class="text-xs text-gray-500">B站直播间</div>
          </div>
          <div v-if="selectedType === 'live'" class="text-[#fb7299]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
        
        <!-- 文章 -->
        <div
          class="flex items-center p-2 rounded-lg cursor-pointer border"
          :class="selectedType === 'article' ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 hover:border-[#fb7299]/50'"
          @click="selectType('article')"
        >
          <div class="flex-1">
            <div class="font-medium">文章</div>
            <div class="text-xs text-gray-500">B站专栏文章</div>
          </div>
          <div v-if="selectedType === 'article'" class="text-[#fb7299]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
        
        <!-- 文集 -->
        <div
          class="flex items-center p-2 rounded-lg cursor-pointer border"
          :class="selectedType === 'article-list' ? 'border-[#fb7299] bg-[#fb7299]/5' : 'border-gray-200 hover:border-[#fb7299]/50'"
          @click="selectType('article-list')"
        >
          <div class="flex-1">
            <div class="font-medium">文集</div>
            <div class="text-xs text-gray-500">B站专栏文集</div>
          </div>
          <div v-if="selectedType === 'article-list'" class="text-[#fb7299]">
            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  </van-popup>
</template>

<script setup>
import { ref, watch } from 'vue'
import 'vant/es/popup/style'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  selectedBusiness: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:show', 'select'])

// 当前选中的类型
const selectedType = ref(props.selectedBusiness)

// 监听props变化
watch(() => props.selectedBusiness, (newVal) => {
  selectedType.value = newVal
})

// 监听show变化，当弹窗显示时重新同步selectedType
watch(() => props.show, (newVal) => {
  if (newVal) {
    selectedType.value = props.selectedBusiness
  }
})

// 选择类型
const selectType = (type) => {
  selectedType.value = type
  emit('select', type)
  emit('update:show', false)
}

// 业务类型映射表
const businessTypeMap = {
  '': '全部',
  'archive': '普通视频',
  'pgc': '番剧',
  'live': '直播',
  'article': '文章',
  'article-list': '文集'
}

// 导出映射表，方便外部使用
defineExpose({
  businessTypeMap
})
</script> 