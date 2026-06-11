import inspect
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Optional

from fastapi import HTTPException

from scripts.utils import get_base_path, load_config


MAX_DEFAULT_PAGE_SIZE = 100
SENSITIVE_CONFIG_KEYS = {
    "SESSDATA",
    "bili_jct",
    "DedeUserID",
    "DedeUserID__ckMd5",
    "password",
    "token",
}


class BearerTokenASGIMiddleware:
    """为 MCP ASGI 应用增加实时开关和轻量 Bearer Token 校验。"""

    def __init__(
        self,
        app: Callable,
        token: Optional[str],
        auth_enabled: bool = True,
        config_loader: Optional[Callable[[], dict[str, Any]]] = None,
    ):
        self.app = app
        self.token = token
        self.auth_enabled = auth_enabled
        self.config_loader = config_loader

    async def __call__(self, scope: dict, receive: Callable, send: Callable) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        try:
            runtime_config = self.config_loader() if self.config_loader else {}
        except Exception as e:
            await self._json_response(
                send,
                503,
                {
                    "status": "error",
                    "message": f"MCP config is unavailable: {e}",
                },
            )
            return

        if runtime_config and not runtime_config.get("enabled", False):
            await self._json_response(
                send,
                503,
                {
                    "status": "error",
                    "message": "MCP service is disabled.",
                },
            )
            return

        auth_enabled = runtime_config.get("auth_enabled", self.auth_enabled)
        if not auth_enabled:
            await self.app(scope, receive, send)
            return

        token = runtime_config.get("token", self.token)
        if not token:
            await self._json_response(
                send,
                503,
                {
                    "status": "error",
                    "message": "MCP token is not configured.",
                },
            )
            return

        headers = dict(scope.get("headers") or [])
        authorization = headers.get(b"authorization", b"").decode("utf-8")
        expected = f"Bearer {token}"
        if authorization != expected:
            await self._json_response(
                send,
                401,
                {
                    "status": "error",
                    "message": "Unauthorized MCP request.",
                },
                {"WWW-Authenticate": "Bearer"},
            )
            return

        await self.app(scope, receive, send)

    async def _json_response(
        self,
        send: Callable,
        status_code: int,
        payload: dict,
        extra_headers: Optional[dict[str, str]] = None,
    ) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers = {
            "content-type": "application/json; charset=utf-8",
            "content-length": str(len(body)),
        }
        if extra_headers:
            headers.update(extra_headers)

        await send(
            {
                "type": "http.response.start",
                "status": status_code,
                "headers": [
                    (key.lower().encode("latin-1"), value.encode("latin-1"))
                    for key, value in headers.items()
                ],
            }
        )
        await send({"type": "http.response.body", "body": body})


def get_mcp_config() -> dict[str, Any]:
    config = load_config()
    server_config = config.get("server", {})
    mcp_config = server_config.get("mcp", {})
    token = os.environ.get("BHF_MCP_TOKEN") or mcp_config.get("token")

    return {
        "enabled": bool(mcp_config.get("enabled", False)),
        "path": mcp_config.get("path", "/mcp"),
        "host": server_config.get("host", "127.0.0.1"),
        "port": int(server_config.get("port", 8899)),
        "token": token,
        "auth_enabled": bool(mcp_config.get("auth_enabled", True)),
        "max_page_size": int(mcp_config.get("max_page_size", MAX_DEFAULT_PAGE_SIZE)),
    }


def create_mcp_app(config: Optional[dict[str, Any]] = None) -> tuple[Callable, Any]:
    from mcp.server.fastmcp import FastMCP

    mcp_config = config or get_mcp_config()
    mcp = FastMCP(
        "BilibiliHistoryFetcher",
        instructions=(
            "Read-only MCP server for local Bilibili history data. "
            "Use paginated tools for records and do not request write operations."
        ),
        host=mcp_config["host"],
        port=mcp_config["port"],
        streamable_http_path="/",
        json_response=True,
    )
    _register_resources(mcp)
    _register_prompts(mcp)
    _register_tools(mcp, max_page_size=mcp_config["max_page_size"])

    mcp_app = mcp.streamable_http_app()
    protected_app = BearerTokenASGIMiddleware(
        mcp_app,
        token=mcp_config.get("token"),
        auth_enabled=mcp_config.get("auth_enabled", True),
        config_loader=get_mcp_config,
    )
    return protected_app, mcp.session_manager


