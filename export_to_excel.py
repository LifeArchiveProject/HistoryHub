import sqlite3
import pandas as pd
import json
from datetime import datetime
import traceback
from openpyxl.utils import get_column_letter

def create_connection(db_file):
    """创建一个到SQLite数据库的连接"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"成功连接到SQLite数据库: {db_file}")
    except sqlite3.Error as e:
        print(f"连接SQLite数据库时出错: {e}")
    return conn

def get_current_year():
    return datetime.now().year

def safe_json_loads(value):
    try:
        if value is None or value == 'null':
            return []
        return json.loads(value)
    except json.JSONDecodeError:
        print(f"JSON解析错误，值为: {value}")
        return []
    except Exception as e:
        print(f"处理JSON时发生未知错误: {e}, 值为: {value}")
        return []

def export_to_excel(db_file, excel_file):
    conn = create_connection(db_file)
    if conn is None:
        return

    try:
        current_year = get_current_year()
        table_name = f"bilibili_history_{current_year}"
        
        # 从数据库读取数据
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        
        # 将 JSON 字符串转换为列表，处理 null 值
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
        
        print(f"数据已成功导出到 {excel_file}")
    
    except Exception as e:
        print(f"导出数据时发生错误: {e}")
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == '__main__':
    db_file = 'bilibili_history.db'
    excel_file = f'bilibili_history_{get_current_year()}.xlsx'
    export_to_excel(db_file, excel_file)
