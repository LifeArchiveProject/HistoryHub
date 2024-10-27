import pymysql
import json
import os
import time
import threading
from datetime import datetime

from config.sql_statements_mysql import *
from scripts.utils import load_config, get_base_path, get_output_path

config = load_config()
base_path = get_base_path()

# 加载分类映射
def load_categories():
    categories_path = os.path.join(base_path, 'config', config['categories_file'])
    with open(categories_path, 'r', encoding='utf-8') as f:
        categories = json.load(f)
    return categories['duplicated_tags'], categories['unique_tag_to_main']

duplicated_tags, unique_tag_to_main = load_categories()

# 雪花算法生成器类
class SnowflakeIDGenerator:
    def __init__(self, machine_id=1, datacenter_id=1):
        self.lock = threading.Lock()
        self.machine_id = machine_id & 0x3FF  # 10 位
        self.datacenter_id = datacenter_id & 0x3FF  # 10 位
        self.sequence = 0
        self.last_timestamp = -1
        self.epoch = 1609459200000  # 2021-01-01 00:00:00 UTC 以毫秒为单位

    def _current_millis(self):
        return int(time.time() * 1000)

    def get_id(self):
        with self.lock:
            timestamp = self._current_millis()

            if timestamp < self.last_timestamp:
                raise Exception("时钟向后移动。拒绝生成 id。")

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & 0xFFF  # 12 bits
                if self.sequence == 0:
                    # 等待下一秒
                    while timestamp <= self.last_timestamp:
                        timestamp = self._current_millis()
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            # 生成64位ID
            id = ((timestamp - self.epoch) << 22) | (self.datacenter_id << 12) | self.sequence
            return id

# 初始化雪花ID生成器
id_generator = SnowflakeIDGenerator(machine_id=1, datacenter_id=1)

# 获取当前年份和上一年份
def get_years():
    current_year = datetime.now().year
    previous_year = current_year - 1
    return current_year, previous_year

# 连接到 MySQL 数据库，并在必要时创建数据库
def connect_to_db():
    try:
        # 首先连接到 MySQL，不指定数据库
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '123456789'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        with connection.cursor() as cursor:
            # 列出所有数据库
            cursor.execute("SHOW DATABASES;")
            databases = cursor.fetchall()

            # 检查数据库是否存在
            db_name = os.getenv('DB_NAME', 'bilibilihistory')
            print(f"使用的数据库名称是: {db_name}")
            cursor.execute(SHOW_DATABASES, (db_name,))
            result = cursor.fetchone()
            if not result:
                # 创建数据库
                cursor.execute(CREATE_DATABASE.format(db_name=db_name))
                print(f"数据库 '{db_name}' 已创建。")
            else:
                print(f"数据库 '{db_name}' 已存在。")
        connection.close()

        # 重新连接到刚创建或已存在的数据库
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', '123456789'),
            db=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        # 再次列出当前连接的数据库
        with connection.cursor() as cursor:
            cursor.execute(SELECT_DATABASE)
            current_db = cursor.fetchone()['current_db']
            print(f"当前连接的数据库是: {current_db}")

        return connection
    except Exception as e:
        print(f"连接到数据库时发生错误: {e}")
        raise

# 创建新年份的表，如果不存在
def create_new_year_table(connection, new_table, reference_table):
    try:
        with connection.cursor() as cursor:
            # 检查新表是否存在
            cursor.execute(SHOW_TABLES, (connection.db, new_table))
            if cursor.fetchone()['COUNT(*)'] == 0:
                # 检查参考表是否存在
                cursor.execute(SHOW_TABLES, (connection.db, reference_table))
                if cursor.fetchone()['COUNT(*)'] == 0:
                    # 如果参考表不存在，使用默认的 CREATE TABLE 语句
                    create_table_sql = CREATE_TABLE_DEFAULT.format(table=new_table)
                else:
                    # 如果参考表存在，复制参考表的结构
                    create_table_sql = CREATE_TABLE_LIKE.format(new_table=new_table, reference_table=reference_table)
                cursor.execute(create_table_sql)
                connection.commit()
                base_structure = "默认结构" if "CREATE TABLE" in create_table_sql else reference_table
                print(f"已创建新表: {new_table}，基于表: {base_structure}")
            else:
                print(f"表 {new_table} 已存在，无需创建。")
    except Exception as e:
        connection.rollback()
        print(f"创建新表时发生错误: {e}")
        raise

