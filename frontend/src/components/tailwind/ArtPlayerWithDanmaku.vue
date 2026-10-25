<template>
  <div ref="artPlayerContainer" class="art-player-container"></div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import Artplayer from 'artplayer'
import artplayerPluginDanmuku from 'artplayer-plugin-danmuku'
import { getDanmakuFile } from '../../api/api'

// 定义组件属性
const props = defineProps({
  // 视频源URL
  videoSrc: {
    type: String,
    required: true
  },
  // 弹幕文件路径
  danmakuFilePath: {
    type: String,
    default: ''
  },
  // 视频CID（用于获取弹幕）
  cid: {
    type: String,
    default: ''
  },
  // 视频封面
  poster: {
    type: String,
    default: ''
  },
  // 视频标题
  title: {
    type: String,
    default: '视频播放'
  },
  // 是否自动播放
  autoplay: {
    type: Boolean,
    default: false
  },
  // 播放器宽度
  width: {
    type: String,
    default: '100%'
  },
  // 播放器高度
  height: {
    type: String,
    default: '100%'
  }
})

// 定义事件
const emit = defineEmits(['ready', 'error'])

// DOM引用
const artPlayerContainer = ref(null)
// 播放器实例
const player = ref(null)
// 弹幕数据
const danmakuData = ref([])

// 加载弹幕文件内容
const loadDanmaku = async () => {
  if (!props.danmakuFilePath && !props.cid) {
    console.log('没有提供弹幕文件路径或CID，跳过弹幕加载')
    return []
  }

  try {
    // 优先使用文件路径
    const path = props.danmakuFilePath || ''
    const cid = props.cid || ''
    
    // 获取弹幕文件内容
    const response = await getDanmakuFile(cid, path)
    
    if (!response || !response.data) {
      console.warn('弹幕文件内容为空')
      return []
    }
    
    // 解析ASS格式弹幕
    const danmakuItems = parseAssDanmaku(response.data)
    danmakuData.value = danmakuItems
    
    // 如果播放器已存在，更新弹幕
    if (player.value && player.value.plugins.artplayerPluginDanmuku) {
      player.value.plugins.artplayerPluginDanmuku.config({
        danmuku: danmakuItems
      })
    }
    
    return danmakuItems
  } catch (error) {
    console.error('加载弹幕文件失败:', error)
    return []
  }
}

