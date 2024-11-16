import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Inspector from 'vite-plugin-vue-inspector'

// 获取环境变量
const isElectron = process.env.ELECTRON === 'true'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    Inspector({
      launchEditor: 'webstorm',
      toggleComboKey: 'alt-x',
    }),
    vue(),
  ],
  base: isElectron ? './' : '/', // Electron 使用相对路径，Web 使用绝对路径
  build: {
    emptyOutDir: true,
  },
  server: {
    host: '0.0.0.0',
  },
})
