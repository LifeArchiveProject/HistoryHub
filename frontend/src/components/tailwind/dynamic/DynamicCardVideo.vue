<template>
  <div class="border rounded-lg bg-white overflow-hidden">
    <!-- 头部：头像 + 名称 + 时间 + 动态链接 -->
    <div class="flex items-center px-3 py-2">
      <img v-if="faceUrl" :src="faceUrl" class="w-6 h-6 rounded-full object-cover border" alt="face" />
      <div class="ml-2 min-w-0">
        <div class="text-sm font-medium truncate">{{ item.author_name || `UID ${item.host_mid || ''}` }}</div>
        <div class="text-[11px] text-gray-500 truncate">{{ formattedTime }}</div>
      </div>
      <button
        v-if="item.id_str"
        type="button"
        class="ml-auto text-[11px] text-[#fb7299] hover:underline"
        @click="openLink(opusUrl)"
      >查看动态</button>
    </div>

    <!-- 主体：封面（更小） + 文本，封面/标题可跳转视频 -->
    <div class="px-3 pb-3">
      <div class="flex items-start">
        <div
          class="relative w-40 sm:w-48 md:w-56 flex-shrink-0 rounded-md overflow-hidden hover:opacity-90 cursor-pointer"
          role="link"
          tabindex="0"
          @click="openLink(videoUrl)"
          @keydown.enter="openLink(videoUrl)"
        >
          <div class="w-full" style="aspect-ratio: 16 / 9">
            <img v-if="coverUrl" :src="coverUrl" class="block w-full h-full object-cover" alt="cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-gray-400 text-xs">no cover</div>
          </div>
          <div v-if="item.bvid" class="absolute bottom-1 left-1 text-[10px] bg-black/60 text-white px-1.5 py-0.5 rounded">{{ item.bvid }}</div>
        </div>
        <div class="ml-3 flex-1 min-w-0">
          <div
            role="link"
            tabindex="0"
            @click="openLink(videoUrl)"
            @keydown.enter="openLink(videoUrl)"
            class="text-sm font-semibold leading-5 line-clamp-2 hover:underline cursor-pointer"
            :title="item.title || item.txt || ''"
          >{{ item.title || item.txt || '视频动态' }}</div>
          <div v-if="item.desc || item.txt" class="text-xs text-gray-600 mt-1 line-clamp-2">{{ item.desc || item.txt }}</div>
        </div>
      </div>
    </div>
  </div>
  
</template>

<script setup>
import { computed } from 'vue'
import { openInBrowser } from '@/utils/openUrl'
import { toStaticUrl } from '@/utils/imageUrl'

const props = defineProps({
  item: { type: Object, required: true },
  faceUrl: { type: String, default: '' }
})

const coverUrl = computed(() => {
  const it = props.item || {}
  if (it.cover) return toStaticUrl(it.cover)
  const list = Array.isArray(it.media_locals) ? it.media_locals : []
  if (list.length) return toStaticUrl(list[0])
  return ''
})

const formattedTime = computed(() => {
  const ts = props.item?.publish_ts
  if (!ts) return '-'
  try {
    const d = new Date(ts * 1000)
    const pad = (n) => String(n).padStart(2, '0')
    return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
  } catch {
    return String(ts)
  }
})

const opusUrl = computed(() => props.item?.id_str ? `https://www.bilibili.com/opus/${props.item.id_str}` : '#')
const videoUrl = computed(() => props.item?.bvid ? `https://www.bilibili.com/video/${props.item.bvid}` : opusUrl.value)

const openLink = (url) => {
  try { openInBrowser(url) } catch { window.open(url, '_blank') }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>


