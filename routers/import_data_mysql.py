from fastapi import APIRouter, HTTPException, BackgroundTasks

from scripts.import_database import import_history

router = APIRouter()

@router.post("/import_data_mysql", summary="导入 Bilibili 历史数据到 MySQL")
def import_bilibili_history(background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(import_history)
        return {"status": "success", "message": "数据导入任务已开始。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
