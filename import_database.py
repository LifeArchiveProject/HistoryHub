import pymysql
import json
import os
from datetime import datetime

# 获取当前年份和上一年份
def get_years():
    current_year = datetime.now().year
    previous_year = current_year - 1
    return current_year, previous_year

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

# 创建新年份的表，如果不存在
def create_new_year_table(connection, new_table, reference_table):
    try:
        with connection.cursor() as cursor:
            # 检查新表是否存在
            cursor.execute("""
                SELECT COUNT(*)
                FROM information_schema.tables 
                WHERE table_schema = %s 
                AND table_name = %s
            """, (connection.db.decode(), new_table))
            if cursor.fetchone()['COUNT(*)'] == 0:
                # 创建新表，基于参考表的结构
                create_table_sql = f"CREATE TABLE {new_table} LIKE {reference_table};"
                cursor.execute(create_table_sql)
                connection.commit()
                print(f"已创建新表: {new_table}，基于表: {reference_table}")
            else:
                print(f"表 {new_table} 已存在，无需创建。")
    except Exception as e:
        connection.rollback()
        print(f"创建新表时发生错误: {e}")

# 获取现有的 oid 集合
def get_existing_oids(connection, table_name, oids):
    if not oids:
        return set()
    query = f"SELECT oid FROM {table_name} WHERE oid IN ({','.join(['%s'] * len(oids))})"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, oids)
            result = cursor.fetchall()
        return {row['oid'] for row in result}
    except Exception as e:
        print(f"查询现有 oid 时发生错误: {e}")
        return set()

# 批量插入数据到 MySQL，支持事务回滚
def batch_insert_data(connection, table_name, insert_sql, data_chunk):
    try:
        with connection.cursor() as cursor:
            cursor.executemany(insert_sql, data_chunk)
        connection.commit()
        print(f"成功插入或更新 {len(data_chunk)} 条数据到 {table_name}。")
        return len(data_chunk)
    except Exception as e:
        connection.rollback()
        print(f"插入数据时发生错误: {e}")
        return 0

# 从 JSON 文件中读取数据并批量插入到 MySQL
def import_data_from_json(connection, table_name, insert_sql, file_path, batch_size=1000):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_inserted = 0

    try:
        all_oids = [item['history']['oid'] for item in data]
        existing_oids = get_existing_oids(connection, table_name, all_oids)

        # 筛选出未在数据库中的新数据
        new_data = [
            {
                "id": item['history']['oid'],
                "title": item['title'],
                "long_title": item.get('long_title', ''),
                "cover": item.get('cover', ''),
                "covers": json.dumps(item.get('covers', [])),
                "uri": item.get('uri', ''),
                "oid": item['history']['oid'],
                "epid": item['history'].get('epid', ''),
                "bvid": item['history'].get('bvid', ''),
                "page": item['history'].get('page', 1),
                "cid": item['history'].get('cid', ''),
                "part": item['history'].get('part', ''),
                "business": item['history'].get('business', ''),
                "dt": item['history'].get('dt', ''),
                "videos": item.get('videos', 1),
                "author_name": item.get('author_name', ''),
                "author_face": item.get('author_face', ''),
                "author_mid": item.get('author_mid', ''),
                "view_at": item.get('view_at', 0),
                "progress": item.get('progress', 0),
                "badge": item.get('badge', ''),
                "show_title": item.get('show_title', ''),
                "duration": item.get('duration', 0),
                "current": item.get('current', 0),
                "total": item.get('total', 0),
                "new_desc": item.get('new_desc', ''),
                "is_finish": item.get('is_finish', 0),
                "is_fav": item.get('is_fav', 0),
                "kid": item.get('kid', ''),
                "tag_name": item.get('tag_name', ''),
                "live_status": item.get('live_status', 0)
            }
            for item in data if item['history']['oid'] not in existing_oids
        ]

        # 分批插入数据
        for i in range(0, len(new_data), batch_size):
            batch_chunk = new_data[i:i + batch_size]
            inserted_count = batch_insert_data(connection, table_name, insert_sql, batch_chunk)
            total_inserted += inserted_count

        print(f"文件 {file_path} 插入或更新了 {total_inserted} 条数据。")
        return total_inserted

    except Exception as e:
        print(f"处理数据时发生错误: {e}")
        return 0

