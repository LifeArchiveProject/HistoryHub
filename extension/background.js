const PAGE_SIZE = 200;
const ALARM_NAME = "historyhub-sync";
const SYNC_MINUTES = 5;
let running = null;
let requested = false;

class SyncStopped extends Error {}

function normalizeBackend(value) {
  let url;
  try { url = new URL(value); } catch { throw new Error("请输入有效的后端地址。"); }
  if (!["http:", "https:"].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
    throw new Error("后端地址须为 HTTP 或 HTTPS 地址，不能包含账号、查询参数或片段。");
  }
  return url.href.replace(/\/+$/, "");
}

function originPattern(backendURL) {
  return `${new URL(backendURL).origin}/*`;
}

async function configureAlarm(settings) {
  if (!settings.enabled) {
    await chrome.alarms.clear(ALARM_NAME);
  } else if (!(await chrome.alarms.get(ALARM_NAME))) {
    await chrome.alarms.create(ALARM_NAME, { periodInMinutes: SYNC_MINUTES });
  }
}

const ready = (async () => {
  let { settings } = await chrome.storage.local.get("settings");
  if (!settings) {
    settings = {
      backendURL: "http://127.0.0.1:8899",
      token: "",
      enabled: false,
      client_id: crypto.randomUUID(),
      revision: crypto.randomUUID()
    };
    await chrome.storage.local.set({ settings });
  }
  await configureAlarm(settings);
})();

async function getSettings() {
  await ready;
  return (await chrome.storage.local.get("settings")).settings;
}

async function checkSettings(expected) {
  const current = await getSettings();
  if (!current.enabled || current.revision !== expected.revision) throw new SyncStopped();
  if (!current.token) throw new Error("请填写后端令牌并保存配置。");
  if (!(await chrome.permissions.contains({ origins: [originPattern(current.backendURL)] }))) {
    throw new Error("尚未授权后端地址，请在设置页保存配置并授权。");
  }
}

function range(start, end, maxResults = PAGE_SIZE) {
  return { start, end, maxResults, afterUrl: "", currentUrl: "", afterVisit: "" };
}

function compareIds(left, right) {
  return left.length - right.length || (left < right ? -1 : left > right ? 1 : 0);
}

async function saveState(state) {
  await chrome.storage.local.set({ syncState: state });
}