def _register_resources(mcp: Any) -> None:
    @mcp.resource(
        "bili://project/overview",
        name="project_overview",
        description="BilibiliHistoryFetcher project capability overview.",
        mime_type="application/json",
    )
    async def project_overview() -> str:
        return _json_text(
            {
                "name": "BilibiliHistoryFetcher",
                "summary": "Bilibili history fetching, storage, analysis and visualization backend.",
                "mcp_policy": "Read-only by default. Full history records are readable through paginated tools.",
                "primary_data": [
                    "output/bilibili_history.db",
                    "output/database/*.db",
                    "output/history_by_date/YYYY/MM/DD.json",
                    "output/logs/YYYY/MM/DD/*.log",
                ],
                "recommended_flow": [
                    "Read bili://project/data-status first.",
                    "Use summary tools before reading large record pages.",
                    "Use page and size on every record-list tool.",
                ],
            }
        )

    @mcp.resource(
        "bili://project/tool-guide",
        name="tool_guide",
        description="When to use each read-only MCP tool.",
        mime_type="application/json",
    )
    async def tool_guide() -> str:
        return _json_text(_tool_guide())

    @mcp.resource(
        "bili://project/data-status",
        name="data_status",
        description="Current local data inventory and available years.",
        mime_type="application/json",
    )
    async def data_status() -> str:
        return _json_text(await _build_project_status())

    @mcp.resource(
        "bili://project/privacy-policy",
        name="privacy_policy",
        description="MCP privacy and safety policy.",
        mime_type="application/json",
    )
    async def privacy_policy() -> str:
        return _json_text(
            {
                "access": "LAN HTTP MCP protected by Bearer Token.",
                "readable": [
                    "Paginated watch history records",
                    "Local video details",
                    "Aggregated analytics",
                    "Scheduler status and execution history",
                    "Data integrity reports",
                ],
                "blocked_in_v1": [
                    "Login",
                    "Sync/fetch from Bilibili",
                    "Download",
                    "Delete",
                    "Reset database",
                    "Update configuration",
                ],
                "sensitive_fields_never_returned_by_status_tools": sorted(SENSITIVE_CONFIG_KEYS),
                "record_tools": "Record tools may return full local record fields, but image URLs default to no SESSDATA.",
            }
        )


def _register_prompts(mcp: Any) -> None:
    @mcp.prompt(
        name="analyze_viewing_pattern",
        description="Analyze viewing habits with minimum context.",
    )
    def analyze_viewing_pattern(year: Optional[int] = None) -> str:
        year_hint = f" for year {year}" if year else ""
        return (
            f"Analyze Bilibili viewing patterns{year_hint}. "
            "First read bili://project/data-status, then call get_annual_summary and "
            "get_viewing_analytics. Only call query_history_records when concrete examples are needed."
        )

    @mcp.prompt(name="find_video_or_author", description="Find history records by video or author.")
    def find_video_or_author(keyword: str) -> str:
        return (
            f"Find local Bilibili history records related to '{keyword}'. "
            "Use search_history_records first, then get_video_detail for any important bvid."
        )

    @mcp.prompt(name="annual_report_insight", description="Generate annual report insights.")
    def annual_report_insight(year: Optional[int] = None) -> str:
        year_hint = f" for year {year}" if year else ""
        return (
            f"Create a concise annual Bilibili viewing report{year_hint}. "
            "Use get_annual_summary first and add only a few paginated examples if needed."
        )

    @mcp.prompt(name="data_health_check", description="Check local data health.")
    def data_health_check() -> str:
        return (
            "Check local BilibiliHistoryFetcher data health. "
            "Read bili://project/data-status, then call get_data_integrity_report, "
            "get_sync_result, and get_scheduler_tasks."
        )


