from typing import Optional, Union

from fastapi import APIRouter, Query, HTTPException
from loguru import logger
from pydantic import BaseModel, Field

from scripts.bilibili_history import fetch_history, find_latest_local_history, fetch_and_compare_history, save_history, \
    load_cookie, get_invalid_videos_from_db
from scripts.import_sqlite import import_all_history_files
from scripts.utils import load_config, setup_logger

# 确保日志系统已初始化
setup_logger()

router = APIRouter()

config = load_config()

# 定义请求体模型
class FetchHistoryRequest(BaseModel):
    sessdata: Optional[str] = Field(None, description="用户的 SESSDATA")


# 定义响应模型
class ResponseModel(BaseModel):
    status: str
    message: str
    data: Optional[Union[list, dict]] = None


def get_headers():
    """获取请求头"""
    # 动态读取配置文件，获取最新的SESSDATA
    current_config = load_config()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Cookie': f'SESSDATA={current_config["SESSDATA"]}'
    }
    return headers


@router.get("/bili-history", summary="获取B站历史记录")
async def get_bili_history(output_dir: Optional[str] = "history_by_date", skip_exists: bool = True, process_video_details: bool = False):
    """获取B站历史记录"""
    try:
        result = await fetch_history(output_dir, skip_exists, process_video_details)
        return {
            "status": "success",
            "message": "历史记录获取成功",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"获取历史记录失败: {str(e)}"
        }


@router.get("/bili-history-realtime", summary="实时获取B站历史记录", response_model=ResponseModel)
async def get_bili_history_realtime(sync_deleted: bool = False, process_video_details: bool = False):
    """实时获取B站历史记录"""
    try:
        # 获取最新的本地历史记录时间戳
        latest_history = find_latest_local_history()
        if not latest_history:
            return {"status": "error", "message": "未找到本地历史记录"}

        # 获取cookie
        cookie = load_cookie()
        if not cookie:
            return {"status": "error", "message": "未找到有效的cookie"}

        # 获取新的历史记录 - 使用await，因为fetch_and_compare_history现在是异步函数
        new_records = await fetch_and_compare_history(cookie, latest_history, True, process_video_details)  # 传递process_video_details参数

        # 保存新历史记录的结果信息
        history_result = {"new_records_count": 0, "inserted_count": 0}
        video_details_result = {"processed": False}

        if new_records:
            # 保存新记录
            save_result = save_history(new_records)
            logger.info("成功保存新记录到本地文件")
            history_result["new_records_count"] = len(new_records)

            # 更新SQLite数据库
            logger.info("=== 开始更新SQLite数据库 ===")
            logger.info(f"同步已删除记录: {sync_deleted}")
            db_result = import_all_history_files(sync_deleted=sync_deleted)

            if db_result["status"] == "success":
                history_result["inserted_count"] = db_result['inserted_count']
                history_result["status"] = "success"
            else:
                history_result["status"] = "error"
                history_result["message"] = db_result["message"]
        else:
            history_result["status"] = "success"
            history_result["message"] = "没有新记录"

        # 处理视频详情 - 已经在fetch_and_compare_history中处理过，这里不需要重复处理
        # 只需生成结果信息
        if process_video_details:
            logger.info("视频详情已在历史记录获取过程中处理")
            video_details_result = {
                "status": "success",
                "message": "视频详情已在历史记录获取过程中处理",
                "processed": True
            }

        # 返回综合结果
        if history_result.get("status") == "success" and (not process_video_details or video_details_result.get("status") == "success"):
            message = "实时更新成功"
            if history_result.get("new_records_count", 0) > 0:
                message += f"，获取到 {history_result['new_records_count']} 条新记录"
                if history_result.get("inserted_count", 0) > 0:
                    message += f"，成功导入 {history_result['inserted_count']} 条记录到SQLite数据库"
            else:
                message += "，暂无新历史记录"

            if process_video_details:
                message += "。视频详情已在历史记录获取过程中处理"

            return {
                "status": "success",
                "message": message,
                "data": {
                    "history": history_result,
                    "video_details": video_details_result.get("data", {})
                }
            }
        else:
            # 有一个失败就返回错误
            error_message = []
            if history_result.get("status") == "error":
                error_message.append(f"历史记录处理失败: {history_result.get('message', '未知错误')}")
            if process_video_details and video_details_result.get("status") == "error":
                error_message.append(f"视频详情处理失败: {video_details_result.get('message', '未知错误')}")

            return {
                "status": "error",
                "message": " | ".join(error_message),
                "data": {
                    "history": history_result,
                    "video_details": video_details_result.get("data", {})
                }
            }

    except Exception as e:
        error_msg = f"实时更新失败: {str(e)}"
        logger.error(error_msg)
        import traceback
        logger.error(traceback.format_exc())  # 添加详细的堆栈跟踪
        return {"status": "error", "message": error_msg}


# 全局变量，用于存储处理进度
video_details_progress = {
    "is_processing": False,
    "total_videos": 0,
    "processed_videos": 0,
    "success_count": 0,
    "failed_count": 0,
    "error_videos": [],
    "skipped_invalid_count": 0,
    "start_time": 0,
    "last_update_time": 0,
    "is_complete": False
}

# 添加新的API端点用于查询失效视频列表
@router.get("/invalid-videos", summary="获取失效视频列表")
async def get_invalid_videos(
    page: int = Query(1, description="页码，从1开始"),
    limit: int = Query(50, description="每页返回数量，最大100"),
    error_type: Optional[str] = Query(None, description="按错误类型筛选")
):
    """获取失效视频列表"""
    try:
        result = await get_invalid_videos_from_db(page, limit, error_type)
        return result
    except Exception as e:
        print(f"获取失效视频列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取失效视频列表失败: {str(e)}"
        )