# 读取标记文件，返回上次导入的日期和文件名
def get_last_imported_file(file_path='last_import_log.json'):
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
def update_last_imported_file(last_imported_date, last_imported_file, file_path='last_import_log.json'):
    data = {
        'last_imported_date': last_imported_date,
        'last_imported_file': last_imported_file
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 遍历所有按日期分割的文件并导入数据
def import_all_history_files(data_folder='history_by_date', log_file='last_import_log.json'):
    total_inserted = 0
    file_insert_counts = {}

    print(f"开始遍历并导入文件夹 '{data_folder}' 中的数据...")

    if not os.path.exists(data_folder):
        print(f"本地文件夹 '{data_folder}' 不存在，无法加载数据。")
        return

    # 获取当前年份和上一年份
    current_year, previous_year = get_years()
    new_table = f"bilibili_history_{current_year}"
    reference_table = f"bilibili_history_{previous_year}"

    connection = connect_to_db()
    try:
        # 创建新年份的表，如果不存在
        create_new_year_table(connection, new_table, reference_table)

        # 定义动态的 INSERT SQL 语句
        insert_sql = f"""
            INSERT INTO {new_table} (
                id, title, long_title, cover, covers, uri, oid, epid, bvid, page, cid, part, 
                business, dt, videos, author_name, author_face, author_mid, view_at, progress, 
                badge, show_title, duration, current, total, new_desc, is_finish, is_fav, kid, 
                tag_name, live_status
            ) VALUES (
                %(id)s, %(title)s, %(long_title)s, %(cover)s, %(covers)s, %(uri)s, %(oid)s, 
                %(epid)s, %(bvid)s, %(page)s, %(cid)s, %(part)s, %(business)s, %(dt)s, 
                %(videos)s, %(author_name)s, %(author_face)s, %(author_mid)s, %(view_at)s, 
                %(progress)s, %(badge)s, %(show_title)s, %(duration)s, %(current)s, %(total)s, 
                %(new_desc)s, %(is_finish)s, %(is_fav)s, %(kid)s, %(tag_name)s, %(live_status)s
            )
            ON DUPLICATE KEY UPDATE 
                title = VALUES(title),
                long_title = VALUES(long_title),
                cover = VALUES(cover),
                covers = VALUES(covers),
                uri = VALUES(uri),
                epid = VALUES(epid),
                page = VALUES(page),
                cid = VALUES(cid),
                part = VALUES(part),
                business = VALUES(business),
                dt = VALUES(dt),
                videos = VALUES(videos),
                author_name = VALUES(author_name),
                author_face = VALUES(author_face),
                author_mid = VALUES(author_mid),
                view_at = VALUES(view_at),
                progress = VALUES(progress),
                badge = VALUES(badge),
                show_title = VALUES(show_title),
                duration = VALUES(duration),
                current = VALUES(current),
                total = VALUES(total),
                new_desc = VALUES(new_desc),
                is_finish = VALUES(is_finish),
                is_fav = VALUES(is_fav),
                tag_name = VALUES(tag_name),
                live_status = VALUES(live_status);
        """

        # 读取上次导入的文件日期和文件名
        last_imported_date, last_imported_file = get_last_imported_file(log_file)

        # 遍历按日期分割的文件夹
        for year in os.listdir(data_folder):
            year_path = os.path.join(data_folder, year)
            if os.path.isdir(year_path) and year.isdigit():
                for month in os.listdir(year_path):
                    month_path = os.path.join(year_path, month)
                    if os.path.isdir(month_path) and month.isdigit():
                        for day_file in os.listdir(month_path):
                            if day_file.endswith('.json'):
                                day_path = os.path.join(month_path, day_file)

                                # 获取当前文件的日期
                                # 假设文件名格式为 "DD.json" 或包含日期信息
                                day = ''.join(filter(str.isdigit, day_file))[:2]  # 提取前两位数字作为日
                                if len(day) != 2:
                                    print(f"无法解析文件名中的日期: {day_file}，跳过文件。")
                                    continue
                                file_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

                                # 如果当前文件日期和上次相同，继续检查文件名顺序
                                if last_imported_date:
                                    if file_date < last_imported_date:
                                        print(f"跳过已处理的文件: {day_path}")
                                        continue
                                    elif file_date == last_imported_date and day_file <= last_imported_file:
                                        print(f"跳过已处理的文件: {day_path}")
                                        continue

                                # 开始导入文件
                                print(f"正在导入文件: {day_path}")
                                inserted_count = import_data_from_json(connection, new_table, insert_sql, day_path)
                                total_inserted += inserted_count
                                file_insert_counts[day_path] = inserted_count

                                # 更新标记文件
                                update_last_imported_file(file_date, day_file, log_file)

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

# 主函数
if __name__ == '__main__':
    # 设置数据文件夹，可以选择导入清理前的文件夹 'history_by_date' 或清理后的文件夹 'cleaned_history_by_date'
    data_folder = 'cleaned_history_by_date'  # 或 'history_by_date'

    # 调用导入函数，导入所有文件
    import_all_history_files(data_folder)