def _register_tools(mcp: Any, max_page_size: int) -> None:
    @mcp.tool(description="Get project, database and MCP status without sensitive configuration.")
    async def get_project_status() -> dict[str, Any]:
        return await _build_project_status()

    @mcp.tool(description="List available years in the local watch history database.")
    async def list_available_years() -> dict[str, Any]:
        from routers import history

        return await _call_route("/history/available-years", history.get_years)

    @mcp.tool(description="Query paginated local watch history records.")
    async def query_history_records(
        page: int = 1,
        size: int = 30,
        sort_order: int = 0,
        tag_name: Optional[str] = None,
        main_category: Optional[str] = None,
        date_range: Optional[str] = None,
        business: Optional[str] = None,
        use_local_images: bool = False,
    ) -> dict[str, Any]:
        from routers import history

        size = _limit_page_size(size, max_page_size)
        return await _call_route(
            "/history/all",
            history.get_history_page,
            page=max(1, page),
            size=size,
            sort_order=sort_order,
            tag_name=tag_name,
            main_category=main_category,
            date_range=date_range,
            use_local_images=use_local_images,
            use_sessdata=False,
            business=business,
            meta={"page": page, "size": size},
        )

    @mcp.tool(description="Search paginated local watch history records.")
    async def search_history_records(
        search: str,
        search_type: str = "all",
        page: int = 1,
        size: int = 30,
        sort_order: int = 0,
        use_local_images: bool = False,
    ) -> dict[str, Any]:
        from routers import history

        size = _limit_page_size(size, max_page_size)
        return await _call_route(
            "/history/search",
            history.search_history,
            page=max(1, page),
            size=size,
            sortOrder=sort_order,
            search=search,
            search_type=search_type,
            use_sessdata=False,
            use_local_images=use_local_images,
            meta={"page": page, "size": size, "search_type": search_type},
        )

    @mcp.tool(description="Get one local watch history video by CID.")
    async def get_history_by_cid(cid: int, use_local_images: bool = False) -> dict[str, Any]:
        from routers import history

        return await _call_route(
            f"/history/by_cid/{cid}",
            history.get_video_by_cid,
            cid=cid,
            use_local_images=use_local_images,
            use_sessdata=False,
        )

    @mcp.tool(description="Get statistics for a specific date. Date format is MMDD, for example 0113.")
    async def get_daily_count(date: str, year: Optional[int] = None) -> dict[str, Any]:
        from routers import daily_count

        return await _call_route(
            "/daily/daily-count",
            daily_count.get_daily_count,
            date=date,
            year=year,
        )

    @mcp.tool(description="Get full annual summary JSON for a year without writing files.")
    async def get_annual_summary(year: Optional[int] = None, use_cache: bool = True) -> dict[str, Any]:
        from routers import viewing_analytics

        return await _call_route(
            "/viewing/annual-summary/json",
            viewing_analytics.get_annual_summary_json,
            year=year,
            use_cache=use_cache,
            save_to_file=False,
        )

    @mcp.tool(
        description=(
            "Get one viewing analytics component: monthly, weekly, time_slots, "
            "continuity, watch_counts, or completion_rates."
        )
    )
    async def get_viewing_analytics(
        analysis_type: str,
        year: Optional[int] = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        from routers import viewing_analytics

        mapping = {
            "monthly": ("/viewing/monthly-stats", viewing_analytics.get_monthly_stats),
            "weekly": ("/viewing/weekly-stats", viewing_analytics.get_weekly_stats),
            "time_slots": ("/viewing/time-slots", viewing_analytics.get_time_slots),
            "continuity": ("/viewing/continuity", viewing_analytics.get_viewing_continuity),
            "watch_counts": ("/viewing/watch-counts", viewing_analytics.get_viewing_watch_counts),
            "completion_rates": (
                "/viewing/completion-rates",
                viewing_analytics.get_viewing_completion_rates,
            ),
        }
        route = mapping.get(analysis_type)
        if not route:
            return _error(
                "Unsupported analysis_type.",
                data={"allowed": sorted(mapping)},
                source_route="/viewing/*",
            )
        source_route, func = route
        return await _call_route(source_route, func, year=year, use_cache=use_cache)

    @mcp.tool(
        description=(
            "Get one title analytics component: keyword, length, sentiment, trend, or interaction."
        )
    )
    async def get_title_analytics(
        analysis_type: str,
        year: Optional[int] = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        from routers import title_analytics

        mapping = {
            "keyword": ("/title/keyword-analysis", title_analytics.get_keyword_analysis),
            "length": ("/title/length-analysis", title_analytics.get_length_analysis),
            "sentiment": ("/title/sentiment-analysis", title_analytics.get_sentiment_analysis),
            "trend": ("/title/trend-analysis", title_analytics.get_trend_analysis),
            "interaction": ("/title/interaction-analysis", title_analytics.get_interaction_analysis),
        }
        route = mapping.get(analysis_type)
        if not route:
            return _error(
                "Unsupported analysis_type.",
                data={"allowed": sorted(mapping)},
                source_route="/title/*",
            )
        source_route, func = route
        return await _call_route(source_route, func, year=year, use_cache=use_cache)

    @mcp.tool(description="Get aggregated local interaction summary.")
    async def get_interaction_summary(year: Optional[int] = None) -> dict[str, Any]:
        from routers import interaction_records

        return await _call_route(
            "/interactions/summary",
            interaction_records.get_interaction_summary,
            year=year,
        )

    @mcp.tool(description="Query paginated local interaction records.")
    async def query_interaction_records(
        page: int = 1,
        size: int = 30,
        source: Optional[str] = None,
        year: Optional[int] = None,
        search: Optional[str] = None,
    ) -> dict[str, Any]:
        from routers import interaction_records

        size = _limit_page_size(size, max_page_size)
        return await _call_route(
            "/interactions/records",
            interaction_records.get_interaction_records,
            page=max(1, page),
            size=size,
            source=source,
            year=year,
            search=search,
            meta={"page": page, "size": size},
        )

    @mcp.tool(description="Get local interaction sync state without triggering sync.")
    async def get_interaction_status() -> dict[str, Any]:
        from routers import interaction_records

        return await _call_route("/interactions/status", interaction_records.get_interaction_status)

    @mcp.tool(description="Get one local video detail record by BV id.")
    async def get_video_detail(bvid: str) -> dict[str, Any]:
        from routers import video_details

        return await _call_route(
            f"/video_details/info/{bvid}",
            video_details.get_video_info_from_db,
            bvid=bvid,
        )

    @mcp.tool(description="Search local video details database.")
    async def search_video_details(
        keyword: Optional[str] = None,
        uploader_mid: Optional[int] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> dict[str, Any]:
        from routers import video_details

        per_page = _limit_page_size(per_page, max_page_size)
        return await _call_route(
            "/video_details/search",
            video_details.search_videos,
            keyword=keyword,
            uploader_mid=uploader_mid,
            page=max(1, page),
            per_page=per_page,
            meta={"page": page, "per_page": per_page},
        )

    @mcp.tool(description="Get local video details database statistics.")
    async def get_video_detail_stats() -> dict[str, Any]:
        from routers import video_details

        return await _call_route(
            "/video_details/stats",
            video_details.get_video_details_database_stats,
        )

    @mcp.tool(description="Get scheduler task status without creating, updating or executing tasks.")
    async def get_scheduler_tasks(
        task_id: Optional[str] = None,
        include_subtasks: bool = True,
        detail_level: str = "basic",
    ) -> dict[str, Any]:
        from routers import scheduler
        from scripts.scheduler_db_enhanced import EnhancedSchedulerDB

        return await _call_route(
            "/scheduler/tasks",
            scheduler.get_tasks,
            task_id=task_id,
            include_subtasks=include_subtasks,
            detail_level=detail_level,
            db=EnhancedSchedulerDB.get_instance(),
        )

    @mcp.tool(description="Get paginated scheduler execution history.")
    async def get_scheduler_history(
        task_id: Optional[str] = None,
        include_subtasks: bool = True,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        from routers import scheduler
        from scripts.scheduler_db_enhanced import EnhancedSchedulerDB

        page_size = _limit_page_size(page_size, max_page_size)
        return await _call_route(
            "/scheduler/tasks/history",
            scheduler.get_task_history,
            task_id=task_id,
            include_subtasks=include_subtasks,
            status=status,
            start_date=start_date,
            end_date=end_date,
            page=max(1, page),
            page_size=page_size,
            db=EnhancedSchedulerDB.get_instance(),
        )

    @mcp.tool(description="Get latest data integrity report content if it exists.")
    async def get_data_integrity_report() -> dict[str, Any]:
        from routers import data_sync

        return await _call_route("/data_sync/report", data_sync.get_report)

    @mcp.tool(description="Get latest JSON/database sync result if it exists.")
    async def get_sync_result() -> dict[str, Any]:
        from routers import data_sync

        return await _call_route("/data_sync/sync/result", data_sync.get_sync_result)

    @mcp.tool(description="Get local output directory inventory for key data files.")
    async def get_local_data_inventory() -> dict[str, Any]:
        return _ok(
            _build_data_inventory(),
            source_route="local:output-inventory",
        )


async def _call_route(
    source_route: str,
    func: Callable[..., Any],
    meta: Optional[dict[str, Any]] = None,
    **kwargs: Any,
) -> dict[str, Any]:
    try:
        result = func(**kwargs)
        if inspect.isawaitable(result):
            result = await result

        route_status = result.get("status") if isinstance(result, dict) else None
        if route_status == "error":
            return _error(
                result.get("message", "Route returned an error."),
                data=result,
                source_route=source_route,
                meta=meta,
            )
        return _ok(result, source_route=source_route, meta=meta)
    except HTTPException as exc:
        return _error(
            str(exc.detail),
            error_type="HTTPException",
            source_route=source_route,
            meta={"status_code": exc.status_code, **(meta or {})},
        )
    except Exception as exc:
        return _error(
            str(exc),
            error_type=type(exc).__name__,
            source_route=source_route,
            meta=meta,
        )


def _ok(data: Any, source_route: str, meta: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return {
        "status": "success",
        "data": data,
        "error": None,
        "meta": {
            "source_route": source_route,
            "generated_at": datetime.now().isoformat(),
            **(meta or {}),
        },
    }


def _error(
    message: str,
    error_type: str = "Error",
    data: Any = None,
    source_route: Optional[str] = None,
    meta: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    return {
        "status": "error",
        "data": data,
        "error": {
            "type": error_type,
            "message": message,
        },
        "meta": {
            "source_route": source_route,
            "generated_at": datetime.now().isoformat(),
            **(meta or {}),
        },
    }


async def _build_project_status() -> dict[str, Any]:
    config = load_config()
    server_config = config.get("server", {})
    mcp_config = get_mcp_config()
    history_years: list[int] = []

    try:
        from routers.history import get_available_years

        history_years = get_available_years()
    except Exception:
        history_years = []

    return {
        "status": "success",
        "project": {
            "name": "BilibiliHistoryFetcher",
            "base_path": get_base_path(),
            "output_path": str(Path(get_base_path()) / "output"),
        },
        "server": {
            "host": server_config.get("host"),
            "port": server_config.get("port"),
            "ssl_enabled": bool(server_config.get("ssl_enabled", False)),
        },
        "mcp": {
            "enabled": mcp_config["enabled"],
            "path": mcp_config["path"],
            "host": mcp_config["host"],
            "port": mcp_config["port"],
            "auth_enabled": mcp_config["auth_enabled"],
            "token_configured": bool(mcp_config.get("token")),
            "max_page_size": mcp_config["max_page_size"],
        },
        "data": {
            "available_years": history_years,
            "inventory": _build_data_inventory(),
        },
        "generated_at": datetime.now().isoformat(),
    }


def _build_data_inventory() -> dict[str, Any]:
    base_path = Path(get_base_path())
    output_path = base_path / "output"
    database_path = output_path / "database"

    watched_paths = {
        "main_history_db": output_path / "bilibili_history.db",
        "video_details_db": database_path / "bilibili_video_details.db",
        "history_by_date": output_path / "history_by_date",
        "analytics": output_path / "analytics",
        "logs": output_path / "logs",
        "database_dir": database_path,
        "data_integrity_report": output_path / "check" / "data_integrity_report.md",
        "sync_result": output_path / "check" / "sync_result.json",
    }

    return {
        name: _path_status(path)
        for name, path in watched_paths.items()
    }


def _path_status(path: Path) -> dict[str, Any]:
    exists = path.exists()
    status: dict[str, Any] = {
        "path": str(path),
        "exists": exists,
        "type": "missing",
    }
    if not exists:
        return status

    stat = path.stat()
    status.update(
        {
            "type": "directory" if path.is_dir() else "file",
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    )
    if path.is_file():
        status["size_bytes"] = stat.st_size
    else:
        try:
            status["item_count"] = sum(1 for _ in path.iterdir())
        except OSError:
            status["item_count"] = None
    return status


def _limit_page_size(size: int, max_page_size: int) -> int:
    try:
        normalized = int(size)
    except (TypeError, ValueError):
        normalized = 30
    return max(1, min(normalized, max_page_size))


def _json_text(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _tool_guide() -> dict[str, Any]:
    return {
        "status": "success",
        "tools": {
            "get_project_status": "Read service, MCP and data status without secrets.",
            "list_available_years": "Check which history years can be queried.",
            "query_history_records": "Read paginated watch history records.",
            "search_history_records": "Search watch history by title, author, tag or remark.",
            "get_history_by_cid": "Read one watch-history video by CID.",
            "get_daily_count": "Analyze one calendar day.",
            "get_annual_summary": "Read the full annual summary JSON.",
            "get_viewing_analytics": "Read one viewing behavior analytics component.",
            "get_title_analytics": "Read one title analytics component.",
            "get_interaction_summary": "Read aggregated favorite/like/coin summary.",
            "query_interaction_records": "Read paginated favorite/like/coin records.",
            "get_interaction_status": "Read interaction sync status without syncing.",
            "get_video_detail": "Read one local video detail by bvid.",
            "search_video_details": "Search local video details.",
            "get_video_detail_stats": "Read video detail database statistics.",
            "get_scheduler_tasks": "Read scheduler task status.",
            "get_scheduler_history": "Read scheduler execution history.",
            "get_data_integrity_report": "Read latest data integrity report.",
            "get_sync_result": "Read latest JSON/database sync result.",
            "get_local_data_inventory": "Read key output directory file status.",
        },
        "blocked_operations": [
            "fetch",
            "sync",
            "download",
            "delete",
            "reset",
            "login",
            "update_config",
        ],
    }
