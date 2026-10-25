import os
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import browser_history, fetch_bili_history, history, import_data_sqlite, login
from scripts.utils import load_config, setup_logger


setup_logger()

app = FastAPI(
    title="HistoryHub",
    description="浏览器历史同步、检索与 B 站观看历史获取",
    version="1.7.2",
)


@app.get("/health")
async def health_check():
    return {"status": "running", "timestamp": datetime.now().isoformat()}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router, prefix="/login", tags=["用户登录"])
app.include_router(fetch_bili_history.router, prefix="/fetch", tags=["历史记录获取"])
app.include_router(import_data_sqlite.router, prefix="/importSqlite", tags=["SQLite数据导入"])
app.include_router(history.router, prefix="/history", tags=["历史记录查询"])
app.include_router(browser_history.router, prefix="/browser-history", tags=["浏览历史"])


if __name__ == "__main__":
    import uvicorn

    server_config = load_config().get("server", {})
    ssl_options = {}
    if server_config.get("ssl_enabled", False):
        for option in ("ssl_certfile", "ssl_keyfile"):
            path = server_config.get(option)
            if not path or not os.path.isfile(path):
                raise FileNotFoundError(f"SSL文件不存在: {option}")
            ssl_options[option] = path

    uvicorn.run(
        "main:app",
        host=server_config.get("host", "0.0.0.0"),
        port=server_config.get("port", 8899),
        log_level="info",
        reload=False,
        **ssl_options,
    )
