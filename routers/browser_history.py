import os
import secrets
import sqlite3
from contextlib import closing
from typing import Optional
from urllib.parse import urlsplit

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from pydantic import BaseModel

from scripts.utils import get_output_path, load_config


router = APIRouter()
config = load_config()


class BrowserVisit(BaseModel):
    visit_id: str
    url: str
    title: str
    visited_at: float


class BrowserHistorySync(BaseModel):
    client_id: str
    records: list[BrowserVisit]


def require_sync_token(authorization: Optional[str] = Header(None)):
    token = os.environ.get("HISTORYHUB_SYNC_TOKEN")
    if token is None:
        token = (config.get("browser_history") or {}).get("sync_token")
    if not token:
        raise HTTPException(status_code=503, detail="浏览历史同步密钥未配置")

    scheme, _, supplied_token = (authorization or "").partition(" ")
    if scheme.lower() != "bearer" or not secrets.compare_digest(
        supplied_token.encode("utf-8"), str(token).encode("utf-8")
    ):
        raise HTTPException(
            status_code=401,
            detail="浏览历史同步密钥无效",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_db():
    conn = sqlite3.connect(get_output_path("browser_history.sqlite3"))
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS browser_history (
            id INTEGER PRIMARY KEY,
            client_id TEXT NOT NULL,
            visit_id TEXT NOT NULL,
            url TEXT NOT NULL,
            title TEXT NOT NULL,
            visited_at REAL NOT NULL,
            domain TEXT NOT NULL,
            UNIQUE (client_id, visit_id)
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_browser_history_visited_at "
        "ON browser_history (visited_at DESC, id DESC)"
    )
    conn.commit()
    return conn


@router.post("/sync", dependencies=[Depends(require_sync_token)])
def sync_browser_history(payload: BrowserHistorySync):
    records = []
    for record in payload.records:
        try:
            parsed = urlsplit(record.url)
            domain = parsed.hostname
        except ValueError:
            continue
        if parsed.scheme not in ("http", "https") or not domain:
            continue
        records.append(
            (
                payload.client_id,
                record.visit_id,
                record.url,
                record.title,
                record.visited_at,
                domain,
            )
        )

    with closing(get_db()) as conn, conn:
        conn.executemany(
            """
            INSERT INTO browser_history
                (client_id, visit_id, url, title, visited_at, domain)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT (client_id, visit_id) DO UPDATE SET
                url = excluded.url,
                title = CASE WHEN excluded.title != '' THEN excluded.title ELSE browser_history.title END,
                visited_at = excluded.visited_at,
                domain = excluded.domain
            """,
            records,
        )
    return {"status": "success", "accepted": len(records)}


@router.get("/records", dependencies=[Depends(require_sync_token)])
def get_browser_history(
    cursor: Optional[str] = None,
    size: int = Query(50, ge=1),
    query: str = "",
    domain: str = "",
):
    conditions = []
    parameters = []
    if cursor:
        try:
            visited_at, record_id = cursor.rsplit(":", 1)
            visited_at = float(visited_at)
            record_id = int(record_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="分页游标无效")
        conditions.append("(visited_at < ? OR (visited_at = ? AND id < ?))")
        parameters.extend((visited_at, visited_at, record_id))
    if query:
        conditions.append("(title LIKE ? OR url LIKE ?)")
        parameters.extend((f"%{query}%", f"%{query}%"))
    if domain:
        conditions.append("domain = ?")
        parameters.append(domain.strip().lower())

    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    with closing(get_db()) as conn:
        rows = conn.execute(
            "SELECT id, client_id, visit_id, url, title, visited_at, domain "
            f"FROM browser_history{where} "
            "ORDER BY visited_at DESC, id DESC LIMIT ?",
            [*parameters, size + 1],
        ).fetchall()

    records = [dict(row) for row in rows[:size]]
    next_cursor = None
    if len(rows) > size:
        last = records[-1]
        next_cursor = f"{last['visited_at']}:{last['id']}"
    return {"status": "success", "records": records, "next_cursor": next_cursor}
