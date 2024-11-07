import asyncio
import logging
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime

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
from scripts.scheduler_manager import SchedulerManager
from scripts.utils import load_config


# 配置根日志记录器
def setup_logging():
    """设置日志系统"""
    # 创建日志格式化器
    formatter = logging.Formatter('%(message)s')
    
    # 确保日志目录存在
    current_date = datetime.now().strftime("%Y/%m/%d")
    log_dir = f'output/logs/{current_date.rsplit("/", 1)[0]}'
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建文件处理器
    log_file = f'output/logs/{current_date}.log'
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8', errors='replace')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # 清除现有的处理器
    root_logger.handlers.clear()
    
    root_logger.addHandler(file_handler)

    # 重定向 print 输出到日志
    class PrintToLogger:
        def __init__(self, logger, stdout):
            self.logger = logger
            self.stdout = stdout
            self._line_buffer = []
        
        def write(self, buf):
            # 跳过调度器和FastAPI的日志
            if any(skip in buf for skip in [
                'INFO:', 'ERROR:', 'WARNING:', '[32m', '[0m', 
                'Application', 'Started', 'Waiting', 'HTTP',
                'uvicorn', 'DEBUG'
            ]):
                # 只写入到控制台
                self.stdout.write(buf)
                return
            
            # 收集完整的行
            for c in buf:
                if c == '\n':
                    line = ''.join(self._line_buffer).rstrip()
                    if line:  # 只记录非空行
                        # 只写入到日志文件，不再写入控制台
                        record = logging.LogRecord(
                            name='print',
                            level=logging.INFO,
                            pathname='',
                            lineno=0,
                            msg=line,
                            args=(),
                            exc_info=None
                        )
                        file_handler.emit(record)
                    self._line_buffer = []
                else:
                    self._line_buffer.append(c)
        
        def flush(self):
            if self._line_buffer:
                line = ''.join(self._line_buffer).rstrip()
                if line:
                    record = logging.LogRecord(
                        name='print',
                        level=logging.INFO,
                        pathname='',
                        lineno=0,
                        msg=line,
                        args=(),
                        exc_info=None
                    )
                    file_handler.emit(record)
                self._line_buffer = []
            self.stdout.flush()
        
        def isatty(self):
            return self.stdout.isatty()
        
        def fileno(self):
            return self.stdout.fileno()

    # 保存原始的 stdout
    original_stdout = sys.stdout
    # 创建新的 PrintToLogger 实例,传入原始 stdout
    sys.stdout = PrintToLogger(root_logger, original_stdout)

    return log_file

# 在应用启动时调用
setup_logging()

# 全局调度器实例
scheduler_manager = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    global scheduler_manager
    scheduler_manager = SchedulerManager.get_instance(app)
    
    # 等待应用完全启动
    await asyncio.sleep(2)  # 给应用一些启动时间
    
    # 启动调度器
    asyncio.create_task(scheduler_manager.run_scheduler())
    
    yield  # 应用运行中
    
    # 关闭时执行
    if scheduler_manager:
        scheduler_manager.stop_scheduler()

    # 恢复原始的 stdout
    sys.stdout = sys.stdout.stdout

# 创建 FastAPI 应用实例
app = FastAPI(
    title="Bilibili History Analyzer",
    description="一个用于分析和导出Bilibili观看历史的API",
    version="1.0.0",
    lifespan=lifespan
)

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    
    # 加载配置
    config = load_config()
    server_config = config.get('server', {})
    
    uvicorn.run(
        "main:app", 
        host=server_config.get('host', "127.0.0.1"),
        port=server_config.get('port', 8000),  # 如果没有配置则使用8000作为默认值
    )
