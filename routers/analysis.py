from fastapi import APIRouter
from utils.analyze_bilibili_history import get_daily_counts, get_monthly_counts, update_counts

router = APIRouter()

@router.get("/daily_counts", summary="获取每天的观看计数")
def get_daily_video_counts():
    daily_count = get_daily_counts()
    if "error" in daily_count:
        return {"status": "error", "message": daily_count["error"]}
    return {"status": "success", "data": daily_count}

@router.get("/monthly_counts", summary="获取每月的观看计数")
def get_monthly_video_counts():
    monthly_count = get_monthly_counts()
    if "error" in monthly_count:
        return {"status": "error", "message": monthly_count["error"]}
    return {"status": "success", "data": monthly_count}

@router.get("/update_counts", summary="更新视频观看计数")
def get_update_counts():
    result = update_counts()
    return {"status": "success", "message": result}
