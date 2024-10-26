from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from scripts.bilibili_history import fetch_new_history
from scripts.utils import load_config

router = APIRouter()

config = load_config()

# 定义请求体模型
class FetchHistoryRequest(BaseModel):
    cookie: Optional[str] = Field(None, description="用户的 SESSDATA cookie")


# 定义响应模型
class FetchHistoryResponse(BaseModel):
    status: str
    message: str


@router.post("/fetch_history", summary="抓取并更新Bilibili历史记录，不传参数则默认读取配置文件里的cookie", response_model=FetchHistoryResponse)
def fetch_and_update_history(request: FetchHistoryRequest = None):
    """
    抓取并更新Bilibili历史记录。

    - **cookie**: 用户的 SESSDATA cookie，如果不提供则使用配置文件中的cookie。
    """
    cookie = request.cookie if request and request.cookie else config.get('cookie')
    if not cookie:
        return {"status": "error", "message": "未提供cookie，且配置文件中也没有cookie。"}
    
    result = fetch_new_history(cookie=cookie)
    return {"status": result["status"], "message": result["message"]}
