import json
import os
import sqlite3
import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from scripts.utils import get_database_path, get_output_path, load_config

router = APIRouter()

DB_PATH = get_database_path("bilibili_interactions.db")
BILI_NAV_URL = "https://api.bilibili.com/x/web-interface/nav"
BILI_CREATED_FOLDERS_URL = "https://api.bilibili.com/x/v3/fav/folder/created/list-all"
BILI_FAVORITE_CONTENTS_URL = "https://api.bilibili.com/x/v3/fav/resource/list"
BILI_LIKE_VIDEOS_URL = "https://api.bilibili.com/x/space/like/video"
BILI_COIN_VIDEOS_URL = "https://api.bilibili.com/x/space/coin/video"
HISTORY_IMPORT_SOURCE = "__history_import__"
HISTORY_IMPORT_BADGE = "互动补充"
HISTORY_IMPORT_REMARK_PREFIX = "互动补充："
SOURCE_LABELS = {"favorite": "收藏", "like": "点赞", "coin": "投币"}


CREATE_INTERACTION_TABLE = """
CREATE TABLE IF NOT EXISTS interaction_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dedupe_key TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    oid INTEGER DEFAULT 0,
    aid INTEGER DEFAULT 0,
    bvid TEXT,
    title TEXT NOT NULL,
    cover TEXT,
    author_mid INTEGER DEFAULT 0,
    author_name TEXT,
    author_face TEXT,
    tname TEXT,
    duration INTEGER DEFAULT 0,
    pubtime INTEGER DEFAULT 0,
    ctime INTEGER DEFAULT 0,
    action_time INTEGER DEFAULT 0,
    action_time_source TEXT DEFAULT 'unknown',
    effective_time INTEGER DEFAULT 0,
    media_id INTEGER DEFAULT 0,
    media_title TEXT,
    raw_json TEXT,
    fetch_time INTEGER NOT NULL
);
"""

CREATE_SYNC_STATE_TABLE = """
CREATE TABLE IF NOT EXISTS interaction_sync_state (
    source TEXT PRIMARY KEY,
    last_sync_time INTEGER NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    total_records INTEGER DEFAULT 0,
    inserted_count INTEGER DEFAULT 0,
    updated_count INTEGER DEFAULT 0,
    details_json TEXT
);
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_interaction_source ON interaction_records (source);",
    "CREATE INDEX IF NOT EXISTS idx_interaction_bvid ON interaction_records (bvid);",
    "CREATE INDEX IF NOT EXISTS idx_interaction_author_mid ON interaction_records (author_mid);",
    "CREATE INDEX IF NOT EXISTS idx_interaction_action_time ON interaction_records (action_time);",
    "CREATE INDEX IF NOT EXISTS idx_interaction_effective_time ON interaction_records (effective_time);",
    "CREATE INDEX IF NOT EXISTS idx_interaction_media_id ON interaction_records (media_id);",
]


class InteractionSyncRequest(BaseModel):
    include_favorites: bool = Field(True, description="是否同步收藏记录")
    include_likes: bool = Field(True, description="是否同步点赞记录")
    include_coins: bool = Field(True, description="是否同步投币记录")
    max_favorite_pages: int = Field(0, ge=0, description="每个收藏夹最多同步页数，0表示不限")
    favorite_page_size: int = Field(20, ge=1, le=20, description="收藏夹分页大小")
    request_interval: float = Field(0.6, ge=0, le=10, description="请求间隔秒数")
    sessdata: Optional[str] = Field(None, description="用户的SESSDATA")
    up_mid: Optional[int] = Field(None, description="目标用户MID，不传则使用当前登录用户")


def get_db_connection() -> sqlite3.Connection:
    """获取互动记录数据库连接并确保表结构存在。"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(CREATE_INTERACTION_TABLE)
    cursor.execute(CREATE_SYNC_STATE_TABLE)
    for index_sql in CREATE_INDEXES:
        cursor.execute(index_sql)
    conn.commit()
    return conn


def get_headers(sessdata: Optional[str] = None) -> Dict[str, str]:
    """构建B站请求头。"""
    current_config = load_config()
    if sessdata is None:
        sessdata = current_config.get("SESSDATA", "")

    cookies = []
    if sessdata:
        cookies.append(f"SESSDATA={str(sessdata).strip('\"')}")

    for key in ("bili_jct", "DedeUserID", "DedeUserID__ckMd5"):
        value = current_config.get(key, "")
        if value:
            cookies.append(f"{key}={value}")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/116.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.bilibili.com/",
    }
    if cookies:
        headers["Cookie"] = "; ".join(cookies)
    return headers


def _to_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _first_non_empty(*values: Any) -> Any:
    for value in values:
        if value not in (None, ""):
            return value
    return ""


