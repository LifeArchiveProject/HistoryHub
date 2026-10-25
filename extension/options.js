const form = document.querySelector("#settings-form");
const backendInput = document.querySelector("#backend-url");
const tokenInput = document.querySelector("#token");
const mainButton = document.querySelector("#main-action");
const syncButton = document.querySelector("#sync-now");
const statusLine = document.querySelector("#status");
const notice = document.querySelector("#notice");
let saved;
let state;
let busy = false;
let syncing = false;

async function send(message) {
  const result = await chrome.runtime.sendMessage(message);
  if (!result?.ok) throw new Error(result?.error || "无法连接扩展后台，请重新打开设置页。");
  return result;
}

function edited() {
  return backendInput.value.trim().replace(/\/+$/, "") !== saved.backendURL || tokenInput.value.trim() !== saved.token;
}

function render() {
  if (!saved) return;
  const dirty = edited();
  mainButton.textContent = busy ? "正在保存…" : dirty || !saved.token ? (saved.enabled ? "保存配置" : "保存并开启同步") : saved.enabled ? "暂停同步" : "开启同步";
  mainButton.disabled = busy;
  backendInput.disabled = busy;
  tokenInput.disabled = busy;
  syncButton.textContent = syncing ? "同步中…" : "立即同步";
  syncButton.disabled = busy || dirty || !saved.enabled || syncing;
  if (!saved.enabled) {
    statusLine.textContent = "同步已关闭。填写配置并开启后才会读取和上传浏览历史。";
  } else if (state?.revision !== saved.revision) {
    statusLine.textContent = "同步已开启，等待首次导入。";
  } else if (state.lastError) {
    statusLine.textContent = `同步未完成：${state.lastError} 下次自动同步或点击“立即同步”时会继续。`;
  } else if (syncing || state.status === "syncing") {
    statusLine.textContent = `${state.backfillComplete ? "正在同步" : "正在导入浏览器当前保留的历史"}，本轮已提交 ${state.scan?.accepted || 0} 条。`;
  } else {
    statusLine.textContent = state.lastSuccess ? `同步已开启，上次完成：${new Date(state.lastSuccess).toLocaleString()}。` : "同步已开启，等待首次导入。";
  }
}

form.addEventListener("input", () => { notice.textContent = ""; render(); });
form.addEventListener("submit", async event => {
  event.preventDefault();
  if (busy || !saved) return;
  notice.textContent = "";
  const pause = saved.enabled && !edited();
  try {
    let backendURL = saved.backendURL;
    let token = saved.token;
    let permission;
    if (!pause) {
      if (!form.reportValidity()) return;
      let url;
      try { url = new URL(backendInput.value.trim()); } catch { throw new Error("请输入有效的后端地址。"); }
      if (!["http:", "https:"].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
        throw new Error("后端地址须为 HTTP 或 HTTPS 地址，不能包含账号、查询参数或片段。");
      }
      backendURL = url.href.replace(/\/+$/, "");
      token = tokenInput.value.trim();
      if (!token) throw new Error("请填写后端令牌。");
      // Request permission directly in the submit gesture, before any await.
      permission = chrome.permissions.request({ origins: [`${url.origin}/*`] });
    }
    busy = true;
    render();
    if (permission && !(await permission)) throw new Error("未授权后端地址，配置未保存。");
    const result = await send({ type: "save-settings", backendURL, token, enabled: !pause });
    saved = result.settings;
    backendInput.value = saved.backendURL;
    tokenInput.value = saved.token;
  } catch (error) {
    notice.textContent = error.message;
  } finally {
    busy = false;
    render();
  }
});

syncButton.addEventListener("click", async () => {
  notice.textContent = "";
  try { await send({ type: "sync" }); } catch (error) { notice.textContent = error.message; }
});

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== "local") return;
  if (changes.settings) {
    const dirty = saved && edited();
    saved = changes.settings.newValue;
    if (!dirty) {
      backendInput.value = saved.backendURL;
      tokenInput.value = saved.token;
    }
  }
  if (changes.syncState) {
    state = changes.syncState.newValue;
    syncing = state.status === "syncing" && state.revision === saved?.revision;
  }
  render();
});

send({ type: "status" }).then(result => {
  saved = result.settings;
  state = result.syncState;
  syncing = result.running;
  backendInput.value = saved.backendURL;
  tokenInput.value = saved.token;
  render();
}).catch(error => { notice.textContent = error.message; });