# 批量插入数据到 MySQL，支持事务回滚
def batch_insert_data(connection, insert_sql, data_chunk):
    try:
        with connection.cursor() as cursor:
            cursor.executemany(insert_sql, data_chunk)
        connection.commit()
        return len(data_chunk)
    except Exception as e:
        connection.rollback()
        print(f"    插入数据时发生错误: {e}")
        return 0

# 从 JSON 文件导入数据
def import_data_from_json(connection, insert_sql, file_path, batch_size=1000):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"JSON 解码错误在文件 {file_path}: {e}")
            return 0
        except Exception as e:
            print(f"读取文件 {file_path} 时发生错误: {e}")
            return 0

    total_inserted = 0

    try:
        # 构建要插入的数据列表，并生成唯一的id
        new_data = []
        for index, item in enumerate(data, start=1):
            main_category = None
            history = item.get('history', {})
            business = history.get('business', '')

            # 始终获取 tag_name，即使 business 不是 'archive'
            tag_name = item.get('tag_name', '').strip()

            if business == 'archive':
                if tag_name in unique_tag_to_main:
                    main_category = unique_tag_to_main[tag_name]
                elif tag_name in duplicated_tags:
                    main_category = '待定'
                else:
                    main_category = '待定'
            # 如果 business 不为 'archive'，main_category 保持为 None

            record = {
                "id": id_generator.get_id(),  # 生成唯一ID
                "title": item.get('title', ''),
                "long_title": item.get('long_title', ''),
                "cover": item.get('cover', ''),
                "covers": json.dumps(item.get('covers', [])),
                "uri": item.get('uri', ''),
                "oid": history.get('oid', 0),
                "epid": history.get('epid', 0),
                "bvid": history.get('bvid', ''),
                "page": history.get('page', 1),
                "cid": history.get('cid', 0),
                "part": history.get('part', ''),
                "business": business,
                "dt": history.get('dt', 0),
                "videos": item.get('videos', 1),
                "author_name": item.get('author_name', ''),
                "author_face": item.get('author_face', ''),
                "author_mid": item.get('author_mid', 0),
                "view_at": item.get('view_at', 0),
                "progress": item.get('progress', 0),
                "badge": item.get('badge', ''),
                "show_title": item.get('show_title', ''),
                "duration": item.get('duration', 0),
                "current": item.get('current', ''),
                "total": item.get('total', 0),
                "new_desc": item.get('new_desc', ''),
                "is_finish": item.get('is_finish', 0),
                "is_fav": item.get('is_fav', 0),
                "kid": item.get('kid', 0),
                "tag_name": tag_name,  # 确保 tag_name 被赋值
                "live_status": item.get('live_status', 0),
                "main_category": main_category  # 设置主分区
            }
            new_data.append(record)

        # 分批插入数据
        for i in range(0, len(new_data), batch_size):
            batch_chunk = new_data[i:i + batch_size]
            inserted_count = batch_insert_data(connection, insert_sql, batch_chunk)
            total_inserted += inserted_count

        return total_inserted

    except Exception as e:
        print(f"处理数据时发生错误: {e}")
        return 0

# 读取标记文件，返回上次导入的日期和文件名
def get_last_imported_file():
    file_path = get_output_path(config['log_file'])
    if not os.path.exists(file_path):
        return None, None
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data.get('last_imported_date'), data.get('last_imported_file')
        except json.JSONDecodeError:
            print("标记文件格式错误，无法解析。")
            return None, None

