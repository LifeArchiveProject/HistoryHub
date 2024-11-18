from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, date

from scripts.analyze_bilibili_history import get_daily_and_monthly_counts, analyze_history_by_params

router = APIRouter()

@router.post("/analyze", summary="分析历史数据")
async def analyze_history(
    date_str: Optional[str] = Query(None, description="指定日期，格式为YYYY-MM-DD"),
    start_date: Optional[str] = Query(None, description="起始日期，格式为YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式为YYYY-MM-DD")
):
    """分析历史数据，支持指定日期和日期范围查询"""
    # 验证日期格式
    if date_str:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return {"status": "error", "message": "日期格式无效，请使用YYYY-MM-DD格式"}
            
    if start_date or end_date:
        try:
            if start_date:
                datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return {"status": "error", "message": "日期格式无效，请使用YYYY-MM-DD格式"}
        
        # 确保结束日期不早于开始日期
        if start_date and end_date and start_date > end_date:
            return {"status": "error", "message": "结束日期不能早于开始日期"}

    result = analyze_history_by_params(date_str, start_date, end_date)
    if "error" in result:
        return {"status": "error", "message": result["error"]}
    
    return {
        "status": "success",
        "message": "分析完成",
        "data": result
    }

@router.get("/analyze/overview", summary="获取总体观看数据统计")
async def get_overview():
    """获取总体观看数据统计"""
    result = get_daily_and_monthly_counts()
    if "error" in result:
        return {"status": "error", "message": result["error"]}
    return {
        "status": "success",
        "message": "分析完成",
        "data": result
    }
