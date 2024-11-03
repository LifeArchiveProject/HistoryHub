from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    analysis,
    clean_data,
    export,
    fetch_bili_history,
    import_data_mysql,
    import_data_sqlite,
    heatmap,
    send_log,
    download,
    history,
    categories
)
import os
import sys

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Bilibili History Analyzer",
    description="一个用于分析和导出Bilibili观看历史的API",
    version="1.0.0",
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许的源列表
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],    # 允许的HTTP方法
    allow_headers=["*"],    # 允许的HTTP头
)

# 注册路由
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(fetch_bili_history.router, prefix="/fetch", tags=["Fetch"])
app.include_router(export.router, prefix="/export", tags=["Export"])
app.include_router(import_data_mysql.router, prefix="/importMysql", tags=["Import"])
app.include_router(import_data_sqlite.router, prefix="/importSqlite", tags=["Import"])
app.include_router(clean_data.router, prefix="/clean", tags=["Clean"])
app.include_router(heatmap.router, prefix="/heatmap", tags=["Heatmap"])
app.include_router(send_log.router, prefix="/log", tags=["Log"])
app.include_router(download.router, prefix="/download", tags=["Download"])
app.include_router(history.router, prefix="/BiliHistory2024", tags=["History"])
app.include_router(categories.router, prefix="/BiliHistory2024", tags=["Categories"])

# 入口点，启动应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
