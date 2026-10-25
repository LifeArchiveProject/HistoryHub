# HistoryHub

个人历史记录中心。获取 B 站观看历史，通过 Chrome 扩展同步网页访问记录，在本地或自托管服务中保存、搜索和查看。

## 功能

- **B 站历史**：扫码登录、获取历史记录、同步新增记录，保存为 SQLite 数据和按日期归档的 JSON。
- **网页历史**：通过 Chrome 扩展导入浏览器当前保留的访问记录，并持续同步新增访问。
- **历史查询**：搜索历史记录、按时间查看、滚动加载、打开原始链接。

网页访问记录包含网址、标题和访问时间，不代表视频播放完成或文章阅读完成。手机 App 内的历史需要该平台单独提供，不能由 Chrome 历史接口读取。

## 项目结构

```text
main.py / routers/ / scripts/   Python 后端
frontend/                      Vue 网页与 Tauri 桌面端
extension/                     Chrome 扩展
config/                        服务配置
output/                        历史数据
```

## 本地运行

需要 Python 3.10+、Node.js 20+ 和 npm。下面使用 uv 管理 Python 依赖。

```bash
git clone https://github.com/LifeArchiveProject/HistoryHub.git
cd HistoryHub
uv sync
uv run main.py
```

在另一个终端启动前端：

```bash
cd HistoryHub/frontend
npm ci
npm run dev
```

访问 `http://localhost:5173`。在设置中填写后端地址，默认是 `http://127.0.0.1:8899`。

## B 站历史

打开 B 站历史页面，登录后同步记录。首次同步获取平台当前可返回的历史，后续同步保存新增记录。本地已经保存的记录可直接查看，无需保持 B 站登录。

登录状态保存在服务端配置中。浏览器扩展的连接密钥与 B 站登录凭据相互独立。

## 网页历史

### 配置后端

在 `config/config.yaml` 中设置自己生成的随机连接密钥，然后重启后端：

```yaml
browser_history:
  sync_token: "替换为你自己生成的随机密钥"
```

也可使用服务进程的 `HISTORYHUB_SYNC_TOKEN` 环境变量。环境变量优先；未配置密钥时网页历史接口关闭。

### 配置 Chrome 扩展

1. 打开 `chrome://extensions` 并开启开发者模式。
2. 点击“加载已解压的扩展程序”，选择本仓库的 `extension/` 目录。
3. 打开 HistoryHub 扩展设置，填写后端地址和连接密钥，授权访问该地址并开启同步。
4. 在网页端打开“网页历史”，输入同一连接密钥，即可搜索和滚动查看。

扩展仅向配置并授权的后端发送 HTTP/HTTPS 访问记录，不上传 Cookie。首次导入覆盖 Chrome 当前仍保留且接口可见的历史；后续同步会保留同一网址的多次访问，重复同步不会生成重复记录。标题采用浏览器为该网址保存的标题。

## Docker 部署

在仓库根目录配置 `config/config.yaml`，然后执行：

```bash
docker compose up -d --build
```

- 管理页面：`http://localhost:5173`
- 后端：`http://localhost:8899`
- API 文档：`http://localhost:8899/docs`

Chrome 扩展中的地址必须是浏览器能够访问的后端地址。自托管时填写对应服务的地址。

## 数据保存

- `output/bilibili_history.db`：B 站历史数据库，文件名由 `config/config.yaml` 的 `db_file` 指定。
- `output/history_by_date/`：按日期归档的 B 站历史 JSON。
- `output/browser_history.sqlite3`：浏览器访问记录数据库。
- `config/`：服务配置、B 站登录信息和连接密钥。

迁移或备份时，停止服务后复制 `output/` 和 `config/`，在新环境恢复到相同目录或挂载位置。不要将包含真实凭据的配置提交到仓库。

## API

完整接口见运行中的 `/docs`。

| 接口 | 用途 |
| --- | --- |
| `GET /health` | 服务状态 |
| `/login/*` | B 站登录 |
| `GET /fetch/bili-history` | 获取并保存 B 站历史 |
| `GET /fetch/bili-history-realtime` | 同步 B 站新增历史 |
| `GET /history/all` | 分页查看 B 站历史 |
| `GET /history/search` | 搜索 B 站历史 |
| `POST /browser-history/sync` | 接收 Chrome 访问记录 |
| `GET /browser-history/records` | 游标分页查询网页历史 |

网页历史两个接口都需要 `Authorization: Bearer <连接密钥>`。

## 构建

网页构建：在 `frontend/` 运行 `npm run build`。桌面端使用同目录下的 `npm run tauri:build`，需要对应平台的 Tauri 构建环境。后端可通过项目根目录的 `python build.py` 打包。

## 许可证

[MIT](LICENSE.md)
