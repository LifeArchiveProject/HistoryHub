from fastapi import APIRouter
from scripts.send_log_email import send_latest_log

router = APIRouter()

@router.post("/send_log", summary="发送最新的日志邮件")
def api_send_log():
    return send_latest_log()
