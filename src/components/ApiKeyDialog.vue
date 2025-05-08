<template>
  <div v-if="show" class="api-key-dialog-overlay" @click.self="handleCancel">
    <div class="api-key-dialog">
      <div class="api-key-dialog-header">
        <h3>{{ title }}</h3>
      </div>
      <div class="api-key-dialog-content">
        <p>{{ message }}</p>
        <div class="api-key-input-container">
          <input
            type="text"
            v-model="apiKey"
            :placeholder="inputPlaceholder"
            class="api-key-input"
            ref="inputRef"
          />
          <div class="api-key-hint">
            {{ hintText }}
          </div>
          <div v-if="error" class="api-key-error">
            {{ error }}
          </div>
        </div>
      </div>
      <div class="api-key-dialog-footer">
        <button v-if="showCancelButton" class="api-key-cancel-btn" @click="handleCancel">{{ cancelText }}</button>
        <button class="api-key-confirm-btn" :class="{'api-key-confirm-btn-full': !showCancelButton}" @click="handleConfirm">{{ confirmText }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '安全警告'
  },
  message: {
    type: String,
    default: '检测到服务器正在使用默认的API密钥，这可能会导致安全风险。请输入新的API密钥：'
  },
  confirmText: {
    type: String,
    default: '确认修改'
  },
  cancelText: {
    type: String,
    default: '稍后修改'
  },
  showCancelButton: {
    type: Boolean,
    default: true
  },
  inputPlaceholder: {
    type: String,
    default: '请输入新的API密钥'
  },
  hintText: {
    type: String,
    default: '建议使用复杂的随机字符串。注意：为了安全，此密钥将不会在前端显示，请妥善保存。后续只能在配置文件中查看。'
  }
})

const emit = defineEmits(['update:show', 'confirm', 'cancel'])

const apiKey = ref('')
const error = ref('')
const inputRef = ref(null)

// 监听show变化，当显示弹窗时，自动聚焦输入框
watch(() => props.show, (newVal) => {
  if (newVal) {
    // 清空之前的输入和错误
    apiKey.value = ''
    error.value = ''

    // 自动聚焦输入框
    nextTick(() => {
      if (inputRef.value) {
        inputRef.value.focus()
      }
    })
  }
})

// 处理确认按钮点击
const handleConfirm = () => {
  // 验证输入
  if (!apiKey.value.trim()) {
    error.value = 'API密钥不能为空，请输入有效的密钥'
    return
  }

  // 清除错误
  error.value = ''

  // 触发确认事件，传递API密钥
  emit('confirm', apiKey.value.trim())

  // 关闭弹窗
  emit('update:show', false)
}

// 处理取消按钮点击
const handleCancel = () => {
  // 触发取消事件
  emit('cancel')

  // 关闭弹窗
  emit('update:show', false)
}
</script>

<style scoped>
.api-key-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
}

.api-key-dialog {
  width: 90%;
  max-width: 500px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.api-key-dialog-header {
  padding: 16px;
  border-bottom: 1px solid #ebedf0;
}

.api-key-dialog-header h3 {
  margin: 0;
  font-size: 18px;
  color: #323233;
}

.api-key-dialog-content {
  padding: 16px;
}

.api-key-dialog-content p {
  margin: 0 0 16px;
  font-size: 14px;
  line-height: 1.5;
  color: #646566;
}

.api-key-input-container {
  margin-top: 16px;
}

.api-key-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #dcdee0;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.api-key-input:focus {
  border-color: #fb7299;
  outline: none;
}

.api-key-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #969799;
  line-height: 1.5;
}

.api-key-error {
  margin-top: 8px;
  font-size: 12px;
  color: #ee0a24;
}

.api-key-dialog-footer {
  display: flex;
  padding: 16px;
  border-top: 1px solid #ebedf0;
}

.api-key-cancel-btn,
.api-key-confirm-btn {
  flex: 1;
  height: 36px;
  margin: 0 4px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
}

.api-key-cancel-btn {
  background-color: #f7f8fa;
  color: #323233;
}

.api-key-confirm-btn {
  background-color: #fb7299;
  color: white;
}

.api-key-cancel-btn:hover {
  background-color: #e8e8e8;
}

.api-key-confirm-btn:hover {
  background-color: #f06292;
}

.api-key-confirm-btn-full {
  flex: 1;
  margin: 0 !important;
  width: 100%;
}
</style>
