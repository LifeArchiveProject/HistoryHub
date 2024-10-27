import sqlite3
import os
import json
import time
import threading
from datetime import datetime
import logging
from scripts.utils import load_config, get_base_path, get_output_path
from config.sql_statements_sqlite import INSERT_DATA, CREATE_TABLE_DEFAULT, CREATE_INDEXES

config = load_config()

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IS_SCRIPT_RUN = True

def get_base_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if IS_SCRIPT_RUN else os.getcwd()

# 定义读取分类信息的函数
def load_categories(config_path=None):
    if config_path is None:
        base_path = get_base_path()
        config_path = os.path.join(base_path, 'config', 'categories.json')
    """从 categories.json 文件中加载分类信息"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            categories = json.load(f)
            duplicated_tags = set(categories.get('duplicated_tags', []))
            unique_tag_to_main = categories.get('unique_tag_to_main', {})
            logger.info(f"成功加载分类信息：{config_path}")
            return duplicated_tags, unique_tag_to_main
    except Exception as e:
        logger.error(f"加载分类信息时发生错误: {e}")
        return set(), {}

# 加载分类信息
duplicated_tags, unique_tag_to_main = load_categories()

class SnowflakeIDGenerator:
    def __init__(self, machine_id=1, datacenter_id=1):
        self.lock = threading.Lock()
        self.machine_id = machine_id & 0x3FF
        self.datacenter_id = datacenter_id & 0x3FF
        self.sequence = 0
        self.last_timestamp = -1
        self.epoch = 1609459200000

    def _current_millis(self):
        return int(time.time() * 1000)

    def get_id(self):
        with self.lock:
            timestamp = self._current_millis()

            if timestamp < self.last_timestamp:
                raise Exception("时钟向后移动。拒绝生成 id。")

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & 0xFFF
                if self.sequence == 0:
                    while timestamp <= self.last_timestamp:
                        timestamp = self._current_millis()
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            id = ((timestamp - self.epoch) << 22) | (self.datacenter_id << 12) | self.sequence
            return id

id_generator = SnowflakeIDGenerator(machine_id=1, datacenter_id=1)

def get_years():
    current_year = datetime.now().year
    previous_year = current_year - 1
    return current_year, previous_year

def create_connection(db_file):
    """创建一个到SQLite数据库的连接"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.info(f"成功连接到SQLite数据库: {db_file}")
    except sqlite3.Error as e:
        logger.error(f"连接SQLite数据库时出错: {e}")
    return conn

def create_table(conn, table_name):
    """创建数据表并创建索引"""
    try:
        cursor = conn.cursor()
        sql = CREATE_TABLE_DEFAULT.format(table=table_name)
        cursor.execute(sql)
        conn.commit()
        logger.info(f"成功创建表: {table_name}")

        # 创建索引
        for index_sql in CREATE_INDEXES:
            cursor.execute(index_sql.format(table=table_name))
        conn.commit()
        logger.info(f"成功为表 {table_name} 创建索引")
    except sqlite3.Error as e:
        logger.error(f"创建表或索引时发生错误: {e}")
        raise

def batch_insert_data(conn, table_name, data_chunk):
    try:
        cursor = conn.cursor()
        placeholders = ', '.join(['?'] * 32)  # 添加这行代码
        insert_sql = INSERT_DATA.format(table=table_name, placeholders=placeholders)  # 修改这行代码
        cursor.executemany(insert_sql, data_chunk)
        conn.commit()
        return len(data_chunk)
    except sqlite3.Error as e:
        conn.rollback()
        logger.error(f"插入数据时发生错误: {e}")
        return 0

def import_data_from_json(conn, table_name, file_path, batch_size=1000):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"读取文件 {file_path} 时发生错误: {e}")
        return 0

    total_inserted = 0
    new_data = []

    for item in data:
        main_category = None
        history = item.get('history', {})
        business = history.get('business', '')
        tag_name = item.get('tag_name', '').strip()

        if business == 'archive':
            if tag_name in unique_tag_to_main:
                main_category = unique_tag_to_main[tag_name]
            elif tag_name in duplicated_tags:
                main_category = '待定'
            else:
                main_category = '待定'

        new_data.append((
            id_generator.get_id(),
            item.get('title', ''),
            item.get('long_title', ''),
            item.get('cover', ''),
            json.dumps(item.get('covers', [])),
            item.get('uri', ''),
            history.get('oid', 0),
            history.get('epid', 0),
            history.get('bvid', ''),
            history.get('page', 1),
            history.get('cid', 0),
            history.get('part', ''),
            business,
            history.get('dt', 0),
            item.get('videos', 1),
            item.get('author_name', ''),
            item.get('author_face', ''),
            item.get('author_mid', 0),
            item.get('view_at', 0),
            item.get('progress', 0),
            item.get('badge', ''),
            item.get('show_title', ''),
            item.get('duration', 0),
            item.get('current', ''),
            item.get('total', 0),
            item.get('new_desc', ''),
            item.get('is_finish', 0),
            item.get('is_fav', 0),
            item.get('kid', 0),
            tag_name,
            item.get('live_status', 0),
            main_category
        ))

    total_inserted = 0
    for i in range(0, len(new_data), batch_size):
        batch_chunk = new_data[i:i + batch_size]
        inserted_count = batch_insert_data(conn, table_name, batch_chunk)
        total_inserted += inserted_count

    return total_inserted

def import_all_history_files():
    base_path = get_base_path()
    full_data_folder = os.path.join(base_path, config['input_folder'])
    full_db_file = get_output_path(config['db_file'])

    total_inserted = 0
    file_insert_counts = {}

    logger.info(f"开始遍历并导入文件夹 '{full_data_folder}' 中的数据...")

    if not os.path.exists(full_data_folder):
        message = f"本地文件夹 '{full_data_folder}' 不存在，无法加载数据。"
        logger.error(message)
        return {"status": "error", "message": message}

    current_year, previous_year = get_years()
    table_name = f"bilibili_history_{current_year}"

    conn = create_connection(full_db_file)
    if conn is None:
        message = f"无法连接到数据库 {full_db_file}。"
        logger.error(message)
        return {"status": "error", "message": message}

    try:
        create_table(conn, table_name)

        for year in sorted(os.listdir(full_data_folder)):
            year_path = os.path.join(full_data_folder, year)
            if os.path.isdir(year_path) and year.isdigit():
                for month in sorted(os.listdir(year_path)):
                    month_path = os.path.join(year_path, month)
                    if os.path.isdir(month_path) and month.isdigit():
                        for day_file in sorted(os.listdir(month_path)):
                            if day_file.endswith('.json'):
                                day_path = os.path.join(month_path, day_file)
                                inserted_count = import_data_from_json(conn, table_name, day_path)
                                total_inserted += inserted_count
                                file_insert_counts[day_path] = inserted_count

        message = f"所有文件均已导入数据库，总共插入了 {total_inserted} 条数据。"
        return {"status": "success", "message": message}

    except Exception as e:
        message = f"导入过程中发生错误: {e}"
        logger.error(message)
        return {"status": "error", "message": message}

    finally:
        conn.close()

# 允许脚本独立运行
if __name__ == '__main__':
    result = import_all_history_files()
    if result["status"] == "success":
        print(result["message"])
    else:
        print(f"错误: {result['message']}")
