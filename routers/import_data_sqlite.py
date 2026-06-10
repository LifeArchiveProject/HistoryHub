from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from scripts.import_sqlite import import_all_history_files
from .interaction_records import import_interactions_to_history_once

router = APIRouter()

class ImportHistoryResponse(BaseModel):
    status: str
    message: str
    data: dict | None = None

@router.post("/import_data_sqlite", summary="导入历史记录到SQLite数据库", response_model=ImportHistoryResponse)
def import_history():
    result = import_all_history_files()

    if result["status"] == "success":
        interaction_import = import_interactions_to_history_once()
        return {
            "status": "success",
            "message": result["message"],
            "data": {
                "history_import": result,
                "interaction_history_import": interaction_import,
            },
        }
    else:
        raise HTTPException(status_code=500, detail=result["message"])
