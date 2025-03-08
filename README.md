# Bilibili History Analyzer (获取B站历史记录并进行分析的工具)

<div align="center">
  <a href="https://github.com/SocialSisterYi/bilibili-API-collect" target="_blank">
    <img src="https://socialsisteryi.github.io/bilibili-API-collect/logo2.jpg" alt="bilibili-API-collect Logo" width="64" height="64">
  </a>
  <p>本项目基于 <a href="https://github.com/SocialSisterYi/bilibili-API-collect" target="_blank">bilibili-API-collect</a> 提供的API文档开发，感谢 SocialSisterYi 的杰出贡献。</p>
</div>

由于b站历史只会显示最近几个月的，所以历史记录会慢慢过期，因此该项目用于获取、处理、分析和可视化哔哩哔哩用户的观看历史数据。它提供了完整的数据处理流程，从数据获取到可视化展示，并支持自动化运行和邮件通知。

## 配套前端请前往此项目[BiliHistoryFrontend](https://github.com/LifeArchiveProject/BiliHistoryFrontend) 

## 主要功能

1. **数据获取与存储**
   - 自动获取B站观看历史记录
   - 按年/月/日层级存储数据
   - 支持增量更新，避免重复获取
   - 自动分类视频内容

2. **数据处理与分析**
   - 数据清洗和标准化
   - SQLite数据库存储
   - 视频分类统计
   - 观看时间分析

3. **可视化展示**
   - 生成年度观看热力图
   - 支持自定义热力图样式
   - 可配置图表尺寸和颜色

4. **视频下载功能**
   - 支持下载B站视频
   - 自定义下载目录
   - 实时显示下载进度

<div align="center">
  <a href="https://yutto.nyakku.moe/" target="_blank">
    <img src="https://yutto.nyakku.moe/logo-mini.svg" alt="Yutto Logo" width="32" height="32">
  </a>
  <p>视频下载功能通过 <a href="https://yutto.nyakku.moe/" target="_blank">Yutto</a> 实现，感谢 Yutto 开发团队的开源贡献。</p>
</div>

5. **图片管理功能**
   - 下载视频封面
   - 下载UP主头像
   - 支持本地图片缓存
   - 支持按年份下载
   - 自动清理无效图片

6. **自动化任务**
   - 支持定时任务调度
   - 自动数据同步
   - 错误重试机制
   - 邮件通知功能

7. **本地摘要功能**
   - DeepSeek AI 集成
   - 使用faster whisper 将音频转换为字幕
   - 视频摘要获取与保存

8. **API接口**
   - RESTful API设计
   - 完整的接口文档
   - 支持多种查询方式

## 系统要求

- Python 3.10+
- SQLite 3
- FFmpeg（用于视频下载）
- 必要的Python包（见requirements.txt）
- NVIDIA GPU（可选，用于加速音频转文字）
  - 支持CUDA 9.0 及以上版本
  - 建议使用CUDA 11.8 或更高版本以获得最佳性能
  - 如果没有GPU，将自动使用CPU模式运行

## 快速开始

1. **安装依赖**

项目提供了自动化的依赖安装脚本，可以自动检测您的系统环境并安装合适的依赖：

```bash
python install_dependencies.py
```

该脚本会：
- 安装基本依赖（requirements.txt中的包）
- 检测系统CUDA环境
- 安装适配您系统的PyTorch版本
- 安装音频转文字所需的依赖（faster-whisper等）

您也可以使用以下选项：
```bash
# 查看系统环境信息和CUDA兼容性
python install_dependencies.py --info

# 强制使用CPU版本（不使用GPU加速）
python install_dependencies.py --force-cpu

# 指定CUDA版本安装
python install_dependencies.py --force-cuda 12.7

# 跳过PyTorch相关依赖安装
python install_dependencies.py --skip-torch
```

音频转文字功能依赖说明：
- 如果您的系统有NVIDIA GPU，脚本会自动安装GPU加速版本的依赖
- 如果没有检测到GPU，会安装CPU版本（性能较低但仍可使用）
- 所需的主要依赖包括：
  - PyTorch：深度学习框架
  - faster-whisper：优化版语音识别模型
  - huggingface-hub：模型下载和管理

详细的CUDA和PyTorch版本对应关系请参考 [CUDA_SETUP.md](CUDA_SETUP.md)

2. **配置文件**

在 `config/config.yaml` 中配置以下信息：
```yaml
# B站用户认证
SESSDATA: "你的SESSDATA"

# 邮件通知配置
email:
  smtp_server: smtp.qq.com
  smtp_port: 587
  sender: "发件人邮箱"
  password: "邮箱授权码"
  receiver: "收件人邮箱"

# DeepSeek AI API配置
deepseek:
  api_key: "你的DeepSeek API密钥"
  api_base: "https://api.deepseek.com/v1"
  default_model: "deepseek-reasoner"

# 服务器配置
server:
  host: "localhost"
  port: 8899
```

3. **运行程序**
```bash
python main.py
```

## API接口

基础URL: `http://localhost:8899`

完整API文档访问：`http://localhost:8899/docs`

## 自动化任务配置

在 `config/scheduler_config.yaml` 中配置定时任务：
```yaml
tasks:
  fetch_history:
    schedule:
      type: "daily"
      time: "00:00"
  
  analyze_data:
    schedule:
      type: "chain"
    requires:
      - fetch_history
```

## 数据存储结构

```
output/
├── BSummary/            # b站视频摘要
├── database/            # 计划任务SQLite数据库
├── download_video/      # 视频下载目录
├── history_by_date/     # 原始历史数据
│   └── YYYY/MM/DD.json
├── images/              # 图片
├── logs/                # 运行日志
├── stt/                 # 转换后的字幕
├── summary/             # 视频摘要
├── cleaned_history/     # 清理后的数据
├── heatmap/             # 热力图输出
```

## 安全说明

1. API请求限制：
   - 默认每秒1次请求
   - 可在配置文件中调整

2. Cookie安全：
   - 定期更新SESSDATA
   - 不要分享配置文件

## 常见问题

1. **Cookie经常失效**
   - 删除localStorage中的`ac_time_value`
   - 重新获取SESSDATA
   - 更新配置文件

2. **视频下载失败**
   - 确保已安装FFmpeg
   - 检查网络连接
   - 确认视频是否可以下载（会员限制等）
   - 检查磁盘空间是否充足

3. **图片下载问题**
   - 检查网络连接
   - 确保有足够的磁盘空间
   - 尝试清理并重新下载
   - 检查图片目录权限

4. **音频转文字问题**
   - 确保已正确安装PyTorch和相关依赖
   - 检查CUDA版本是否兼容（GPU用户）
   - 确保系统内存充足（建议至少4GB可用内存）
   - 如遇性能问题，可尝试使用`--force-cuda`指定其他CUDA版本

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 许可证

MIT License

## 致谢

- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect) - 没有它就没有这个项目
- [Yutto](https://yutto.nyakku.moe/) - 可爱的B站视频下载工具
- [FasterWhisper](https://github.com/SYSTRAN/faster-whisper) - 音频转文字
- [DeepSeek](https://github.com/deepseek-ai/DeepSeek-R1) - DeepSeek AI API
- 所有贡献者

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=LifeArchiveProject/HistoryHub&type=Date)](https://star-history.com/#LifeArchiveProject/HistoryHub&Date)