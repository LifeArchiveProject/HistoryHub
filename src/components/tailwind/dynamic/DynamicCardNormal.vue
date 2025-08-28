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

    <!-- 主体：配文/标题内容 + 图片/实况九宫格（如有） -->
    <div class="px-3 pb-3">
      <!-- DYNAMIC_TYPE_DRAW: 展示 opus 标题与摘要 -->
      <template v-if="isDraw">
        <div
          class="text-sm font-semibold text-gray-900 leading-6"
          v-if="drawTitle"
        >{{ drawTitle }}</div>
        <div
          class="mt-1 text-sm text-gray-700 leading-6"
          v-if="drawSummary"
        >
          <span class="whitespace-pre-wrap">
            <template v-for="(seg, i) in parsedSummary" :key="i">
              <span v-if="seg.type==='text'">{{ seg.text }}</span>
              <img v-else :src="seg.url" :alt="seg.name" class="emoji emoji-lg inline-block align-text-bottom" />
            </template>
          </span>
        </div>
      </template>
      <!-- 其他类型：展示 txt（解析表情） -->
      <div
        v-else-if="item.txt"
        role="link"
        tabindex="0"
        @click="openLink(opusUrl)"
        @keydown.enter="openLink(opusUrl)"
        class="text-sm text-gray-800 leading-6 hover:underline cursor-pointer"
      >
        <span class="whitespace-pre-wrap">
          <template v-for="(seg, i) in parsedTxt" :key="'t'+i">
            <span v-if="seg.type==='text'">{{ seg.text }}</span>
            <img v-else :src="seg.url" :alt="seg.name" class="emoji emoji-lg inline-block align-text-bottom" />
          </template>
        </span>
      </div>

      <div v-if="displayMedias.length" class="mt-2 grid gap-1 md:gap-2 grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6">
        <template v-for="(m, idx) in displayMedias" :key="idx">
          <!-- 普通图片 -->
          <div v-if="m.kind==='image'" class="relative rounded-md overflow-hidden hover:opacity-90 cursor-pointer h-28 sm:h-32 md:h-36" role="button" tabindex="0" @click="openPreview('image', m.url)" @keydown.enter="openPreview('image', m.url)">
            <img :src="m.url" class="block w-full h-full object-cover" />
          </div>
          <!-- 实况照片（悬停播放） -->
          <div v-else class="relative rounded-md overflow-hidden hover:opacity-90 cursor-pointer h-28 sm:h-32 md:h-36"
               role="button" tabindex="0"
               @mouseenter="handleLiveEnter(idx)" @mouseleave="handleLiveLeave(idx)"
               @click="openPreview('video', m.videoUrl, m.coverUrl)" @keydown.enter="openPreview('video', m.videoUrl, m.coverUrl)">
            <video :poster="m.coverUrl" :src="m.videoUrl" muted playsinline loop
                   class="absolute inset-0 w-full h-full object-cover"
                   :ref="el => setLiveRef(idx, el)"
            ></video>
            <!-- 右下角 实况 徽标 -->
            <div class="absolute bottom-1 right-1 px-1.5 py-0.5 bg-black/60 text-white text-[10px] flex items-center rounded">
              <img src="/live.svg" class="w-3 h-3 mr-1 filter invert" alt="live" />
              <span>实况</span>
            </div>
          </div>
        </template>
      </div>
    </div>

    <!-- 预览弹层 -->
    <Teleport to="body">
      <div v-if="showPreview" class="fixed inset-0 z-50 bg-black/80 flex items-center justify-center" @click="closePreview">
        <div class="max-w-[95vw] max-h-[90vh] relative" @click.stop>
          <img v-if="previewType==='image'" :src="previewSrc" class="max-w-[95vw] max-h-[90vh] object-contain rounded-md" />
          <video v-else :src="previewSrc" :poster="previewPoster" controls autoplay loop muted class="max-w-[95vw] max-h-[90vh] rounded-md"></video>
          <button class="absolute -top-3 -right-3 w-8 h-8 rounded-full bg-black/70 text-white flex items-center justify-center" @click="closePreview">×</button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { openInBrowser } from '@/utils/openUrl'
import { toStaticUrl } from '@/utils/imageUrl'

const props = defineProps({
  item: { type: Object, required: true },
  faceUrl: { type: String, default: '' }
})

// 是否图文动态
const isDraw = computed(() => String(props.item?.type || '') === 'DYNAMIC_TYPE_DRAW')
const drawTitle = computed(() => props.item?.opus_title || '')
const drawSummary = computed(() => props.item?.opus_summary_text || '')

