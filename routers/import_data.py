from fastapi import APIRouter, HTTPException, BackgroundTasks

from utils.import_database import import_history

router = APIRouter()

@router.post("/import_data", summary="导入 Bilibili 历史数据")
def import_bilibili_history(background_tasks: BackgroundTasks, data_folder: str = 'history_by_date', log_file: str = 'last_import_log.json'):
    try:
        background_tasks.add_task(import_history, data_folder, log_file)
        return {"status": "success", "message": "数据导入任务已开始。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))