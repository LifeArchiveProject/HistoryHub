const { contextBridge, ipcRenderer } = require('electron')

// 使用 contextBridge 暴露 API 给渲染进程
contextBridge.exposeInMainWorld('api', {
  send: (channel, data) => {
    // 允许的通道
    const validChannels = ['toMain']
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data)
    }
  },
  receive: (channel, func) => {
    const validChannels = ['fromMain']
    if (validChannels.includes(channel)) {
      // 移除事件对象，防止泄露
      ipcRenderer.on(channel, (event, ...args) => func(...args))
    }
  },
})
