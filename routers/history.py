import json
import os
import sqlite3
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from scripts.utils import get_output_path, load_config


router = APIRouter()
config = load_config()


def get_db():
    """获取数据库连接，并确保数据库版本兼容性"""
    db_path = get_output_path(config['db_file'])

    # 检查数据库文件是否存在
    db_exists = os.path.exists(db_path)

    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 设置数据库兼容性参数
        pragmas = [
            ('legacy_file_format', 1),
            ('journal_mode', 'DELETE'),
            ('synchronous', 'NORMAL'),
            ('user_version', 317)  # 使用固定的用户版本号
        ]

        for pragma, value in pragmas:
            cursor.execute(f'PRAGMA {pragma}={value}')
        conn.commit()

        if not db_exists:
            print("数据库文件不存在，将创建新数据库")
            print("已配置数据库兼容性设置")

        return conn

    except sqlite3.Error as e:
        print(f"数据库连接错误: {str(e)}")
        if 'conn' in locals() and conn:
            conn.close()
        raise HTTPException(
            status_code=500,
            detail=f"数据库连接失败: {str(e)}"
        )


def get_available_years():
    """获取数据库中已有历史记录表的年份。"""
    conn = get_db()
    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'bilibili_history_%'"
        ).fetchall()
        return sorted(
            (int(name.rsplit('_', 1)[-1]) for (name,) in tables if name.rsplit('_', 1)[-1].isdigit()),
            reverse=True,
        )
    finally:
        conn.close()

@router.get("/available-years", summary="获取可用的年份列表")
async def get_years():
    return {"status": "success", "data": get_available_years()}

def _build_original_url(record: dict) -> str:
    """根据历史记录字段构建可打开的B站原始链接"""
    uri = (record.get('uri') or '').strip()
    if uri:
        return uri

    business = (record.get('business') or '').strip().lower()
    bvid = (record.get('bvid') or '').strip()
    page = record.get('page') or 1
    oid = record.get('oid') or 0
    epid = record.get('epid') or 0

    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1

    if business == 'archive' and bvid:
        url = f"https://www.bilibili.com/video/{bvid}"
        if page > 1:
            url = f"{url}?p={page}"
        return url

    if business == 'pgc':
        if epid:
            return f"https://www.bilibili.com/bangumi/play/ep{epid}"
        if oid:
            return f"https://www.bilibili.com/bangumi/play/ss{oid}"

    if business == 'live' and oid:
        return f"https://live.bilibili.com/{oid}"

    if business in {'article', 'article-list'} and oid:
        return f"https://www.bilibili.com/read/cv{oid}"

    if bvid:
        return f"https://www.bilibili.com/video/{bvid}"

    return ''


def _process_record(record: dict) -> dict:
    """解析封面列表并提供历史记录的原始链接。"""
    covers = record.get("covers")
    if isinstance(covers, str):
        try:
            covers = json.loads(covers)
        except json.JSONDecodeError:
            covers = []
    record["covers"] = covers if isinstance(covers, list) else []
    record["original_url"] = _build_original_url(record)
    return record

