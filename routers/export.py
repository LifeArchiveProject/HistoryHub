from fastapi import APIRouter, HTTPException, Response, Query
from fastapi.responses import FileResponse
from scripts.export_to_excel import export_bilibili_history
from scripts.utils import get_output_path, load_config
from typing import Dict, Any
import os

router = APIRouter(tags=["Export"])
config = load_config()

@router.post(
    "/export_history",
    summary="导出Bilibili历史记录到Excel",
    response_model=Dict[str, Any],
    description="将历史记录数据导出为Excel文件，支持按年份导出数据"
)
def export_history(year: int = Query(None, description="要导出的年份，不指定则使用当前年份")):
    """
    导出Bilibili历史记录到Excel文件。
    
    Args:
        year: 要导出的年份，不指定则使用当前年份
    
    Returns:
        Dict[str, Any]: 包含状态和消息的响应
    """
    result = export_bilibili_history(year)
    
    if result["status"] == "success":
        return {"status": "success", "message": result["message"]}
    else:
        raise HTTPException(status_code=500, detail=result["message"])

@router.get(
    "/download_excel/{year}",
    summary="下载Excel文件",
    description="下载指定年份的Excel文件，支持浏览器直接下载",
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
                    "example": {"detail": "未找到指定年份的Excel文件"}
                }
            }
        }
    }
)
def download_excel(year: int):
    """
    下载指定年份的Excel文件。
    
    Args:
        year: 要下载的年份
    
    Returns:
        FileResponse: Excel文件响应
    """
    file_path = get_output_path(f'bilibili_history_{year}.xlsx')
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"未找到 {year} 年的Excel文件")
    
    return FileResponse(
        path=file_path,
        filename=f"bilibili_history_{year}.xlsx",
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
