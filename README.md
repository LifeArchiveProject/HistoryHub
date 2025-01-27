# BilibiliHistoryFrontend

这是一个基于 Vue 3 + Electron 开发的B站历史记录分析工具的前端项目，为用户提供丰富的B站观看历史数据分析功能。

## 该项目需要配合 [BilibiliHistoryFetcher](https://github.com/LifeArchiveProject/HistoryHub) 后端项目一起使用

## 功能特点

- 🎯 **观看数据总览**：展示用户的观看历史统计数据
- 📊 **多维度分析**：
  - 标题分析：了解最受欢迎的视频标题特征
  - 时长分析：分析不同时长视频的观看偏好
  - 时间分布：展示每日、每周的观看时间分布
  - 标签分析：统计最常观看的视频标签
  - 完成率分析：分析视频观看完成度
- 🎨 **美观的数据可视化**：使用 ECharts 提供丰富的图表展示
- 💻 **跨平台支持**：能使用浏览器的地方就可以显示此页面

## 页面功能介绍

### 1. 主页面（历史记录页）
<img src="./public/home.png" alt="">

- **实时更新**：一键同步最新观看记录
- **隐私模式**：模糊化展示视频标题、封面和UP主信息
- **日期筛选**：按日期范围筛选历史记录
- **分区筛选**：按视频分区类型筛选
- **搜索功能**：
  - 支持标题搜索
  - 支持UP主搜索
  - 关键词高亮显示

- **视频基本信息展示**:
  - 标题和封面
  - UP主信息
  - 观看时间
  - 观看进度
  - 设备标记（手机、电脑、平板）
  - 视频分类标签
  - 一键跳转原视频

### 2. 设置页面
<img src="./public/setting.png" alt="">

- **数据导出**：
  - 支持按年份导出历史记录到 Excel
  - 导出过程状态实时反馈
  - 自动下载导出的文件
- **数据库下载**：
  - 支持下载完整的 SQLite 数据库文件
  - 包含所有历史记录数据
  - 方便本地备份和高级查询

### 3. 数据分析页面（部分页面涉及到隐私就不截图了）

#### 3.1 开场页（HeroPage）
<img src="public/HeroPage.png" alt="">

#### 3.2 数据概览（OverviewPage）
<img src="./public/OverviewPage.png" alt="">

#### 3.3 连续观看分析（StreakPage）
<img src="./public/StreakPage.png">

#### 3.4 时间分析（TimeAnalysisPage）
<img src="./public/TimeAnalysisPage.png">

#### 3.5 重复观看分析（RewatchPage）
<img src="./public/RewatchPage.png">

#### 3.6 整体完成率分析（OverallCompletionPage）
<img src="./public/OverallCompletionPage.png">

#### 3.7 UP主完成率分析（AuthorCompletionPage）
<img src="./public/AuthorCompletionPage.png">

#### 3.8 标签分析（TagsPage）

#### 3.9 时间分布分析（TimeDistributionPage）

#### 3.10 月度趋势分析（MonthlyPage）

#### 3.11 视频时长分析（DurationAnalysisPage）

#### 3.12 标题分析（TitleAnalysisPage）

## 技术栈

- **前端框架**：Vue 3
- **构建工具**：Vite
- **桌面端框架**：Electron
- **UI 框架**：
  - Tailwind CSS
  - Vant
  - Headless UI
- **图表库**：ECharts
- **动画效果**：
  - GSAP
  - Lottie
  - Vue Use Motion
- **工具库**：
  - Vue Router
  - Axios
  - Vue Use
  - TypeIt

## 开发环境设置

1. 克隆项目
```bash
git clone https://github.com/LifeArchiveProject/BiliHistoryFrontend.git
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

# Electron版本开发
npm run electron:dev
```

4. 构建应用
```bash
# 网页版构建
npm run build

# Electron版本构建
npm run electron:build
```

## 项目结构

```
BilibiliHistoryFrontend/
├── src/                    # 源代码目录
│   ├── api/               # API 接口
│   ├── components/        # Vue 组件
│   │   └── tailwind/     # Tailwind 样式组件
│   ├── router/           # 路由配置
│   └── style.css         # 全局样式
├── electron/              # Electron 相关代码
├── public/               # 静态资源
└── vite.config.js        # Vite 配置
```

## 使用说明

1. 首先需要运行 [BilibiliHistoryFetcher](https://github.com/LifeArchiveProject/HistoryHub) 后端服务
2. 启动本前端应用
3. 登录B站账号（通过后端服务）
4. 开始浏览和分析您的B站观看历史数据

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目。

## 许可证

[MIT License](LICENSE)

## 致谢

- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)
- 所有贡献者

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LifeArchiveProject/BiliHistoryFrontend&type=Date)](https://star-history.com/#LifeArchiveProject/BiliHistoryFrontend&Date)
