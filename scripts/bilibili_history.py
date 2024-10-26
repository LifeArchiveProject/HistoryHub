import json
import logging
import os
import time
from datetime import datetime, timedelta
import requests
from scripts.utils import load_config, get_base_path

config = load_config()

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 读取本地cookie文件
def load_cookie():
    return config['cookie']

# 查找本地最新的日期文件并加载数据
def find_latest_local_history():
    base_path = get_base_path()
    full_base_folder = os.path.join(base_path, config['input_folder'])
    logger.info("正在查找本地最新的历史记录...")
    if not os.path.exists(full_base_folder):
        logger.info("本地历史记录文件夹不存在，将从头开始同步。")
        return None

    latest_date = None

    try:
        # 获取最新的年份
        latest_year = max([int(year) for year in os.listdir(full_base_folder) if year.isdigit()], default=None)
        if latest_year:
            # 获取最新的月份
            latest_month = max(
                [int(month) for month in os.listdir(os.path.join(full_base_folder, str(latest_year))) if month.isdigit()],
                default=None
            )
            if latest_month:
                # 获取最新的日期
                latest_day = max([
                    int(day.split('.')[0]) for day in
                    os.listdir(os.path.join(full_base_folder, str(latest_year), f"{latest_month:02}"))
                    if day.endswith('.json')
                ], default=None)
                if latest_day:
                    latest_file = os.path.join(full_base_folder, str(latest_year), f"{latest_month:02}", f"{latest_day:02}.json")
                    logger.info(f"找到最新历史记录文件: {latest_file}")
                    with open(latest_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # 获取最新日期
                        latest_date = datetime.fromtimestamp(data[-1]['view_at']).date()
    except ValueError:
        logger.error("历史记录目录格式不正确，可能尚未创建任何文件。")

    if latest_date:
        logger.info(f"本地最新的观看日期: {latest_date}")
    return latest_date

# 保存更新后的历史记录
def save_history(history_data):
    base_path = get_base_path()
    full_base_folder = os.path.join(base_path, config['input_folder'])
    logger.info(f"开始保存{len(history_data)}条新历史记录...")
    saved_count = 0  # 添加一个计数器
    for entry in history_data:
        timestamp = entry['view_at']
        dt_object = datetime.fromtimestamp(timestamp)
        year = dt_object.strftime('%Y')
        month = dt_object.strftime('%m')
        day = dt_object.strftime('%d')

        # 创建文件夹路径 年/月/日
        folder_path = os.path.join(full_base_folder, year, month)
        os.makedirs(folder_path, exist_ok=True)

        # 文件名为当天的日期
        file_path = os.path.join(folder_path, f"{day}.json")

        # 加载当天已有的 oid 集合
        existing_oids = set()
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    daily_data = json.load(f)
                    existing_oids = {item['history']['oid'] for item in daily_data}
                except json.JSONDecodeError:
                    logger.warning(f"无法解析文件 {file_path}，将重新创建。")
                    daily_data = []
        else:
            daily_data = []

        # 检查当前条目是否已存在
        if entry['history']['oid'] not in existing_oids:
            daily_data.append(entry)
            existing_oids.add(entry['history']['oid'])
            logger.info(f"添加新记录: {entry['title']} ({entry['history']['oid']})")
            saved_count += 1  # 每次成功保存都增加计数

        # 将数据保存回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(daily_data, f, ensure_ascii=False, indent=4)
    logger.info(f"历史记录保存完成，共保存了{saved_count}条新记录。")

# 获取新历史记录并与本地记录对比
def fetch_and_compare_history(headers, params, latest_date):
    logger.info("正在从B站API获取历史记录...")
    url = 'https://api.bilibili.com/x/web-interface/history/cursor'
    all_new_data = []
    page_count = 0
    error_message = None  # 用于存储错误信息

    # 计算停止日期，即本地最新日期的前一天
    if latest_date:
        cutoff_date = latest_date - timedelta(days=1)
        cutoff_timestamp = int(datetime.combine(cutoff_date, datetime.min.time()).timestamp())
        logger.info(f"设置停止条件：view_at <= {cutoff_timestamp} ({cutoff_date})")
    else:
        # 如果没有本地数据，设置一个较大的时间戳以抓取所有数据
        cutoff_timestamp = 0
        logger.info("没有本地数据，抓取所有可用的历史记录。")

    while True:
        page_count += 1
        logger.info(f"发送请求获取数据... (第{page_count}页)")
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
            except json.JSONDecodeError:
                error_message = "JSON Decode Error: 无法解析服务器响应"
                logger.error(error_message)
                break

            # 检查code是否为0
            if data.get('code') != 0:
                error_message = f"API请求失败，错误码: {data.get('code')}, 错误信息: {data.get('message')}"
                logger.error(error_message)
                break

            # 检查数据中的list
            if 'data' in data and 'list' in data['data']:
                fetched_list = data['data']['list']
                logger.info(f"获取到{len(fetched_list)}条记录，进行对比...")

                # 打印获取到的数据
                for entry in fetched_list:
                    logger.debug(f"标题: {entry['title']}, 观看时间: {datetime.fromtimestamp(entry['view_at'])}")

                new_entries = []
                should_stop = False

                for entry in fetched_list:
                    view_at = entry['view_at']

                    if view_at > cutoff_timestamp:
                        # 不再检查全局的 local_oids
                        new_entries.append(entry)
                    else:
                        # 当view_at <= cutoff_timestamp时，不再收集新数据
                        should_stop = True

                if new_entries:
                    all_new_data.extend(new_entries)
                    logger.info(f"找到{len(new_entries)}条新记录。")

                if should_stop:
                    logger.info("达到停止条件，停止请求。")
                    break

                # 更新请求的游标参数
                if 'cursor' in data['data']:
                    current_max = data['data']['cursor'].get('max')
                    params['max'] = current_max
                    params['view_at'] = data['data']['cursor'].get('view_at')
                    logger.info(f"请求游标更新：max={params['max']}, view_at={params['view_at']}")
                else:
                    error_message = "未能获取游标信息，停止请求。"
                    logger.error(error_message)
                    break

                # 暂停1秒再请求
                time.sleep(1)
            else:
                error_message = "没有更多的数据或数据结构错误。"
                logger.error(error_message)
                break
        else:
            error_message = f"请求失败，状态码: {response.status_code}, 原因: {response.text}"
            logger.error(error_message)
            break

    # 过滤掉已经在当天存在的记录
    filtered_new_data = []
    for entry in all_new_data:
        entry_date = datetime.fromtimestamp(entry['view_at']).date()
        # 构造文件路径
        file_path = os.path.join('history_by_date', entry_date.strftime('%Y'), entry_date.strftime('%m'),
                                 f"{entry_date.strftime('%d')}.json")
        existing_oids = set()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    daily_data = json.load(f)
                    existing_oids = {item['history']['oid'] for item in daily_data}
            except json.JSONDecodeError:
                logger.warning(f"无法解析文件 {file_path}，将重新创建。")
        if entry['history']['oid'] not in existing_oids:
            filtered_new_data.append(entry)

    if error_message:
        return {"status": "error", "message": error_message}
    else:
        return {"status": "success", "new_history": filtered_new_data}

# 主逻辑函数
def fetch_new_history(cookie=None):
    try:
        if cookie:
            sessdata = cookie
            logger.info("使用传入的cookie进行API请求。")
        else:
            sessdata = load_cookie()
            logger.info("使用配置文件中的cookie进行API请求。")
    except Exception as e:
        logger.error(f"获取cookie时发生错误: {e}")
        return {"status": "error", "message": f"获取cookie失败: {str(e)}"}

    headers = {
        'Cookie': f"SESSDATA={sessdata}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
    }

    # 初始化请求参数
    params = {
        'ps': 30,  # 每页数量，默认为 20，最大 30
        'max': '',  # 初始为空
        'view_at': '',  # 初始为空
        'business': '',  # 可选参数，默认为空表示获取所有类型
    }

    # 查找本地最新的历史记录
    latest_date = find_latest_local_history()

    # 获取新历史记录
    result = fetch_and_compare_history(headers, params, latest_date)

    if result["status"] == "error":
        return result  # 直接返回错误信息

    new_history = result.get("new_history", [])

    if new_history:
        # 保存新历史记录
        save_history(new_history)
        return {"status": "success", "message": f"共获取到{len(new_history)}条新记录。"}
    else:
        return {"status": "success", "message": "没有新记录可更新。"}

# 允许脚本独立运行
if __name__ == '__main__':
    result = fetch_new_history()
    if result["status"] == "success":
        print(result["message"])
    else:
        print(f"错误: {result['message']}")
