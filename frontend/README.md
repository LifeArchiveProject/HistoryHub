<p align="center">
  <img src="./public/logo.png" width="128" height="128" alt="HistoryHub Logo" />
</p>

# HistoryHub 前端

基于 Vue 3 的 B站与网页历史记录界面，提供历史同步、搜索和原链接访问。列表使用后端分页，滚动加载后续记录。

## 启动

在仓库根目录配置并启动后端，然后在此目录执行：

```bash
npm ci
npm run dev
```

前端默认连接 `http://localhost:8899`，可在“设置”中修改后端地址。

## B站历史

在“设置”中扫码登录 B站，也可在后端 `config/config.yaml` 中配置 `SESSDATA`。点击“同步历史”获取观看记录；首次同步回填历史，之后续取新记录。已有本地历史无需当前登录即可查看和搜索，点击记录标题打开原链接。

## 网页历史

在后端配置 `HISTORYHUB_SYNC_TOKEN`，或在 `config/config.yaml` 中设置 `browser_history.sync_token`。将 Chrome 扩展连接到同一后端并使用相同密钥，在“网页历史”输入密钥并保存连接。可按标题或网址搜索，点击标题打开原链接。

网页历史无需 B站登录。连接密钥仅保存在当前浏览器，按后端地址隔离，仅随网页历史请求发送。浏览器扩展位于仓库的 [extension](../extension/) 目录。

设置中可切换深色模式和隐私模式。
