import json
import os
import yaml
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, BackgroundTasks, Query, HTTPException
from pydantic import BaseModel

from scripts.check_data_integrity import check_data_integrity
from scripts.sync_db_json import sync_data
from scripts.utils import load_config, get_output_path

router = APIRouter()

class SyncedDayInfo(BaseModel):
    date: str
    imported_count: int
    source: str
    titles: List[str]

class SyncDBJsonResponse(BaseModel):
    success: bool
    json_to_db_count: int
    db_to_json_count: int
    total_synced: int
    timestamp: str
    synced_days: Optional[List[SyncedDayInfo]] = None
    message: Optional[str] = None

class CheckDataIntegrityResponse(BaseModel):
    success: bool
    total_json_files: int
    total_json_records: int
    total_db_records: int
    missing_records_count: int
    extra_records_count: int
    difference: int
    result_file: str
    report_file: str
    timestamp: str

class IntegrityCheckConfigRequest(BaseModel):
    check_on_startup: bool

class IntegrityCheckConfigResponse(BaseModel):
    success: bool
    message: str
    check_on_startup: bool

def run_sync_data(db_path: Optional[str] = None, json_root_path: Optional[str] = None):
    """在后台运行数据同步任务"""
    # 确保输出目录存在
    os.makedirs("output/check", exist_ok=True)

    # 调用同步函数
    result = sync_data(db_path, json_root_path)
    return result

def run_check_integrity(db_path: Optional[str] = None, json_root_path: Optional[str] = None):
    """在后台运行数据完整性检查任务"""
    # 确保输出目录存在
    os.makedirs("output/check", exist_ok=True)

    # 调用检查函数
    result = check_data_integrity(db_path, json_root_path)
    return result

@router.post("/sync", response_model=SyncDBJsonResponse, summary="同步数据库和JSON文件")
async def sync_db_json(
    background_tasks: BackgroundTasks,
    db_path: Optional[str] = Query(None, description="数据库文件路径，默认为 output/bilibili_history.db"),
    json_path: Optional[str] = Query(None, description="JSON文件根目录，默认为 output/history_by_date"),
    async_mode: bool = Query(False, description="是否异步执行（后台任务）")
):
    """
    同步数据库和JSON文件中的历史记录数据。

    - 将JSON文件中的新记录导入到数据库
    - 将数据库中的新记录导出到JSON文件

    返回:
    - 导入和导出的记录数量
    - 按日期同步的详细信息，包括每天同步的记录数和记录标题
    """
    if async_mode:
        # 异步模式下，将任务放入后台执行
        background_tasks.add_task(run_sync_data, db_path, json_path)
        return {
            "success": True,
            "json_to_db_count": 0,
            "db_to_json_count": 0,
            "total_synced": 0,
            "timestamp": datetime.now().isoformat(),
            "message": "同步任务已在后台启动，请稍后查看日志获取结果"
        }
    else:
        # 同步模式下，直接执行并返回结果
        result = run_sync_data(db_path, json_path)

        # 如果result不包含synced_days字段，添加一个空列表
        if "synced_days" not in result:
            result["synced_days"] = []

        # 添加timestamp如果不存在
        if "timestamp" not in result:
            result["timestamp"] = datetime.now().isoformat()

        return result

@router.post("/check", response_model=CheckDataIntegrityResponse, summary="检查数据完整性")
async def check_integrity(
    background_tasks: BackgroundTasks,
    db_path: Optional[str] = Query(None, description="数据库文件路径，默认为 output/bilibili_history.db"),
    json_path: Optional[str] = Query(None, description="JSON文件根目录，默认为 output/history_by_date"),
    async_mode: bool = Query(False, description="是否异步执行（后台任务）"),
    force_check: bool = Query(False, description="是否强制执行检查，忽略配置设置")
):
    """
    检查数据库和JSON文件之间的数据完整性。

    - 检查JSON文件是否都被正确导入到数据库
    - 检查数据库中的记录是否都存在于JSON文件中
    - 生成详细的差异报告

    返回检查结果和报告文件路径。
    """
    # 检查配置是否允许执行数据完整性校验
    if not force_check:
        config = load_config()
        check_enabled = config.get('server', {}).get('data_integrity', {}).get('check_on_startup', True)
        if not check_enabled:
            return {
                "success": True,
                "total_json_files": 0,
                "total_json_records": 0,
                "total_db_records": 0,
                "missing_records_count": 0,
                "extra_records_count": 0,
                "difference": 0,
                "result_file": "",
                "report_file": "",
                "timestamp": datetime.now().isoformat(),
                "message": "数据完整性校验已在配置中禁用，跳过检查。如需强制检查，请使用force_check=true参数。"
            }

    if async_mode:
        # 异步模式下，将任务放入后台执行
        background_tasks.add_task(run_check_integrity, db_path, json_path)
        return {
            "success": True,
            "total_json_files": 0,
            "total_json_records": 0,
            "total_db_records": 0,
            "missing_records_count": 0,
            "extra_records_count": 0,
            "difference": 0,
            "result_file": "output/check/data_integrity_results.json",
            "report_file": "output/check/data_integrity_report.md",
            "timestamp": datetime.now().isoformat(),
            "message": "数据完整性检查任务已在后台启动，请稍后查看报告文件获取结果"
        }
    else:
        # 同步模式下，直接执行并返回结果
        result = run_check_integrity(db_path, json_path)
        return {
            **result,
            "timestamp": datetime.now().isoformat()
        }

