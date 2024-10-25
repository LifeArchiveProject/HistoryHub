from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os

from utils.export_to_excel import export_bilibili_history

router = APIRouter()


# 定义请求体模型
class ExportHistoryRequest(BaseModel):
    db_file: Optional[str] = Field('bilibili_history.db', description="SQLite数据库文件路径")
    base_folder: Optional[str] = Field('history_by_date', description="历史记录的基础文件夹路径")


# 定义响应模型
class ExportHistoryResponse(BaseModel):
    status: str
    message: str


@router.post("/export_history", summary="导出Bilibili历史记录到Excel", response_model=ExportHistoryResponse)
def export_history(request: ExportHistoryRequest):
    """
    导出Bilibili历史记录到Excel文件。

    - **db_file**: SQLite数据库文件路径，默认为 'bilibili_history.db'。
    - **base_folder**: 历史记录的基础文件夹路径，默认为 'history_by_date'。
    """
    db_file = request.db_file
    base_folder = request.base_folder

    # 检查数据库文件是否存在
    if not os.path.exists(db_file):
        raise HTTPException(status_code=400, detail=f"数据库文件 {db_file} 不存在。")

    # 确保基础文件夹存在
    if not os.path.exists(base_folder):
        os.makedirs(base_folder, exist_ok=True)

    result = export_bilibili_history(db_file=db_file, base_folder=base_folder)

    if result["status"] == "success":
        return {"status": "success", "message": result["message"]}
    else:
        raise HTTPException(status_code=500, detail=result["message"])