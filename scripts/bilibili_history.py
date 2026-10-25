import asyncio
import json
import logging
import os
from datetime import datetime

import requests

from scripts.utils import get_output_path, load_config


def load_cookie():
    """从配置文件读取 SESSDATA。"""
    return load_config().get("SESSDATA", "").strip('"')


def find_latest_local_history(base_folder='history_by_date'):
    """查找本地最新的历史记录"""
    print("正在查找本地最新的历史记录...")
    full_base_folder = get_output_path(base_folder)  # 使用 get_output_path
    
    print(f"\n=== 查找历史记录 ===")
    print(f"查找路径: {full_base_folder}")
    print(f"路径存在: {os.path.exists(full_base_folder)}")
    
    if not os.path.exists(full_base_folder):
        print("本地历史记录文件夹不存在，将从头开始同步。")
        return None

    latest_date = None
    try:
        latest_year = max([int(year) for year in os.listdir(full_base_folder) if year.isdigit()], default=None)
        if latest_year:
            latest_month = max(
                [int(month) for month in os.listdir(os.path.join(full_base_folder, str(latest_year))) if month.isdigit()],
                default=None
            )
            if latest_month:
                latest_day = max([
                    int(day.split('.')[0]) for day in
                    os.listdir(os.path.join(full_base_folder, str(latest_year), f"{latest_month:02}"))
                    if day.endswith('.json')
                ], default=None)
                if latest_day:
                    latest_file = os.path.join(full_base_folder, str(latest_year), f"{latest_month:02}",
                                             f"{latest_day:02}.json")
                    print(f"找到最新历史记录文件: {latest_file}")
                    with open(latest_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        latest_date = datetime.fromtimestamp(data[-1]['view_at']).date()
    except ValueError:
        print("历史记录目录格式不正确，可能尚未创建任何文件。")

    if latest_date:
        print(f"本地最新的观看日期: {latest_date}")
    return latest_date

def save_history(history_data, base_folder='history_by_date'):
    """保存历史记录"""
    logging.info(f"开始保存{len(history_data)}条新历史记录...")
    full_base_folder = get_output_path(base_folder)
    saved_count = 0

    print(f"\n=== 保存历史记录 ===")
    print(f"保存路径: {full_base_folder}")
    
    for entry in history_data:
        timestamp = entry['view_at']
        dt_object = datetime.fromtimestamp(timestamp)
        year = dt_object.strftime('%Y')
        month = dt_object.strftime('%m')
        day = dt_object.strftime('%d')

        folder_path = os.path.join(full_base_folder, year, month)
        os.makedirs(folder_path, exist_ok=True)

        file_path = os.path.join(folder_path, f"{day}.json")

        existing_records = set()  # 使用集合存储bvid和view_at的组合
        if os.path.exists(file_path):
            try:
                # 尝试不同的编码方式读取
                for encoding in ['utf-8', 'gbk', 'utf-8-sig']:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            daily_data = json.load(f)
                            # 将bvid和view_at组合作为唯一标识
                            existing_records = {
                                (item['history']['bvid'], item['view_at']) 
                                for item in daily_data
                            }
                            break
                    except UnicodeDecodeError:
                        continue
                    except json.JSONDecodeError:
                        continue
            except Exception as e:
                logging.warning(f"警告: 读取文件 {file_path} 失败: {e}，将创建新文件")
                daily_data = []
        else:
            daily_data = []

        # 检查当前记录的bvid和view_at组合是否已存在
        current_record = (entry['history']['bvid'], entry['view_at'])
        if current_record not in existing_records:
            daily_data.append(entry)
            existing_records.add(current_record)
            saved_count += 1

        # 保存时使用 utf-8 编码
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(daily_data, f, ensure_ascii=False, indent=4)
            
    logging.info(f"历史记录保存完成，共保存了{saved_count}条新记录。")
    return {"status": "success", "message": "历史记录获取成功", "data": {"new_records_count": saved_count}}


async def fetch_and_compare_history(cookie, latest_date):
    """按游标获取历史记录，增量获取保留本地最新日期内的记录。"""
    url = "https://api.bilibili.com/x/web-interface/history/cursor"
    headers = {
        "Cookie": f"SESSDATA={cookie}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://www.bilibili.com",
        "Origin": "https://www.bilibili.com",
        "Accept": "application/json, text/plain, */*",
    }
    params = {"ps": 30, "max": "", "view_at": "", "business": ""}
    cutoff_timestamp = (
        int(datetime.combine(latest_date, datetime.min.time()).timestamp())
        if latest_date else 0
    )
    new_history = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        result = response.json()
        if result.get("code") != 0:
            raise ValueError(result.get("message", "获取历史记录失败"))

        data = result["data"]
        records = data["list"]
        if not records:
            break

        new_history.extend(record for record in records if record["view_at"] >= cutoff_timestamp)
        if any(record["view_at"] < cutoff_timestamp for record in records):
            break

        cursor = data.get("cursor")
        if not cursor or not cursor.get("max"):
            break
        params["max"] = cursor["max"]
        params["view_at"] = cursor["view_at"]
        await asyncio.sleep(1)

    return new_history


async def fetch_history(skip_exists: bool = True) -> dict:
    """获取B站历史记录并按日期保存JSON。"""
    try:
        cookie = load_cookie()
        if not cookie:
            return {"status": "error", "message": "未找到SESSDATA配置，请先登录"}

        latest_date = find_latest_local_history() if skip_exists else None
        records = await fetch_and_compare_history(cookie, latest_date)
        os.makedirs(get_output_path("history_by_date"), exist_ok=True)
        if records:
            return save_history(records)
        return {
            "status": "success",
            "message": "没有新记录需要更新",
            "data": {"new_records_count": 0},
        }
    except Exception as error:
        logging.error("获取历史记录失败: %s", error)
        return {"status": "error", "message": f"获取历史记录失败: {error}"}