async function upload(settings, records) {
  await checkSettings(settings);
  const response = await fetch(`${settings.backendURL}/browser-history/sync`, {
    method: "POST",
    credentials: "omit",
    redirect: "error",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${settings.token}` },
    body: JSON.stringify({ client_id: settings.client_id, records })
  });
  if (!response.ok) throw new Error(`后端请求失败（HTTP ${response.status}），请检查后端地址和令牌。`);
  const result = await response.json();
  if (result.status !== "success" || result.accepted !== records.length) {
    throw new Error("后端未确认接收整批记录，已保留同步位置。");
  }
}

async function syncHistory() {
  const settings = await getSettings();
  if (!settings.enabled) return;
  let { syncState: state } = await chrome.storage.local.get("syncState");
  if (!state || state.revision !== settings.revision) {
    state = { revision: settings.revision, completedThrough: 0, backfillComplete: false, scan: null, lastSuccess: null };
  }
  try {
    await checkSettings(settings);
    state.status = "syncing";
    state.lastError = "";
    if (!state.scan) {
      // A small overlap lets the next alarm refresh titles recorded before page load.
      const start = Math.max(0, state.completedThrough - SYNC_MINUTES * 60_000);
      const end = Date.now();
      state.scan = { end, accepted: 0, ranges: [range(start, end)] };
    }
    await saveState(state);
    while (state.scan.ranges.length) {
      await checkSettings(settings);
      const current = state.scan.ranges.at(-1);
      const items = await chrome.history.search({
        text: "", startTime: current.start, endTime: current.end, maxResults: current.maxResults
      });
      if (items.length >= current.maxResults) {
        // lastVisitTime is global to the URL, so it cannot page historical visits.
        // Empty-text searches match visits inside the requested time range instead.
        state.scan.ranges.pop();
        if (current.end - current.start > 1) {
          const middle = (current.start + current.end) / 2;
          state.scan.ranges.push(range(current.start, middle), range(middle, current.end));
        } else {
          // Same-time results need a larger page, rather than skipping a timestamp.
          state.scan.ranges.push(range(current.start, current.end, current.maxResults * 2));
        }
        await saveState(state);
        continue;
      }
      items.sort((left, right) => compareIds(left.id, right.id));
      let records = [];
      const checkpoint = { afterUrl: current.afterUrl, currentUrl: current.currentUrl, afterVisit: current.afterVisit };
      const flush = async () => {
        if (!records.length) return;
        await upload(settings, records);
        Object.assign(current, checkpoint);
        state.scan.accepted += records.length;
        await saveState(state);
        records = [];
      };
      for (const item of items) {
        if (compareIds(item.id, current.afterUrl) <= 0 || !/^https?:\/\//i.test(item.url || "")) continue;
        await checkSettings(settings);
        const afterVisit = current.currentUrl === item.id ? current.afterVisit : "";
        const visits = await chrome.history.getVisits({ url: item.url });
        const pending = visits.filter(visit => {
          if (!visit.visitId || !Number.isFinite(visit.visitTime)) throw new Error("Chrome 返回的访问记录缺少 ID 或访问时间。");
          return visit.visitTime >= current.start && visit.visitTime < current.end && compareIds(visit.visitId, afterVisit) > 0;
        }).sort((left, right) => compareIds(left.visitId, right.visitId));
        for (const visit of pending) {
          records.push({
            visit_id: visit.visitId, url: item.url, title: item.title || "", visited_at: visit.visitTime
          });
          checkpoint.currentUrl = item.id;
          checkpoint.afterVisit = visit.visitId;
          if (records.length >= PAGE_SIZE) await flush();
        }
        checkpoint.afterUrl = item.id;
        checkpoint.currentUrl = "";
        checkpoint.afterVisit = "";
      }
      await flush();
      state.scan.ranges.pop();
      await saveState(state);
    }
    await checkSettings(settings);
    state.completedThrough = state.scan.end;
    state.scan = null;
    state.backfillComplete = true;
    state.lastSuccess = Date.now();
    state.status = "idle";
    await saveState(state);
  } catch (error) {
    state.status = error instanceof SyncStopped ? "idle" : "error";
    state.lastError = error instanceof SyncStopped ? "" : error.message || String(error);
    await saveState(state);
  }
}

function requestSync() {
  if (running) {
    requested = true;
    return;
  }
  running = ready.then(syncHistory).finally(() => {
    running = null;
    if (requested) {
      requested = false;
      requestSync();
    }
  });
}

async function handleMessage(message) {
  const settings = await getSettings();
  if (message.type === "status") {
    const { syncState } = await chrome.storage.local.get("syncState");
    return { ok: true, settings, syncState, running: Boolean(running) };
  }
  if (message.type === "save-settings") {
    const backendURL = normalizeBackend(message.backendURL);
    const token = message.token.trim();
    if (message.enabled && !token) throw new Error("请填写后端令牌。");
    if (message.enabled && !(await chrome.permissions.contains({ origins: [originPattern(backendURL)] }))) {
      throw new Error("尚未授权后端地址，配置未保存。");
    }
    const changed = backendURL !== settings.backendURL || token !== settings.token;
    const next = { ...settings, backendURL, token, enabled: Boolean(message.enabled), revision: changed ? crypto.randomUUID() : settings.revision };
    await chrome.storage.local.set({ settings: next });
    return { ok: true, settings: next };
  }
  if (message.type === "sync") {
    if (!settings.enabled) throw new Error("请先开启同步。");
    requestSync();
    return { ok: true };
  }
  throw new Error("未知操作。");
}

chrome.runtime.onMessage.addListener((message, sender, respond) => {
  handleMessage(message).then(respond, error => respond({ ok: false, error: error.message }));
  return true;
});
chrome.action.onClicked.addListener(() => chrome.runtime.openOptionsPage());
chrome.history.onVisited.addListener(() => requestSync());
chrome.alarms.onAlarm.addListener(alarm => { if (alarm.name === ALARM_NAME) requestSync(); });
chrome.runtime.onStartup.addListener(() => requestSync());
chrome.runtime.onInstalled.addListener(() => requestSync());
chrome.storage.onChanged.addListener((changes, area) => {
  if (area === "local" && changes.settings) {
    ready.then(() => configureAlarm(changes.settings.newValue)).then(requestSync);
  }
});
ready.then(requestSync);
