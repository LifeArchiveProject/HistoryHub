import json
import logging
import os
import sqlite3
import traceback
from datetime import datetime

import pandas as pd
from openpyxl.utils import get_column_letter

from scripts.utils import load_config, get_output_path

config = load_config()

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def export_bilibili_history(year=None, month=None, start_date=None, end_date=None):
    """导出B站历史记录到Excel文件

    Args:
        year: 要导出的年份，如果不指定则使用当前年份
        month: 要导出的月份（1-12），如果指定则只导出该月数据
        start_date: 开始日期，格式为'YYYY-MM-DD'，如果指定则从该日期开始导出
        end_date: 结束日期，格式为'YYYY-MM-DD'，如果指定则导出到该日期为止
    """
    full_db_file = get_output_path(config['db_file'])
    target_year = year if year is not None else get_current_year()

    # 构建文件名
    filename_parts = ['bilibili_history']
    if year is not None:
        filename_parts.append(str(target_year))
    if month is not None:
        filename_parts.append(f"{month:02d}月")
    if start_date and end_date:
        filename_parts.append(f"{start_date}至{end_date}")
    elif start_date:
        filename_parts.append(f"从{start_date}开始")
    elif end_date:
        filename_parts.append(f"至{end_date}")

    excel_file = get_output_path(f'{"_".join(filename_parts)}.xlsx')

    conn = create_connection(full_db_file)
    if conn is None:
        return {"status": "error", "message": f"无法连接到数据库 {full_db_file}。数据库文件可能不存在。"}

    try:
        # 如果指定了日期范围，需要确定要查询的年份表
        years_to_query = [target_year]

        # 如果指定了日期范围，可能需要查询多个年份的表
        if start_date or end_date:
            # 获取开始和结束年份
            start_year = int(start_date.split('-')[0]) if start_date else target_year
            end_year = int(end_date.split('-')[0]) if end_date else target_year

            # 确保年份范围有效
            start_year = max(2000, min(start_year, datetime.now().year))
            end_year = max(2000, min(end_year, datetime.now().year))

            # 生成要查询的年份列表
            years_to_query = list(range(start_year, end_year + 1))
            logger.info(f"将查询以下年份的表: {years_to_query}")

        # 获取所有存在的表
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'bilibili_history_%'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        logger.info(f"存在的表: {existing_tables}")

        # 过滤出实际存在的表
        tables_to_query = [f"bilibili_history_{year}" for year in years_to_query if f"bilibili_history_{year}" in existing_tables]

        if not tables_to_query:
            return {"status": "error", "message": f"没有找到符合条件的数据表。"}

        logger.info(f"将查询以下表: {tables_to_query}")

        # 准备查询条件
        conditions = []
        params = []

        # 如果指定了月份，添加月份筛选条件
        if month is not None:
            conditions.append("strftime('%m', datetime(view_at, 'unixepoch', 'localtime')) = ?")
            params.append(f"{month:02d}")

        # 如果指定了开始日期，添加开始日期筛选条件
        if start_date:
            conditions.append("date(view_at, 'unixepoch', 'localtime') >= ?")
            params.append(start_date)

        # 如果指定了结束日期，添加结束日期筛选条件
        if end_date:
            conditions.append("date(view_at, 'unixepoch', 'localtime') <= ?")
            params.append(end_date)

        # 准备查询条件字符串
        condition_str = ""
        if conditions:
            condition_str = " WHERE " + " AND ".join(conditions)

        # 从所有表中查询数据
        all_data = []
        for table in tables_to_query:
            query = f"SELECT * FROM {table}{condition_str}"

            # 打印调试信息
            logger.info(f"执行SQL查询: {query}")
            logger.info(f"参数: {params}")

            # 使用params参数执行查询
            table_df = pd.read_sql_query(query, conn, params=params)
            if not table_df.empty:
                all_data.append(table_df)
                logger.info(f"从表 {table} 中获取了 {len(table_df)} 条数据")

        # 合并所有表的数据
        if all_data:
            df = pd.concat(all_data, ignore_index=True)
            logger.info(f"合并后共有 {len(df)} 条数据")
        else:
            df = pd.DataFrame()

        if df.empty:
            return {"status": "error", "message": f"没有找到符合条件的数据。"}

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

# 如果该脚本直接运行，则调用导出函数
if __name__ == '__main__':
    result = export_bilibili_history()
    if result["status"] == "success":
        print(result["message"])
    else:
        print(f"错误: {result['message']}")