@router.get("/report", summary="获取最新的数据完整性报告")
async def get_report():
    """
    获取最新的数据完整性检查报告的内容。

    返回报告的内容和最后修改时间。
    """
    # 检查配置是否允许执行数据完整性校验
    config = load_config()
    check_enabled = config.get('server', {}).get('data_integrity', {}).get('check_on_startup', True)

    report_file = "output/check/data_integrity_report.md"

    if not os.path.exists(report_file):
        # 如果报告文件不存在，检查是否是因为配置禁用了校验
        if not check_enabled:
            return {
                "message": "数据完整性校验已在配置中禁用，无法获取报告。如需查看报告，请先执行数据完整性检查。"
            }
        else:
            raise HTTPException(status_code=404, detail="报告文件不存在，请先执行数据完整性检查")

    try:
        with open(report_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 获取文件修改时间
        mod_time = os.path.getmtime(report_file)
        mod_time_str = datetime.fromtimestamp(mod_time).isoformat()

        return {
            "content": content,
            "modified_time": mod_time_str,
            "file_path": report_file
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取报告文件时出错: {str(e)}")

@router.get("/sync/result", summary="获取最新的同步结果")
async def get_sync_result():
    """
    获取最新的数据同步结果。

    返回同步的详细信息，包括每天同步的记录数量和记录标题。
    """
    result_file = "output/check/sync_result.json"

    if not os.path.exists(result_file):
        raise HTTPException(status_code=404, detail="同步结果文件不存在，请先执行数据同步")

    try:
        with open(result_file, "r", encoding="utf-8") as f:
            result = json.load(f)

        # 获取文件修改时间
        mod_time = os.path.getmtime(result_file)
        mod_time_str = datetime.fromtimestamp(mod_time).isoformat()

        # 添加文件修改时间
        result["file_modified_time"] = mod_time_str

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取同步结果文件时出错: {str(e)}")

@router.get("/config", summary="获取数据完整性校验配置")
async def get_integrity_check_config():
    """
    获取数据完整性校验配置。

    返回当前的数据完整性校验配置，包括是否在启动时进行校验。
    """
    try:
        # 加载配置
        config = load_config()

        # 获取数据完整性校验配置
        check_on_startup = config.get('server', {}).get('data_integrity', {}).get('check_on_startup', True)

        return IntegrityCheckConfigResponse(
            success=True,
            message="获取配置成功",
            check_on_startup=check_on_startup
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据完整性校验配置时出错: {str(e)}")

@router.post("/config", response_model=IntegrityCheckConfigResponse, summary="更新数据完整性校验配置")
async def update_integrity_check_config(request: IntegrityCheckConfigRequest):
    """
    更新数据完整性校验配置。

    - 设置是否在启动时进行数据完整性校验

    返回更新后的配置。
    """
    try:
        # 获取配置文件路径
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "config.yaml")

        # 读取当前配置文件内容
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            config = yaml.safe_load(content)  # 仅用于获取当前配置和检查结构

        # 确保server和data_integrity配置存在
        if 'server' not in config:
            config['server'] = {}
        if 'data_integrity' not in config['server']:
            config['server']['data_integrity'] = {}

        # 使用正则表达式精确更新配置值
        import re

        # 检查是否已存在data_integrity配置
        data_integrity_exists = False
        server_exists = False
        check_on_startup_exists = False

        lines = content.split('\n')
        for i, line in enumerate(lines):
            if re.match(r'^\s*server\s*:', line):
                server_exists = True
            elif server_exists and re.match(r'^\s{2}data_integrity\s*:', line):
                data_integrity_exists = True
            elif data_integrity_exists and re.match(r'^\s{4}check_on_startup\s*:', line):
                check_on_startup_exists = True
                # 更新check_on_startup的值
                indent = line[:line.find('check_on_startup')]
                lines[i] = f"{indent}check_on_startup: {str(request.check_on_startup).lower()}"
                break

        # 如果没有找到check_on_startup配置，需要添加
        if not check_on_startup_exists:
            if data_integrity_exists:
                # 找到data_integrity行，在其后添加check_on_startup
                for i, line in enumerate(lines):
                    if re.match(r'^\s{2}data_integrity\s*:', line):
                        lines.insert(i + 1, f"    check_on_startup: {str(request.check_on_startup).lower()}")
                        break
            elif server_exists:
                # 找到server行，在其后添加data_integrity和check_on_startup
                for i, line in enumerate(lines):
                    if re.match(r'^\s*server\s*:', line):
                        lines.insert(i + 1, f"  data_integrity:")
                        lines.insert(i + 2, f"    check_on_startup: {str(request.check_on_startup).lower()}")
                        break
            else:
                # 如果没有server配置，在文件末尾添加
                lines.append("server:")
                lines.append("  data_integrity:")
                lines.append(f"    check_on_startup: {str(request.check_on_startup).lower()}")

        # 写回配置文件
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        # 更新内存中的配置
        config['server']['data_integrity']['check_on_startup'] = request.check_on_startup

        return IntegrityCheckConfigResponse(
            success=True,
            message="配置已更新",
            check_on_startup=request.check_on_startup
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新数据完整性校验配置时出错: {str(e)}")