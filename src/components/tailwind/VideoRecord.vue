<template>
  <!-- 每条记录的容器，添加边框和圆角 -->
  <div class="border-b border-gray-200 mx-auto max-w-2xl space-y-8 sm:px-4 lg:max-w-4xl lg:px-0">
    <!-- 内层容器，加入 padding 以确保内容有足够的内边距 -->
    <div class="p-2">
      <!-- 当类型为文章或文集时，图片铺满整行，标题在上方 -->
      <div v-if="record.business === 'article-list' || record.business === 'article'">
        <!-- 标题在封面图片上方 -->
        <div class="mb-2">
          <div class="text-gray-900 lm:text-sm lg:font-semibold line-clamp-2">{{ record.title }}</div>
        </div>
        <!-- 封面图片，铺满整行 -->
        <div class="h-28 w-full overflow-hidden rounded-lg relative">
          <img :src="record.cover || record.covers[0]" class="h-full w-full object-cover" alt=""/>
          <!-- 右上角的类型角标，仅当不是稿件时显示 -->
          <div v-if="record.business !== 'archive'"
               class="absolute top-1 right-1 bg-[#FF6699] text-white text-[10px] rounded px-1 py-0.5">
            {{ getBusinessType(record.business) }}
          </div>
        </div>
        <!-- 文章类型：作者信息、观看设备、时间放在封面图片下方 -->
        <div class="flex justify-between items-center mt-2 lm:text-xs text-sm text-[#99a2aa]">
          <!-- 左侧：仅当类型不是剧集或课程时，显示作者头像和名字 -->
          <div v-if="record.business !== 'cheese' && record.business !== 'pgc'" class="flex items-center space-x-2">
            <img :src="record.authorFace" alt="author" class="w-4 h-4 lg:w-8 lg:h-8 rounded-full"/>
            <p>{{ record.authorName }}</p>
          </div>

          <!-- 右侧：设备和时间信息 -->
          <div class="flex items-center space-x-2">
            <img v-if="record.dt === 1 || record.dt === 3 || record.dt === 5 || record.dt === 7" src="/Mobile.svg"
                 alt="Mobile" class="w-4 h-4 lg:w-8 lg:h-8"/>

            <img v-else-if="record.dt === 2 || record.dt === 33" src="/public/PC.svg" alt="PC"
                 class="w-4 h-4 lg:w-8 lg:h-8"/>

            <img v-else-if="record.dt === 4 || record.dt === 6" src="/public/Pad.svg" alt="Pad"
                 class="w-4 h-4 lg:w-8 lg:h-8"/>

            <p v-else>未知设备</p>

            <!-- 显示时间 -->
            <span>{{ formatTimestamp(record.viewAt) }}</span>
          </div>
        </div>
      </div>

      <!-- 其他类型的展示方式 -->
      <div v-else class="flex space-x-2">
        <!-- 封面图片区域，设置为 relative，方便放置绝对定位的角标 -->
        <div class="h-20 w-32 overflow-hidden rounded-lg sm:h-28 sm:w-40 relative">
          <img v-if="record.cover" :src="record.cover" class="h-full w-full object-cover" alt=""/>
          <div v-else>
            <div v-for="(cover, index) in record.covers" :key="index" class="mb-1">
              <img :src="cover" class="h-full w-full object-cover" alt=""/>
            </div>
          </div>
          <!-- 右上角的类型角标，稿件不显示角标 -->
          <div v-if="record.business !== 'archive'"
               class="absolute top-1 right-1 bg-[#FF6699] text-white text-[10px] font-semibold rounded px-1 py-0.5">
            {{ getBusinessType(record.business) }}
          </div>
          <!-- 右下角的时间进度角标和进度条，仅当不是文章时显示 -->
          <div v-if="record.business !== 'article-list' && record.business !== 'article' && record.business !== 'live'">
            <div class="absolute bottom-1 right-1 bg-black/50 text-white text-[10px] font-semibold rounded px-1 py-1">
              <span>{{ formatDuration(record.progress) }}</span>
              <span>/</span>
              <span>{{ formatDuration(record.duration) }}</span>
            </div>
            <div class="absolute bottom-0 left-0 w-full h-0.5 bg-black">
              <div class="h-full bg-[#FF6699]"
                   :style="{ width: getProgressWidth(record.progress, record.duration) }"></div>
            </div>
          </div>
        </div>

        <!-- 右侧内容区域 -->
        <div class="ml-2 flex-1 flex flex-col justify-between lm:text-sm lg:font-semibold">
          <div class="lg:flex justify-between items-center">
            <div class="text-gray-900 lm:text-sm lg:font-semibold line-clamp-2">{{ record.title }}</div>
          </div>
          <div>
            <span class="inline-flex items-center rounded-md bg-[#f1f2f3] px-2 py-1 text-xs text-[#71767d]">
              {{ record.tagName }}
            </span>
          </div>

          <div class="flex justify-between items-end lm:text-xs text-sm text-[#99a2aa]">
            <div class="flex items-center space-x-2">
              <img v-if="record.business !== 'cheese' && record.business !== 'pgc'" :src="record.authorFace"
                   alt="author" class="w-5 h-5 lg:w-8 lg:h-8 rounded-full"/>
              <p>{{ record.authorName }}</p>
            </div>

            <div class="flex items-center space-x-2">
              <img v-if="record.dt === 1 || record.dt === 3 || record.dt === 5 || record.dt === 7" src="/Mobile.svg"
                   alt="Mobile" class="w-4 h-4 lg:w-8 lg:h-8"/>
              <img v-else-if="record.dt === 2 || record.dt === 33" src="/public/PC.svg" alt="PC"
                   class="w-4 h-4 lg:w-8 lg:h-8"/>
              <img v-else-if="record.dt === 4 || record.dt === 6" src="/public/Pad.svg" alt="Pad"
                   class="w-4 h-4 lg:w-8 lg:h-8"/>
              <p v-else>未知设备</p>

              <!-- 显示时间 -->
              <span>{{ formatTimestamp(record.viewAt) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  record: Object // 父组件传入的 record 数据
});

// 复用函数，比如格式化时间、获取业务类型等
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000);
  const now = new Date();
  const isToday = now.toDateString() === date.toDateString();
  const isYesterday = new Date(now.setDate(now.getDate() - 1)).toDateString() === date.toDateString();
  const timeString = date.toLocaleTimeString('zh-CN', {hour: '2-digit', minute: '2-digit'});

  if (isToday) {
    return timeString;
  } else if (isYesterday) {
    return `昨天 ${timeString}`;
  } else if (now.getFullYear() === date.getFullYear()) {
    return `${date.getMonth() + 1}-${date.getDate()} ${timeString}`;
  } else {
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${timeString}`;
  }
};

const formatDuration = (seconds) => {
  if (seconds === -1) return '已看完';
  const minutes = String(Math.floor(seconds / 60)).padStart(2, '0');
  const secs = String(seconds % 60).padStart(2, '0');
  return `${minutes}:${secs}`;
};

const getBusinessType = (business) => {
  const businessTypes = {
    'archive': '稿件',
    'cheese': '课堂',
    'pgc': '电影',
    'live': '直播',
    'article-list': '专栏',
    'article': '专栏'
  };
  return businessTypes[business] || '其他类型';
};

const getProgressWidth = (progress, duration) => {
  if (progress === -1 || duration === 0) return '100%';
  return `${(progress / duration) * 100}%`;
};
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
