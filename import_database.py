import pymysql
import json
import os
import time
import threading
from datetime import datetime

# 重复的 tag_name 集合，需要映射为 '待定'
duplicated_tags = {
    '资讯',
    '综合'
}

# 唯一的 tag_name 到 main_category 的映射
unique_tag_to_main = {
    # 动画
    '动画': '动画',
    'MAD·AMV': '动画',
    'MMD·3D': '动画',
    '短片·手书': '动画',
    '配音': '动画',
    '手办·模玩': '动画',
    '特摄': '动画',
    '动漫杂谈': '动画',

    # 番剧
    '番剧': '番剧',
    '官方延伸': '番剧',
    '完结动画': '番剧',
    '连载动画': '番剧',

    # 国创
    '国创': '国创',
    '国产动画': '国创',
    '国产原创相关': '国创',
    '布袋戏': '国创',
    '动态漫·广播剧': '国创',

    # 音乐
    '音乐': '音乐',
    '原创音乐': '音乐',
    '翻唱': '音乐',
    'VOCALOID·UTAU': '音乐',
    '演奏': '音乐',
    'MV': '音乐',
    '音乐现场': '音乐',
    '音乐综合': '音乐',
    '乐评盘点': '音乐',
    '音乐教学': '音乐',

    # 舞蹈
    '舞蹈': '舞蹈',
    '宅舞': '舞蹈',
    '舞蹈综合': '舞蹈',
    '舞蹈教程': '舞蹈',
    '街舞': '舞蹈',
    '明星舞蹈': '舞蹈',
    '国风舞蹈': '舞蹈',
    '手势·网红舞': '舞蹈',

    # 游戏
    '游戏': '游戏',
    '单机游戏': '游戏',
    '电子竞技': '游戏',
    '手机游戏': '游戏',
    '网络游戏': '游戏',
    '桌游棋牌': '游戏',
    'GMV': '游戏',
    '音游': '游戏',
    'Mugen': '游戏',

    # 知识
    '知识': '知识',
    '科学科普': '知识',
    '社科·法律·心理': '知识',
    '人文历史': '知识',
    '财经商业': '知识',
    '校园学习': '知识',
    '职业职场': '知识',
    '设计·创意': '知识',
    '野生技术协会': '知识',

    # 科技
    '科技': '科技',
    '数码': '科技',
    '软件应用': '科技',
    '计算机技术': '科技',
    '科工机械': '科技',
    '极客DIY': '科技',

    # 运动
    '运动': '运动',
    '篮球': '运动',
    '足球': '运动',
    '健身': '运动',
    '竞技体育': '运动',
    '运动文化': '运动',
    '运动综合': '运动',

    # 汽车
    '汽车': '汽车',
    '汽车知识科普': '汽车',
    '赛车': '汽车',
    '改装玩车': '汽车',
    '新能源车': '汽车',
    '房车': '汽车',
    '摩托车': '汽车',
    '购车攻略': '汽车',
    '汽车生活': '汽车',

    # 生活
    '生活': '生活',
    '搞笑': '生活',
    '出行': '生活',
    '三农': '生活',
    '家居房产': '生活',
    '手工': '生活',
    '绘画': '生活',
    '日常': '生活',
    '亲子': '生活',

    # 美食
    '美食': '美食',
    '美食制作': '美食',
    '美食侦探': '美食',
    '美食测评': '美食',
    '田园美食': '美食',
    '美食记录': '美食',

    # 动物圈
    '动物圈': '动物圈',
    '喵星人': '动物圈',
    '汪星人': '动物圈',
    '动物二创': '动物圈',
    '野生动物': '动物圈',
    '小宠异宠': '动物圈',
    '动物综合': '动物圈',

    # 鬼畜
    '鬼畜': '鬼畜',
    '鬼畜调教': '鬼畜',
    '音MAD': '鬼畜',
    '人力VOCALOID': '鬼畜',
    '鬼畜剧场': '鬼畜',
    '教程演示': '鬼畜',

    # 时尚
    '时尚': '时尚',
    '美妆护肤': '时尚',
    '仿妆cos': '时尚',
    '穿搭': '时尚',
    '时尚潮流': '时尚',

    # 资讯 (唯一部分)
    '热点': '资讯',
    '环球': '资讯',
    '社会': '资讯',
    'multiple': '资讯',  # '综合' 已经在 duplicated_tags 中

    # 娱乐
    '娱乐': '娱乐',
    '综艺': '娱乐',
    '娱乐杂谈': '娱乐',
    '粉丝创作': '娱乐',
    '明星综合': '娱乐',

    # 影视
    '影视': '影视',
    '影视杂谈': '影视',
    '影视剪辑': '影视',
    '小剧场': '影视',
    '预告·资讯': '影视',
    '短片': '影视',

    # 纪录片
    '纪录片': '纪录片',
    '人文·历史': '纪录片',
    '科学·探索·自然': '纪录片',
    '军事': '纪录片',
    '社会·美食·旅行': '纪录片',

    # 电影
    '电影': '电影',
    '华语电影': '电影',
    '欧美电影': '电影',
    '日本电影': '电影',
    '其他国家': '电影',

    # 电视剧
    '电视剧': '电视剧',
    '国产剧': '电视剧',
    '海外剧': '电视剧',
}


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
                    # 等待下一毫秒
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

def import_data_from_json(connection, table_name, insert_sql, file_path, batch_size=1000):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_inserted = 0

    try:
        # 构建要插入的数据列表，并生成唯一的id
        new_data = []
        for item in data:
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

            new_data.append({
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
            })

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
                tag_name, live_status, main_category
            ) VALUES (
                %(id)s, %(title)s, %(long_title)s, %(cover)s, %(covers)s, %(uri)s, %(oid)s, 
                %(epid)s, %(bvid)s, %(page)s, %(cid)s, %(part)s, %(business)s, %(dt)s, 
                %(videos)s, %(author_name)s, %(author_face)s, %(author_mid)s, %(view_at)s, 
                %(progress)s, %(badge)s, %(show_title)s, %(duration)s, %(current)s, %(total)s, 
                %(new_desc)s, %(is_finish)s, %(is_fav)s, %(kid)s, %(tag_name)s, %(live_status)s, 
                %(main_category)s
            )
        """

        # 读取上次导入的文件日期和文件名
        last_imported_date, last_imported_file = get_last_imported_file(log_file)

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
    data_folder = 'history_by_date'  # 或 'cleaned_history_by_date'

    # 调用导入函数，导入所有文件
    import_all_history_files(data_folder)