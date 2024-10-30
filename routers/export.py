from fastapi import APIRouter, HTTPException
from scripts.export_to_excel import export_bilibili_history

router = APIRouter()

@router.post("/export_history", summary="导出Bilibili历史记录到Excel")
def export_history():
    """
    导出Bilibili历史记录到Excel文件。
    """
    result = export_bilibili_history()
    
    if result["status"] == "success":
        return {"status": "success", "message": result["message"]}
    else:
        raise HTTPException(status_code=500, detail=result["message"])
