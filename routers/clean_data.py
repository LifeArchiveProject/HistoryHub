from fastapi import APIRouter
from scripts.clean_data import clean_history_data

router = APIRouter()

@router.post("/clean_data", summary="清理Bilibili历史数据")
def api_clean_data():
    return clean_history_data()
