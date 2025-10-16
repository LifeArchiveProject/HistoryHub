<template>
  <van-dialog
    v-model:show="visible"
    :title="title"
    :width="350"
    class="favorite-dialog"
    show-cancel-button
    :confirm-button-text="confirmText"
    :cancel-button-text="cancelText"
    @confirm="handleConfirm"
    @cancel="handleCancel"
  >
    <div class="p-5 bg-transparent">
      <div v-if="loading" class="flex justify-center py-4">
        <div class="inline-flex items-center">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-[#fb7299]" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>加载中...</span>
        </div>
      </div>
      
      <div v-else-if="favorites.length === 0" class="text-center py-4">
        <p class="text-gray-500 dark:text-gray-400">暂无收藏夹</p>
        <div class="mt-3">
          <button 
            class="px-3 py-1.5 text-sm bg-[#fb7299] text-white rounded-md hover:bg-[#fb7299]/90 transition-colors"
            @click="openLoginDialog"
          >
            登录账号
          </button>
        </div>
      </div>
      
      <div v-else>
        <div v-if="videoInfo" class="mb-3">
          <p class="text-sm text-gray-700 truncate">
            <span v-if="videoInfo.isBatch">批量收藏：{{ videoInfo.selectedCount }}个视频</span>
            <span v-else>收藏视频：{{ videoInfo.title }}</span>
          </p>
        </div>
        
        <div class="max-h-60 overflow-y-auto pr-2 space-y-2">
          <div
            v-for="folder in favorites"
            :key="folder.id"
            class="flex items-center p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <input 
              type="checkbox" 
              :id="`folder-${folder.id}`" 
              :value="folder.id" 
              v-model="selectedFolders"
              class="w-4 h-4 text-[#fb7299] border-gray-300 dark:border-gray-600 rounded focus:ring-[#fb7299]"
            />
            <label :for="`folder-${folder.id}`" class="ml-2 flex-1 cursor-pointer">
              <div class="flex items-center">
                <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ folder.title }}</span>
                <span class="ml-1 text-xs text-gray-500 dark:text-gray-400">({{ folder.media_count }})</span>
              </div>
            </label>
          </div>
        </div>
      </div>
    </div>
  </van-dialog>
  
  <!-- 登录对话框 -->
  <Teleport to="body">
    <LoginDialog
      v-model:show="showLoginDialog"
      @login-success="handleLoginSuccess"
    />
  </Teleport>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed, watch, onMounted } from 'vue'
import { getCreatedFavoriteFolders, favoriteResource, batchFavoriteResource, localBatchFavoriteResource } from '../../api/api.js'
import { showNotify } from 'vant'
import LoginDialog from './LoginDialog.vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  videoInfo: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'favoriteDone'])

// 对话框状态
const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// 组件数据
const loading = ref(false)
const favorites = ref([])
const selectedFolders = ref([])
const showLoginDialog = ref(false)
const isLoggedIn = ref(false)

// 对话框文本
const title = computed(() => '选择收藏夹')
const confirmText = computed(() => '确认收藏')
const cancelText = computed(() => '取消')

// 加载收藏夹列表
const loadFavorites = async () => {
  loading.value = true
  try {
    const response = await getCreatedFavoriteFolders()
    if (response.data.status === 'success') {
      favorites.value = response.data.data.list || []
      isLoggedIn.value = true
    } else {
      // 没有权限或未登录
      isLoggedIn.value = false
      favorites.value = []
    }
  } catch (error) {
    console.error('获取收藏夹列表失败:', error)
    showNotify({ type: 'danger', message: '获取收藏夹列表失败' })
  } finally {
    loading.value = false
  }
}