@router.get("/all", summary="分页查询历史记录")
async def get_history_page(
    page: int = Query(1, ge=1, description="当前页码"),
    size: int = Query(10, ge=1, description="每页记录数"),
    sort_order: int = Query(0, description="排序顺序，0为降序，1为升序"),
    tag_name: Optional[str] = Query(None, description="视频子分区名称"),
    main_category: Optional[str] = Query(None, description="主分区名称"),
    date_range: Optional[str] = Query(None, description="日期范围，格式为yyyyMMdd-yyyyMMdd"),
    business: Optional[str] = Query(None, description="业务类型，如archive(普通视频)、pgc(番剧)、live(直播)、article-list(文集)、article(文章)")
):
    """分页查询历史记录，支持跨年份查询"""
    print("\n=== 接收到的请求参数 ===")
    print(f"页码(page): {page}")
    print(f"每页记录数(size): {size}")
    print(f"排序顺序(sort_order): {'升序' if sort_order == 1 else '降序'}")
    print(f"子分区名称(tag_name): {tag_name if tag_name else '无'}")
    print(f"主分区名称(main_category): {main_category if main_category else '无'}")
    print(f"日期范围(date_range): {date_range if date_range else '无'}")
    print(f"业务类型(business): {business if business else '全部'}")
    print("=====================\n")

    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # 获取可用年份列表
        available_years = get_available_years()
        if not available_years:
            return {
                "status": "success",
                "data": {
                    "records": [],
                    "total": 0,
                    "size": size,
                    "current": page,
                    "available_years": [],
                },
            }

        # 构建UNION ALL查询
        queries = []
        params = []

        # 处理日期范围
        start_timestamp = None
        end_timestamp = None
        if date_range:
            try:
                start_date, end_date = date_range.split('-')
                start_timestamp = int(datetime.strptime(start_date, '%Y%m%d').timestamp())
                end_timestamp = int(datetime.strptime(end_date, '%Y%m%d').timestamp()) + 86400
            except ValueError:
                return {"status": "error", "message": "日期格式无效，应为yyyyMMdd-yyyyMMdd"}

        # 为每个年份构建查询
        for year in available_years:
            table_name = f"bilibili_history_{year}"
            query = f"SELECT * FROM {table_name} WHERE 1=1"

            # 添加日期范围条件
            if start_timestamp is not None and end_timestamp is not None:
                query += " AND view_at >= ? AND view_at < ?"
                params.extend([start_timestamp, end_timestamp])

            # 添加分类筛选
            if main_category:
                query += " AND main_category = ?"
                params.append(main_category)
            elif tag_name:
                query += " AND tag_name = ?"
                params.append(tag_name)

            # 添加业务类型筛选
            if business:
                query += " AND business = ?"
                params.append(business)

            queries.append(query)

        # 组合所有查询
        base_query = " UNION ALL ".join(queries)

        # 获取总记录数
        count_query = f"SELECT COUNT(*) FROM ({base_query})"
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]

        # 添加排序和分页
        final_query = f"""
            SELECT * FROM ({base_query})
            ORDER BY view_at {('ASC' if sort_order == 1 else 'DESC')}
            LIMIT ? OFFSET ?
        """
        params.extend([size, (page - 1) * size])

        print("=== SQL查询构建 ===")
        print(f"最终SQL: {final_query}")
        print(f"参数: {params}")
        print("==================\n")

        # 执行查询
        cursor.execute(final_query, params)
        columns = [description[0] for description in cursor.description]
        records = []

        for row in cursor.fetchall():
            record = dict(zip(columns, row))
            record = _process_record(record)
            records.append(record)

        print("=== 响应结果 ===")
        print(f"返回记录数: {len(records)}")
        print(f"第一条记录: {records[0] if records else '无记录'}")
        print("================\n")

        return {
            "status": "success",
            "data": {
                "records": records,
                "total": total,
                "size": size,
                "current": page,
                "available_years": available_years
            }
        }

    except sqlite3.Error as e:
        error_msg = f"数据库错误: {str(e)}"
        print(f"=== 错误 ===\n{error_msg}\n===========")
        return {"status": "error", "message": error_msg}
    finally:
        if conn:
            conn.close()

def process_search_keyword(keyword: str) -> str:
    """处理搜索关键词，返回处理后的关键词

    Args:
        keyword: 搜索关键词

    Returns:
        str: 处理后的关键词
    """
    if not keyword:
        return ""

    # 移除多余的空格，但保留单个空格
    keyword = ' '.join(keyword.split())
    return keyword


def build_field_search_conditions(field: str, search: str, exact_match: bool) -> tuple:
    """构建字段搜索条件"""
    params = []
    conditions = []

    if exact_match:
        # 精确匹配
        conditions.append(f"{field} = ?")
        params.append(search)
    else:
        # 模糊匹配
        conditions.append(f"{field} LIKE ?")
        params.append(f"%{search}%")

    # 使用 OR 连接所有条件
    condition = "(" + " OR ".join(conditions) + ")"

    print(f"\n=== 字段条件构建 [{field}] ===")
    print(f"条件: {condition}")
    print(f"参数: {params}")
    print("===================")
    return condition, params


