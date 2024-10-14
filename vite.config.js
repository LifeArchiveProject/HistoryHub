import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Inspector from "vite-plugin-vue-inspector"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    Inspector({
      launchEditor: 'webstorm',
      toggleComboKey: 'alt-x' // 设置快捷键为 alt加x
    }),
    vue(),
  ],
  server:{
    host:'0.0.0.0',
  },
})
