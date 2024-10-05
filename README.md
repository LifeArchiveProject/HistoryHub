# 获取哔哩哔哩历史记录并生成日历图

该项目旨在处理、分析和可视化哔哩哔哩用户的历史数据。这些工具包括数据清洗、数据库导入、历史分析以及通过邮件通知进行自动化日志记录。以下部分详细解释了每个模块的用途和使用方法。

最终效果如下：
<img src="heatmap.png"/>

## 项目起因
由于想找以前的一个历史视频时发现只有前面10几天记录的视频数量是准确的，往前推半个月发现每天记录的视频只有4，5个甚至只有1个，于是有了此项目

## 风险
API设置了每隔1秒请求一次，目前我已经自动化运行几天了，由于是每天晚上0点请求且一天只运行1次，所以还没有任何风险，还是不放心的可以调整下面内容来自定义暂停频率和个性化请求：
```python
# 暂停1秒在请求
time.sleep(1)

headers = {
    'Cookie': "SESSDATA=" + cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Referer': 'https://www.bilibili.com',
}

# 初始化参数
params = {
    'ps': 30,  # 每页数量，默认为 20，最大 30
    'max': '',  # 初始为空
    'view_at': '',  # 初始为空
    'business': '',  # 可选参数，默认为空表示获取所有类型
}
```

## 获取历史记录

- `bilibili_history.py`  
  输入自己的哔哩哔哩Cookie来处理和获取历史数据，使用的API来自[bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)

  ```text
  在当前目录下新建名为 cookie.txt 的文件，在里面输入自己的Cookie即可被程序读取
  ```
  第一次运行会直接获取所有历史记录，并生成年月文件夹，后续则会读取`cursor_history.json`里的oid(kid)，这两个id是一样的，以及生成的文件夹里的天数来判断已有的数据，并同步未同步的数据，文件夹结构如下：
  ```text
  ├───history_by_date
  │   └───2024
  │       ├───07
  │       ├───08
  │       ├───09
  │       └───10
  ```

## 简单的数据分析
- `analyze_bilibili_history.py`  
  简单的分析获取到的哔哩哔哩历史数据，运行后保存的`daily_count.json`文件（统计每日观看的视频数量）用于后续生成日历图，数据分析输出内容如下：
  ```text
  2024-09-28: 看了 87 个视频，最早是 00:01:22，最晚是 19:50:56
  2024-09-29: 看了 116 个视频，最早是 00:56:13，最晚是 22:06:07
  2024-09-30: 看了 101 个视频，最早是 01:05:14，最晚是 23:35:24
  2024-10-01: 看了 150 个视频，最早是 00:44:03，最晚是 23:57:07
  2024-10-02: 看了 73 个视频，最早是 00:08:38，最晚是 22:19:31
  
  每月观看视频数量：
  2024-07: 21 个视频
  2024-08: 30 个视频
  2024-09: 1108 个视频
  2024-10: 223 个视频
  每天观看数量已保存到 daily_count.json
  ```

## 生成日历图
- `heatmap_visualizer.py`  
将`output_dir`设置为你的输出路径，如果后续要在部署到服务器在线访问，就设置为你服务器网站目录
  ```python
  class HeatmapVisualizer:
      def __init__(self, data_file='daily_count.json', template_file='template.html', output_dir='/xxx/xxx/xxx'):
          self.data_file = data_file
          self.template_file = template_file
          self.output_dir = output_dir  # 添加输出目录
          self.daily_count = self.load_data()
          self.date_range = self.generate_date_range()
  ```
  使用`analyze_bilibili_history.py`生成的`daily_count.json`来生成日历图，效果如下：
<img src="\heatmap.png"/>
- `template.html`
日历图的模板文件，用来定义样式

