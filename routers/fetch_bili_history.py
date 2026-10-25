from fastapi import APIRouter

from scripts.bilibili_history import fetch_history
from scripts.import_sqlite import import_all_history_files


router = APIRouter()


async def sync_history(skip_exists: bool):
    result = await fetch_history(skip_exists=skip_exists)
    if result["status"] != "success":
        return result

    imported = import_all_history_files(incremental=skip_exists)
    if imported["status"] != "success":
        return imported

    return {
        "status": "success",
        "message": f"历史记录获取完成，导入 {imported['inserted_count']} 条记录",
        "data": {
            "new_records_count": result["data"]["new_records_count"],
            "inserted_count": imported["inserted_count"],
        },
    }


@router.get("/bili-history", summary="获取B站历史记录")
async def get_bili_history(skip_exists: bool = True):
    return await sync_history(skip_exists)


@router.get("/bili-history-realtime", summary="增量获取B站历史记录")
async def get_bili_history_realtime():
    return await sync_history(True)