// 解析ASS格式弹幕
const parseAssDanmaku = (assContent) => {
  if (!assContent) return []
  
  const danmakuItems = []
  const lines = assContent.split('\n')
  console.log("弹幕文件总行数:", lines.length)
  
  // 查找Dialogue行
  lines.forEach((line, index) => {
    if (line.startsWith('Dialogue:')) {
      try {
        // ASS格式: Dialogue: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        const parts = line.split(',')
        if (parts.length >= 10) {
          // 提取开始时间
          const startTimeStr = parts[1].trim()
          // 转换时间格式为秒 (h:mm:ss.ms)
          const startTime = parseAssTime(startTimeStr)
          
          // 提取样式名称，可能用于确定弹幕位置
          const styleName = parts[3].trim()
          
          // 提取弹幕文本 (最后一个部分)
          const textParts = parts.slice(9)
          let text = textParts.join(',')
          
          // 提取颜色信息
          let color = '#ffffff' // 默认白色
          
          // B站弹幕可能使用大括号包裹样式，如 {\\c&HFFFFFF&}
          // 或者直接使用反斜杠，如 \\c&HFFFFFF&
          let colorRegex = /(\\c|{\\c)&H([0-9A-Fa-f]{2,6})&/
          let colorMatch = text.match(colorRegex)
          
          if (colorMatch) {
            let colorCode = colorMatch[2]
            console.log(`找到颜色代码: ${colorCode}, 行: ${index}, 文本: ${text}`)
            
            // 标准化颜色代码为6位
            while (colorCode.length < 6) {
              colorCode = '0' + colorCode
            }
            
            // B站弹幕的颜色格式通常是BBGGRR，需要转换为网页的RGB格式
            if (colorCode.length === 6) {
              const blue = colorCode.substring(0, 2)
              const green = colorCode.substring(2, 4)
              const red = colorCode.substring(4, 6)
              color = `#${red}${green}${blue}`
              console.log(`转换后颜色: ${color}`)
            }
          }
          
          // 确定弹幕模式
          // mode: 0=滚动弹幕, 1=顶部弹幕, 2=底部弹幕
          let mode = 0 // 默认为滚动弹幕
          
          // B站弹幕定位可能有多种形式：
          // 1. 使用\an指定位置，\an8是顶部，\an2是底部
          // 2. 使用\pos固定位置显示
          // 3. 使用\move实现滚动效果
          
          // 检查是否有位置标记
          if (text.includes('\\an8') || text.includes('{\\an8}')) {
            mode = 1 // 顶部弹幕
            console.log("找到顶部弹幕: ", text)
          } else if (text.includes('\\an2') || text.includes('{\\an2}')) {
            mode = 2 // 底部弹幕
            console.log("找到底部弹幕: ", text)
          } else if (text.includes('\\pos') || text.includes('{\\pos')) {
            // 根据Y坐标判断是顶部还是底部弹幕
            const posMatch = text.match(/\\pos\((\d+),\s*(\d+)\)/) || text.match(/{\\pos\((\d+),\s*(\d+)\)}/)
            if (posMatch) {
              const yPos = parseInt(posMatch[2])
              // 屏幕高度一般为1080，上半部分认为是顶部弹幕，下半部分认为是底部弹幕
              if (yPos < 540) {
                mode = 1 // 顶部弹幕
                console.log("找到顶部定位弹幕: ", text)
              } else {
                mode = 2 // 底部弹幕
                console.log("找到底部定位弹幕: ", text)
              }
            }
          } else if (text.includes('\\move') || text.includes('{\\move')) {
            // 移动弹幕默认为滚动弹幕(mode=0)
            console.log("找到滚动弹幕: ", text)
          } else if (styleName.toLowerCase().includes('top')) {
            mode = 1 // 通过样式名称判断顶部弹幕
          } else if (styleName.toLowerCase().includes('bottom')) {
            mode = 2 // 通过样式名称判断底部弹幕
          }
          
          // 移除ASS格式标签，保留纯文本
          text = text.replace(/{[^}]*}/g, '') // 去除{}中的内容
          text = text.replace(/\\[a-zA-Z0-9]+(&H[0-9A-Fa-f]+&)?/g, '') // 去除\command&Hxxxx&类格式
          text = text.replace(/\\[a-zA-Z0-9]+\([^)]*\)/g, '') // 去除\command(params)类格式
          text = text.trim()
          
          // 创建弹幕对象
          danmakuItems.push({
            text,
            time: startTime,
            color: color, // 设置提取的颜色
            border: false,
            mode: mode, // 设置弹幕模式
          })
        }
      } catch (error) {
        console.warn('解析弹幕行失败:', line, error)
      }
    }
  })
  
  console.log(`成功解析${danmakuItems.length}条弹幕`)
  return danmakuItems
}

// 将ASS时间格式转换为秒
const parseAssTime = (timeStr) => {
  const parts = timeStr.split(':')
  if (parts.length === 3) {
    const hours = parseInt(parts[0])
    const minutes = parseInt(parts[1])
    const seconds = parseFloat(parts[2])
    
    return hours * 3600 + minutes * 60 + seconds
  }
  return 0
}

