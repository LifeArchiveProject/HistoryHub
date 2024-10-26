from fastapi import FastAPI
from routers import (
    analysis,
    export,
    fetch_bili_history,
    import_data_sqlite,
    import_data_mysql,
    clean_data
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

# 注册路由
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(fetch_bili_history.router, prefix="/fetch", tags=["Fetch"])
app.include_router(export.router, prefix="/export", tags=["Export"])
app.include_router(import_data_mysql.router, prefix="/importMysql", tags=["Import"])
app.include_router(import_data_sqlite.router, prefix="/importSqlite", tags=["Import"])
app.include_router(clean_data.router, prefix="/clean", tags=["Clean"])

# 入口点，启动应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
