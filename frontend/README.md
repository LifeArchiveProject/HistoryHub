<div align="center">
  <img src="./public/logo.png" alt="Logo">
</div>

这是一个基于 Vue 3 开发的 B 站历史记录分析工具的前端项目，为用户提供丰富的 B 站观看历史数据分析功能。

## 该项目需要配合 [BilibiliHistoryFetcher](https://github.com/2977094657/BilibiliHistoryFetcher) 后端项目一起使用

## 零基础快速运行（Windows 免安装版，推荐）

1. 下载 exe：后端 https://github.com/2977094657/BilibiliHistoryFetcher/releases/latest
2. 下载 exe：前端 https://github.com/2977094657/BiliHistoryFrontend/releases/latest
3. 两个都双击运行即可

## 快速开始

### 使用 Docker 安装

#### 使用预构建镜像（GitHub Container Registry）

```bash
docker pull ghcr.io/lifearchiveproject/bili-history-frontend:latest
docker run --name bili-history-frontend-web -p 5173:80 -d ghcr.io/lifearchiveproject/bili-history-frontend:latest
```

仓库迁移到 `LifeArchiveProject` 后，前端镜像使用 `ghcr.io/lifearchiveproject/bili-history-frontend`。`ghcr.io/2977094657/...` 属于历史个人账号命名空间，不再作为推荐安装来源。若拉取时提示 `denied` 或 `unauthorized`，请确认 GitHub Packages 中对应容器包已设为 Public。

1. 安装[Docker](https://docs.docker.com/get-started/get-docker/).
2. 构建镜像：`docker build -t bili-history-frontend-web:dev .`
3. 启动容器：`docker run --name bili-history-frontend-web -p 5173:80 -d bili-history-frontend-web:dev`
4. 停止容器：`docker stop bili-history-frontend-web`

### [通过 1Panel 部署](https://github.com/2977094657/BilibiliHistoryFetcher/discussions/65)
由社区贡献者 [@QYG2297248353](https://github.com/QYG2297248353) 实现 ([#66](https://github.com/2977094657/BilibiliHistoryFetcher/pull/66))
### 使用源码安装

1. 克隆项目
```bash
git clone https://github.com/2977094657/BiliHistoryFrontend.git
cd BilibiliHistoryFrontend
```

2. 安装依赖
```bash
npm install
```

3. 启动开发服务器
```bash
# 网页版开发
npm run dev
```

## 首次使用指南

1. **登录账号**
  - 点击侧边栏的设置，然后配置你的服务器地址
  - 然后点击侧边栏中的"未登录"状态
  - 使用 B 站手机 APP 扫描二维码进行登录
  - 登录成功后会显示你的用户名

2. **获取历史记录**
  - 登录成功后，点击导航栏中的"实时更新"按钮
  - 首次使用时会自动获取你的全部历史记录，这可能需要一些时间
  - 获取完成后数据会自动导入到本地数据库
  - 页面会自动刷新并显示你的观看历史

3. **后续使用**
  - 默认的计划任务会在每天 0 点自动获取历史记录
  - 可去设置里配置邮箱进行通知，不配置不影响自动获取，只是无法收到通知
  - 每次打开页面时，建议点击"实时更新"以获取最新记录
  - 实时更新只会获取新增的记录，速度很快

## 页面介绍

**1. 年度总结页面**
<img src="./public/QQ20250705-180733.png" alt="">
<img src="./public/layout-collage-1751711304790.jpg" alt="">
<img src="./public/layout-collage-1751711351462.jpg" alt="">
<img src="./public/layout-collage-1751711376523.jpg" alt="">
<img src="./public/layout-collage-1751711396674.jpg" alt="">
<img src="./public/layout-collage-1751711408262.jpg" alt="">

**2. 主页** 支持列表/网格切换与日期、分区筛选，一键实时更新，支持隐私模式。
<img src="./public/home.png" alt="">

**3. 评论** 登录后查看我的评论，支持关键词与类型筛选，并可跳转原文。
<img src="./public/Comments.png" alt="">

**4. 我的收藏** 支持查看我创建/收藏及本地收藏夹，可同步到本地并下载收藏内容。
<img src="./public/favorites.png" alt="">

**5. 媒体管理** 集中管理已下载视频与图片，查看/编辑备注与评论，并可批量补全视频详情。
<img src="./public/images.png" alt="">

**6. 计划任务** 统一管理定时与链式任务，支持新建/编辑/执行/启用或禁用，并查看历史与成功率。
<img src="./public/scheduler.png" alt="">

**7. 设置** 配置服务器、隐私与布局、数据导出，也可以启用/关闭后端 MCP 只读服务并复制 AI 连接提示词。
<img src="./public/setting.png" alt="">

**8. 视频下载功能** 输入 BV/链接或 UP UID 下载单个/合集/投稿，过程实时反馈。
<img src="./public/download.png" alt="">
<img src="./public/SingleVideo.png" alt="">
<img src="./public/MultipleVideos.png" alt="">


**9. 动态下载** 输入用户MID下载B站动态内容，实时显示下载进度
<img src="./public/dynamic.png" alt="">


## 使用 Tauri 构建桌面应用

### GitHub Actions 自动构建（多平台包体）

推送 tag（例如 `v1.0.0`）后，会自动在 GitHub Releases 里生成 Windows/macOS/Linux 的安装包与产物。

**环境准备**

1. 安装 Rust 开发环境
  - 按照 [Rust 官方指南](https://www.rust-lang.org/tools/install) 安装 Rust
  - Windows 用户还需安装 [Visual Studio C++ 构建工具](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

2. 安装 Node.js 依赖
   ```bash
   npm install
   ```

**开发与构建**

1. 开发模式
   ```bash
   npm run tauri:dev
   ```
   这将启动一个开发服务器，并自动打开应用窗口，支持热重载。

2. 构建可执行文件
   ```bash
   npm run tauri:build:exe
   ```
   构建完成后，将在项目根目录生成 `BiliBili-History-Frontend.exe` 可执行文件。

3. 清理构建文件
   ```bash
   npm run tauri:clean
   ```
   清理 `src-tauri/target` 目录中的构建产物，释放磁盘空间。

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 致谢

- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) - 没有它就没有这个项目
- [Yutto](https://yutto.nyakku.moe/) - 可爱的 B 站视频下载工具
- [ArtPlayer](https://github.com/zhw2590582/ArtPlayer) - 强大且灵活的 HTML5 视频播放器
- [aicu.cc](https://www.aicu.cc/) - 第三方 B 站用户评论 API
- 所有贡献者，特别感谢:
  - [@eli-yip](https://github.com/eli-yip) 对 Docker 部署的贡献
  - [@QYG2297248353](https://github.com/QYG2297248353) 对 1Panel 部署的贡献

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=2977094657/BiliHistoryFrontend&type=Date)](https://star-history.com/#2977094657/BiliHistoryFrontend&Date)
