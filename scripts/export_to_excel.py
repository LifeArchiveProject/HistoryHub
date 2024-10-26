import sqlite3
import pandas as pd
import json
from datetime import datetime
import traceback
from openpyxl.utils import get_column_letter
import os
import logging
from scripts.utils import load_config, get_base_path

config = load_config()

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IS_SCRIPT_RUN = True

def get_base_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if IS_SCRIPT_RUN else os.getcwd()

def create_connection(db_file):
    """创建一个到SQLite数据库的连接"""
    if not os.path.exists(db_file):
        logger.error(f"数据库文件 {db_file} 不存在。")
        return None
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.info(f"成功连接到SQLite数据库: {db_file}")
    except sqlite3.Error as e:
        logger.error(f"连接SQLite数据库时出错: {e}")
    return conn

def get_current_year():
    return datetime.now().year

def safe_json_loads(value):
    try:
        if value is None or value == 'null':
            return []
        return json.loads(value)
    except json.JSONDecodeError:
        logger.warning(f"JSON解析错误，值为: {value}")
        return []
    except Exception as e:
        logger.error(f"处理JSON时发生未知错误: {e}, 值为: {value}")
        return []

def export_to_excel(db_file, excel_file):
    conn = create_connection(db_file)
    if conn is None:
        return {"status": "error", "message": f"无法连接到数据库 {db_file}。数据库文件可能不存在。"}

    try:
        current_year = get_current_year()
        table_name = f"bilibili_history_{current_year}"

        # 检查表是否存在
        cursor = conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone() is None:
            return {"status": "error", "message": f"数据库中不存在表 {table_name}。"}

        # 从数据库读取数据
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)

        if df.empty:
            return {"status": "error", "message": f"表 {table_name} 中没有数据。"}

        # 将 JSON 字符串转换为列表，处理 null 值
        if 'covers' in df.columns:
            df['covers'] = df['covers'].apply(safe_json_loads)

        # 清理列名，移除非法字符并确保列名有效
        df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True).str.strip()
        df.columns = [f"Column_{i}" if not col or not col[0].isalpha() else col for i, col in enumerate(df.columns)]

        # 导出到Excel
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='BilibiliHistory')

            # 调整列宽
            worksheet = writer.sheets['BilibiliHistory']
            for idx, col in enumerate(df.columns):
                series = df[col]
                max_len = max((
                    series.astype(str).map(len).max(),  # 最长的值
                    len(str(col))  # 列名长度
                )) + 1  # 为了美观增加一个字符的宽度
                worksheet.column_dimensions[get_column_letter(idx + 1)].width = max_len

        logger.info(f"数据已成功导出到 {excel_file}")
        return {"status": "success", "message": f"数据已成功导出到 {excel_file}"}

    except Exception as e:
        logger.error(f"导出数据时发生错误: {e}")
        traceback.print_exc()
        return {"status": "error", "message": f"导出数据时发生错误: {e}"}

    finally:
        if conn:
            conn.close()

def export_bilibili_history():
    base_path = get_base_path()
    full_db_file = os.path.join(base_path, config['db_file'])
    current_year = get_current_year()
    excel_file = os.path.join(base_path, f'bilibili_history_{current_year}.xlsx')
    return export_to_excel(full_db_file, excel_file)

# 允许脚本独立运行
if __name__ == '__main__':
    result = export_bilibili_history()
    if result["status"] == "success":
        print(result["message"])
    else:
        print(f"错误: {result['message']}")
