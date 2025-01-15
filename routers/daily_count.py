from typing import Optional
import sqlite3
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from scripts.utils import load_config, get_output_path

router = APIRouter()
config = load_config()

def get_db():
    """获取数据库连接"""
    db_path = get_output_path(config['db_file'])
    return sqlite3.connect(db_path)

def get_available_years():
    """获取数据库中所有可用的年份"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE 'bilibili_history_%'
            ORDER BY name DESC
        """)
        
        years = []
        for (table_name,) in cursor.fetchall():
            try:
                year = int(table_name.split('_')[-1])
                years.append(year)
            except (ValueError, IndexError):
                continue
                
        return sorted(years, reverse=True)
    except sqlite3.Error as e:
        print(f"获取年份列表时发生错误: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_daily_video_count(cursor, table_name: str, date: str) -> dict:
    """获取指定日期的视频数量统计
    
    Args:
        cursor: 数据库游标
        table_name: 表名
        date: 日期字符串，格式为MMDD
    
    Returns:
        dict: 包含视频数量统计的字典
    """
    try:
        # 解析日期
        month = int(date[:2])
        day = int(date[2:])
        
        # 从表名中获取年份
        year = int(table_name.split('_')[-1])
        
        # 构建日期范围
        start_timestamp = int(datetime(year, month, day, 0, 0, 0).timestamp())
        end_timestamp = int(datetime(year, month, day, 23, 59, 59).timestamp())
        
        # 查询总视频数
        cursor.execute(f"""
            SELECT COUNT(*) as total_count,
                   COUNT(DISTINCT author_mid) as unique_authors,
                   AVG(duration) as avg_duration,
                   AVG(CAST(progress AS FLOAT) / CAST(duration AS FLOAT)) as avg_completion_rate,
                   COUNT(CASE WHEN progress >= duration * 0.9 THEN 1 END) as completed_videos
            FROM {table_name}
            WHERE view_at >= ? AND view_at <= ?
        """, (start_timestamp, end_timestamp))
        
        result = cursor.fetchone()
        total_count, unique_authors, avg_duration, avg_completion_rate, completed_videos = result
        
        # 查询分区分布
        cursor.execute(f"""
            SELECT tag_name, COUNT(*) as count
            FROM {table_name}
            WHERE view_at >= ? AND view_at <= ?
            GROUP BY tag_name
            ORDER BY count DESC
            LIMIT 5
        """, (start_timestamp, end_timestamp))
        
        tag_distribution = {row[0]: row[1] for row in cursor.fetchall()}
        
        # 查询UP主分布
        cursor.execute(f"""
            SELECT author_name, COUNT(*) as count
            FROM {table_name}
            WHERE view_at >= ? AND view_at <= ?
            GROUP BY author_mid
            ORDER BY count DESC
            LIMIT 5
        """, (start_timestamp, end_timestamp))
        
        author_distribution = {row[0]: row[1] for row in cursor.fetchall()}
        
        return {
            "date": f"{year}-{month:02d}-{day:02d}",
            "total_videos": total_count,
            "unique_authors": unique_authors,
            "avg_duration": round(avg_duration if avg_duration else 0, 2),
            "avg_completion_rate": round(avg_completion_rate * 100 if avg_completion_rate else 0, 2),
            "completed_videos": completed_videos,
            "tag_distribution": tag_distribution,
            "author_distribution": author_distribution,
            "insights": [
                f"这一天你一共观看了 {total_count} 个视频",
                f"来自 {unique_authors} 个不同的UP主",
                f"平均时长 {round(avg_duration/60 if avg_duration else 0, 1)} 分钟",
                f"平均完成率 {round(avg_completion_rate * 100 if avg_completion_rate else 0, 1)}%",
                f"完整看完 {completed_videos} 个视频"
            ]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"日期格式错误: {str(e)}")

@router.get("/daily-count")
async def get_daily_count(
    date: str = Query(..., description="日期，格式为MMDD，例如0113表示1月13日"),
    year: Optional[int] = Query(None, description="年份，不传则使用当前年份")
):
    """获取指定日期的视频观看数量统计
    
    Args:
        date: 日期，格式为MMDD，例如0113表示1月13日
        year: 年份，不传则使用当前年份
    
    Returns:
        dict: 包含视频观看统计的数据
    """
    try:
        # 验证日期格式
        if not date.isdigit() or len(date) != 4:
            raise HTTPException(status_code=400, detail="日期格式错误，应为MMDD格式，例如0113")
            
        month = int(date[:2])
        day = int(date[2:])
        if not (1 <= month <= 12 and 1 <= day <= 31):
            raise HTTPException(status_code=400, detail="无效的日期")
        
        # 获取可用年份列表
        available_years = get_available_years()
        if not available_years:
            return {
                "status": "error",
                "message": "未找到任何历史记录数据"
            }
        
        # 如果未指定年份，使用最新的年份
        target_year = year if year is not None else available_years[0]
        
        # 检查指定的年份是否可用
        if year is not None and year not in available_years:
            return {
                "status": "error",
                "message": f"未找到 {year} 年的历史记录数据。可用的年份有：{', '.join(map(str, available_years))}"
            }
        
        table_name = f"bilibili_history_{target_year}"
        
        conn = get_db()
        cursor = conn.cursor()
        
        # 获取每日统计数据
        daily_stats = get_daily_video_count(cursor, table_name, date)
        
        return {
            "status": "success",
            "data": {
                **daily_stats,
                "year": target_year,
                "available_years": available_years
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'conn' in locals() and conn:
            conn.close() 