// 初始化播放器
const initPlayer = async () => {
  if (!artPlayerContainer.value) return
  
  // 销毁现有播放器实例
  if (player.value) {
    player.value.destroy()
    player.value = null
  }
  
  // 加载弹幕数据
  await loadDanmaku()
  
  // 创建播放器选项
  const options = {
    container: artPlayerContainer.value,
    url: props.videoSrc,
    title: props.title,
    poster: props.poster,
    volume: 0.7,
    autoplay: props.autoplay,
    autoSize: false,
    autoMini: true,
    loop: false,
    flip: true,
    playbackRate: true,
    aspectRatio: true,
    setting: true,
    hotkey: true,
    pip: true,
    fullscreen: true,
    fullscreenWeb: true,
    subtitleOffset: true,
    miniProgressBar: true,
    playsInline: true,
    lock: true,
    fastForward: true,
    autoPlayback: true,
    theme: '#fb7299', // B站粉色主题
    lang: 'zh-cn',
    moreVideoAttr: {
      crossOrigin: 'anonymous',
    },
    icons: {
      loading: '<svg xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 24 24"><path fill="#fb7299" d="M12,1A11,11,0,1,0,23,12,11,11,0,0,0,12,1Zm0,19a8,8,0,1,1,8-8A8,8,0,0,1,12,20Z" opacity=".25"/><path fill="#fb7299" d="M12,4a8,8,0,0,1,7.89,6.7A1.53,1.53,0,0,0,21.38,12h0a1.5,1.5,0,0,0,1.48-1.75,11,11,0,0,0-21.72,0A1.5,1.5,0,0,0,2.62,12h0a1.53,1.53,0,0,0,1.49-1.3A8,8,0,0,1,12,4Z"><animateTransform attributeName="transform" dur="0.75s" repeatCount="indefinite" type="rotate" values="0 12 12;360 12 12"/></path></svg>',
    },
    customType: {},
  }
  
  // 如果有弹幕数据，添加弹幕插件
  if (danmakuData.value.length > 0) {
    options.plugins = [
      artplayerPluginDanmuku({
        danmuku: danmakuData.value,
        speed: 5, // 弹幕速度
        opacity: 0.8, // 弹幕透明度
        fontSize: 25, // 弹幕字体大小
        color: '#ffffff', // 默认颜色，实际会被每条弹幕自己的颜色覆盖
        mode: 0, // 默认弹幕模式
        margin: [10, '25%'], // 弹幕上下边距
        antiOverlap: true, // 防重叠
        useWorker: true, // 使用Web Worker
        synchronousPlayback: true, // 同步播放（随视频播放速度变化）
        filter: () => true, // 弹幕过滤
        lockTime: 0, // 锁定弹幕时间
        maxLength: 100, // 最大长度
        minWidth: 200, // 弹幕最小宽度
        maxWidth: 400, // 弹幕最大宽度
        theme: 'dark', // 弹幕主题
        disableDanmuku: false, // 不禁用弹幕
        defaultOff: false, // 默认开启弹幕
        controls: [
          {
            name: 'danmuku',
            position: 'right',
            html: '弹幕',
            tooltip: '显示/隐藏弹幕',
            style: {
              padding: '0 10px',
              fontSize: '14px',
              fontWeight: 'bold'
            }
          }
        ]
      }),
    ]
  }
  
  try {
    // 初始化播放器
    player.value = new Artplayer(options)
    
    // 注册事件监听
    player.value.on('ready', () => {
      emit('ready', player.value)
    })
    
    player.value.on('error', (error) => {
      console.error('播放器错误:', error)
      emit('error', error)
    })
    
  } catch (error) {
    console.error('初始化播放器失败:', error)
    emit('error', error)
  }
}

// 监听属性变化
watch(() => props.videoSrc, () => {
  if (player.value) {
    player.value.switchUrl(props.videoSrc)
    
    // 如果有弹幕，重新加载
    if (props.danmakuFilePath || props.cid) {
      loadDanmaku()
    }
  } else {
    initPlayer()
  }
}, { immediate: false })

// 监听弹幕路径变化
watch([() => props.danmakuFilePath, () => props.cid], () => {
  if (player.value && (props.danmakuFilePath || props.cid)) {
    loadDanmaku()
  }
}, { immediate: false })

// 组件挂载时初始化
onMounted(() => {
  if (props.videoSrc) {
    initPlayer()
  }
})

// 组件卸载时销毁播放器
onUnmounted(() => {
  if (player.value) {
    player.value.destroy()
    player.value = null
  }
})

// 暴露播放器实例和方法
defineExpose({
  player: player,
  reload: initPlayer,
  loadDanmaku
})
</script>

<style scoped>
.art-player-container {
  width: v-bind(width);
  height: v-bind(height);
  background-color: #000;
  position: relative;
}
</style> 