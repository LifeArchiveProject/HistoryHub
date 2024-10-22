import {defineConfig} from 'vite'
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
    base: './', // 设置为相对路径，确保在 Electron 中正确加载静态资源
    build: {
        emptyOutDir: true, // 每次打包清空 dist 目录
    },
    server: {
        host: '0.0.0.0',
    },
})
