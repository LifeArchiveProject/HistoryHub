from fastapi import FastAPI
from routers import analysis, export, fetch_bili_history, import_data

app = FastAPI(
    title="Bilibili History Analyzer",
    description="一个用于分析和导出Bilibili观看历史的API",
    version="1.0.0"
)

# 注册路由
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(fetch_bili_history.router, prefix="/fetch", tags=["Fetch"])
app.include_router(export.router, prefix="/export", tags=["Export"])
app.include_router(import_data.router, prefix="/import", tags=["Import"])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
