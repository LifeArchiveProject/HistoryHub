from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from scripts.export_to_excel import export_bilibili_history
from scripts.utils import get_output_path, load_config
from typing import Dict, Any
import os
from datetime import datetime

router = APIRouter()
config = load_config()

@router.post(
    "/export_history",
    summary="导出Bilibili历史记录到Excel",
    response_model=Dict[str, Any],
    description="将历史记录数据导出为Excel文件，支持按年份、月份或日期范围导出数据"
)
def export_history(
    year: int = Query(None, description="要导出的年份，不指定则使用当前年份"),
    month: int = Query(None, description="要导出的月份（1-12），如果指定则只导出该月数据", ge=1, le=12),
    start_date: str = Query(None, description="开始日期，格式为'YYYY-MM-DD'，如果指定则从该日期开始导出"),
    end_date: str = Query(None, description="结束日期，格式为'YYYY-MM-DD'，如果指定则导出到该日期为止")
):
    """
    导出Bilibili历史记录到Excel文件。

    Args:
        year: 要导出的年份，不指定则使用当前年份
        month: 要导出的月份（1-12），如果指定则只导出该月数据
        start_date: 开始日期，格式为'YYYY-MM-DD'，如果指定则从该日期开始导出
        end_date: 结束日期，格式为'YYYY-MM-DD'，如果指定则导出到该日期为止

    Returns:
        Dict[str, Any]: 包含状态和消息的响应
    """
    # 验证日期格式
    if start_date:
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="开始日期格式错误，应为'YYYY-MM-DD'")

    if end_date:
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=400, detail="结束日期格式错误，应为'YYYY-MM-DD'")

    result = export_bilibili_history(year, month, start_date, end_date)

    if result["status"] == "success":
        # 返回文件名信息，便于前端下载
        filename = os.path.basename(result["message"].split("数据已成功导出到 ")[-1])
        return {"status": "success", "message": result["message"], "filename": filename}
    else:
        raise HTTPException(status_code=500, detail=result["message"])

@router.get(
    "/download_excel/{filename}",
    summary="下载Excel文件",
    description="下载指定的Excel文件，支持浏览器直接下载",
    response_class=FileResponse,
    responses={
        200: {
            "description": "Excel文件",
            "content": {
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": {
                    "schema": {"type": "string", "format": "binary"}
                }
            }
        },
        404: {
            "description": "文件不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "未找到指定的Excel文件"}
                }
            }
        }
    }
)
def download_excel(filename: str):
    """
    下载指定的Excel文件。

    Args:
        filename: 要下载的文件名

    Returns:
        FileResponse: Excel文件响应
    """
    file_path = get_output_path(filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"未找到文件 {filename}")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.get(
    "/download_db",
    summary="下载SQLite数据库",
    description="下载完整的SQLite数据库文件，包含所有年份的历史记录数据",
    response_class=FileResponse,
    responses={
        200: {
            "description": "SQLite数据库文件",
            "content": {
                "application/x-sqlite3": {
                    "schema": {"type": "string", "format": "binary"}
                }
            }
        },
        404: {
            "description": "文件不存在",
            "content": {
                "application/json": {
                    "example": {"detail": "数据库文件不存在"}
                }
            }
        }
    }
)
def download_db():
    """
    下载完整的SQLite数据库文件。

    Returns:
        FileResponse: 数据库文件响应
    """
    db_path = get_output_path(config['db_file'])

    if not os.path.exists(db_path):
        raise HTTPException(status_code=404, detail="数据库文件不存在")

    return FileResponse(
        path=db_path,
        filename="bilibili_history.db",
        media_type="application/x-sqlite3"
    )
