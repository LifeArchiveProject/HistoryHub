from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from utils.bilibili_history import fetch_new_history

router = APIRouter()


# 定义请求体模型
class FetchHistoryRequest(BaseModel):
    cookie: Optional[str] = Field(None, description="用户的 SESSDATA cookie")


# 定义响应模型（可选）
class FetchHistoryResponse(BaseModel):
    status: str
    message: str


@router.post("/fetch_history", summary="抓取并更新Bilibili历史记录，不传参数则默认读取本地文件夹里的cookie", response_model=FetchHistoryResponse)
def fetch_and_update_history(request: FetchHistoryRequest):
    """
    抓取并更新Bilibili历史记录。

    - **cookie**: 用户的 SESSDATA cookie，必须包含 SESSDATA 的值。
    """
    if request.cookie:
        # 传入的cookie应该只包含 SESSDATA 的值，不需要包含 "SESSDATA=" 前缀
        cookie_value = request.cookie
    else:
        cookie_value = None  # 将使用本地文件中的cookie

    result = fetch_new_history(cookie=cookie_value)

    if result["status"] == "success":
        return {"status": "success", "message": result["message"]}
    else:
        # 这里我们抛出一个 HTTPException，并将错误信息传递给客户端
        raise HTTPException(status_code=400, detail=result["message"])