## 清理数据
- `clean_data.py`  
  如果你要存入数据库，并且只想存入有意义的字段数据，具体字段意思见[bilibili-API-collect的历史记录API文档](https://socialsisteryi.github.io/bilibili-API-collect/docs/history_toview/history.html)那么此脚本就是用来删除不想要的字段
  ```python
  # 想要删减的字段
    fields_to_remove = ['long_title', 'uri', 'badge', 'current', 'total', 'new_desc', 'is_finish', 'live_status']
  ```
  删除后的数据存放格式和原来的一样，只不过文件夹前面多了个cleaned

## 导入到MySQL数据库
- `import_database.py`  
  该模块负责将清洗和处理后的数据导入数据库，可以用于存储数据以便后续分析或进行多用户数据处理。
- 建表语句，如果你要导入清理后的数据，那么你需要删除你不需要的字段，以及代码里不需要的字段
  ```mysql
  CREATE TABLE bilibili_history (
    id BIGINT PRIMARY KEY COMMENT'主键，使用雪花算法等库生成的唯一ID',
    title VARCHAR(255) NOT NULL COMMENT'条目标题，字符串，最大255字符',
    long_title VARCHAR(255) COMMENT'条目副标题（有时为空），最大255字符',
    cover VARCHAR(255) COMMENT'条目封面图url，用于专栏以外的条目',
    covers JSON COMMENT'条目封面图组，有效时array无效时null，仅用于专栏',
    uri VARCHAR(255) COMMENT'重定向url仅用于剧集和直播',
    oid BIGINT NOT NULL COMMENT '目标id稿件视频&剧集（当business=archive或business=pgc时）：稿件avid直播（当business=live时）：直播间id文章（当business=article时）：文章cvid文集（当business=article-list时）：文集rlid',
    epid BIGINT DEFAULT 0 COMMENT'剧集epid	仅用于剧集',
    bvid VARCHAR(50) NOT NULL COMMENT'稿件bvid	仅用于稿件视频',
    page INT DEFAULT 1 COMMENT'观看到的视频分P数	仅用于稿件视频',
    cid BIGINT COMMENT'观看到的对象id	稿件视频&剧集（当business=archive或business=pgc时）：视频cid文集（当business=article-list时）：文章cvid',
    part VARCHAR(255) COMMENT'观看到的视频分 P 标题	仅用于稿件视频',
    business VARCHAR(50) COMMENT'视频业务类型（如archive代表普通视频），最大50字符',
    dt INT NOT NULL COMMENT'记录查看的平台代码	1 3 5 7 手机端，2 web端，4 6 pad端，33TV端，0其他',
    videos INT DEFAULT 1 COMMENT'视频分 P 数目	仅用于稿件视频，整数型，默认为1',
    author_name VARCHAR(100) NOT NULL COMMENT 'UP 主昵称',
    author_face VARCHAR(255) COMMENT'UP 主头像 url',
    author_mid BIGINT NOT NULL COMMENT'UP 主 mid',
    view_at BIGINT NOT NULL COMMENT'查看时间	时间戳',
    progress INT DEFAULT 0 COMMENT'视频观看进度，单位为秒，用于稿件视频或剧集',
    badge VARCHAR(50) COMMENT'角标文案	稿件视频 / 剧集 / 笔记',
    show_title VARCHAR(255) COMMENT'分 P 标题	用于稿件视频或剧集',
    duration INT NOT NULL COMMENT'视频总时长	用于稿件视频或剧集',
    current VARCHAR(255) COMMENT'未知字段',
    total INT DEFAULT 0 COMMENT'总计分集数	仅用于剧集',
    new_desc VARCHAR(255) COMMENT'最新一话 / 最新一 P 标识	用于稿件视频或剧集',
    is_finish TINYINT(1) DEFAULT 0 COMMENT'是否观看完，布尔值，0为否，1为是',
    is_fav TINYINT(1) DEFAULT 0 COMMENT'是否收藏，布尔值，0为否，1为是',
    kid BIGINT COMMENT'条目目标 id',
    tag_name VARCHAR(100) COMMENT'子分区名	用于稿件视频和直播',
    live_status TINYINT(1) DEFAULT 0 COMMENT'直播状态	仅用于直播0未开播1已开播',
    INDEX (author_mid) COMMENT'建立作者MID的索引，用于快速查询',
    INDEX (view_at) COMMENT'建立观看时间的索引'
  );
  ```
  ```python
  # 连接到 MySQL 数据库
  def connect_to_db():
      return pymysql.connect(
          host='localhost',# 本地则不需要修改，如果是远程的改为你的远程ip
          port=3306,  # 指定 MySQL 端口，默认是3306
          user='',  # 替换为你的 MySQL 用户名
          password='',  # 替换为你的 MySQL 密码
          db='',  # 替换为你的数据库名
          charset='utf8mb4',
          cursorclass=pymysql.cursors.DictCursor
      )
  
  # 主函数
  if __name__ == '__main__':
      # 设置数据文件夹，可以选择导入清理前的文件夹 'history_by_date' 或清理后的文件夹 'cleaned_history_by_date'
      data_folder = 'cleaned_history_by_date'  # 或 'history_by_date'
  
      # 调用导入函数，导入所有文件
      import_all_history_files(data_folder)
  ```

## 部署到linux服务器实现自动化同步
- 我用的是宝塔面板进行的可视化操作，首先将需要的py文件导入到文件夹，然后点击左侧边栏选择`网站`，进入后选择顶部`Python项目`然后安装解释器版本，我安装的是`3.12.3`
- 安装后需要在安装以下包才可以正常运行：
  ```shell
  # 必装，用于 API 发送请求
  解释器路径/3.12.3/bin/pip3 install requests
  # 想要导入数据到数据库则要安装，与 MySQL 数据库进行交互
  解释器路径/3.12.3/bin/python3.12 -m pip install pymysql
  # 想要生成日历图则要安装，用于生成图表的 Python 库，用来生成日历图
  解释器路径/3.12.3/bin/python3.12 -m pip install pyecharts
  # 想要生成日历图则要安装，用于 Web 开发中生成 HTML
  解释器路径/3.12.3/bin/python3.12 -m pip install jinja2
  ```
- 下面开始部署自动化脚本，我导入的的是未清理过字段的原始数据，所以没有部署`clean_data.py`文件，首先点击左侧边栏的计划任务，点击添加任务，选择自己要执行的时间和频率，然后输入以下脚本内容，脚本里可以带注释：
  ```shell
  #!/bin/bash
  
  # 创建日志文件夹，格式为 /www/wwwroot/python/logs/年/月
  mkdir -p /www/wwwroot/python/logs/$(date +%Y/%m)
  
  # 进入项目目录
  cd /www/wwwroot/python
  
  # 写入运行时间到当天的日志文件
  echo -e "\n========== 运行时间: $(date '+%Y-%m-%d %H:%M:%S') ==========" >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log
  
  # 运行 bilibili_history.py 并将输出追加到日志文件
  /www/server/pyporject_evn/versions/3.12.3/bin/python3.12 bilibili_history.py >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log 2>&1
  
  # 如果 bilibili_history.py 成功运行，运行 import_database.py
  if [ $? -eq 0 ]; then
      /www/server/pyporject_evn/versions/3.12.3/bin/python3.12 import_database.py >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log 2>&1
  else
      echo "bilibili_history.py 执行失败，跳过 import_database.py" >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log
      exit 1  # 如果 bilibili_history.py 失败，则退出脚本
  fi
  
  # 如果 import_database.py 成功运行，运行 analyze_bilibili_history.py
  if [ $? -eq 0 ]; then
      /www/server/pyporject_evn/versions/3.12.3/bin/python3.12 analyze_bilibili_history.py >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log 2>&1
  else
      echo "import_database.py 执行失败，跳过 analyze_bilibili_history.py" >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log
      exit 1  # 如果 import_database.py 失败，则退出脚本
  fi
  
  # 如果 analyze_bilibili_history.py 成功运行，运行 heatmap_visualizer.py
  if [ $? -eq 0 ]; then
      /www/server/pyporject_evn/versions/3.12.3/bin/python3.12 heatmap_visualizer.py >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log 2>&1
  else
      echo "analyze_bilibili_history.py 执行失败，跳过 heatmap_visualizer.py" >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log
      exit 1  # 如果 analyze_bilibili_history.py 失败，则退出脚本
  fi
  
  # 如果 heatmap_visualizer.py 成功运行，运行 send_log_email.py
  if [ $? -eq 0 ]; then
      /www/server/pyporject_evn/versions/3.12.3/bin/python3.12 send_log_email.py >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log 2>&1
  else
      echo "heatmap_visualizer.py 执行失败，跳过 send_log_email.py" >> /www/wwwroot/python/logs/$(date +%Y/%m)/$(date +%d).log
      exit 1  # 如果 heatmap_visualizer.py 失败，则退出脚本
  fi
  
  ```

## 发送日志邮件到邮箱
- `send_log_email.py`  
  该脚本实现日志记录和错误处理。它可以通过电子邮件发送日志报告或错误信息，方便监控数据分析或导入任务的状态。

  ```python
  # 邮件配置信息
  sender_email = 'xxxxxxxxxx@qq.com'  # 发件人QQ邮箱
  receiver_email = 'xxxxxxxxxx@qq.com'  # 收件人邮箱
  smtp_server = 'smtp.qq.com'  # QQ邮箱的SMTP服务器地址
  smtp_port = 465  # SMTP SSL端口号
  smtp_password = 'xxxxxxxxxxxxxxxx'  # 发件人邮箱的授权码
  
  # 获取日志文件路径
  def get_latest_log():
      log_dir = '/xxxx/xxxx/xxxx/xxxx' # 日志路径
      today = date.today()  # 使用 datetime 的 date 获取当前日期
      year_month_dir = os.path.join(log_dir, f"{today.year}/{today.month:02d}")  # 当前年和月的目录
      log_file = os.path.join(year_month_dir, f"{today.day:02d}.log")  # 当前日志文件
      if os.path.exists(log_file):
          return log_file
      else:
          return None
  ```