def _normalize_media_list(data: Any) -> List[Dict[str, Any]]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        for key in ("list", "medias", "archives", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _request_bili_json(
    url: str,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None,
    timeout: int = 15,
) -> Dict[str, Any]:
    response = requests.get(url, params=params, headers=headers, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if data.get("code") != 0:
        return {
            "status": "error",
            "code": data.get("code"),
            "message": data.get("message", "Unknown Bilibili API error"),
            "raw": data,
        }
    return {"status": "success", "data": data.get("data")}


def get_current_user_info(headers: Dict[str, str]) -> Optional[Dict[str, Any]]:
    result = _request_bili_json(BILI_NAV_URL, headers)
    if result.get("status") != "success":
        return None

    data = result.get("data") or {}
    if not data.get("isLogin"):
        return None
    return {
        "uid": data.get("mid"),
        "uname": data.get("uname"),
        "face": data.get("face"),
    }


def _normalize_interaction_record(
    source: str,
    item: Dict[str, Any],
    fetch_time: int,
    media_id: int = 0,
    media_title: str = "",
) -> Dict[str, Any]:
    upper = item.get("upper") if isinstance(item.get("upper"), dict) else {}
    owner = item.get("owner") if isinstance(item.get("owner"), dict) else {}
    stat = item.get("stat") if isinstance(item.get("stat"), dict) else {}

    oid = _to_int(_first_non_empty(item.get("id"), item.get("oid"), item.get("aid")))
    aid = _to_int(_first_non_empty(item.get("aid"), item.get("id"), item.get("oid")))
    bvid = str(_first_non_empty(item.get("bvid"), item.get("bv_id")) or "")
    title = str(_first_non_empty(item.get("title"), item.get("name"), "Untitled"))
    cover = str(_first_non_empty(item.get("cover"), item.get("pic"), item.get("first_frame")) or "")

    author_mid = _to_int(_first_non_empty(upper.get("mid"), owner.get("mid"), item.get("author_mid"), item.get("mid")))
    author_name = str(_first_non_empty(upper.get("name"), owner.get("name"), item.get("author"), item.get("author_name")) or "")
    author_face = str(_first_non_empty(upper.get("face"), owner.get("face"), item.get("author_face")) or "")

    pubtime = _to_int(_first_non_empty(item.get("pubtime"), item.get("pubdate"), item.get("publish_time")))
    ctime = _to_int(item.get("ctime"))
    duration = _to_int(item.get("duration"))
    tname = str(_first_non_empty(item.get("tname"), item.get("typename"), item.get("type_name")) or "")

    if source == "favorite":
        action_time = _to_int(item.get("fav_time"))
        action_time_source = "fav_time" if action_time > 0 else "unknown"
    elif source == "coin":
        action_time = _to_int(item.get("time"))
        action_time_source = "time" if action_time > 0 else "unavailable"
    else:
        action_time = 0
        action_time_source = "unavailable"

    effective_time = action_time or pubtime or ctime or fetch_time
    identity = bvid or str(aid or oid or title)
    dedupe_key = f"{source}:{media_id}:{identity}"

    raw_item = dict(item)
    if stat and "cnt_info" not in raw_item:
        raw_item["cnt_info"] = stat

    return {
        "dedupe_key": dedupe_key,
        "source": source,
        "oid": oid,
        "aid": aid,
        "bvid": bvid,
        "title": title,
        "cover": cover,
        "author_mid": author_mid,
        "author_name": author_name,
        "author_face": author_face,
        "tname": tname,
        "duration": duration,
        "pubtime": pubtime,
        "ctime": ctime,
        "action_time": action_time,
        "action_time_source": action_time_source,
        "effective_time": effective_time,
        "media_id": media_id,
        "media_title": media_title,
        "raw_json": json.dumps(raw_item, ensure_ascii=False),
        "fetch_time": fetch_time,
    }


def save_interaction_records(conn: sqlite3.Connection, records: List[Dict[str, Any]]) -> Dict[str, int]:
    """保存互动记录并返回新增/更新数量。"""
    if not records:
        return {"inserted": 0, "updated": 0}

    cursor = conn.cursor()
    inserted = 0
    updated = 0

    for record in records:
        cursor.execute(
            "SELECT id FROM interaction_records WHERE dedupe_key = ?",
            (record["dedupe_key"],),
        )
        exists = cursor.fetchone() is not None
        cursor.execute(
            """
            INSERT INTO interaction_records (
                dedupe_key, source, oid, aid, bvid, title, cover, author_mid,
                author_name, author_face, tname, duration, pubtime, ctime,
                action_time, action_time_source, effective_time, media_id,
                media_title, raw_json, fetch_time
            ) VALUES (
                :dedupe_key, :source, :oid, :aid, :bvid, :title, :cover, :author_mid,
                :author_name, :author_face, :tname, :duration, :pubtime, :ctime,
                :action_time, :action_time_source, :effective_time, :media_id,
                :media_title, :raw_json, :fetch_time
            )
            ON CONFLICT(dedupe_key) DO UPDATE SET
                oid = excluded.oid,
                aid = excluded.aid,
                bvid = excluded.bvid,
                title = excluded.title,
                cover = excluded.cover,
                author_mid = excluded.author_mid,
                author_name = excluded.author_name,
                author_face = excluded.author_face,
                tname = excluded.tname,
                duration = excluded.duration,
                pubtime = excluded.pubtime,
                ctime = excluded.ctime,
                action_time = excluded.action_time,
                action_time_source = excluded.action_time_source,
                effective_time = excluded.effective_time,
                media_title = excluded.media_title,
                raw_json = excluded.raw_json,
                fetch_time = excluded.fetch_time
            """,
            record,
        )
        if exists:
            updated += 1
        else:
            inserted += 1

    conn.commit()
    return {"inserted": inserted, "updated": updated}


def update_sync_state(
    conn: sqlite3.Connection,
    source: str,
    status: str,
    message: str,
    total_records: int,
    inserted_count: int,
    updated_count: int,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO interaction_sync_state (
            source, last_sync_time, status, message, total_records,
            inserted_count, updated_count, details_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(source) DO UPDATE SET
            last_sync_time = excluded.last_sync_time,
            status = excluded.status,
            message = excluded.message,
            total_records = excluded.total_records,
            inserted_count = excluded.inserted_count,
            updated_count = excluded.updated_count,
            details_json = excluded.details_json
        """,
        (
            source,
            int(time.time()),
            status,
            message,
            total_records,
            inserted_count,
            updated_count,
            json.dumps(details or {}, ensure_ascii=False),
        ),
    )
    conn.commit()


def _get_history_db_path() -> str:
    return get_output_path(load_config()["db_file"])


def _get_history_tables(history_conn: sqlite3.Connection) -> List[str]:
    cursor = history_conn.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name LIKE 'bilibili_history_%'
        ORDER BY name
    """)
    tables = []
    for (table_name,) in cursor.fetchall():
        try:
            int(str(table_name).split("_")[-1])
        except (ValueError, IndexError):
            continue
        tables.append(table_name)
    return tables


def _history_import_state_completed(conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT status FROM interaction_sync_state WHERE source = ?",
        (HISTORY_IMPORT_SOURCE,),
    )
    row = cursor.fetchone()
    return bool(row and row["status"] == "success")


def _has_imported_history_rows(history_conn: sqlite3.Connection) -> bool:
    cursor = history_conn.cursor()
    for table_name in _get_history_tables(history_conn):
        cursor.execute(
            f"""
            SELECT 1
            FROM {table_name}
            WHERE badge = ? OR remark LIKE ?
            LIMIT 1
            """,
            (HISTORY_IMPORT_BADGE, f"{HISTORY_IMPORT_REMARK_PREFIX}%"),
        )
        if cursor.fetchone():
            return True
    return False


def has_interaction_history_import_completed() -> bool:
    """判断互动补充记录是否已经导入过主历史库。"""
    conn = get_db_connection()
    try:
        if _history_import_state_completed(conn):
            return True
    finally:
        conn.close()

    history_db_path = _get_history_db_path()
    if not os.path.exists(history_db_path):
        return False

    history_conn = sqlite3.connect(history_db_path)
    try:
        return _has_imported_history_rows(history_conn)
    finally:
        history_conn.close()


def _create_history_table(history_conn: sqlite3.Connection, table_name: str) -> None:
    from config.sql_statements_sqlite import CREATE_INDEXES, CREATE_TABLE_DEFAULT

    cursor = history_conn.cursor()
    cursor.execute(CREATE_TABLE_DEFAULT.format(table=table_name))
    for index_sql in CREATE_INDEXES:
        cursor.execute(index_sql.format(table=table_name))
    history_conn.commit()


def _ensure_history_fts(history_conn: sqlite3.Connection, year: int) -> None:
    try:
        from .history import create_fts_table

        create_fts_table(history_conn, str(year))
    except Exception:
        # FTS 只是搜索加速能力，失败不应阻断历史补充导入。
        pass


def _history_table_exists(history_conn: sqlite3.Connection, table_name: str) -> bool:
    cursor = history_conn.cursor()
    cursor.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,),
    )
    return cursor.fetchone() is not None


def _load_existing_history_bvids(history_conn: sqlite3.Connection) -> set:
    existing_bvids = set()
    cursor = history_conn.cursor()
    for table_name in _get_history_tables(history_conn):
        cursor.execute(f"SELECT DISTINCT bvid FROM {table_name} WHERE bvid IS NOT NULL AND bvid != ''")
        existing_bvids.update(row[0] for row in cursor.fetchall())
    return existing_bvids


def _next_history_id(sequence: int) -> int:
    return ((int(time.time() * 1000) - 1609459200000) << 22) | (sequence & 0x3FFFFF)


def _interaction_row_to_history_record(row: sqlite3.Row, sequence: int) -> Optional[Tuple[Any, ...]]:
    source = row["source"]
    bvid = row["bvid"] or ""
    view_at = _to_int(row["effective_time"])
    if not bvid or view_at <= 0:
        return None

    source_label = SOURCE_LABELS.get(source, source)
    time_note = ""
    if row["action_time_source"] in ("unavailable", "unknown"):
        time_note = "，时间为系统推断"

    return (
        _next_history_id(sequence),
        row["title"] or "Untitled",
        "",
        row["cover"] or "",
        json.dumps([row["cover"]] if row["cover"] else [], ensure_ascii=False),
        f"https://www.bilibili.com/video/{bvid}",
        _to_int(row["aid"]) or _to_int(row["oid"]),
        0,
        bvid,
        1,
        0,
        "",
        "archive",
        0,
        1,
        row["author_name"] or "",
        row["author_face"] or "",
        _to_int(row["author_mid"]),
        view_at,
        0,
        HISTORY_IMPORT_BADGE,
        f"{source_label}记录",
        0,
        "",
        0,
        "Interaction supplement record; not a real viewing history item.",
        0,
        1 if source == "favorite" else 0,
        _to_int(row["aid"]) or _to_int(row["oid"]),
        row["tname"] or "",
        0,
        "待定",
        f"{HISTORY_IMPORT_REMARK_PREFIX}{source_label}{time_note}",
        int(time.time()),
    )


def import_interactions_to_history_once() -> Dict[str, Any]:
    """将互动记录一次性补充进主历史库，已导入过则直接跳过。"""
    interaction_conn = get_db_connection()
    history_conn: Optional[sqlite3.Connection] = None
    try:
        history_db_path = _get_history_db_path()
        os.makedirs(os.path.dirname(history_db_path), exist_ok=True)
        history_conn = sqlite3.connect(history_db_path)

        if _history_import_state_completed(interaction_conn) or _has_imported_history_rows(history_conn):
            return {
                "status": "skipped",
                "message": "Interaction history supplement already imported.",
                "inserted_count": 0,
                "already_imported": True,
            }

        existing_bvids = _load_existing_history_bvids(history_conn)
        cursor = interaction_conn.cursor()
        cursor.execute("""
            SELECT *
            FROM interaction_records
            WHERE bvid IS NOT NULL AND bvid != '' AND effective_time > 0
            ORDER BY effective_time ASC, fetch_time ASC
        """)

        records_by_year: Dict[int, List[Tuple[Any, ...]]] = defaultdict(list)
        source_counts = {"favorite": 0, "like": 0, "coin": 0}
        seen_bvids = set()
        candidates = 0
        skipped_existing = 0
        skipped_invalid = 0
        sequence = 0

        for row in cursor.fetchall():
            candidates += 1
            bvid = row["bvid"]
            if bvid in existing_bvids or bvid in seen_bvids:
                skipped_existing += 1
                continue

            history_record = _interaction_row_to_history_record(row, sequence)
            if history_record is None:
                skipped_invalid += 1
                continue

            year = datetime.fromtimestamp(_to_int(row["effective_time"])).year
            records_by_year[year].append(history_record)
            source_counts[row["source"]] = source_counts.get(row["source"], 0) + 1
            seen_bvids.add(bvid)
            sequence += 1

        inserted_count = 0
        from config.sql_statements_sqlite import INSERT_DATA

        placeholders = ",".join(["?" for _ in range(34)])
        history_cursor = history_conn.cursor()
        for year, records in records_by_year.items():
            table_name = f"bilibili_history_{year}"
            if not _history_table_exists(history_conn, table_name):
                _create_history_table(history_conn, table_name)
            _ensure_history_fts(history_conn, year)

            insert_sql = INSERT_DATA.format(table=table_name, placeholders=placeholders)
            history_cursor.executemany(insert_sql, records)
            inserted_count += len(records)

        history_conn.commit()
        status = "success" if inserted_count > 0 else "skipped"
        message = (
            f"Imported {inserted_count} interaction supplement records into history."
            if inserted_count > 0
            else "No interaction supplement records need importing."
        )
        details = {
            "candidates": candidates,
            "source_counts": source_counts,
            "skipped_existing": skipped_existing,
            "skipped_invalid": skipped_invalid,
        }
        update_sync_state(
            interaction_conn,
            HISTORY_IMPORT_SOURCE,
            status,
            message,
            candidates,
            inserted_count,
            0,
            details,
        )
        return {
            "status": status,
            "message": message,
            "inserted_count": inserted_count,
            "already_imported": inserted_count == 0 and status == "skipped",
            "details": details,
        }
    finally:
        if history_conn is not None:
            history_conn.close()
        interaction_conn.close()


def fetch_created_folders(headers: Dict[str, str], up_mid: int) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    result = _request_bili_json(
        BILI_CREATED_FOLDERS_URL,
        headers,
        params={"up_mid": up_mid, "type": 0},
    )
    if result.get("status") != "success":
        return [], result.get("message", "Failed to fetch favorite folders")

    data = result.get("data") or {}
    folders = data.get("list", []) if isinstance(data, dict) else []
    return [folder for folder in folders if isinstance(folder, dict)], None


def fetch_favorite_contents(
    headers: Dict[str, str],
    media_id: int,
    media_title: str,
    page_size: int,
    max_pages: int,
    request_interval: float,
) -> Dict[str, Any]:
    all_records: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    fetch_time = int(time.time())
    page = 1
    total = 0

    while True:
        result = _request_bili_json(
            BILI_FAVORITE_CONTENTS_URL,
            headers,
            params={
                "media_id": media_id,
                "pn": page,
                "ps": page_size,
                "order": "mtime",
                "type": 0,
                "tid": 0,
                "platform": "web",
            },
        )

        if result.get("status") != "success":
            errors.append({
                "media_id": media_id,
                "page": page,
                "message": result.get("message", "Failed to fetch favorite contents"),
                "code": result.get("code"),
            })
            break

        data = result.get("data") or {}
        info = data.get("info", {}) if isinstance(data, dict) else {}
        total = _to_int(info.get("media_count"), total)
        medias = _normalize_media_list(data)

        for item in medias:
            all_records.append(_normalize_interaction_record("favorite", item, fetch_time, media_id, media_title))

        has_more = bool(data.get("has_more")) if isinstance(data, dict) else False
        inferred_total_reached = total > 0 and page * page_size >= total
        if not medias or inferred_total_reached or (not has_more and len(medias) < page_size):
            break

        page += 1
        if max_pages > 0 and page > max_pages:
            break
        if request_interval > 0:
            time.sleep(request_interval)

    return {
        "records": all_records,
        "errors": errors,
        "pages": page,
        "total": total or len(all_records),
    }


def fetch_space_interactions(headers: Dict[str, str], source: str, up_mid: int) -> Dict[str, Any]:
    fetch_time = int(time.time())
    url = BILI_LIKE_VIDEOS_URL if source == "like" else BILI_COIN_VIDEOS_URL
    result = _request_bili_json(url, headers, params={"vmid": up_mid})

    if result.get("status") != "success":
        return {
            "records": [],
            "status": "error",
            "message": result.get("message", f"Failed to fetch {source} records"),
            "code": result.get("code"),
        }

    items = _normalize_media_list(result.get("data"))
    records = [_normalize_interaction_record(source, item, fetch_time) for item in items]
    return {
        "records": records,
        "status": "success",
        "message": "OK",
        "code": 0,
    }


def sync_interactions(request: InteractionSyncRequest) -> Dict[str, Any]:
    headers = get_headers(request.sessdata)
    user_info = get_current_user_info(headers)
    up_mid = request.up_mid or (user_info or {}).get("uid")
    if not up_mid:
        return {
            "status": "error",
            "message": "Unable to determine current user MID. Please login first.",
        }

    conn = get_db_connection()
    results: Dict[str, Any] = {}
    try:
        if request.include_favorites:
            folders, folder_error = fetch_created_folders(headers, int(up_mid))
            favorite_records: List[Dict[str, Any]] = []
            folder_errors: List[Dict[str, Any]] = []

            if folder_error:
                update_sync_state(conn, "favorite", "error", folder_error, 0, 0, 0)
                results["favorite"] = {"status": "error", "message": folder_error}
            else:
                for folder in folders:
                    media_id = _to_int(_first_non_empty(folder.get("id"), folder.get("media_id")))
                    if not media_id:
                        continue
                    media_title = str(folder.get("title") or "")
                    contents = fetch_favorite_contents(
                        headers,
                        media_id,
                        media_title,
                        request.favorite_page_size,
                        request.max_favorite_pages,
                        request.request_interval,
                    )
                    favorite_records.extend(contents["records"])
                    folder_errors.extend(contents["errors"])
                    if request.request_interval > 0:
                        time.sleep(request.request_interval)

                save_result = save_interaction_records(conn, favorite_records)
                status = "partial" if folder_errors else "success"
                message = "Favorite records synced"
                if folder_errors:
                    message = f"Favorite records synced with {len(folder_errors)} folder/page errors"
                update_sync_state(
                    conn,
                    "favorite",
                    status,
                    message,
                    len(favorite_records),
                    save_result["inserted"],
                    save_result["updated"],
                    {"folder_count": len(folders), "errors": folder_errors[:20]},
                )
                results["favorite"] = {
                    "status": status,
                    "message": message,
                    "folder_count": len(folders),
                    "total_records": len(favorite_records),
                    **save_result,
                    "errors": folder_errors,
                }

        for source, enabled in (("like", request.include_likes), ("coin", request.include_coins)):
            if not enabled:
                continue
            fetch_result = fetch_space_interactions(headers, source, int(up_mid))
            records = fetch_result["records"]
            save_result = save_interaction_records(conn, records)
            update_sync_state(
                conn,
                source,
                fetch_result["status"],
                fetch_result["message"],
                len(records),
                save_result["inserted"],
                save_result["updated"],
                {"code": fetch_result.get("code"), "api_scope": "recent_space_records"},
            )
            results[source] = {
                "status": fetch_result["status"],
                "message": fetch_result["message"],
                "total_records": len(records),
                **save_result,
                "api_scope": "recent_space_records",
            }

        return {
            "status": "success",
            "message": "Interaction sync finished",
            "data": {
                "mid": up_mid,
                "user": user_info,
                "sources": results,
            },
        }
    finally:
        conn.close()


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    data = dict(row)
    raw_json = data.pop("raw_json", None)
    if raw_json:
        try:
            data["raw"] = json.loads(raw_json)
        except json.JSONDecodeError:
            data["raw"] = None
    return data


def _get_available_history_years() -> List[int]:
    db_path = get_output_path(load_config()["db_file"])
    if not os.path.exists(db_path):
        return []
    conn = sqlite3.connect(db_path)
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
                years.append(int(table_name.split("_")[-1]))
            except (ValueError, IndexError):
                continue
        return sorted(years, reverse=True)
    finally:
        conn.close()


def _get_history_overlap(year: int, interaction_bvids: set) -> Dict[str, int]:
    db_path = get_output_path(load_config()["db_file"])
    table_name = f"bilibili_history_{year}"
    if not os.path.exists(db_path):
        return {"history_unique_videos": 0, "matched_history_videos": 0, "supplement_videos": len(interaction_bvids)}

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        if cursor.fetchone() is None:
            return {
                "history_unique_videos": 0,
                "matched_history_videos": 0,
                "supplement_videos": len(interaction_bvids),
            }
        cursor.execute(f"SELECT DISTINCT bvid FROM {table_name} WHERE bvid IS NOT NULL AND bvid != ''")
        history_bvids = {row[0] for row in cursor.fetchall()}
        matched = history_bvids & interaction_bvids
        return {
            "history_unique_videos": len(history_bvids),
            "matched_history_videos": len(matched),
            "supplement_videos": len(interaction_bvids - history_bvids),
        }
    finally:
        conn.close()


def _effective_year_expr() -> str:
    return "CAST(strftime('%Y', datetime(effective_time + 28800, 'unixepoch')) AS INTEGER)"


def collect_interaction_summary(year: Optional[int] = None) -> Dict[str, Any]:
    """收集互动记录统计数据，供接口和年度总结复用。"""
    if not os.path.exists(DB_PATH):
        selected_year = year or (datetime.now().year)
        return {
            "year": selected_year,
            "generated_at": datetime.now().isoformat(),
            "totals": {
                "total_records": 0,
                "unique_videos": 0,
                "history_unique_videos": 0,
                "matched_history_videos": 0,
                "supplement_videos": 0,
            },
            "source_counts": {"favorite": 0, "like": 0, "coin": 0},
            "monthly": {},
            "top_authors": [],
            "top_tags": [],
            "recent_records": [],
            "time_quality": {},
            "sync_state": [],
            "api_notes": get_api_capabilities()["data"]["notes"],
        }

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        available_years = _get_available_history_years()
        if year is None:
            cursor.execute(f"""
                SELECT {_effective_year_expr()} AS year_value
                FROM interaction_records
                WHERE effective_time > 0
                GROUP BY year_value
                ORDER BY year_value DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            selected_year = row["year_value"] if row and row["year_value"] else (available_years[0] if available_years else datetime.now().year)
        else:
            selected_year = year

        where_sql = f"WHERE {_effective_year_expr()} = ?"
        params = [selected_year]

        cursor.execute(f"SELECT COUNT(*) FROM interaction_records {where_sql}", params)
        total_records = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT COUNT(DISTINCT bvid)
            FROM interaction_records
            {where_sql} AND bvid IS NOT NULL AND bvid != ''
        """, params)
        unique_videos = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT source, COUNT(*) AS count
            FROM interaction_records
            {where_sql}
            GROUP BY source
        """, params)
        source_counts = {"favorite": 0, "like": 0, "coin": 0}
        source_counts.update({row["source"]: row["count"] for row in cursor.fetchall()})

        cursor.execute(f"""
            SELECT
                strftime('%Y-%m', datetime(effective_time + 28800, 'unixepoch')) AS month,
                source,
                COUNT(*) AS count
            FROM interaction_records
            {where_sql}
            GROUP BY month, source
            ORDER BY month
        """, params)
        monthly = defaultdict(lambda: {"favorite": 0, "like": 0, "coin": 0, "total": 0})
        for row in cursor.fetchall():
            monthly[row["month"]][row["source"]] = row["count"]
            monthly[row["month"]]["total"] += row["count"]

        cursor.execute(f"""
            SELECT author_mid, author_name, author_face, COUNT(*) AS count
            FROM interaction_records
            {where_sql}
            GROUP BY author_mid, author_name, author_face
            ORDER BY count DESC
            LIMIT 10
        """, params)
        top_authors = [dict(row) for row in cursor.fetchall()]

        cursor.execute(f"""
            SELECT tname, COUNT(*) AS count
            FROM interaction_records
            {where_sql} AND tname IS NOT NULL AND tname != ''
            GROUP BY tname
            ORDER BY count DESC
            LIMIT 10
        """, params)
        top_tags = [dict(row) for row in cursor.fetchall()]

        cursor.execute(f"""
            SELECT action_time_source, COUNT(*) AS count
            FROM interaction_records
            {where_sql}
            GROUP BY action_time_source
        """, params)
        time_quality = {row["action_time_source"]: row["count"] for row in cursor.fetchall()}

        cursor.execute(f"""
            SELECT *
            FROM interaction_records
            {where_sql}
            ORDER BY effective_time DESC
            LIMIT 12
        """, params)
        recent_records = [_row_to_dict(row) for row in cursor.fetchall()]

        cursor.execute(f"""
            SELECT DISTINCT bvid
            FROM interaction_records
            {where_sql} AND bvid IS NOT NULL AND bvid != ''
        """, params)
        interaction_bvids = {row["bvid"] for row in cursor.fetchall()}
        overlap = _get_history_overlap(selected_year, interaction_bvids)

        cursor.execute("SELECT * FROM interaction_sync_state ORDER BY last_sync_time DESC")
        sync_state = []
        for row in cursor.fetchall():
            item = dict(row)
            try:
                item["details"] = json.loads(item.pop("details_json") or "{}")
            except json.JSONDecodeError:
                item["details"] = {}
            sync_state.append(item)

        return {
            "year": selected_year,
            "available_years": available_years,
            "generated_at": datetime.now().isoformat(),
            "totals": {
                "total_records": total_records,
                "unique_videos": unique_videos,
                **overlap,
            },
            "source_counts": source_counts,
            "monthly": dict(monthly),
            "top_authors": top_authors,
            "top_tags": top_tags,
            "recent_records": recent_records,
            "time_quality": time_quality,
            "sync_state": sync_state,
            "api_notes": get_api_capabilities()["data"]["notes"],
        }
    finally:
        conn.close()


def build_interaction_insights(summary: Dict[str, Any]) -> Dict[str, str]:
    totals = summary.get("totals", {})
    source_counts = summary.get("source_counts", {})
    insights = {}

    total_records = totals.get("total_records", 0)
    supplement_videos = totals.get("supplement_videos", 0)
    if total_records:
        insights["interaction_coverage"] = (
            f"互动记录为年度总结补充了{total_records}条点赞、投币和收藏数据，"
            f"其中有{supplement_videos}个视频不在当年观看历史表中。"
        )

    if source_counts:
        source_labels = {"favorite": "收藏", "like": "点赞", "coin": "投币"}
        top_source = max(source_counts.items(), key=lambda item: item[1])
        if top_source[1] > 0:
            insights["primary_interaction"] = f"你最常留下痕迹的互动类型是{source_labels.get(top_source[0], top_source[0])}，共{top_source[1]}条。"

    time_quality = summary.get("time_quality", {})
    unavailable = time_quality.get("unavailable", 0)
    if unavailable:
        insights["time_quality"] = (
            f"有{unavailable}条互动记录缺少可靠动作时间，系统使用发布时间或抓取时间作为统计兜底。"
        )

    return insights


def get_api_capabilities() -> Dict[str, Any]:
    return {
        "status": "success",
        "data": {
            "sources": [
                {
                    "source": "favorite",
                    "endpoint": BILI_FAVORITE_CONTENTS_URL,
                    "time_field": "fav_time",
                    "scope": "created favorite folders, paginated",
                    "confidence": "high",
                },
                {
                    "source": "like",
                    "endpoint": BILI_LIKE_VIDEOS_URL,
                    "time_field": None,
                    "scope": "space recent liked videos",
                    "confidence": "medium",
                },
                {
                    "source": "coin",
                    "endpoint": BILI_COIN_VIDEOS_URL,
                    "time_field": "time",
                    "scope": "space recent coined videos",
                    "confidence": "medium",
                },
            ],
            "notes": [
                "Favorite folder contents are paginated and include fav_time, so all available favorite records can be counted by year reliably.",
                "The Web coin API includes time for returned records, but the endpoint is still a recent space list rather than a proven full-history archive.",
                "The Web like API exposes recent liked videos but does not provide a stable like timestamp in the documented response.",
                "Bilibili's documented space info fields include jointime, but current documented responses return 0, so sync cannot reliably start from account registration time.",
                "Records without an action timestamp use publish time, ctime, or fetch time as a conservative effective_time fallback.",
            ],
        },
    }


@router.get("/api-capabilities", summary="查看互动记录可用的B站接口")
async def api_capabilities():
    return get_api_capabilities()


@router.post("/sync", summary="同步点赞、投币、收藏互动记录")
async def sync_interaction_records(
    include_favorites: bool = Query(True, description="是否同步收藏记录"),
    include_likes: bool = Query(True, description="是否同步点赞记录"),
    include_coins: bool = Query(True, description="是否同步投币记录"),
    max_favorite_pages: int = Query(0, ge=0, description="每个收藏夹最多同步页数，0表示不限"),
    favorite_page_size: int = Query(20, ge=1, le=20, description="收藏夹分页大小"),
    request_interval: float = Query(0.6, ge=0, le=10, description="请求间隔秒数"),
    sessdata: Optional[str] = Query(None, description="用户的SESSDATA"),
    up_mid: Optional[int] = Query(None, description="目标用户MID，不传则使用当前登录用户"),
):
    request = InteractionSyncRequest(
        include_favorites=include_favorites,
        include_likes=include_likes,
        include_coins=include_coins,
        max_favorite_pages=max_favorite_pages,
        favorite_page_size=favorite_page_size,
        request_interval=request_interval,
        sessdata=sessdata,
        up_mid=up_mid,
    )
    return sync_interactions(request)


@router.get("/summary", summary="获取互动记录年度统计")
async def get_interaction_summary(
    year: Optional[int] = Query(None, description="要统计的年份，不传则使用最新互动年份"),
):
    summary = collect_interaction_summary(year)
    return {
        "status": "success",
        "data": summary,
        "insights": build_interaction_insights(summary),
    }


@router.get("/records", summary="分页查询互动记录")
async def get_interaction_records(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(30, ge=1, le=100, description="每页数量"),
    source: Optional[str] = Query(None, description="互动来源 favorite/like/coin"),
    year: Optional[int] = Query(None, description="按统计年份筛选"),
    search: Optional[str] = Query(None, description="标题或UP主关键词"),
):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        where = ["1=1"]
        params: List[Any] = []
        if source:
            where.append("source = ?")
            params.append(source)
        if year:
            where.append(f"{_effective_year_expr()} = ?")
            params.append(year)
        if search:
            where.append("(title LIKE ? OR author_name LIKE ? OR bvid LIKE ?)")
            keyword = f"%{search}%"
            params.extend([keyword, keyword, keyword])

        where_sql = "WHERE " + " AND ".join(where)
        cursor.execute(f"SELECT COUNT(*) FROM interaction_records {where_sql}", params)
        total = cursor.fetchone()[0]

        offset = (page - 1) * size
        cursor.execute(
            f"""
            SELECT *
            FROM interaction_records
            {where_sql}
            ORDER BY effective_time DESC, fetch_time DESC
            LIMIT ? OFFSET ?
            """,
            params + [size, offset],
        )
        records = [_row_to_dict(row) for row in cursor.fetchall()]
        return {
            "status": "success",
            "data": {
                "records": records,
                "total": total,
                "page": page,
                "size": size,
            },
        }
    finally:
        conn.close()


@router.get("/status", summary="获取互动记录同步状态")
async def get_interaction_status():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM interaction_sync_state ORDER BY last_sync_time DESC")
        states = []
        for row in cursor.fetchall():
            item = dict(row)
            try:
                item["details"] = json.loads(item.pop("details_json") or "{}")
            except json.JSONDecodeError:
                item["details"] = {}
            states.append(item)
        return {"status": "success", "data": states}
    finally:
        conn.close()