@router.get("/search", summary="搜索历史记录")
async def search_history(
    page: int = Query(1, ge=1, description="当前页码"),
    size: int = Query(30, ge=1, description="每页记录数"),
    sortOrder: int = Query(0, description="排序顺序，0为降序，1为升序"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    search_type: Optional[str] = Query("all", description="搜索类型：all-全部, title-标题, author-作者, tag-分区"),
):
    """高级搜索历史记录，按观看时间排序，使用模糊匹配"""
    conn = None
    try:
        print("\n=== 搜索开始 ===")
        print(f"关键词: {search}")
        print(f"类型: {search_type}")
        print(f"匹配方式: 模糊匹配")
        print(f"排序顺序: {'升序' if sortOrder == 1 else '降序'}")
        print("==============\n")

        conn = get_db()
        cursor = conn.cursor()

        # 获取可用年份列表
        available_years = get_available_years()
        if not available_years:
            return {
                "status": "success",
                "data": {
                    "records": [],
                    "total": 0,
                    "size": size,
                    "current": page,
                    "available_years": [],
                },
            }

        # 构建每个年份的子查询
        sub_queries = []
        base_params = []

        # 处理搜索关键词
        field_map = {
            "title": "title",
            "author": "author_name",
            "tag": "tag_name"
        }

        where_clause = ""
        search_params = []
        if search:
            search = process_search_keyword(search)
            print(f"\n处理后的搜索关键词: {search}\n")

            print("\n=== 开始构建查询条件 ===")

            # 构建WHERE子句（强制使用模糊匹配）
            exact_match = False
            if search_type == "all":
                field_conditions = []
                for field_name, field in field_map.items():
                    print(f"\n处理字段: {field_name}")
                    condition, params = build_field_search_conditions(field, search, exact_match)
                    field_conditions.append(condition)
                    search_params.extend(params)
                    print(f"当前参数数量: {len(search_params)}")

                if field_conditions:
                    where_clause = f"WHERE ({' OR '.join(field_conditions)})"
            else:
                field = field_map.get(search_type)
                if field:
                    condition, params = build_field_search_conditions(field, search, exact_match)
                    where_clause = f"WHERE {condition}"
                    search_params.extend(params)

        # 构建基础查询
        for year in available_years:
            table_name = f"bilibili_history_{year}"
            sub_query = f"SELECT * FROM {table_name} {where_clause}"
            sub_queries.append(sub_query)
            # 为每个子查询添加一组参数
            base_params.extend(search_params)

        base_query = f"{' UNION ALL '.join(sub_queries)}"

        print("\n=== 基础查询 ===")
        print(f"SQL: {base_query}")
        print(f"参数: {base_params}")
        print(f"参数数量: {len(base_params)}")
        print("================\n")

        # 获取总记录数
        count_query = f"SELECT COUNT(*) FROM ({base_query})"
        print("\n=== 计数查询 ===")
        print(f"SQL: {count_query}")
        print(f"参数: {base_params}")
        print("================\n")

        cursor.execute(count_query, base_params)
        total = cursor.fetchone()[0]

        # 构建最终查询，按观看时间排序和分页
        params = base_params.copy()
        query = f"""
            SELECT * FROM ({base_query})
            ORDER BY view_at {('ASC' if sortOrder == 1 else 'DESC')}
        """

        # 添加分页
        query += " LIMIT ? OFFSET ?"
        params.extend([size, (page - 1) * size])

        print("\n=== 最终查询 ===")
        print(f"SQL: {query}")
        print(f"参数: {params}")
        print(f"参数数量: {len(params)}")
        print("================\n")

        # 执行查询
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        records = []

        for row in cursor.fetchall():
            record = dict(zip(columns, row))
            record = _process_record(record)
            records.append(record)

        return {
            "status": "success",
            "data": {
                "records": records,
                "total": total,
                "size": size,
                "current": page,
                "available_years": available_years,
                "search_info": {
                    "keyword": search,
                    "type": search_type,
                    "exact_match": False,
                    "sort_by": "view_at"
                }
            }
        }

    except sqlite3.Error as e:
        error_msg = f"数据库错误: {str(e)}"
        print(f"\n=== 数据库错误 ===\n{error_msg}\n=================\n")
        return {"status": "error", "message": error_msg}
    finally:
        if conn:
            conn.close()