// 处理确认按钮
const handleConfirm = async () => {
  if (selectedFolders.value.length === 0) {
    showNotify({ type: 'warning', message: '请至少选择一个收藏夹' })
    return
  }
  
  loading.value = true
  try {
    let response;
    
    // 判断是批量收藏还是单个收藏
    if (props.videoInfo.isBatch && props.videoInfo.batchIds) {
      // 批量收藏
      const requestParams = {
        rids: props.videoInfo.batchIds,
        add_media_ids: selectedFolders.value.join(',')
      };
      
      // 先远程操作，然后本地同步
      response = await batchFavoriteResource(requestParams);
      
      // 成功后进行本地同步（不展示给用户）
      if (response.data.status === 'success') {
        try {
          await localBatchFavoriteResource({
            rids: props.videoInfo.batchIds,
            add_media_ids: selectedFolders.value.join(','),
            operation_type: 'local' // 只在本地操作，不需要再同步远程
          });
        } catch (syncError) {
          console.error('本地同步失败，但不影响用户体验:', syncError);
        }
        
        showNotify({ type: 'success', message: `成功收藏${props.videoInfo.selectedCount}个视频` });
        
        emit('favoriteDone', { 
          success: true, 
          videoInfo: props.videoInfo, 
          folders: selectedFolders.value,
          isBatch: true
        });
        
        visible.value = false;
      } else {
        throw new Error(response.data.message || '批量收藏失败');
      }
    } else {
      // 单个视频收藏
      // 获取视频ID，适配不同的属性名（aid或avid）
      const videoId = props.videoInfo?.aid || props.videoInfo?.avid || (props.videoInfo?.business === 'archive' ? props.videoInfo?.oid : null);
      
      if (!props.videoInfo || !videoId) {
        showNotify({ type: 'warning', message: '视频信息不完整，无法收藏' });
        return;
      }
      
      // 先远程操作
      response = await favoriteResource({
        rid: videoId,
        add_media_ids: selectedFolders.value.join(',')
      });
      
      if (response.data.status === 'success') {
        // 成功后进行本地同步（不展示给用户）
        try {
          await localBatchFavoriteResource({
            rids: videoId.toString(),
            add_media_ids: selectedFolders.value.join(','),
            operation_type: 'local' // 只在本地操作，不需要再同步远程
          });
        } catch (syncError) {
          console.error('本地同步失败，但不影响用户体验:', syncError);
        }
        
        showNotify({ type: 'success', message: '收藏成功' });
        
        emit('favoriteDone', { 
          success: true, 
          videoInfo: props.videoInfo, 
          folders: selectedFolders.value
        });
        
        visible.value = false;
      } else {
        throw new Error(response.data.message || '收藏失败');
      }
    }
  } catch (error) {
    console.error('收藏视频失败:', error);
    showNotify({ type: 'danger', message: '收藏失败: ' + (error.message || '未知错误') });
  } finally {
    loading.value = false;
  }
}

// 处理取消按钮
const handleCancel = () => {
  visible.value = false
}

// 打开登录对话框
const openLoginDialog = () => {
  showLoginDialog.value = true
}

// 登录成功回调
const handleLoginSuccess = () => {
  showNotify({ type: 'success', message: '登录成功' })
  loadFavorites()
}

// 监听对话框显示状态变化
watch(() => visible.value, (newVal) => {
  if (newVal) {
    selectedFolders.value = []
    loadFavorites()
  }
})

onMounted(() => {
  if (visible.value) {
    loadFavorites()
  }
})
</script>

<style scoped>
.favorite-dialog {
  border-radius: 8px;
  overflow: hidden;
}

/* 对话框标题背景与分隔线（明暗主题） */
.favorite-dialog :deep(.van-dialog__header) {
  /* 与正文一致的标题背景（浅色） */
  background-color: #ffffff; /* white */
  border-bottom: 1px solid #e5e7eb; /* gray-200 */
  color: #111827; /* gray-900 */
}
.dark .favorite-dialog :deep(.van-dialog__header) {
  /* 与正文一致的标题背景（深色） */
  background-color: #1f2937; /* gray-800 */
  border-bottom-color: #374151; /* gray-700 */
  color: #e5e7eb; /* gray-200 */
}

/* 对话框内容区域背景与正文一致（非标题部分） */
.favorite-dialog :deep(.van-dialog__content) {
  background-color: #ffffff; /* white */
}
.dark .favorite-dialog :deep(.van-dialog__content) {
  background-color: #1f2937; /* gray-800 */
}
</style>