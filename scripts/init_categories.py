import sqlite3
from scripts.utils import get_output_path, load_config

def init_categories():
    """初始化视频分类表"""
    config = load_config()
    db_path = get_output_path(config['db_file'])
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 创建视频分类表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            main_category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            alias TEXT NOT NULL,
            tid INTEGER NOT NULL,
            image TEXT
        )
        ''')
        
        # 插入数据
        categories_data = [
            ('动画', '动画', 'douga', 1, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg'),
            ('动画', 'MAD·AMV', 'mad', 24, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg' ),
            ('动画', 'MMD·3D', 'mmd', 25, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg'),
            ('动画', '短片·手书', 'handdrawn', 47, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg'),
            ('动画', '配音', 'voice', 257, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg'),
            ('动画', '手办·模玩', 'garage_kit', 210, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg'),
            ('动画', '特摄', 'tokusatsu', 86, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg'),
            ('动画', '动漫杂谈', 'acgntalks', 253, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg'),
            ('动画', '综合', 'other', 27, 'https://socialsisteryi.github.io/bilibili-API-collect/assets/douga-551968c9.svg'),

            ('番剧', '番剧', 'anime', 13,'https://socialsisteryi.github.io/bilibili-API-collect/assets/anime-b33a4df8.svg'),
            ('番剧', '资讯', 'information', 51,'https://socialsisteryi.github.io/bilibili-API-collect/assets/anime-b33a4df8.svg'),
            ('番剧', '官方延伸', 'offical', 152,'https://socialsisteryi.github.io/bilibili-API-collect/assets/anime-b33a4df8.svg'),
            ('番剧', '完结动画', 'finish', 32,'https://socialsisteryi.github.io/bilibili-API-collect/assets/anime-b33a4df8.svg'),
            ('番剧', '连载动画', 'serial', 33,'https://socialsisteryi.github.io/bilibili-API-collect/assets/anime-b33a4df8.svg'),

            ('国创', '国创', 'guochuang', 167,'https://socialsisteryi.github.io/bilibili-API-collect/assets/guochuang-2887858d.svg'),
            ('国创', '国产动画', 'chinese', 153,'https://socialsisteryi.github.io/bilibili-API-collect/assets/guochuang-2887858d.svg'),
            ('国创', '国产原创相关', 'original', 168,'https://socialsisteryi.github.io/bilibili-API-collect/assets/guochuang-2887858d.svg'),
            ('国创', '布袋戏', 'puppetry', 169,'https://socialsisteryi.github.io/bilibili-API-collect/assets/guochuang-2887858d.svg'),
            ('国创', '资讯', 'information', 170,'https://socialsisteryi.github.io/bilibili-API-collect/assets/guochuang-2887858d.svg'),
            ('国创', '动态漫·广播剧', 'motioncomic', 195,'https://socialsisteryi.github.io/bilibili-API-collect/assets/guochuang-2887858d.svg'),

            ('音乐', '音乐', 'music', 3,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', '原创音乐', 'original', 28,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', '翻唱', 'cover', 31,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', 'VOCALOID·UTAU', 'vocaloid', 30,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', '演奏', 'perform', 59,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', 'MV', 'mv', 193,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', '音乐现场', 'live', 29,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', '音乐综合', 'other', 130,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', '乐评盘点', 'commentary', 243,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),
            ('音乐', '音乐教学', 'tutorial', 244,'https://socialsisteryi.github.io/bilibili-API-collect/assets/music-1d6aa097.svg'),

            ('舞蹈', '舞蹈', 'dance', 129,'https://socialsisteryi.github.io/bilibili-API-collect/assets/dance-26e4156b.svg'),
            ('舞蹈', '宅舞', 'otaku', 20,'https://socialsisteryi.github.io/bilibili-API-collect/assets/dance-26e4156b.svg'),
            ('舞蹈', '舞蹈综合', 'three_d', 154,'https://socialsisteryi.github.io/bilibili-API-collect/assets/dance-26e4156b.svg'),
            ('舞蹈', '舞蹈教程', 'demo', 156,'https://socialsisteryi.github.io/bilibili-API-collect/assets/dance-26e4156b.svg'),
            ('舞蹈', '街舞', 'hiphop', 198,'https://socialsisteryi.github.io/bilibili-API-collect/assets/dance-26e4156b.svg'),
            ('舞蹈', '明星舞蹈', 'star', 199,'https://socialsisteryi.github.io/bilibili-API-collect/assets/dance-26e4156b.svg'),
            ('舞蹈', '国风舞蹈', 'china', 200,'https://socialsisteryi.github.io/bilibili-API-collect/assets/dance-26e4156b.svg'),
            ('舞蹈', '手势·网红舞', 'gestures', 255,'https://socialsisteryi.github.io/bilibili-API-collect/assets/dance-26e4156b.svg'),

            ('游戏', '游戏', 'game', 4,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),
            ('游戏', '单机游戏', 'stand_alone', 17,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),
            ('游戏', '电子竞技', 'esports', 171,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),
            ('游戏', '手机游戏', 'mobile', 172,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),
            ('游戏', '网络游戏', 'online', 65,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),
            ('游戏', '桌游棋牌', 'board', 173,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),
            ('游戏', 'GMV', 'gmv', 121,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),
            ('游戏', '音游', 'music', 136,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),
            ('游戏', 'Mugen', 'mugen', 19,'https://socialsisteryi.github.io/bilibili-API-collect/assets/game-158a0730.svg'),

            ('知识', '知识', 'knowledge', 36,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),
            ('知识', '科学科普', 'science', 201,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),
            ('知识', '社科·法律·心理', 'social_science', 124,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),
            ('知识', '人文历史', 'humanity_history', 228,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),
            ('知识', '财经商业', 'business', 207,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),
            ('知识', '校园学习', 'campus', 208,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),
            ('知识', '职业职场', 'career', 209,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),
            ('知识', '设计·创意', 'design', 229,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),
            ('知识', '野生技术协会', 'skill', 122,'https://socialsisteryi.github.io/bilibili-API-collect/assets/knowledge-65fd8dce.svg'),


            ('科技', '科技', 'tech', 188,'https://socialsisteryi.github.io/bilibili-API-collect/assets/tech-8f2eb72e.svg'),
            ('科技', '数码', 'digital', 95,'https://socialsisteryi.github.io/bilibili-API-collect/assets/tech-8f2eb72e.svg'),
            ('科技', '软件应用', 'application', 230,'https://socialsisteryi.github.io/bilibili-API-collect/assets/tech-8f2eb72e.svg'),
            ('科技', '计算机技术', 'computer_tech', 231,'https://socialsisteryi.github.io/bilibili-API-collect/assets/tech-8f2eb72e.svg'),
            ('科技', '科工机械', 'industry', 232,'https://socialsisteryi.github.io/bilibili-API-collect/assets/tech-8f2eb72e.svg'),
            ('科技', '极客DIY', 'diy', 233,'https://socialsisteryi.github.io/bilibili-API-collect/assets/tech-8f2eb72e.svg'),


            ('运动', '运动', 'sports', 234,'https://socialsisteryi.github.io/bilibili-API-collect/assets/sports-bfc825f3.svg'),
            ('运动', '篮球', 'basketball', 235,'https://socialsisteryi.github.io/bilibili-API-collect/assets/sports-bfc825f3.svg'),
            ('运动', '足球', 'football', 249,'https://socialsisteryi.github.io/bilibili-API-collect/assets/sports-bfc825f3.svg'),
            ('运动', '健身', 'aerobics', 164,'https://socialsisteryi.github.io/bilibili-API-collect/assets/sports-bfc825f3.svg'),
            ('运动', '竞技体育', 'athletic', 236,'https://socialsisteryi.github.io/bilibili-API-collect/assets/sports-bfc825f3.svg'),
            ('运动', '运动文化', 'culture', 237,'https://socialsisteryi.github.io/bilibili-API-collect/assets/sports-bfc825f3.svg'),
            ('运动', '运动综合', 'comprehensive', 238,'https://socialsisteryi.github.io/bilibili-API-collect/assets/sports-bfc825f3.svg'),


            ('汽车', '汽车', 'car', 223,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),
            ('汽车', '汽车知识科普', 'knowledge', 258,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),
            ('汽车', '赛车', 'racing', 245,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),
            ('汽车', '改装玩车', 'modifiedvehicle', 246,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),
            ('汽车', '新能源汽车', 'newenergyvehicle', 247,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),
            ('汽车', '房车', 'touringcar', 248,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),
            ('汽车', '摩托车', 'motorcycle', 240,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),
            ('汽车', '购车攻略', 'strategy', 227,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),
            ('汽车', '汽车生活', 'life', 176,'https://socialsisteryi.github.io/bilibili-API-collect/assets/car-c766485c.svg'),


            ('生活', '生活', 'life', 160,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),
            ('生活', '搞笑', 'funny', 138,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),
            ('生活', '出行', 'travel', 250,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),
            ('生活', '三农', 'rurallife', 251,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),
            ('生活', '家居房产', 'home', 239,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),
            ('生活', '手工', 'handmake', 161,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),
            ('生活', '绘画', 'painting', 162,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),
            ('生活', '日常', 'daily', 21,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),
            ('生活', '亲子', 'parenting', 254,'https://socialsisteryi.github.io/bilibili-API-collect/assets/life-1f4a6ef5.svg'),


            ('美食', '美食', 'food', 211,'https://socialsisteryi.github.io/bilibili-API-collect/assets/food-5883d8d8.svg'),
            ('美食', '美食制作', 'make', 76,'https://socialsisteryi.github.io/bilibili-API-collect/assets/food-5883d8d8.svg'),
            ('美食', '美食侦探', 'detective', 212,'https://socialsisteryi.github.io/bilibili-API-collect/assets/food-5883d8d8.svg'),
            ('美食', '美食测评', 'measurement', 213,'https://socialsisteryi.github.io/bilibili-API-collect/assets/food-5883d8d8.svg'),
            ('美食', '田园美食', 'rural', 214,'https://socialsisteryi.github.io/bilibili-API-collect/assets/food-5883d8d8.svg'),
            ('美食', '美食记录', 'record', 215,'https://socialsisteryi.github.io/bilibili-API-collect/assets/food-5883d8d8.svg'),


            ('动物圈', '动物圈', 'animal', 217,'https://socialsisteryi.github.io/bilibili-API-collect/assets/animal-95ff87f2.svg'),
            ('动物圈', '喵星人', 'cat', 218,'https://socialsisteryi.github.io/bilibili-API-collect/assets/animal-95ff87f2.svg'),
            ('动物圈', '汪星人', 'dog', 219,'https://socialsisteryi.github.io/bilibili-API-collect/assets/animal-95ff87f2.svg'),
            ('动物圈', '动物二创', 'second_edition', 220,'https://socialsisteryi.github.io/bilibili-API-collect/assets/animal-95ff87f2.svg'),
            ('动物圈', '野生动物', 'wild_animal', 221,'https://socialsisteryi.github.io/bilibili-API-collect/assets/animal-95ff87f2.svg'),
            ('动物圈', '小宠异宠', 'reptiles', 222,'https://socialsisteryi.github.io/bilibili-API-collect/assets/animal-95ff87f2.svg'),
            ('动物圈', '动物综合', 'animal_composite', 75,'https://socialsisteryi.github.io/bilibili-API-collect/assets/animal-95ff87f2.svg'),


            ('鬼畜', '鬼畜', 'kichiku', 119,'https://socialsisteryi.github.io/bilibili-API-collect/assets/kichiku-8f960ae2.svg'),
            ('鬼畜', '鬼畜调教', 'guide', 22,'https://socialsisteryi.github.io/bilibili-API-collect/assets/kichiku-8f960ae2.svg'),
            ('鬼畜', '音MAD', 'mad', 26,'https://socialsisteryi.github.io/bilibili-API-collect/assets/kichiku-8f960ae2.svg'),
            ('鬼畜', '人力VOCALOID', 'manual_vocaloid', 126,'https://socialsisteryi.github.io/bilibili-API-collect/assets/kichiku-8f960ae2.svg'),
            ('鬼畜', '鬼畜剧场', 'theatre', 216,'https://socialsisteryi.github.io/bilibili-API-collect/assets/kichiku-8f960ae2.svg'),
            ('鬼畜', '教程演示', 'course', 127,'https://socialsisteryi.github.io/bilibili-API-collect/assets/kichiku-8f960ae2.svg'),


            ('时尚', '时尚', 'fashion', 155,'https://socialsisteryi.github.io/bilibili-API-collect/assets/fashion-773241bb.svg'),
            ('时尚', '美妆护肤', 'makeup', 157,'https://socialsisteryi.github.io/bilibili-API-collect/assets/fashion-773241bb.svg'),
            ('时尚', '仿妆cos', 'cos', 252,'https://socialsisteryi.github.io/bilibili-API-collect/assets/fashion-773241bb.svg'),
            ('时尚', '穿搭', 'clothing', 158,'https://socialsisteryi.github.io/bilibili-API-collect/assets/fashion-773241bb.svg'),
            ('时尚', '时尚潮流', 'catwalk', 159,'https://socialsisteryi.github.io/bilibili-API-collect/assets/fashion-773241bb.svg'),


            ('资讯', '资讯', 'information', 202,'https://socialsisteryi.github.io/bilibili-API-collect/assets/information-d98c5ed0.svg'),
            ('资讯', '热点', 'hotspot', 203,'https://socialsisteryi.github.io/bilibili-API-collect/assets/information-d98c5ed0.svg'),
            ('资讯', '环球', 'global', 204,'https://socialsisteryi.github.io/bilibili-API-collect/assets/information-d98c5ed0.svg'),
            ('资讯', '社会', 'social', 205,'https://socialsisteryi.github.io/bilibili-API-collect/assets/information-d98c5ed0.svg'),
            ('资讯', '综合', 'multiple', 206,'https://socialsisteryi.github.io/bilibili-API-collect/assets/information-d98c5ed0.svg'),


            ('娱乐', '娱乐', 'ent', 5,'https://socialsisteryi.github.io/bilibili-API-collect/assets/ent-ed6247e0.svg'),
            ('娱乐', '综艺', 'variety', 71,'https://socialsisteryi.github.io/bilibili-API-collect/assets/ent-ed6247e0.svg'),
            ('娱乐', '娱乐杂谈', 'talker', 241,'https://socialsisteryi.github.io/bilibili-API-collect/assets/ent-ed6247e0.svg'),
            ('娱乐', '粉丝创作', 'fans', 242,'https://socialsisteryi.github.io/bilibili-API-collect/assets/ent-ed6247e0.svg'),
            ('娱乐', '明星综合', 'celebrity', 137,'https://socialsisteryi.github.io/bilibili-API-collect/assets/ent-ed6247e0.svg'),


            ('影视', '影视', 'cinephile', 181,'https://socialsisteryi.github.io/bilibili-API-collect/assets/cinephile-c8d74b94.svg'),
            ('影视', '影视杂谈', 'cinecism', 182,'https://socialsisteryi.github.io/bilibili-API-collect/assets/cinephile-c8d74b94.svg'),
            ('影视', '影视剪辑', 'montage', 183,'https://socialsisteryi.github.io/bilibili-API-collect/assets/cinephile-c8d74b94.svg'),
            ('影视', '小剧场', 'shortfilm', 85,'https://socialsisteryi.github.io/bilibili-API-collect/assets/cinephile-c8d74b94.svg'),
            ('影视', '预告·资讯', 'trailer_info', 184,'https://socialsisteryi.github.io/bilibili-API-collect/assets/cinephile-c8d74b94.svg'),
            ('影视', '短片', 'shortfilm', 256,'https://socialsisteryi.github.io/bilibili-API-collect/assets/cinephile-c8d74b94.svg'),


            ('纪录片', '纪录片', 'documentary', 177,'https://socialsisteryi.github.io/bilibili-API-collect/assets/documentary-2c550e67.svg'),
            ('纪录片', '人文·历史', 'history', 37,'https://socialsisteryi.github.io/bilibili-API-collect/assets/documentary-2c550e67.svg'),
            ('纪录片', '科学·探索·自然', 'science', 178,'https://socialsisteryi.github.io/bilibili-API-collect/assets/documentary-2c550e67.svg'),
            ('纪录片', '军事', 'military', 179,'https://socialsisteryi.github.io/bilibili-API-collect/assets/documentary-2c550e67.svg'),
            ('纪录片', '社会·美食·旅行', 'travel', 180,'https://socialsisteryi.github.io/bilibili-API-collect/assets/documentary-2c550e67.svg'),


            ('电影', '电影', 'movie', 23,'https://socialsisteryi.github.io/bilibili-API-collect/assets/movie-693cc994.svg'),
            ('电影', '华语电影', 'chinese', 147,'https://socialsisteryi.github.io/bilibili-API-collect/assets/movie-693cc994.svg'),
            ('电影', '欧美电影', 'west', 145,'https://socialsisteryi.github.io/bilibili-API-collect/assets/movie-693cc994.svg'),
            ('电影', '日本电影', 'japan', 146,'https://socialsisteryi.github.io/bilibili-API-collect/assets/movie-693cc994.svg'),
            ('电影', '其他国家', 'movie', 83,'https://socialsisteryi.github.io/bilibili-API-collect/assets/movie-693cc994.svg'),


            ('电视剧', '电视剧', 'tv', 11,'https://socialsisteryi.github.io/bilibili-API-collect/assets/teleplay-1f3272a8.svg'),
            ('电视剧', '国产剧', 'mainland', 185,'https://socialsisteryi.github.io/bilibili-API-collect/assets/teleplay-1f3272a8.svg'),
            ('电视剧', '海外剧', 'overseas', 187,'https://socialsisteryi.github.io/bilibili-API-collect/assets/teleplay-1f3272a8.svg'),

        ]
        
        # 先清空表
        cursor.execute('DELETE FROM video_categories')
        
        # 插入所有数据
        cursor.executemany('''
        INSERT INTO video_categories (main_category, sub_category, alias, tid, image)
        VALUES (?, ?, ?, ?, ?)
        ''', categories_data)
        
        conn.commit()
        print("视频分类表初始化成功！")
        
    except sqlite3.Error as e:
        print(f"数据库错误: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    init_categories() 