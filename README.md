# Bilibili 历史记录分析器

该项目旨在处理、分析和可视化哔哩哔哩（Bilibili）用户的观看历史数据。它提供了一系列工具，包括数据获取、清洗、数据库导入、历史分析以及通过 API 进行访问的功能。

## 项目结构

```
./
├─ config/
│   ├─ config.yaml
│   └─ categories.json
├─ routers/
│   ├─ analysis.py
│   ├─ clean_data.py
│   ├─ export.py
│   ├─ fetch_bili_history.py
│   ├─ import_data_mysql.py
│   └─ import_data_sqlite.py
├─ scripts/
│   ├─ analyze_bilibili_history.py
│   ├─ bilibili_history.py
│   ├─ clean_data.py
│   ├─ export_to_excel.py
│   ├─ import_database.py
│   ├─ import_sqlite.py
│   ├─ sql_statements_mysql.py
│   └─ utils.py
├─ main.py
└─ README.md
```

## 主要功能

1. **数据获取**：从 Bilibili API 获取用户的观看历史数据。
2. **数据清洗**：清理和格式化原始数据。
3. **数据库导入**：支持将数据导入到 MySQL 或 SQLite 数据库。
4. **数据分析**：分析用户的观看习惯，包括每日和每月的观看统计。
5. **数据导出**：将分析结果导出为 Excel 文件。
6. **API 接口**：提供 RESTful API 以访问各种功能。

## 配置

项目使用 `config/config.yaml` 文件进行配置。主要配置项包括：

- `cookie`：Bilibili 用户的 cookie，用于 API 认证。
- `input_folder`：原始历史记录数据的输入文件夹。
- `output_folder`：清理后的历史记录数据的输出文件夹。
- `db_file`：SQLite 数据库文件名。
- `log_file`：导入日志文件名。
- `categories_file`：分类配置文件名。
- `fields_to_remove`：清理数据时需要移除的字段列表。

## 使用方法

1. 克隆仓库并安装依赖：
   ```
   git clone <repository-url>
   cd <repository-name>
   pip install -r requirements.txt
   ```

2. 配置 `config/config.yaml` 文件，确保填入正确的 Bilibili cookie。

3. 运行主程序：
   ```
   python main.py
   ```

4. 访问 API 接口（默认地址为 `http://127.0.0.1:8000`）：
   - `/fetch/fetch_history`：获取历史记录
   - `/clean/clean_data`：清理数据
   - `/importMysql/import_data_mysql`：导入数据到 MySQL
   - `/importSqlite/import_data_sqlite`：导入数据到 SQLite
   - `/analysis/daily_counts`：获取每日观看计数
   - `/analysis/monthly_counts`：获取每月观看计数
   - `/export/export_history`：导出数据到 Excel

## 注意事项

- 确保在使用前正确配置 `config.yaml` 文件。
- 首次运行时，程序会获取所有可用的历史记录。后续运行只会同步新的记录。
- API 请求频率限制为每秒一次，以避免对 Bilibili 服务器造成过大压力。

## 贡献

欢迎提交 issues 和 pull requests 来改进这个项目。

## 许可证

[MIT License](LICENSE)