// 归一化扩展名检查
const isVideoPath = (p) => /\.mp4$/i.test(String(p || '').replace(/\\/g, '/'))
const isImagePath = (p) => /\.(png|jpe?g|gif|webp)$/i.test(String(p || '').replace(/\\/g, '/'))
const getNameFromPath = (p) => {
  const filename = String(p || '').split(/[/\\]/).pop() || ''
  const decoded = decodeURIComponent(filename)
  return decoded.replace(/\.[^.]+$/, '')
}

// 从摘要中提取 [xxx] 表情名集合
const extractEmojiNames = (text) => {
  const set = new Set()
  if (!text) return set
  const re = /\[([^\[\]]+?)\]/g
  let m
  while ((m = re.exec(text)) !== null) {
    set.add(m[1])
  }
  return set
}

const emojiNamesFromSummary = computed(() => extractEmojiNames(drawSummary.value))
const emojiNamesFromTxt = computed(() => extractEmojiNames(props.item?.txt || ''))
const allEmojiNames = computed(() => new Set([...emojiNamesFromSummary.value, ...emojiNamesFromTxt.value]))

// 构建 emoji 名称到图片URL的映射（仅使用摘要中出现过的表情名）
const emojiMap = computed(() => {
  const map = {}
  const ml = Array.isArray(props.item?.media_locals) ? props.item.media_locals : []
  for (const p of ml) {
    if (!isImagePath(p)) continue
    const name = getNameFromPath(p)
    if (/^live_/i.test(name)) continue
    if (allEmojiNames.value.has(name)) {
      map[name] = toStaticUrl(p)
    }
  }
  return map
})

// 将摘要解析为文本/emoji 片段
const parseWithEmoji = (text) => {
  const map = emojiMap.value || {}
  if (!text) return []
  const result = []
  const re = /\[([^\[\]]+?)\]/g
  let last = 0
  let m
  while ((m = re.exec(text)) !== null) {
    const idx = m.index
    const raw = m[0]
    const name = m[1]
    if (idx > last) {
      result.push({ type: 'text', text: text.slice(last, idx) })
    }
    if (map[name]) {
      result.push({ type: 'emoji', name, url: map[name] })
    } else {
      result.push({ type: 'text', text: raw })
    }
    last = idx + raw.length
  }
  if (last < text.length) {
    result.push({ type: 'text', text: text.slice(last) })
  }
  return result
}

const parsedSummary = computed(() => {
  const text = drawSummary.value || ''
  return parseWithEmoji(text)
})

const parsedTxt = computed(() => parseWithEmoji(props.item?.txt || ''))

// 构造展示媒体：普通图片 + 实况照片（由 live_media_locals 配对 png+mp4）
const displayMedias = computed(() => {
  const medias = []
  const ml = Array.isArray(props.item?.media_locals) ? props.item.media_locals : []
  for (const p of ml) {
    if (isImagePath(p) && !/live_/i.test(p)) {
      const name = getNameFromPath(p)
      // 过滤掉作为emoji使用的图片
      if (!allEmojiNames.value.has(name)) {
        medias.push({ kind: 'image', url: toStaticUrl(p) })
      }
    }
  }

  const live = Array.isArray(props.item?.live_media_locals) ? props.item.live_media_locals : []
  if (live.length) {
    const covers = live.filter(isImagePath)
    const videos = live.filter(isVideoPath)
    const n = Math.min(covers.length, videos.length, 9)
    for (let i = 0; i < n; i++) {
      medias.push({ kind: 'live', coverUrl: toStaticUrl(covers[i]), videoUrl: toStaticUrl(videos[i]) })
    }
  }

  return medias.slice(0, 12) // 限制单条最多展示若干项
})

// 网格固定为每行最多6列（随断点 3/4/5/6 列）

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

const openLink = (url) => {
  try { openInBrowser(url) } catch { window.open(url, '_blank') }
}

// 实况播放控制
const liveRefs = ref({})
const setLiveRef = (idx, el) => {
  if (!liveRefs.value) liveRefs.value = {}
  if (el) liveRefs.value[idx] = el
  else delete liveRefs.value[idx]
}
const handleLiveEnter = (idx) => {
  const v = liveRefs.value?.[idx]
  if (v) {
    try { v.play() } catch (e) {}
  }
}
const handleLiveLeave = (idx) => {
  const v = liveRefs.value?.[idx]
  if (v) {
    try { v.pause(); v.currentTime = 0 } catch (e) {}
  }
}

// 预览逻辑
const showPreview = ref(false)
const previewType = ref('image')
const previewSrc = ref('')
const previewPoster = ref('')
const openPreview = (type, src, poster = '') => {
  previewType.value = type
  previewSrc.value = src
  previewPoster.value = poster
  showPreview.value = true
}
const closePreview = () => { showPreview.value = false }
</script>

<style scoped>
/* 使emoji图片与文字同高 */
.emoji {
  height: 1em;
  width: 1em;
  margin: 0 2px;
}
.emoji-lg {
  height: 1.25em;
  width: 1.25em;
}
</style>


