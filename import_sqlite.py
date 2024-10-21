import sqlite3
import os
import json
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
        print(f"成功连接到SQLite数据库: {db_file}")
    except sqlite3.Error as e:
        print(f"连接SQLite数据库时出错: {e}")
    return conn

def create_table(conn, table_name):
    """创建数据表"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            title TEXT,
            long_title TEXT,
            cover TEXT,
            covers TEXT,
            uri TEXT,
            oid INTEGER,
            epid INTEGER,
            bvid TEXT,
            page INTEGER,
            cid INTEGER,
            part TEXT,
            business TEXT,
            dt INTEGER,
            videos INTEGER,
            author_name TEXT,
            author_face TEXT,
            author_mid INTEGER,
            view_at INTEGER,
            progress INTEGER,
            badge TEXT,
            show_title TEXT,
            duration INTEGER,
            current TEXT,
            total INTEGER,
            new_desc TEXT,
            is_finish INTEGER,
            is_fav INTEGER,
            kid INTEGER,
            tag_name TEXT,
            live_status INTEGER,
            main_category TEXT
        )
        """)
        conn.commit()
        print(f"成功创建表: {table_name}")
    except sqlite3.Error as e:
        print(f"创建表时发生错误: {e}")

def batch_insert_data(conn, table_name, data_chunk):
    try:
        cursor = conn.cursor()
        insert_sql = f"""
        INSERT INTO {table_name} (
            id, title, long_title, cover, covers, uri, oid, epid, bvid, page, cid, part, 
            business, dt, videos, author_name, author_face, author_mid, view_at, progress, 
            badge, show_title, duration, current, total, new_desc, is_finish, is_fav, kid, 
            tag_name, live_status, main_category
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(insert_sql, data_chunk)
        conn.commit()
        print(f"成功插入 {len(data_chunk)} 条数据到 {table_name}。")
        return len(data_chunk)
    except sqlite3.Error as e:
        conn.rollback()
        print(f"插入数据时发生错误: {e}")
        return 0

def import_data_from_json(conn, table_name, file_path, batch_size=1000):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    total_inserted = 0

    try:
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

        for i in range(0, len(new_data), batch_size):
            batch_chunk = new_data[i:i + batch_size]
            inserted_count = batch_insert_data(conn, table_name, batch_chunk)
            total_inserted += inserted_count

        print(f"文件 {file_path} 插入了 {total_inserted} 条数据。")
        return total_inserted

    except Exception as e:
        print(f"处理数据时发生错误: {e}")
        return 0

def import_all_history_files(data_folder='history_by_date', db_file='bilibili_history.db'):
    total_inserted = 0
    file_insert_counts = {}

    print(f"开始遍历并导入文件夹 '{data_folder}' 中的数据...")

    if not os.path.exists(data_folder):
        print(f"本地文件夹 '{data_folder}' 不存在，无法加载数据。")
        return

    current_year, previous_year = get_years()
    table_name = f"bilibili_history_{current_year}"

    conn = create_connection(db_file)
    if conn is None:
        return

    try:
        create_table(conn, table_name)

        for year in sorted(os.listdir(data_folder)):
            year_path = os.path.join(data_folder, year)
            if os.path.isdir(year_path) and year.isdigit():
                for month in sorted(os.listdir(year_path)):
                    month_path = os.path.join(year_path, month)
                    if os.path.isdir(month_path) and month.isdigit():
                        for day_file in sorted(os.listdir(month_path)):
                            if day_file.endswith('.json'):
                                day_path = os.path.join(month_path, day_file)
                                print(f"正在导入文件: {day_path}")
                                inserted_count = import_data_from_json(conn, table_name, day_path)
                                total_inserted += inserted_count
                                file_insert_counts[day_path] = inserted_count

        print("\n每个文件的插入记录：")
        for file, count in file_insert_counts.items():
            print(f"{file}: 插入了 {count} 条数据")

        print(f"\n所有文件均已导入数据库，总共插入了 {total_inserted} 条数据。")

    except Exception as e:
        print(f"导入过程中发生错误: {e}")

    finally:
        conn.close()

if __name__ == '__main__':
    data_folder = 'history_by_date'  # 或 'cleaned_history_by_date'
    db_file = 'bilibili_history.db'
    import_all_history_files(data_folder, db_file)
