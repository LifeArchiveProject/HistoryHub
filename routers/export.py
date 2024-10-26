from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os

from scripts.export_to_excel import export_bilibili_history

router = APIRouter()


# 定义请求体模型
class ExportHistoryRequest(BaseModel):
    base_folder: Optional[str] = Field('./', description="导出Excel文件的基础文件夹路径")


# 定义响应模型
class ExportHistoryResponse(BaseModel):
    status: str
    message: str


@router.post("/export_history", summary="导出Bilibili历史记录到Excel", response_model=ExportHistoryResponse)
def export_history(request: ExportHistoryRequest):
    """
    导出Bilibili历史记录到Excel文件。

    - **base_folder**: 导出Excel文件的基础文件夹路径，默认为 './'。
    """
    base_folder = request.base_folder

    # 确保基础文件夹存在
    if not os.path.exists(base_folder):
        os.makedirs(base_folder, exist_ok=True)

    result = export_bilibili_history()

    if result["status"] == "success":
        return {"status": "success", "message": result["message"]}
    else:
        raise HTTPException(status_code=500, detail=result["message"])