# 更新标记文件，记录本次导入的日期和文件名
def update_last_imported_file(last_imported_date, last_imported_file):
    file_path = get_output_path(config['log_file'])
    data = {
        'last_imported_date': last_imported_date,
        'last_imported_file': last_imported_file
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 遍历所有按日期分割的文件并导入数据
def import_all_history_files():
    data_folder = os.path.join(base_path, config['input_folder'])
    log_file = os.path.join(base_path, config['log_file'])

    total_inserted = 0
    file_insert_counts = {}

    print(f"开始遍历并导入文件夹 '{data_folder}' 中的数据...")

    if not os.path.exists(data_folder):
        print(f"本地文件夹 '{data_folder}' 不存在，无法加载数据。")
        return {"status": "error", "message": f"本地文件夹 '{data_folder}' 不存在，无法加载数据。"}

    # 获取当前年份和上一年份
    current_year, previous_year = get_years()
    new_table = f"bilibili_history_{current_year}"
    reference_table = f"bilibili_history_{previous_year}"

    connection = connect_to_db()
    try:
        # 创建新年份的表，如果不存在
        create_new_year_table(connection, new_table, reference_table)

        # 定义动态的 INSERT SQL 语句
        insert_sql = INSERT_DATA.format(table=new_table)

        # 读取上次导入的文件日期和文件名
        last_imported_date, last_imported_file = get_last_imported_file()
        print(f"上次导入的日期: {last_imported_date}, 文件: {last_imported_file}")

        # 遍历按日期分割的文件夹
        for year in sorted(os.listdir(data_folder)):
            year_path = os.path.join(data_folder, year)
            if os.path.isdir(year_path) and year.isdigit():
                for month in sorted(os.listdir(year_path)):
                    month_path = os.path.join(year_path, month)
                    if os.path.isdir(month_path) and month.isdigit():
                        for day_file in sorted(os.listdir(month_path)):
                            if day_file.endswith('.json'):
                                day_path = os.path.join(month_path, day_file)

                                # 获取当前文件的日期
                                day = ''.join(filter(str.isdigit, day_file))[:2]  # 提取前两位数字作为日
                                if len(day) != 2:
                                    print(f"无法解析文件名中的日期: {day_file}，跳过文件。")
                                    continue
                                file_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

                                # 如果当前文件日期和上次相同，继续检查文件名顺序
                                if last_imported_date:
                                    if file_date < last_imported_date:
                                        print(f"跳过文件 {day_path}，日期 {file_date} 在上次导入日期之前。")
                                        continue
                                    elif file_date == last_imported_date and day_file <= last_imported_file:
                                        print(f"跳过文件 {day_path}，文件名 {day_file} 在上次导入文件之前或相同。")
                                        continue

                                # 开始导入文件
                                inserted_count = import_data_from_json(connection, insert_sql, day_path)
                                total_inserted += inserted_count
                                file_insert_counts[day_path] = inserted_count

                                # 更新标记文件
                                update_last_imported_file(file_date, day_file)

        # 输出每个文件的插入条数
        print("\n每个文件的插入记录：")
        for file, count in file_insert_counts.items():
            print(f"{file}: 插入或更新了 {count} 条数据")

        # 输出总插入条数
        print(f"\n所有文件均已导入数据库，总共插入或更新了 {total_inserted} 条数据。")

    except Exception as e:
        print(f"导入过程中发生错误: {e}")

    finally:
        connection.close()

    return {"status": "success", "message": f"所有文件均已导入数据库，总共插入或更新了 {total_inserted} 条数据。"}

# 供外部调用的接口
def import_history():
    return import_all_history_files()

# 如果该脚本直接运行，则调用 import_all_history_files()
if __name__ == '__main__':
    result = import_all_history_files()
    if result["status"] == "success":
        print(result["message"])
    else:
        print(f"错误: {result['message']}")
