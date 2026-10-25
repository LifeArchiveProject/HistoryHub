import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createMyRouter } from './router/router'

async function bootstrap() {
  const isTauri = Boolean(window.__TAURI_INTERNALS__)
  if (isTauri) {
    const { invoke } = await import('@tauri-apps/api/core')
    window.__TAURI_INVOKE__ = invoke
  }

  createApp(App)
    .use(createMyRouter(isTauri ? 'hash' : 'history'))
    .mount('#app')
}

bootstrap()
