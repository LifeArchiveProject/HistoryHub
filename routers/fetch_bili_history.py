from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from scripts.bilibili_history import fetch_history
from scripts.utils import load_config

router = APIRouter()

config = load_config()

# 定义请求体模型
class FetchHistoryRequest(BaseModel):
    sessdata: Optional[str] = Field(None, description="用户的 SESSDATA")


# 定义响应模型
class FetchHistoryResponse(BaseModel):
    status: str
    message: str


def get_headers():
    """获取请求头"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': f'SESSDATA={config["SESSDATA"]}'
    }
    return headers


@router.get("/bili-history")
async def get_bili_history(output_dir: Optional[str] = "output/history"):
    """获取B站历史记录"""
    try:
        result = await fetch_history(output_dir)
        return {
            "status": "success",
            "message": "历史记录获取成功",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"获取历史记录失败: {str(e)}"
        }
