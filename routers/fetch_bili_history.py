from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from scripts.bilibili_history import fetch_new_history
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


@router.post("/fetch_history", summary="抓取并更新Bilibili历史记录，不传参数则默认读取配置文件里的SESSDATA", response_model=FetchHistoryResponse)
def fetch_and_update_history(request: FetchHistoryRequest = None):
    """
    抓取并更新Bilibili历史记录。

    - **sessdata**: 用户的 SESSDATA，如果不提供则使用配置文件中的SESSDATA。
    """
    sessdata = request.sessdata if request and request.sessdata else config.get('SESSDATA')
    if not sessdata:
        return {"status": "error", "message": "未提供SESSDATA，且配置文件中也没有SESSDATA。"}
    
    result = fetch_new_history(sessdata=sessdata)
    return {"status": result["status"], "message": result["message"]}
